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
    # --- Family ---
    Document(
    page_content="My family is the center of my life, consisting of my wife and our two young boys - a toddler and an infant. As parents of young children, much of our free time revolves around family-oriented activities that allow us to spend quality time together while fostering our children's development and appreciation for the outdoors.\n\nWe particularly enjoy spending time outside as a family, frequently exploring local hiking trails that are manageable with young children. These outings give us an opportunity to introduce our boys to nature, teach them about plants and animals, and build their physical endurance in an enjoyable way. The trails provide a perfect balance of adventure and accessibility for our family at different stages of development.\n\nWhen we're not hitting the trails, we're often found at local playgrounds where my wife and I have become what we jokingly call 'playground warriors' - experts at spotting the best playground equipment and creating imaginative games to keep our children engaged and active. These playground visits serve as both physical outlets for our energetic toddler and social opportunities for all of us to connect with other local families.\n\nBalancing the demands of parenting two young children while maintaining our other interests and responsibilities is certainly challenging, but the joy of watching our boys discover the world around them makes it all worthwhile.",
    metadata={
        "section": "Family", 
        "category": "Personal Life",
        "members": ["Wife", "Toddler son", "Infant son"],
        "activities": ["Hiking", "Outdoor play", "Playground visits"],
        "life_stage": "Young family"
        }
    ),

    # --- Hobbies: Mushroom Foraging ---
    Document(
    page_content="Mushroom foraging has developed into one of my most engaging and rewarding hobbies, combining my interests in outdoor exploration, natural science, and culinary experimentation. I spend considerable time in local forests and natural areas searching for and identifying various species of edible mushrooms throughout their respective growing seasons.\n\nMy foraging activities involve careful identification of safe edible species, sustainable harvesting practices to ensure future growth, and meticulous documentation of locations and conditions where specific varieties thrive. I've developed a particular knowledge of local species that appear at different times throughout the year in New Jersey's diverse ecosystems.\n\nAs an active member of the New Jersey Mycological Association, I regularly participate in group forays where knowledge is shared among members ranging from beginners to experts. These organized excursions provide valuable learning opportunities and allow me to connect with others who share this specialized interest. The association also offers identification workshops and educational sessions that have helped me develop confidence in distinguishing edible varieties from potentially dangerous lookalikes.\n\nThe culinary aspect of mushroom foraging is equally important to me. I enjoy experimenting with different preparation methods and recipes specifically designed to highlight the unique flavors and textures of wild-foraged fungi. From simple sautés that preserve the natural essence of chanterelles to more complex dishes incorporating multiple foraged varieties, I continuously explore new ways to incorporate my harvests into memorable meals.\n\nThis hobby connects me deeply with the seasonal rhythms of the local environment and provides a satisfying combination of outdoor activity, scientific learning, social connection, and culinary creativity.",
    metadata={
        "section": "Hobbies", 
        "category": "Mushroom Foraging",
        "activities": ["Identification", "Harvesting", "Cooking"],
        "organizations": ["New Jersey Mycological Association"],
        "locations": ["New Jersey forests"],
        "related_interests": ["Cooking", "Botany", "Outdoor activities"]
        }
    ),
    # --- Hobbies: Smart Home Technology ---
    Document(
    page_content="My smart home hobby represents a significant technical interest and time investment, focused specifically on creating a privacy-conscious and locally-controlled home automation system. Unlike mainstream consumer approaches that rely heavily on cloud services, I've deliberately built a system that operates entirely on my local network without external dependencies.\n\nAt the core of my setup is the Home Assistant ecosystem, which serves as the central hub for integrating various devices and automation workflows. This open-source platform allows me to maintain complete control over my data while avoiding the subscription costs and potential privacy concerns associated with cloud-based alternatives. I've configured Home Assistant to manage everything from lighting and climate control to security monitoring and entertainment systems.\n\nOne of my most technically advanced projects has been implementing a voice command system using a locally-hosted LLaMA model. This runs on a dedicated desktop computer equipped with a discrete GPU that provides the necessary processing power. The system converts spoken commands into actions within my home without sending any audio data to external servers, maintaining complete privacy while still offering convenient voice control functionality.\n\nI frequently work with ESP8266 microcontrollers to create custom sensors and control modules that integrate with my system. This often involves light soldering work and custom firmware development to 'hack' commercial products that would otherwise require cloud connectivity. These modifications ensure that all devices operate fully within my local network architecture.\n\nBeyond the practical benefits of privacy and cost savings, this hobby satisfies my technical curiosity and desire for complete understanding of the systems I use daily. Each component represents a small project in itself, from hardware modifications to software configuration and integration challenges.",
    metadata={
        "section": "Hobbies", 
        "category": "Smart Home Technology",
        "focus": ["Privacy", "Local networking", "DIY hardware"],
        "technologies": ["Home Assistant", "LLaMA", "ESP8266"],
        "skills": ["Soldering", "Hardware hacking", "System integration", "Local hosting"],
        "motivations": ["Privacy concerns", "Cost reduction", "Technical control"]
        }
    ),
