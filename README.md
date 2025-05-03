# Virt-Me

Virt-Me is a personalized AI assistant application built with Next.js and the Vercel AI SDK. It leverages retrieval-augmented generation (RAG) to provide contextually relevant responses based on your knowledge base. This project demonstrates how AI can be seamlessly integrated into modern web applications to deliver intelligent and interactive user experiences.

## Features

- **AI Chat Interface**: Interact with an AI assistant powered by OpenAI's GPT-4.1.
- **Knowledge Retrieval**: Automatically retrieves relevant information from your vector database.
- **Memory Management**: Add new information to your knowledge base (in development mode).
- **Vector Database**: Uses Pinecone for efficient similarity search and storage.

## Prerequisites

Before you begin, ensure you have the following:

- Node.js (v18 or higher recommended)
- [pnpm](https://pnpm.io/installation) package manager
- OpenAI API key
- Pinecone account and API key

## Installation

Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone www.github.com/ramyij/virt-me
   cd virt-me
   ```

2. Install dependencies using `pnpm`:
   ```bash
   pnpm install
   ```

3. Create a `.env.local` file in the root directory and add the following environment variables:
   ```env
   OPENAI_API_KEY=<your-openai-api-key>
   PINECONE_API_KEY=<your-pinecone-api-key>
   PINECONE_ENVIRONMENT=<your-pinecone-environment>
   ```

4. Set up your Pinecone index:
   - Log in to your Pinecone account.
   - Create a new index with the desired configuration (e.g., dimensions matching your embeddings model).
   - Update the `.env.local` file with the index name:
     ```env
     PINECONE_INDEX=<your-pinecone-index-name>
     ```

5. Start the development server:
   ```bash
   pnpm dev
   ```

6. Open your browser and navigate to `http://localhost:3000` to access the application.

## Deployment

To deploy the application, follow these steps:

1. Push your code to a GitHub repository.
2. Connect your repository to Vercel.
3. Add the same environment variables from `.env.local` to your Vercel project settings.
4. Deploy the application directly from Vercel.

## Usage

- Interact with the AI assistant through the chat interface.
- Add new knowledge to the database in development mode.
- Customize the application by modifying the components and API routes.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
