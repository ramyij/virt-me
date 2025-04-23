import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document # Keep this import

# --- Add imports for loading and splitting ---
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader # For loading files
from langchain.text_splitter import RecursiveCharacterTextSplitter # For chunking other docs
import pathlib # For robust path handling

# ================== START: Define Resume Chunks ==================
# Paste the pre-defined resume_chunks list here
# (Copied from the 'resume_chunks_code' artifact)
resume_chunks = [
    # --- Contact Info ---
    Document(
        page_content="Ramy Jaber\nlinkedin.com/in/ramyj\nNew Jersey\nramyij@pm.me\n732.567.2603",
        metadata={"section": "Contact"}
    ),
    # --- Experience: Intel (Verbose) ---
    Document(
        page_content="My most recent professional experience is at Intel, where I've been working remotely from New Jersey since October 2022. My roles here have included Cloud Solution Architect focused on LLMs and, previously, Manager of Cloud Solution Architects for Performance Engineering at Granulate.io (which Intel acquired).\n\nAs a Cloud Solution Architect for LLMs, I played a key role in the technical go-to-market integration for a major $70 million, 3-year partnership with SeekrFlow's Enterprise LLM (seekr.com). My responsibilities included developing demonstration Python notebooks, creating technical sales materials, and training both sales and solutions teams. This work directly resulted in driving 7 enterprise customer engagements and securing two committed Proofs of Value (POVs) within just the first three months.\n\nI also led technical pre-sales engagements, guiding customers from the initial meeting all the way through the technical proof-of-concept (POC) phase. A significant part of this involved migrating customer's existing CUDA-based LLM pipelines to Intel's Gaudi hardware. This required ensuring full functionality, carefully measuring performance, and implementing necessary optimizations. I'm proud to say we achieved technical wins on 5 out of the 6 POCs I completed, contributing directly to approximately $8 million in new business over a 9-month period.\n\nFurthermore, I've partnered closely with several high-growth AI startups like Stability AI, Character.ai, and Pathway. In these collaborations, I helped architect LLM solutions specifically for them, guiding their technical migrations to the Gaudi architecture and securing technical wins across multiple POCs.\n\nIn my prior role as Manager for Performance Engineering (at Granulate.io before the Intel acquisition), I led a team of 4 Solution Engineers managing a portfolio worth $7 million in Annual Recurring Revenue (ARR). I served as the main point of escalation for critical customer technical issues and strategically coordinated limited research resources to maximize business impact.\n\nOne notable experience was successfully managing the crisis response during a major production outage at our largest customer. We were able to mitigate the performance degradation within 25 minutes, and I subsequently led the root cause analysis which was crucial in rebuilding the customer's trust.\n\nI also focused on growing startup customer accounts significantly. For example, I expanded the Nylas account from $200K to $800K ARR over two years. With iFood, a major Brazilian delivery platform, I scaled their engagement from the initial call to $1.1 million through a phased adoption of our Databricks and Kubernetes optimization solutions.\n\nAdditionally, I developed Python automation tools that dramatically increased our customer onboarding capacity from handling 20 workloads per day to 300. This automation typically resulted in compute cost reductions of around 40% for our customers.",
        metadata={"section": "Experience", "company": "Intel", "roles": ["Cloud Solution Architect - LLMs", "Manager, Cloud Solution Architect - Performance Engineering"], "location": "Remote, NJ", "dates": "Oct 2022 - Present"}
    ),
    # --- Experience: DataRobot (Verbose) ---
    Document(
        page_content="Before Intel, I worked at DataRobot from July 2021 to October 2022 as a Pre-sales Data Scientist, based remotely in New Jersey.\n\nIn this role, I led technical presales activities for accounts across various sectors including Financial Services, Retail, and Telecom within the NYC region. My work involved delivering demos tailored to specific client needs. One example I'm particularly proud of is developing a novel credit rating prediction solution designed for private business loans, which directly led to three additional POC engagements.\n\nI also played a key role in preventing a potential $2 million account churn. I achieved this by proactively identifying and incubating new use cases for DataRobot's platform across two different departments within the client organization, which included developing a novel automation solution for model compliance documentation.",
        metadata={"section": "Experience", "company": "DataRobot", "roles": ["Pre-sales Data Scientist"], "location": "Remote, NJ", "dates": "Jul 2021 - Oct 2022"}
    ),
    # --- Experience: Udacity (Verbose) ---
    Document(
        page_content="Prior to DataRobot, I was with Udacity from February 2019 to April 2021, working remotely from New York. I held two key roles there: Director of Solution Architects for Global Enterprise, and earlier, Senior Solution Architect.\n\nAs Director, I built the Solutions Architecture team entirely from the ground up. Over 18 months, I hired and managed a team of 10 Solution Architects, handling everything from performance reviews to career development coaching. During this time, the team consistently exceeded revenue targets: achieving $13M (1.7x quota) in Year 1, $33M (1.8x quota) in Year 2, and projecting $40M (1.1x quota) in Year 3.\n\nOne major initiative I led was the development of an enterprise skills transformation program for a Big 4 consultancy firm. This involved designing the curriculum and creating custom projects aimed at upskilling over 400 of their employees in data analytics.\n\nI also spearheaded the development of a comprehensive sales methodology in partnership with Force Management. This involved defining key elements like Value Messaging and MEDDPICC, as well as standardizing sales stages, which led to more consistent performance across different regions.\n\nIn my earlier role as Senior Solution Architect at Udacity, I was the very first pre-sales technical resource brought onto their rapidly growing Enterprise Sales team. I essentially defined the Solution Architect role within the company and personally supported $13 million in sales during 2019.\n\nI was instrumental in expanding a key account's revenue (Shell Oil & Gas) by $2.1 million through building strong executive relationships and acting as a technical partner.\n\nAdditionally, I regularly evangelized our technical content knowledge across Data Science, AI/ML, and Cloud topics by presenting monthly content 'deep dives' and other enablement sessions for the broader teams.",
        metadata={"section": "Experience", "company": "Udacity", "roles": ["Director, Solution Architects - Global Enterprise", "Senior Solution Architect"], "location": "Remote, NY", "dates": "Feb 2019 - Apr 2021"}
    ),
    # --- Experience: Appian Corporation (Verbose) ---
    Document(
        page_content="My earlier experience includes working at Appian Corporation in Reston, VA, from February 2015 to July 2017. I progressed through roles from Solution Engineer to Senior Solution Engineer, and finally to Lead Solution Engineer.\n\nAs a Lead Solution Engineer, I was one of three team leads responsible for managing the significant growth of our team, which expanded from 8 to 29 members. My direct management responsibilities included 3 engineers, covering their performance evaluations and career development planning.\n\nDuring my time there, I led a project team focused on analyzing the performance of about 600 different sites. As part of this project, I developed Python scripts designed to ingest monitoring alerts. These scripts successfully reduced the overwhelming noise of hundreds of hourly emails by approximately 85%, making the alert system much more manageable.\n\nI also collaborated closely with the Product Development team. By providing detailed analysis of performance log data and offering recommended actions, I helped them resolve several high-impact software bugs.",
        metadata={"section": "Experience", "company": "Appian Corporation", "roles": ["Lead Solution Engineer", "Senior Solution Engineer", "Solution Engineer"], "location": "Reston, VA", "dates": "Feb 2015 - Jul 2017"}
    ),
    # --- Education: Columbia ---
    Document(
        page_content="EDUCATION\nColumbia University in the City of New York (December 2018 - New York, NY)\nMasters of Science in Data Science",
        metadata={"section": "Education", "institution": "Columbia University", "degree": "Masters of Science in Data Science", "graduation_date": "December 2018", "location": "New York, NY"}
    ),
    # --- Education: Stevens ---
    Document(
        page_content="Stevens Institute of Technology (May 2012 - Hoboken, NJ)\nBachelors of Engineering in Engineering Management\nMinor in Economics\nMinor in Pure and Applied Mathematics",
        metadata={"section": "Education", "institution": "Stevens Institute of Technology", "degree": "Bachelors of Engineering in Engineering Management", "minors": ["Economics", "Pure and Applied Mathematics"], "graduation_date": "May 2012", "location": "Hoboken, NJ"}
    ),
    # --- Skills: Leadership & Strategy ---
    Document(
        page_content="SKILLS\nLEADERSHIP & STRATEGY\nExecutive Relationship Management\nTechnical Team Management\nSales Enablement & Training\nEnterprise Account Strategy\nCross-functional Collaboration",
        metadata={"section": "Skills", "category": "Leadership & Strategy"}
    ),
    # --- Skills: Data Science / ML / Gen AI ---
    Document(
        page_content="DATA SCIENCE / ML / GEN AI\nPyTorch\nTransformers\nModel performance analysis\nInference Optimization\nInfrastructure Evaluation\nModel deployment and monitoring\nModel Serving (vLLM)",
        metadata={"section": "Skills", "category": "Data Science / ML / Gen AI"}
    ),
    # --- Skills: Cloud Administration ---
    Document(
        page_content="CLOUD ADMINISTRATION\nSpark - Databricks, EMR, Dataproc\nInfrastructure - VMs, storage, serverless\nKubernetes Orchestration",
        metadata={"section": "Skills", "category": "Cloud Administration"}
    ),
    # --- Skills: Solution Architecture ---
    Document(
        page_content="SOLUTION ARCHITECTURE\nProduct demos\nUse Case identification\nPOV Execution\nProduct feedback",
        metadata={"section": "Skills", "category": "Solution Architecture"}
    ),
    # --- Skills: Sales ---
    Document(
        page_content="SALES\nMEDDPICC\nValue based selling\nForce Management",
        metadata={"section": "Skills", "category": "Sales"}
    ),
]
# =================== END: Define Resume Chunks ===================


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