# --- Hobbies: Photography ---
Document(
    page_content="Photography has been a passionate hobby of mine for many years, with a particular focus on three distinct subject areas: landscapes, neighborhood wildlife, and mushroom macrophotography.\n\nIn landscape photography, I've had the privilege of capturing the dramatic coastal scenes of Acadia National Park in Maine, with its rocky shorelines and striking sunrises over the Atlantic. I've also photographed the majestic mountain vistas and alpine lakes of Glacier National Park in Montana. Most recently, I've documented the otherworldly desert landscapes of Joshua Tree National Park in California, focusing on the unique Joshua trees against stunning sunset skies and the fascinating rock formations throughout the park.\n\nCloser to home, I've developed an eye for local wildlife photography, patiently documenting the birds, squirrels, rabbits, and occasional foxes that inhabit my neighborhood. This practice has taught me the value of patience and quick reflexes to capture fleeting natural moments.\n\nMy most specialized photography interest lies in macro photography of mushrooms and fungi. I'm fascinated by capturing the intricate details, textures, and colors of various mushroom species. This niche has led me to explore local forests during the damper seasons, carefully documenting the ephemeral fungi that emerge after rainfall. My macro equipment allows me to reveal the hidden details of these often-overlooked natural marvels.\n\nFor all my photographic work, I use a Sony a6000 crop sensor camera paired with a collection of E-mount prime lenses. My lens arsenal includes an 18mm for wide landscape vistas, a 24mm for general purpose shooting, a 50mm that excels at neighborhood wildlife, and a 105mm that's perfect for detailed macro work with mushrooms and fungi. This versatile yet compact setup allows me to capture everything from sweeping national park landscapes to the minute details of forest floor mushrooms.",
    metadata={
        "section": "Hobbies", 
        "category": "Photography", 
        "subjects": ["Landscapes", "Wildlife", "Macro", "Mushrooms"],
        "locations": ["Acadia National Park", "Glacier National Park", "Joshua Tree National Park", "Neighborhood"],
        "equipment_type": "Sony a6000 crop sensor with E-mount prime lenses (18mm, 24mm, 50mm, 105mm)",
        "experience_level": "Enthusiast"
        }
    ),
    # --- Contact Information (Alternative) ---
Document(
    page_content="Ramy Jaber\nNew Jersey resident\nContact: ramyij@pm.me | 732.567.2603\nProfessional profile: linkedin.com/in/ramyj",
    metadata={"section": "Contact"}
),

