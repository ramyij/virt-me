import os
from dotenv import load_dotenv
from pinecone import Pinecone

# --- Load Environment Variables ---
load_dotenv() # Or load from .env.local if needed
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "virt-me") # Use your index name

if not PINECONE_API_KEY or not PINECONE_INDEX:
    raise ValueError("Pinecone API Key or Index Name not found in environment variables.")

# --- Initialize Pinecone ---
print("Initializing Pinecone client...")
pc = Pinecone(api_key=PINECONE_API_KEY)

print(f"Connecting to Pinecone index '{PINECONE_INDEX}'...")
index = pc.Index(PINECONE_INDEX)

# --- !! DANGER ZONE: Delete All Vectors !! ---
print("\n" + "="*40)
print(f"WARNING: About to delete ALL vectors from index '{PINECONE_INDEX}'.")
print("This action is irreversible.")
confirmation = input("Type 'DELETE' to confirm: ")

if confirmation == "DELETE":
    try:
        print(f"Deleting all vectors from index '{PINECONE_INDEX}'...")
        index.delete(deleteAll=True)
        print("✅ Successfully deleted all vectors.")
        # Optional: Verify by checking stats
        # stats = index.describe_index_stats()
        # print("Current stats:", stats)
    except Exception as e:
        print(f"❌ Error deleting vectors: {e}")
else:
    print("Deletion cancelled.")

print("="*40)