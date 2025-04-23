import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document # Already imported

# --- Add imports for loading and splitting ---
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader # For loading files
from langchain.text_splitter import RecursiveCharacterTextSplitter # For chunking
import pathlib # For robust path handling

# ----- LOAD ENV VARS -----
load_dotenv() # Load variables from .env file in the same directory or parent dirs
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Needed for embeddings
PINECONE_INDEX = "virt-me" # Your specified index name

# --- Environment Variable Checks ---
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Make sure it's in your .env file.")
if not PINECONE_API_KEY:
     raise ValueError("PINECONE_API_KEY not found in environment variables. Make sure it's in your .env file.")

# ----- Define Data Path -----
# Assumes your source documents (PDFs, TXTs) are in a 'data' directory
# located in the parent directory of this script.
# Example: ProjectRoot/data/*, ProjectRoot/scripts/ingest.py
# Adjust the path if your structure is different.
try:
    script_dir = pathlib.Path(__file__).parent.resolve()
    DATA_PATH = script_dir.parent / "data"
    # If your script is in the Project Root, you might just use:
    # DATA_PATH = pathlib.Path("data")
    if not DATA_PATH.is_dir():
         print(f"Warning: Data directory not found at expected location: {DATA_PATH}")
         print("Please ensure your documents are in the correct 'data' directory.")
         # Decide if you want to exit or continue (maybe create it?)
         # exit(1) # Uncomment to exit if data directory is missing
except NameError:
     # Handle case where __file__ is not defined (e.g., running in interactive session)
     DATA_PATH = pathlib.Path("data")
     print(f"Warning: Could not determine script location automatically. Assuming data directory is: {DATA_PATH}")


# ----- INIT -----
print("Initializing Pinecone client...")
pc = Pinecone(api_key=PINECONE_API_KEY)
# Consider adding a check here to ensure the index 'virt-me' exists
# and has the correct dimension (1536 for text-embedding-3-small)

print(f"Connecting to Pinecone index '{PINECONE_INDEX}'...")
index = pc.Index(PINECONE_INDEX)
# You might need index.describe_index_stats() to confirm connection & dimension

print("Initializing OpenAI Embeddings (model='text-embedding-3-small')...")
# Pass the API key explicitly for clarity and robustness
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

print("Initializing PineconeVectorStore...")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# ================== START: Load & Chunk Documents ==================
print(f"Loading documents from: {DATA_PATH}")
all_loaded_docs = [] # Initialize an empty list to store documents from all loaders

# --- Load Text and Markdown files (.txt, .md) ---
try:
    print("-" * 40)
    print("Attempting to load text (.txt, .md) files...")
    text_loader_instance = DirectoryLoader(
        path=str(DATA_PATH),            # Path to the directory
        glob="*.txt",     # Pattern for .txt and .md files (excludes hidden)
        loader_cls=TextLoader,        # Specify TextLoader for these files
        loader_kwargs={'encoding': 'utf-8'}, # Optional: Specify encoding for TextLoader
        use_multithreading=True,      # Use multiple threads for loading
        show_progress=True,           # Display a progress bar
        recursive=True,               # Search subdirectories
        silent_errors=False,           # Continue if a single file fails to load
    )
    loaded_text_docs = text_loader_instance.load()
    if loaded_text_docs:
        print(f"Successfully loaded {len(loaded_text_docs)} text/markdown documents.")
        all_loaded_docs.extend(loaded_text_docs)
    else:
        print("No text/markdown documents found or loaded.")
except Exception as e:
    print(f"An error occurred while loading text/markdown files: {e}")

# --- Load PDF files (.pdf) ---
# Requires 'pypdf': pip install pypdf
try:
    print("-" * 40)
    print("Attempting to load PDF (.pdf) files...")
    pdf_loader_instance = DirectoryLoader(
        path=str(DATA_PATH),
        glob="**/*.pdf",             # Pattern specifically for .pdf files
        loader_cls=PyPDFLoader,     # Specify PyPDFLoader
        use_multithreading=True,    # Multithreading might be slow for some PDFs
        show_progress=True,
        recursive=True,
        silent_errors=True,         # Recommended for PDFs which can be complex/corrupted
    )
    loaded_pdf_docs = pdf_loader_instance.load()
    if loaded_pdf_docs:
        print(f"Successfully loaded {len(loaded_pdf_docs)} PDF documents.")
        all_loaded_docs.extend(loaded_pdf_docs)
    else:
        print("No PDF documents found or loaded.")
except ImportError:
     print("\n>>> PyPDFLoader requires the 'pypdf' library. <<<")
     print(">>> Please install it using: pip install pypdf <<<")
     print(">>> Skipping PDF loading for now. <<<\n")
except Exception as e:
    print(f"An error occurred while loading PDF files: {e}")


