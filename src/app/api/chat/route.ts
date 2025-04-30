// src/app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server';
// Use 'ai' package for core Vercel AI SDK functions and types
import { Message, streamText, tool, Tool } from 'ai'; // Added 'Tool' type import
import { openai } from '@ai-sdk/openai';
import { z } from 'zod'; // Import zod for tool parameters
import fs from 'fs/promises'; // Import Node.js file system module
import path from 'path'; // Import Node.js path module

// --- Core Langchain/AI Imports (for Retrieval & Adding Info) ---
import { OpenAIEmbeddings } from '@langchain/openai';
import { PineconeStore } from "@langchain/pinecone";
import { Pinecone } from "@pinecone-database/pinecone";
// import { PromptTemplate } from "@langchain/core/prompts";
// import { RunnableLambda } from "@langchain/core/runnables";
import { Document } from "@langchain/core/documents";
import { v4 as uuidv4 } from 'uuid'; // Import uuid for generating IDs for new docs

// --- Define Inline Helper ---
const formatDocumentsAsString = (docs: Document[]): string => {
   // Add a check for empty docs array
   if (!docs || docs.length === 0) {
       return "No relevant context found.";
   }
   return docs.map(doc => doc.pageContent).join("\n\n");
};

// --- Set Runtime ---
export const runtime = 'nodejs'; // Keep nodejs for Pinecone compatibility

// --- Configuration ---
const openAIApiKey = process.env.OPENAI_API_KEY;
const pineconeApiKey = process.env.PINECONE_API_KEY;
const pineconeHost = process.env.PINECONE_INDEX_HOST;
const pineconeIndexName = process.env.PINECONE_INDEX;

// --- Environment Variable Check ---
if (!openAIApiKey || !pineconeApiKey || !pineconeHost || !pineconeIndexName) {
    console.error("FATAL ERROR: Missing required environment variables!");
    throw new Error("Missing required environment variables!");
}

// --- Model & Retrieval/Addition Settings ---
const embeddingModelName = 'text-embedding-3-small';
const chatModelName = 'gpt-4.1'; // Or 'gpt-4-turbo' etc.
const retrievalDocsCount = 4;