# --- Experience: Intel (Alternative) ---
Document(
    page_content="Since October 2022, I've been working at Intel in a remote capacity from my home in New Jersey. I initially joined as Manager of Cloud Solution Architects for Performance Engineering at Granulate.io (following Intel's acquisition) and later transitioned to the role of Cloud Solution Architect specializing in Large Language Models.\n\nIn my LLM-focused position, I was instrumental in the technical implementation of a significant partnership with SeekrFlow's Enterprise LLM platform (seekr.com), valued at $70 million over 3 years. My contributions included creating Python demonstration notebooks, developing technical sales collateral, and conducting training sessions for both sales representatives and solutions teams. These efforts yielded impressive results within just three months: 7 enterprise customer engagements initiated and two Proofs of Value (POVs) secured.\n\nMy responsibilities also encompassed end-to-end technical pre-sales management, from initial customer discussions through to the technical proof-of-concept stage. A critical component of this work involved helping customers transition their existing CUDA-based LLM implementations to Intel's Gaudi hardware platform. This required ensuring seamless functionality, conducting detailed performance analysis, and implementing optimizations where needed. My effectiveness in this area is reflected in our success rate: 5 successful technical wins out of 6 completed POCs, contributing approximately $8 million in revenue generation across a 9-month timeframe.\n\nI've also established strong working relationships with emerging AI companies including Stability AI, Character.ai, and Pathway. My collaboration with these organizations involved designing customized LLM solutions, facilitating their technical transition to Gaudi architecture, and achieving technical success across multiple proof-of-concept implementations.\n\nBefore my LLM specialization, I served as Manager for Performance Engineering at Granulate.io prior to its acquisition by Intel. In this capacity, I led a team of 4 Solution Engineers responsible for a $7 million ARR portfolio. I functioned as the primary escalation point for major customer technical challenges and strategically allocated limited research resources to maximize business outcomes.\n\nA particularly notable achievement was successfully managing the emergency response during a significant production outage affecting our largest client. We reduced performance degradation within 25 minutes, and I subsequently directed the comprehensive root cause investigation that proved essential in rebuilding customer confidence.\n\nI also focused on expanding startup customer relationships. With Nylas, I grew their account from $200K to $800K ARR over a two-year period. For iFood, a prominent Brazilian food delivery service, I guided their engagement from initial contact to a $1.1 million implementation through progressive adoption of our Databricks and Kubernetes optimization offerings.\n\nAnother significant contribution was my development of Python-based automation tools that substantially increased our customer onboarding capacity from 20 workloads daily to 300. This automation typically generated compute cost savings of approximately 40% for our customers.",
    metadata={"section": "Experience", "company": "Intel", "roles": ["Cloud Solution Architect - LLMs", "Manager, Cloud Solution Architect - Performance Engineering"], "location": "Remote, NJ", "dates": "Oct 2022 - Present"}
),

# --- Experience: DataRobot (Alternative) ---
Document(
    page_content="I was employed at DataRobot as a Pre-sales Data Scientist from July 2021 until October 2022, working remotely from my base in New Jersey.\n\nDuring my tenure, I spearheaded technical presales initiatives for clients across multiple industries including Financial Services, Retail, and Telecommunications throughout the NYC region. A core aspect of my role involved creating and delivering customized demonstrations aligned with specific client requirements. A particularly successful example was my development of an innovative credit rating prediction solution specifically designed for private business lending, which generated three additional proof-of-concept engagements.\n\nOne of my key accomplishments was successfully preventing potential revenue loss of $2 million. I achieved this by proactively identifying and developing new use cases for DataRobot's platform across multiple departments within an existing client organization, including creating an innovative automation solution focused on model compliance documentation.",
    metadata={"section": "Experience", "company": "DataRobot", "roles": ["Pre-sales Data Scientist"], "location": "Remote, NJ", "dates": "Jul 2021 - Oct 2022"}
),

# --- Experience: Udacity (Alternative) ---
Document(
    page_content="Between February 2019 and April 2021, I worked with Udacity in a remote capacity from New York. During this period, I progressed from Senior Solution Architect to Director of Solution Architects for Global Enterprise.\n\nIn my capacity as Director, I established the Solutions Architecture team from inception. Throughout an 18-month period, I recruited and supervised a team consisting of 10 Solution Architects, overseeing all aspects from conducting performance assessments to providing professional development guidance. Throughout my leadership, the team consistently surpassed revenue expectations: delivering $13M (exceeding quota by 1.7x) in the first year, $33M (exceeding quota by 1.8x) in the second year, with projections of $40M (exceeding quota by 1.1x) for the third year.\n\nA significant project under my leadership was creating an enterprise-wide skills transformation initiative for a major consultancy within the Big 4. This comprehensive undertaking involved curriculum design and development of specialized projects aimed at enhancing data analytics capabilities for more than 400 employees.\n\nI also led the creation of a detailed sales methodology working collaboratively with Force Management. This encompassed defining critical components such as Value Messaging frameworks and MEDDPICC sales processes, alongside standardizing various sales stages, resulting in more uniform performance across geographic regions.\n\nDuring my initial position as Senior Solution Architect at Udacity, I was the inaugural pre-sales technical specialist integrated into their expanding Enterprise Sales division. I essentially pioneered the Solution Architect function within the organization and personally contributed to $13 million in sales revenue throughout 2019.\n\nI played a crucial role in growing revenue from a strategic account (Shell Oil & Gas) by $2.1 million through developing robust executive-level relationships and serving as their dedicated technical advisor.\n\nI also regularly shared technical knowledge across Data Science, AI/ML, and Cloud domains by delivering monthly in-depth content presentations and facilitation sessions for broader team education.",
    metadata={"section": "Experience", "company": "Udacity", "roles": ["Director, Solution Architects - Global Enterprise", "Senior Solution Architect"], "location": "Remote, NY", "dates": "Feb 2019 - Apr 2021"}
),