# --- Add other DirectoryLoader instances here for other file types ---
# Example: Load Word documents (.docx)
# Requires 'python-docx' and potentially 'unstructured': pip install python-docx unstructured
# try:
#     from langchain_community.document_loaders import UnstructuredWordDocumentLoader # Or Docx2txtLoader etc.
#     print("-" * 40)
#     print("Attempting to load Word (.docx) files...")
#     docx_loader_instance = DirectoryLoader(
#         path=str(DATA_PATH),
#         glob="**/*.docx",
#         loader_cls=UnstructuredWordDocumentLoader,
#         # loader_kwargs={'mode': 'single'}, # Example kwarg if needed by loader
#         show_progress=True, recursive=True, silent_errors=True
#     )
#     loaded_docx_docs = docx_loader_instance.load()
#     if loaded_docx_docs:
#         print(f"Successfully loaded {len(loaded_docx_docs)} Word documents.")
#         all_loaded_docs.extend(loaded_docx_docs)
#     else:
#         print("No Word documents found or loaded.")
# except ImportError:
#     print("\n>>> Loading .docx files requires additional libraries (e.g., 'unstructured', 'python-docx'). <<<")
#     print(">>> See Langchain docs for specific requirements. Skipping DOCX loading. <<<\n")
# except Exception as e:
#     print(f"An error occurred while loading Word files: {e}")
# print("-" * 40)

# --- Proceed with splitting if any documents were loaded ---
if not all_loaded_docs:
    print("\nNo documents were successfully loaded from any specified type. Nothing to ingest.")
    exit() # Stop the script

print(f"\nSuccessfully loaded a total of {len(all_loaded_docs)} documents from all sources.")
print("-" * 40)

# Initialize the text splitter (same as before)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    add_start_index=True,
)

print(f"Splitting {len(all_loaded_docs)} documents into chunks (chunk_size=1000, overlap=200)...")
# Use the combined 'all_loaded_docs' list for splitting
documents = text_splitter.split_documents(all_loaded_docs)
print(f"Created {len(documents)} document chunks.")

# Optional: Log sample chunk details for verification (same as before)
if documents:
    print("-" * 40)
    print(f"Sample Chunk 1 Metadata: {documents[0].metadata}")
    print(f"Sample Chunk 1 Content Preview: {documents[0].page_content[:250]}...")
    print("-" * 40)

# =================== END: Load & Chunk Documents ===================

# ... (The rest of your script: UUID generation, adding documents to Pinecone, etc.) ...

if not documents: # Add a check here too before proceeding
    print("No document chunks were created after splitting. Exiting.")
    exit()

print(f"Generating {len(documents)} UUIDs for document chunks...")
# ... (rest of the script)


if not all_loaded_docs:
    print("\nNo documents were successfully loaded from any specified type. Nothing to ingest.")
    exit() # Stop the script

print(f"\nSuccessfully loaded a total of {len(all_loaded_docs)} documents from all sources.")
print("-" * 40)

# Initialize the text splitter for chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, # Target size for each chunk (in characters)
    chunk_overlap=200, # Number of characters to overlap between chunks
    length_function=len, # How to measure chunk size (standard len is fine)
    add_start_index=True, # Optional: Adds metadata about chunk start position
)

print(f"Splitting {len(all_loaded_docs)} documents into chunks (chunk_size=1000, overlap=200)...")
# Use the combined 'all_loaded_docs' list for splitting
documents = text_splitter.split_documents(all_loaded_docs)
print(f"Created {len(documents)} document chunks.")

# Optional: Log sample chunk details for verification
if documents:
    print("-" * 40)
    print(f"Sample Chunk 1 Metadata: {documents[0].metadata}")
    print(f"Sample Chunk 1 Content Preview: {documents[0].page_content[:250]}...")
    print("-" * 40)
# =================== END: Load & Chunk Documents ===================

# --- Continue with your existing logic ---

if not documents:
    print("No document chunks were created. Exiting.")
    exit()

print(f"Generating {len(documents)} UUIDs for document chunks...")
# Note: Using random UUIDs means duplicates might be added if the script runs multiple times.
# For automatic deduplication based on content, you might omit the 'ids' parameter below,
# letting Langchain generate deterministic IDs (if supported by PineconeVectorStore).
uuids = [str(uuid4()) for _ in range(len(documents))]

print(f"Adding {len(documents)} document chunks to Pinecone index '{PINECONE_INDEX}'...")
# The add_documents method handles embedding the chunks and upserting them
try:
    vector_store.add_documents(documents=documents, ids=uuids)
    print("✅ Document ingestion complete.")
    print(f"Successfully added {len(documents)} chunks to the '{PINECONE_INDEX}' index.")
except Exception as e:
     print(f"Error adding documents to Pinecone: {e}")
     print("Check Pinecone API key, index status, and network connection.")