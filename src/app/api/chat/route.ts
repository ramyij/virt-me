// src/app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server';
// Corrected: Use 'ai' package for core Vercel AI SDK functions and types
import { Message, streamText } from 'ai';
import { openai } from '@ai-sdk/openai'; // Keep OpenAI provider import

// --- Core Langchain/AI Imports (for Retrieval) ---
import { OpenAIEmbeddings } from '@langchain/openai';
import { PineconeStore } from "@langchain/pinecone";
import { Pinecone } from "@pinecone-database/pinecone";
import { PromptTemplate } from "@langchain/core/prompts";
import { RunnableLambda } from "@langchain/core/runnables"; // Needed for retriever input fix
import { Document } from "@langchain/core/documents";

// --- Define Inline Helper ---
// Define formatting logic inline to avoid import issues
const formatDocumentsAsString = (docs: Document[]): string => {
   return docs.map(doc => doc.pageContent).join("\n\n");
};

// --- Set Runtime ---
// Edge is preferred for Vercel AI SDK Core
export const runtime = 'edge';
// export const runtime = 'nodejs'; // Use nodejs if edge causes dependency issues

// --- Configuration ---
const openAIApiKey = process.env.OPENAI_API_KEY;
const pineconeApiKey = process.env.PINECONE_API_KEY;
const pineconeHost = process.env.PINECONE_INDEX_HOST;
const pineconeIndexName = process.env.PINECONE_INDEX;

// --- Environment Variable Check ---
if (!openAIApiKey || !pineconeApiKey || !pineconeHost || !pineconeIndexName) {
    console.error("FATAL ERROR: Missing required environment variables!");
    // In non-edge environments, you might throw an error here
    // if (runtime === 'nodejs') throw new Error("Missing required environment variables!");
}

// --- Model & Retrieval Settings ---
const embeddingModelName = 'text-embedding-3-small';
const chatModelName = 'gpt-3.5-turbo';
const retrievalDocsCount = 4;

// --- Prompt Template ---
const TEMPLATE_STRING = `You are Virtual Me, an AI assistant representing the person whose information is in the documents provided.
Answer the user's question based *only* on the context below.
If the context doesn't contain the answer, state that you don't have that specific information in your documented knowledge.
Be conversational and answer from the first-person perspective (e.g., "I worked on...", "My experience includes...").
Do not make up information or discuss topics outside the provided context.

Context:
{context}

Question: {question}

Answer (respond as "I"):`;

// --- API Route Handler ---
export async function POST(req: NextRequest) {
    if (!openAIApiKey || !pineconeApiKey || !pineconeHost || !pineconeIndexName) {
         console.error("API Error: Missing environment variables during request processing.");
         return NextResponse.json({ error: "Internal configuration error." }, { status: 500 });
    }

    try {
        const body = await req.json();
        // Use Message type from 'ai' package
        const messages: Message[] = body.messages ?? [];
        const currentMessageContent = messages[messages.length - 1]?.content;

        if (typeof currentMessageContent !== 'string') {
             console.error(`[API /api/chat] Invalid query type received: ${typeof currentMessageContent}`);
             return NextResponse.json({ error: "Invalid query format" }, { status: 400 });
        }

        console.log(`[API /api/chat] Received query: "${currentMessageContent}"`);

        // --- Initialize Embeddings & Pinecone (using Langchain for Retrieval) ---
        const embeddings = new OpenAIEmbeddings({ openAIApiKey, model: embeddingModelName });
        const pinecone = new Pinecone({ apiKey: pineconeApiKey });
        const pineconeIndex = pinecone.Index(pineconeIndexName, pineconeHost);
        const vectorStore = await PineconeStore.fromExistingIndex(embeddings, { pineconeIndex });
        const retriever = vectorStore.asRetriever({ k: retrievalDocsCount });

        // --- 1. Retrieve Relevant Documents (using Langchain) ---
        // Use RunnableLambda to correctly pass the string query to the retriever
        const retrieveDocs = RunnableLambda.from(async (input: string) => {
             // Ensure retriever is correctly initialized before calling
             if (!retriever) throw new Error("Retriever not initialized");
             return await retriever.getRelevantDocuments(input);
        });
        const relevantDocs = await retrieveDocs.invoke(currentMessageContent);

        // Format the retrieved documents into a single string context
        const context = formatDocumentsAsString(relevantDocs); // Use inline helper

        console.log(`[API /api/chat] Retrieved ${relevantDocs.length} documents for context.`);
        // console.log(`[API /api/chat] Context:\n---\n${context}\n---`); // Uncomment for debugging context

        // --- 2. Construct the Final Prompt String ---
        // Use Langchain's PromptTemplate or simple string formatting
        const prompt = await PromptTemplate.fromTemplate(TEMPLATE_STRING).format({
            context: context,
            question: currentMessageContent,
        });

        // --- 3. Call the AI model using Vercel AI SDK 'streamText' ---
        // Get the Vercel AI SDK OpenAI provider instance
        const model = openai(chatModelName, { apiKey: openAIApiKey });

        console.log(`[API /api/chat] Calling model '${chatModelName}' via streamText...`);

        // Call streamText (imported from 'ai') with the model and the final formatted prompt
        const streamResult = await streamText({
            model: model,
            prompt: prompt,
            temperature: 0.3,
        });

        // --- 4. Return the stream as a Data Stream Response ---
        // This creates the specific format the useChat hook expects
        return streamResult.toDataStreamResponse(); // <<< CORRECT RETURN TYPE

    } catch (error: any) {
        console.error("[API /api/chat] Error processing request:", error);
        console.error("[API /api/chat] Error details:", error.message, error.stack);
        return NextResponse.json(
             { error: "An error occurred while processing your request.", details: error.message },
             { status: 500 }
        );
    }
}
