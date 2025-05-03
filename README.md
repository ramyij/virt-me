# Virt-Me

A personalized AI assistant application built with Next.js and the Vercel AI SDK that leverages retrieval-augmented generation (RAG) to provide contextually relevant responses based on your knowledge base.

## Features

- **AI Chat Interface**: Interact with an AI assistant powered by OpenAI's GPT-4.1
- **Knowledge Retrieval**: Automatically retrieves relevant information from your vector database
- **Memory Management**: Add new information to your knowledge base (in development mode)
- **Vector Database**: Uses Pinecone for efficient similarity search and storage

## Prerequisites

- Node.js (v18 or higher recommended)
- [pnpm](https://pnpm.io/installation) package manager
- OpenAI API key
- Pinecone account and API key

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd virt-me
   ```

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