# ----- INIT -----
print("Initializing Pinecone client...")
pc = Pinecone(api_key=PINECONE_API_KEY)

print(f"Connecting to Pinecone index '{PINECONE_INDEX}'...")
index = pc.Index(PINECONE_INDEX)

print("Initializing OpenAI Embeddings (model='text-embedding-3-small')...")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

print("Initializing PineconeVectorStore...")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# ================== START: Load & Chunk OTHER Documents ==================
# This section now only loads and splits documents *other than* the resume
# Ensure your resume file itself is NOT in the DATA_PATH or adjust globs to exclude it.

print(f"Loading OTHER documents (non-resume) from: {DATA_PATH}")
loaded_other_docs = [] # Initialize list for docs loaded from files

# --- Load Text and Markdown files (.txt, .md) ---
# Modify glob if needed to exclude specific filenames like 'resume.txt'
try:
    print("-" * 40)
    print("Attempting to load text (.txt, .md) files...")
    text_loader_instance = DirectoryLoader(
        path=str(DATA_PATH),
        glob="**/*.{txt,md}", # Adjust glob if resume file needs exclusion
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'},
        use_multithreading=True,
        show_progress=True,
        recursive=True,
        silent_errors=True, # Set True to ignore files it can't load
    )
    loaded_text_docs = text_loader_instance.load()
    if loaded_text_docs:
        print(f"Successfully loaded {len(loaded_text_docs)} text/markdown documents.")
        loaded_other_docs.extend(loaded_text_docs)
    else:
        print("No text/markdown documents found or loaded.")