// --- API Route Handler ---
export async function POST(req: NextRequest) {
    // Environment variables checked at startup

    try {
        // --- Load System Prompt from File ---
        const systemPromptFilePath = path.join(process.cwd(), '/public/system_prompt.txt');
        const systemPrompt = await fs.readFile(systemPromptFilePath, 'utf-8');
        console.log("[API /api/chat] Loaded system prompt from file.");

        const body = await req.json();
        const messages: Message[] = body.messages ?? [];
        const currentMessageContent = messages[messages.length - 1]?.content;

        if (typeof currentMessageContent !== 'string') {
             console.error(`[API /api/chat] Invalid query type received: ${typeof currentMessageContent}`);
             return NextResponse.json({ error: "Invalid query format" }, { status: 400 });
        }

        console.log(`[API /api/chat] Received query: "${currentMessageContent}"`);
        console.log(`[API /api/chat] Environment NODE_ENV: ${process.env.NODE_ENV}`); // Log environment

        // --- Initialize Embeddings Client (used by tools) ---
        const embeddings = new OpenAIEmbeddings({ openAIApiKey, model: embeddingModelName });

        // --- Define Tools ---
        // Tool to Retrieve Information (Always available)
        const getInformationTool: Tool = tool({
            description: `Retrieve relevant information from the knowledge base based on the user's question. Always use this tool first when asked a question.`,
            parameters: z.object({
                question: z.string().describe('The user question to search for in the knowledge base'),
            }),
            execute: async ({ question }) => {
                console.log(`[Tool getInformation] Searching for: "${question}"`);
                // Check env vars needed specifically for this tool
                if (!pineconeApiKey || !pineconeHost || !pineconeIndexName || !openAIApiKey) {
                    return "Error: Tool is missing required configuration.";
                }
                try {
                    // Initialize clients within the tool execution
                    const toolEmbeddings = new OpenAIEmbeddings({ openAIApiKey, model: embeddingModelName });
                    const pinecone = new Pinecone({ apiKey: pineconeApiKey });
                    const pineconeIndex = pinecone.Index(pineconeIndexName, pineconeHost);
                    const vectorStore = await PineconeStore.fromExistingIndex(toolEmbeddings, { pineconeIndex });
                    const retriever = vectorStore.asRetriever({ k: retrievalDocsCount });

                    const relevantDocs = await retriever.getRelevantDocuments(question);
                    console.log(`[Tool getInformation] Retrieved ${relevantDocs.length} documents.`);

                    // Use the updated helper function which handles empty arrays
                    const context = formatDocumentsAsString(relevantDocs);
                    return context; // Return context (or "No relevant context found.") to the LLM
                } catch (toolError: unknown) {
                    console.error("[Tool getInformation] Error:", toolError);
                    const message = (toolError instanceof Error) ? toolError.message : "Unknown error";
                    return `Error executing information retrieval: ${message}`;
                }
            },
        }); // End of getInformation tool

        // --- Conditionally Define addInformation Tool ---
        // Initialize availableTools object with the always-present getInformation tool
        const availableTools: Record<string, Tool> = { getInformation: getInformationTool };

        // Check the environment variable
        if (process.env.NODE_ENV === 'development') {
            console.log("[API /api/chat] Development environment detected. Enabling 'addInformation' tool.");
            // Define and add the addInformation tool ONLY in development
            availableTools.addInformation = tool({
                description: "Adds new information provided by the user to the knowledge base. Use this when the user gives new facts about themselves or asks to remember something. This tool is only available in specific environments.",
                parameters: z.object({
                    content: z.string().describe("The new piece of information or fact to add to the knowledge base."),
                }),
                execute: async ({ content }) => {
                    console.log(`[Tool addInformation] Received content: "${content}"`);
                     // Check env vars needed specifically for this tool
                    if (!pineconeApiKey || !pineconeHost || !pineconeIndexName || !openAIApiKey) {
                        return "Error: Tool is missing required configuration.";
                    }
                    try {
                        // Initialize Pinecone connection within the tool execution
                        const pinecone = new Pinecone({ apiKey: pineconeApiKey });
                        const pineconeIndex = pinecone.Index(pineconeIndexName, pineconeHost);
                        // Re-use embeddings initialized outside the tool scope
                        const vectorStore = await PineconeStore.fromExistingIndex(embeddings, { pineconeIndex });

                        // Create a Langchain Document for the new piece of information
                        const newDoc = new Document({
                            pageContent: content,
                            metadata: { source: 'chat_addition', timestamp: new Date().toISOString() }
                        });

                        // Generate a unique ID
                        const newId = uuidv4();

                        // Add the document to Pinecone
                        await vectorStore.addDocuments([newDoc], { ids: [newId] });

                        console.log(`[Tool addInformation] Successfully added document with ID: ${newId}`);
                        // Return confirmation message to the LLM
                        return "Successfully added the new information to the knowledge base.";

                    } catch (toolError: unknown) {
                        console.error("[Tool addInformation] Error:", toolError);
                         const message = (toolError instanceof Error) ? toolError.message : "Unknown error";
                        return `Error adding information to the knowledge base: ${message}`;
                    }
                },
            }); // End of addInformation tool definition
        } else {
             console.log("[API /api/chat] Production environment detected. 'addInformation' tool is disabled.");
        }


        // --- Call streamText with Available Tools ---
        const result = await streamText({
            model: openai(chatModelName), // API key read from env
            system: systemPrompt, // Use the loaded system prompt
            messages,
            temperature: 0.3,
            tools: availableTools, // Pass the conditionally populated tools object
        });

        // --- Return the Data Stream Response ---
        return result.toDataStreamResponse();

    } catch (error: unknown) {
        console.error("[API /api/chat] Error processing request:", error);
        let errorMessage = "An unknown error occurred.";
        let errorStack: string | undefined = undefined;
        if (error instanceof Error) {
            errorMessage = error.message;
            errorStack = error.stack;
        } else if (typeof error === 'string') {
            errorMessage = error;
        }
        console.error("[API /api/chat] Error details - Message:", errorMessage);
        if (errorStack) {
             console.error("[API /api/chat] Error details - Stack:", errorStack);
        }
        return NextResponse.json(
             { error: "An error occurred while processing your request.", details: errorMessage },
             { status: 500 }
        );
    }
}