# --- Experience: Appian Corporation (Alternative) ---
Document(
    page_content="From February 2015 to July 2017, I was employed at Appian Corporation in Reston, Virginia. During this time, I advanced through several positions, beginning as a Solution Engineer, then progressing to Senior Solution Engineer, and ultimately reaching the position of Lead Solution Engineer.\n\nAs a Lead Solution Engineer, I was among three team leaders tasked with guiding the substantial expansion of our department, which grew from 8 to 29 team members. My specific leadership responsibilities included directly managing 3 engineers, conducting their performance reviews, and developing their professional advancement plans.\n\nOne of my significant contributions was leading a project team dedicated to analyzing performance metrics across approximately 600 different installations. Within this initiative, I created Python scripts designed to process monitoring alerts. These tools effectively reduced the overwhelming volume of several hundred hourly notification emails by roughly 85%, significantly improving the usability of the alert system.\n\nAnother important aspect of my role involved close collaboration with the Product Development team. By conducting thorough analysis of performance log data and providing specific action recommendations, I contributed to the resolution of several critical software defects.",
    metadata={"section": "Experience", "company": "Appian Corporation", "roles": ["Lead Solution Engineer", "Senior Solution Engineer", "Solution Engineer"], "location": "Reston, VA", "dates": "Feb 2015 - Jul 2017"}
),

# --- Education: Columbia (Alternative) ---
Document(
    page_content="ACADEMIC CREDENTIALS\nColumbia University, New York, NY\nMS, Data Science\nGraduated: December 2018",
    metadata={"section": "Education", "institution": "Columbia University", "degree": "Masters of Science in Data Science", "graduation_date": "December 2018", "location": "New York, NY"}
),

# --- Education: Stevens (Alternative) ---
Document(
    page_content="Stevens Institute of Technology, Hoboken, NJ\nBE in Engineering Management, May 2012\nAdditional Concentrations: Economics, Pure and Applied Mathematics",
    metadata={"section": "Education", "institution": "Stevens Institute of Technology", "degree": "Bachelors of Engineering in Engineering Management", "minors": ["Economics", "Pure and Applied Mathematics"], "graduation_date": "May 2012", "location": "Hoboken, NJ"}
),

# --- Skills: Leadership & Strategy (Alternative) ---
Document(
    page_content="PROFESSIONAL COMPETENCIES\nSTRATEGIC LEADERSHIP\nC-Suite Relationship Building\nTechnical Team Leadership\nSales Training & Knowledge Transfer\nEnterprise Client Strategy Development\nMulti-departmental Collaboration",
    metadata={"section": "Skills", "category": "Leadership & Strategy"}
),

# --- Skills: Data Science / ML / Gen AI (Alternative) ---
Document(
    page_content="ARTIFICIAL INTELLIGENCE & DATA SCIENCE\nPyTorch Framework Implementation\nTransformer Architecture\nModel Evaluation & Benchmarking\nPerformance Optimization for Inference\nHardware Infrastructure Assessment\nProduction Model Deployment\nEfficient Model Serving (vLLM)",
    metadata={"section": "Skills", "category": "Data Science / ML / Gen AI"}
),

# --- Skills: Cloud Administration (Alternative) ---
Document(
    page_content="CLOUD PLATFORM EXPERTISE\nBig Data Processing - Databricks, AWS EMR, Google Dataproc\nCore Infrastructure - Virtual Machines, Storage Solutions, Serverless Computing\nContainer Orchestration with Kubernetes",
    metadata={"section": "Skills", "category": "Cloud Administration"}
),