except Exception as e:
    print(f"An error occurred while loading text/markdown files: {e}")

# --- Load PDF files (.pdf) ---
# Modify glob if needed to exclude specific filenames like 'resume.pdf'
try:
    print("-" * 40)
    print("Attempting to load PDF (.pdf) files...")
    pdf_loader_instance = DirectoryLoader(
        path=str(DATA_PATH),
        glob="**/*.pdf", # Adjust glob if resume file needs exclusion
        loader_cls=PyPDFLoader,
        use_multithreading=True,
        show_progress=True,
        recursive=True,
        silent_errors=True,
    )
    loaded_pdf_docs = pdf_loader_instance.load()
    if loaded_pdf_docs:
        print(f"Successfully loaded {len(loaded_pdf_docs)} PDF documents.")
        loaded_other_docs.extend(loaded_pdf_docs)
    else:
        print("No PDF documents found or loaded.")
except ImportError:
     print("\n>>> PyPDFLoader requires 'pypdf'. Skipping PDF loading. <<<\n")
except Exception as e:
    print(f"An error occurred while loading PDF files: {e}")

# --- Split ONLY the loaded OTHER documents ---
split_other_docs = []
if loaded_other_docs:
    print(f"\nSplitting {len(loaded_other_docs)} loaded documents (non-resume)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    split_other_docs = text_splitter.split_documents(loaded_other_docs)
    print(f"Created {len(split_other_docs)} chunks from other documents.")
else:
    print("\nNo other documents were loaded to be split.")

# =================== END: Load & Chunk OTHER Documents ===================

# --- Combine Resume Chunks and Split Other Docs ---
print("-" * 40)
print(f"Defined {len(resume_chunks)} resume chunks.")
all_docs_to_ingest = resume_chunks + split_other_docs # Combine the lists

if not all_docs_to_ingest:
    print("No documents or resume chunks available to ingest. Exiting.")
    exit()

print(f"Total documents/chunks to ingest: {len(all_docs_to_ingest)}")

# --- Generate UUIDs ---
print(f"Generating {len(all_docs_to_ingest)} UUIDs for document chunks...")
# Consider deterministic IDs if you might re-run ingestion often
# uuids = [generate_deterministic_id(doc) for doc in all_docs_to_ingest]
uuids = [str(uuid4()) for _ in range(len(all_docs_to_ingest))]

# --- Add Documents to Pinecone ---
print(f"Adding {len(all_docs_to_ingest)} document chunks to Pinecone index '{PINECONE_INDEX}'...")
try:
    # Consider batching if you have a very large number of chunks
    vector_store.add_documents(documents=all_docs_to_ingest, ids=uuids) # Pass combined list
    print("-" * 40)
    print("✅ Document ingestion complete.")
    print(f"Successfully added {len(all_docs_to_ingest)} chunks to the '{PINECONE_INDEX}' index.")
    print("-" * 40)
except Exception as e:
     print(f"Error adding documents to Pinecone: {e}")
     print("Check Pinecone API key, index status, and network connection.")

