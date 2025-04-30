import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
import pathlib # Keep for path handling for .env file

# --- Import pre-defined data ---
# Assume all data to be ingested is imported here
from resume_data import resume_chunks

# Try to import auto-generated chunked data
try:
    from chunked_data import text_chunks
    print(f"Successfully imported {len(text_chunks)} chunks from chunked_data.py")
except ImportError:
    print("Warning: Could not import from chunked_data.py. Run utils/chunk.py first?")
    text_chunks = [] # Default to empty list if file doesn't exist or is empty
except Exception as e:
    print(f"Warning: An error occurred importing from chunked_data.py: {e}")
    text_chunks = []

# If you have other data files (e.g., blog_data.py), import them too:
# from .blog_data import blog_chunks


# ----- LOAD ENV VARS -----
# Determine the directory containing the script file
try:
    script_dir = pathlib.Path(__file__).parent.resolve()
    dotenv_file_path = script_dir.parent / ".env.local" # Assuming .env.local is in parent dir
    print(f"Looking for .env.local file at: {dotenv_file_path}")
except NameError:
    dotenv_file_path = pathlib.Path(".env.local")
    print(f"Warning: Could not determine script directory. Looking for .env.local in current directory: {dotenv_file_path}")

loaded_successfully = load_dotenv(dotenv_path=dotenv_file_path)
if not loaded_successfully:
    print(f"Warning: .env.local file not found at {dotenv_file_path} or is empty.")
    # Decide if you want to exit if the file is crucial
    # exit(1)

# ----- Get Environment Variables using os.getenv -----
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "virt-me") # Default to 'virt-me' if not set

# --- Environment Variable Checks ---
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Check .env.local.")
if not PINECONE_API_KEY:
     raise ValueError("PINECONE_API_KEY not found in environment variables. Check .env.local.")
if not PINECONE_INDEX:
     raise ValueError("PINECONE_INDEX not found or is empty. Check .env.local or set a default.")

# ----- Define Data Path (for non-resume files) -----
# Assumes your *other* source documents (transcripts, etc.) are in 'data'
try:
    # Use the script_dir calculated earlier
    DATA_PATH = script_dir.parent / "data"
except NameError:
     DATA_PATH = pathlib.Path("data") # Fallback

if not DATA_PATH.is_dir():
     print(f"Warning: Data directory for other documents not found at: {DATA_PATH}")
     # Continue even if missing, as we have resume chunks


# ----- INIT CLIENTS -----
print("Initializing Pinecone client...")
pc = Pinecone(api_key=PINECONE_API_KEY)

print(f"Connecting to Pinecone index '{PINECONE_INDEX}'...")
index = pc.Index(PINECONE_INDEX)

print("Initializing OpenAI Embeddings (model='text-embedding-3-small')...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

print("Initializing PineconeVectorStore...")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)


# --- Prepare Documents for Ingestion ---
print("-" * 40)
# Combine all imported document lists here
all_docs_to_ingest = resume_chunks # Start with resume chunks

# Extend with the auto-generated chunks if they were loaded
if text_chunks:
    all_docs_to_ingest.extend(text_chunks)
    print(f"Added {len(text_chunks)} chunks from text files.")
else:
    print("No additional text file chunks were added.")

if not all_docs_to_ingest:
    print("No documents found in imported lists (e.g., resume_chunks). Exiting.")
    exit()

print(f"Found {len(all_docs_to_ingest)} pre-defined document chunks to ingest.")


# --- Generate UUIDs ---
print(f"Generating {len(all_docs_to_ingest)} UUIDs for document chunks...")
uuids = [str(uuid4()) for _ in range(len(all_docs_to_ingest))]


# --- Add Documents to Pinecone ---
print(f"Adding {len(all_docs_to_ingest)} document chunks to Pinecone index '{PINECONE_INDEX}'...")
try:
    # Consider batching if you have a very large number of chunks (e.g., > 1000)
    vector_store.add_documents(documents=all_docs_to_ingest, ids=uuids)
    print("-" * 40)
    print("✅ Document ingestion complete.")
    print(f"Successfully added {len(all_docs_to_ingest)} chunks to the '{PINECONE_INDEX}' index.")
    print("-" * 40)
except Exception as e:
     print(f"Error adding documents to Pinecone: {e}")
     print("Check Pinecone API key, index status, and network connection.")