# --- Skills: Solution Architecture (Alternative) ---
Document(
    page_content="TECHNICAL SOLUTION DEVELOPMENT\nProduct Demonstrations & Showcases\nBusiness Use Case Discovery\nProof of Value Implementation\nProduct Enhancement Recommendations",
    metadata={"section": "Skills", "category": "Solution Architecture"}
),

# --- Skills: Sales (Alternative) ---
Document(
    page_content="REVENUE GENERATION\nMEDDPICC Sales Methodology\nValue-oriented Selling Approach\nForce Management Principles",
    metadata={"section": "Skills", "category": "Sales"}
),

# --- Family (Alternative) ---
Document(
    page_content="At the heart of my personal life is my growing family - my wife and I are raising two young children, a toddler and a baby. The dynamics of parenting young kids shapes much of how we spend our non-working hours, with a focus on activities that combine quality family time with developmental experiences that foster our children's connection to the natural world.\n\nOur family regularly explores hiking paths in our area that are suitable for children at different developmental stages. These adventures serve multiple purposes - they allow us to introduce environmental awareness to our boys, teach them to identify various plants and wildlife, and help them build stamina in an enjoyable context. We carefully select trails that offer the right balance of exploration opportunities while remaining manageable for small children.\n\nBetween our hiking excursions, we frequently visit neighborhood playgrounds where we've become skilled at maximizing the play value of different equipment types. We create engaging activities that keep our children - particularly our energetic toddler - physically active while developing their social skills. These playground outings not only provide essential physical outlets but also create opportunities to connect with other families in our community.\n\nJuggling the responsibilities of raising two young children while maintaining our own personal interests and career obligations presents daily challenges, but witnessing our sons' excitement as they explore and discover their surroundings makes these challenges worthwhile.",
    metadata={
        "section": "Family", 
        "category": "Personal Life",
        "members": ["Wife", "Toddler son", "Infant son"],
        "activities": ["Hiking", "Outdoor play", "Playground visits"],
        "life_stage": "Young family"
    }
),

# --- Hobbies: Mushroom Foraging (Alternative) ---
Document(
    page_content="Wild mushroom foraging has evolved into a passion that perfectly combines my interests in wilderness exploration, natural history, and experimental cooking. Throughout the various growing seasons, I dedicate significant time to exploring New Jersey's woodlands and natural areas in search of edible fungal species.\n\nMy approach to foraging encompasses several key practices: careful species identification with safety as the primary concern, responsible harvesting techniques that preserve future growth, and detailed recording of locations and environmental conditions that favor specific varieties. Over time, I've gained specialized knowledge about local mushroom species that appear seasonally throughout New Jersey's diverse ecological zones.\n\nMy active participation in the New Jersey Mycological Association provides valuable community connections through organized group foraging expeditions that bring together enthusiasts with varying experience levels. These collective outings offer rich learning experiences and connections with fellow foragers. The association's workshops and educational programs have been instrumental in developing my ability to confidently distinguish edible species from potentially harmful lookalikes.\n\nThe culinary dimension of mushroom foraging is equally compelling for me. I take pleasure in testing various cooking approaches and recipes specifically created to showcase the distinct flavors and textures of wild mushrooms. My culinary experiments range from minimalist preparations that highlight chanterelles' natural qualities to more elaborate dishes that incorporate multiple foraged varieties, constantly exploring innovative ways to feature these seasonal harvests in memorable dining experiences.\n\nThis hobby creates a profound connection to the seasonal patterns of my local environment while offering a fulfilling blend of outdoor activity, scientific learning, community engagement, and creative cooking.",
    metadata={
        "section": "Hobbies", 
        "category": "Mushroom Foraging",
        "activities": ["Identification", "Harvesting", "Cooking"],
        "organizations": ["New Jersey Mycological Association"],
        "locations": ["New Jersey forests"],
        "related_interests": ["Cooking", "Botany", "Outdoor activities"]
    }
),

# --- Hobbies: Smart Home Technology (Alternative) ---
Document(
    page_content="I devote considerable time and technical effort to my smart home project, with a specific emphasis on building a privacy-focused home automation ecosystem that operates independently of cloud services. Unlike conventional consumer smart home setups that heavily rely on external servers, I've intentionally designed my system to function exclusively within my local network infrastructure.\n\nThe foundation of my implementation is built on Home Assistant, which functions as the integration hub for my diverse collection of devices and automation routines. This open-source solution provides complete data sovereignty while eliminating subscription fees and addressing privacy concerns associated with cloud-dependent alternatives. My Home Assistant configuration manages numerous household systems including illumination control, temperature regulation, security monitoring, and media distribution.\n\nA particularly sophisticated component of my setup is a voice control system powered by a locally-running LLaMA language model. This operates on a dedicated computer with specialized graphics processing hardware providing the necessary computational resources. This arrangement enables voice-activated home control without transmitting audio recordings to external servers, preserving privacy while maintaining convenient hands-free functionality.\n\nI regularly incorporate ESP8266 microcontrollers into my system to create purpose-built sensors and control interfaces. This process frequently involves electronics work including soldering and custom firmware development to modify commercial products that would typically require cloud connectivity. These technical modifications ensure that all components operate exclusively within my secured local network.\n\nBeyond the practical advantages of enhanced privacy and reduced ongoing costs, this technical pursuit satisfies my innate curiosity and desire for comprehensive understanding of my daily technology environment. Each system element represents an individual technical challenge spanning hardware customization, software configuration, and integration problem-solving.",
    metadata={
        "section": "Hobbies", 
        "category": "Smart Home Technology",
        "focus": ["Privacy", "Local networking", "DIY hardware"],
        "technologies": ["Home Assistant", "LLaMA", "ESP8266"],
        "skills": ["Soldering", "Hardware hacking", "System integration", "Local hosting"],
        "motivations": ["Privacy concerns", "Cost reduction", "Technical control"]
    }
),

# --- Hobbies: Photography (Alternative) ---
Document(
    page_content="I've cultivated a deep interest in photography over many years, concentrating primarily on three distinct subject categories: natural landscapes, local wildlife, and close-up fungi photography.\n\nMy landscape photography portfolio includes captures from several iconic national parks. At Acadia in Maine, I've documented the dramatic coastline with its granite formations and Atlantic sunrise vistas. In Montana's Glacier National Park, I've focused on capturing alpine scenery with its pristine lakes and mountain panoramas. My more recent work in Joshua Tree National Park features the distinctive desert environment with its characteristic yucca-like trees silhouetted against vibrant sunset skies and the park's remarkable geological formations.\n\nWithin my immediate surroundings, I've developed techniques for photographing the diverse wildlife that inhabits my neighborhood ecosystem. This practice has enhanced my skills in patient observation and quick response timing to document fleeting moments as birds, squirrels, rabbits, and occasional foxes go about their daily activities.\n\nMy most technically specialized photographic interest involves macro imagery of mushrooms and fungi species. The intricate structures, surface textures, and varied coloration of different fungal specimens provide fascinating subjects for close-up documentation. This specialized focus has led me to explore wooded areas during periods of high moisture, documenting the temporary fungal growths that appear following rainfall events. My specialized macro equipment reveals minute details invisible to casual observation of these often-overlooked natural subjects.\n\nFor all these photographic pursuits, I employ a Sony a6000 camera with APS-C sensor complemented by a selection of fixed focal length E-mount lenses. My lens collection includes: an 18mm optic for expansive landscape compositions, a versatile 24mm for general photography, a 50mm lens particularly effective for wildlife subjects, and a 105mm that excels at detailed macro work with fungi specimens. This adaptable yet relatively compact equipment configuration enables me to capture subjects ranging from vast landscape perspectives to microscopic mushroom details.",
    metadata={
        "section": "Hobbies", 
        "category": "Photography", 
        "subjects": ["Landscapes", "Wildlife", "Macro", "Mushrooms"],
        "locations": ["Acadia National Park", "Glacier National Park", "Joshua Tree National Park", "Neighborhood"],
        "equipment_type": "Sony a6000 crop sensor with E-mount prime lenses (18mm, 24mm, 50mm, 105mm)",
        "experience_level": "Enthusiast"
    }
)
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

