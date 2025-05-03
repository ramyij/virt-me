from langchain_core.documents import Document

resume_chunks = [
    # --- Contact Info ---
    Document(page_content="Name: Ramy Jaber\nEmail: ramyij@pm.me\nPhone: 732.567.2603\nLocation: New Jersey\nLinkedIn: linkedin.com/in/ramyj", metadata={"section": "Contact"}),

    # --- Experience --- (Add all Document(...) entries here)
    Document(page_content="Company: Intel\nTitle: Cloud Solution Architect - LLMs\nLocation: Remote, NJ\nDates: Oct 2022 - Present\n- Led GTM integration for $70M, 3-year LLM partnership with SeekrFlow\n- Created demo notebooks, sales materials, trained sales and solution teams\n- Delivered 7 enterprise engagements, 2 POVs in 3 months\n- Migrated CUDA-based LLMs to Intel Gaudi hardware\n- Completed 6 POCs, won 5, resulting in ~$8M business\n- Architected LLM solutions for Stability AI, Character.ai, and Pathway", metadata={"section": "Experience", "company": "Intel", "role": "Cloud Solution Architect - LLMs"}),

    Document(page_content="Company: Intel (formerly Granulate.io)\nTitle: Manager, Cloud Solution Architects - Performance Engineering\n- Managed 4 engineers, $7M ARR portfolio\n- Mitigated major customer outage in 25 minutes; led RCA\n- Scaled Nylas account from $200K to $800K ARR\n- Grew iFood account to $1.1M using Databricks + Kubernetes optimizations\n- Built Python automation to increase onboarding from 20 to 300 workloads/day\n- Delivered 40% compute cost reductions", metadata={"section": "Experience", "company": "Intel", "role": "Manager, Cloud Solution Architects"}),

    Document(page_content="Company: DataRobot\nTitle: Pre-sales Data Scientist\nLocation: Remote, NJ\nDates: Jul 2021 - Oct 2022\n- Led technical presales for Financial, Retail, and Telecom sectors in NYC\n- Developed credit rating prediction solution; led to 3 POCs\n- Prevented $2M churn by creating cross-departmental use cases\n- Built automation for model compliance documentation", metadata={"section": "Experience", "company": "DataRobot", "role": "Pre-sales Data Scientist"}),

    Document(page_content="Company: Udacity\nTitle: Director, Solution Architects - Global Enterprise\nLocation: Remote, NY\nDates: Feb 2019 - Apr 2021\n- Built and led 10-person team from scratch\n- Exceeded revenue targets: $13M (1.7x), $33M (1.8x), projected $40M (1.1x)\n- Designed upskilling program for Big 4 firm (400+ employees)\n- Co-developed sales methodology (MEDDPICC, value messaging)", metadata={"section": "Experience", "company": "Udacity", "role": "Director, Solution Architects"}),

    Document(page_content="Company: Udacity\nTitle: Senior Solution Architect\n- First presales technical hire in Enterprise Sales\n- Supported $13M in 2019 sales\n- Expanded Shell account by $2.1M\n- Led monthly deep dives in Data Science, AI/ML, Cloud", metadata={"section": "Experience", "company": "Udacity", "role": "Senior Solution Architect"}),

    Document(page_content="Company: Appian Corporation\nTitles: Solution Engineer → Senior → Lead Solution Engineer\nLocation: Reston, VA\nDates: Feb 2015 - Jul 2017\n- Managed 3 engineers as team expanded from 8 to 29\n- Analyzed 600 sites; reduced alert email noise by 85%\n- Built Python tools for monitoring and performance analysis\n- Collaborated with Product Dev to fix high-impact bugs", metadata={"section": "Experience", "company": "Appian Corporation", "roles": ["Lead", "Senior", "Solution Engineer"]}),

    # --- Education --- (Add Document(...) entries)
    Document(page_content="Institution: Columbia University\nDegree: MS in Data Science\nGraduation: Dec 2018\nLocation: New York, NY", metadata={"section": "Education", "institution": "Columbia University", "degree": "Masters of Science in Data Science"}),

    Document(page_content="Institution: Stevens Institute of Technology\nDegree: BE in Engineering Management\nMinors: Economics, Pure & Applied Mathematics\nGraduation: May 2012\nLocation: Hoboken, NJ", metadata={"section": "Education", "institution": "Stevens Institute of Technology", "degree": "Bachelors of Engineering"}),

    # --- Skills --- (Add Document(...) entries)
    Document(page_content="Leadership: Executive relationships, Team management, Sales enablement, Account strategy, Cross-functional collaboration", metadata={"section": "Skills", "category": "Leadership & Strategy"}),

    Document(page_content="Data Science & GenAI: PyTorch, Transformers, Model analysis, Inference optimization, Infrastructure evaluation, Deployment, vLLM", metadata={"section": "Skills", "category": "Data Science / ML / Gen AI"}),

    Document(page_content="Cloud: Spark (Databricks, EMR, Dataproc), VMs, Storage, Serverless, Kubernetes", metadata={"section": "Skills", "category": "Cloud Administration"}),

    Document(page_content="Solution Architecture: Demos, Use case scoping, POVs, Feedback loop with Product", metadata={"section": "Skills", "category": "Solution Architecture"}),

    Document(page_content="Sales: MEDDPICC, Value selling, Force Management methodology", metadata={"section": "Skills", "category": "Sales"}),

    # --- Personal Life --- (Add Document(...) entries)
    Document(page_content="Family: Wife, toddler son, infant son\nActivities: Hiking, Outdoor play, Playgrounds\nLocation: New Jersey\nStage: Young family", metadata={"section": "Family", "category": "Personal Life", "members": ["Wife", "Toddler son", "Infant son"], "activities": ["Hiking", "Outdoor play", "Playground visits"], "life_stage": "Young family"}),

    Document(page_content="Hobby: Mushroom Foraging\nActivities: Identification, Harvesting, Cooking\nOrgs: New Jersey Mycological Association\nLocation: New Jersey forests\nRelated Interests: Cooking, Botany, Outdoors", metadata={"section": "Hobbies", "category": "Mushroom Foraging"}),

    Document(page_content="Hobby: Smart Home Tech\nFocus: Privacy-first, Local-only automation\nTech: Home Assistant, LLaMA, ESP8266\nSkills: Soldering, Hardware hacking, Local hosting\nMotivations: Privacy, Cost savings, System control", metadata={"section": "Hobbies", "category": "Smart Home Technology"}),

    Document(page_content="Hobby: Photography\nSubjects: Landscapes, Wildlife, Macro (Mushrooms)\nLocations: Acadia, Glacier, Joshua Tree, Neighborhood\nCamera: Sony a6000 with 18mm, 24mm, 50mm, 105mm lenses\nLevel: Enthusiast", metadata={"section": "Hobbies", "category": "Photography"}),

    Document(
        page_content="Q: Welcome to the show! Can you introduce yourself and tell us what you do at Granulate?\n\nA: Thanks for having me. I’m a Solutions Architect at Intel Granulate. I help customers optimize their cloud and on-prem workloads by reducing resource consumption and improving performance, all without requiring code changes. That means we’re able to quickly unlock cost savings and performance improvements for complex environments.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Introduction"
        }
    ),
    Document(
        page_content="Q: What is Granulate and how does it help companies save money?\n\nA: Granulate is an optimization layer that installs as an agent on your machines—whether they’re cloud VMs, on-prem servers, or Kubernetes nodes. It learns workload patterns and dynamically adjusts low-level OS and runtime parameters to improve throughput and reduce latency. That typically translates to 20–40% cost savings without any application changes.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Granulate Overview"
        }
    ),
    Document(
        page_content="Q: Who is the ideal customer for Granulate?\n\nA: Any company running large-scale workloads—especially batch processing, data-intensive pipelines, or real-time applications. We work with customers across verticals, but the biggest ROI comes when customers are already spending a lot on compute and want to optimize without rewriting code.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Customer Profile"
        }
    ),
    Document(
        page_content="Q: How does Granulate differ from traditional APM or monitoring tools?\n\nA: Monitoring tells you where the problems are. Granulate goes one step further and automatically fixes performance issues by changing how resources are allocated at the OS level. Think of it as a continuous performance tuning system that runs alongside your apps.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Product Differentiation"
        }
    ),
    Document(
        page_content="Q: You mentioned saving money and optimizing resources. Can you explain how customers typically see ROI?\n\nA: Absolutely. When we first engage with a customer, we conduct a health check and baseline performance. After implementing Granulate, we typically see immediate improvements—like reducing CPU or memory usage. The ROI usually comes from two things: first, cost savings on cloud instances or on-prem hardware, and second, improved performance leading to better user experiences and faster processing times.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "ROI Explanation"
        }
    ),
    Document(
        page_content="Q: Can you provide an example of a customer where Granulate made a significant impact?\n\nA: Sure, one of our large retail customers was facing high infrastructure costs for their inventory management platform. By using Granulate, they were able to reduce their cloud bill by 30% while also improving the speed of data processing, which had a direct impact on inventory tracking accuracy and timely decisions.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Customer Example"
        }
    ),
    Document(
        page_content="Q: What’s the process like for integrating Granulate with a new customer?\n\nA: The process is very straightforward. It’s a low-touch deployment. We work with the customer’s team to install our agent, and from there, the system begins analyzing workloads in real time. Most of the work is done by the Granulate platform itself, so there’s very little disruption to the customer’s operations. We monitor progress closely, and within a couple of weeks, they start seeing meaningful results.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Integration Process"
        }
    ),
    Document(
        page_content="Q: How does Granulate scale for larger organizations or complex environments?\n\nA: Granulate scales seamlessly. Whether a customer has a few machines or thousands, the agent is lightweight and doesn’t require significant changes to the infrastructure. We have customers running on everything from small VMs to large clusters with thousands of nodes, and Granulate performs optimally in each case.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Scalability"
        }
    ),
    Document(
        page_content="Q: How do you handle different types of workloads, such as batch versus real-time?\n\nA: Granulate is flexible enough to handle both batch and real-time workloads. For batch workloads, we optimize for throughput and efficient resource use. For real-time applications, we focus on reducing latency and ensuring fast response times. Our platform adapts based on the type of workload and the goals of the customer.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Workload Types"
        }
    ),
    Document(
        page_content="Q: How does Granulate ensure security and data privacy for its customers?\n\nA: Security and privacy are paramount. Granulate’s agent runs entirely on the customer’s infrastructure, and we don’t have access to customer data. We only collect non-sensitive, anonymized telemetry data to improve our platform’s optimization. All data processing happens locally, ensuring that sensitive data remains private.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Security and Privacy"
        }
    ),
    Document(
        page_content="Q: What’s next for Granulate? Any new features or directions you’re excited about?\n\nA: We’re always working on improving the platform. We’re focused on expanding our support for new environments, such as serverless computing and container orchestration systems. Additionally, we’re enhancing our machine learning models to better predict future workload patterns and optimize in a more proactive way, even before issues arise.",
        metadata={
            "section": "Podcast",
            "source": "Spend Advantage",
            "guest": "Ramy",
            "company": "Intel Granulate",
            "role": "Solutions Architect",
            "topic": "Future Plans"
        }
    ),
    Document(
    page_content="In my current role, I worked with a large pharmacy chain in France to improve the response times and reduce cost at the same time of their inference pipeline. The use case was to extract information from pdf files of Invoices and Prescriptions and format the extracted info into a structured JSON file. The customer's current approach was to leverage the OpenAI API which provided excellent accuracy, but the cost and latency due to cloud was not sufficient for the point-of-sale customer experience. I worked with the customer to recreate the inference pipeline using open source models (testing both Llama3.2-VL and Qwen2.5-VL) deployed on Intel Tiber AI Cloud on Gaudi accelerated hardware, using vLLM as the inference engine. Several challenges presented themselves as there were several variables including change of model, deciding which size model to use, and tuning the parameters like context size to improve the performance of the open sourced models. Ultimately we were able to achieve near equality in accuracy and a 23% reduction in response time compared to the OpenAI API pipeline.",
    metadata={
        "section": "Customer Story",
        "source": "Personal Experience",
        "customer_industry": "Pharmacy/Retail",
        "customer_location": "France",
        "role_in_project": "Solutions Architect / AI Engineer", # Inferred role based on description
        "use_case": "PDF Document Extraction (Invoices, Prescriptions) to JSON",
        "problem_solved": "High Cost and Latency of Cloud API (OpenAI)",
        "solution_implemented": "Open Source VLM (Llama3.2-VL, Qwen2.5-VL) on Intel Tiber AI Cloud (Gaudi) via vLLM",
        "key_technologies": "Vision Language Models (VLM), Intel Tiber AI Cloud, Intel Gaudi, vLLM, OpenAI API, PDF Processing, JSON",
        "models_compared": "OpenAI API vs Llama3.2-VL / Qwen2.5-VL",
        "outcome_metrics": "Near-equal Accuracy, 23% Latency Reduction",
        "challenges": "Model Selection, Parameter Tuning (Context Size), Open Source Performance Optimization"
    }
    ),
    Document(
    page_content="At DataRobot, I led the technical effort to save a $2M account with a large bank from churning. The initial sponsor had left, usage declined, and executives questioned the ROI, giving 60 days' notice. I led a team of SEs, CSMs, and Account Managers to revive the relationship by identifying new use cases, demonstrating existing successes, and building rapport with new executives. Developing a prototype to automatically document Machine Learning models for compliance approval was the key factor in winning the renewal. This addressed a major bottleneck in regulated finance, where explaining ML model decisions for compliance officers is crucial. DataRobot's automated process for explaining and documenting models significantly increases the velocity of adopting ML solutions in such environments. The customer remained, satisfied with the demonstrated ROI.",
    metadata={
        "section": "Account Retention Story",
        "source": "Personal Experience",
        "my_company_at_time": "DataRobot", # Company where this role was held
        "customer_industry": "Banking/Finance",
        "role_in_project": "Technical Lead / Team Lead", # Role played in this specific scenario
        "situation": "Account Churn Risk ($2M value, 60-day notice)",
        "problem_solved": "Lack of Perceived ROI, Low Usage, Sponsor Change, ML Model Compliance Bottleneck",
        "key_actions": "Cross-functional Team Leadership (SEs, CSMs, AMs), Use Case Discovery, Value Demonstration, Executive Rapport Building, Prototype Development",
        "winning_solution": "Automated ML Model Documentation Prototype (for Compliance)",
        "key_technologies": "DataRobot Platform, Machine Learning (ML), Explainable AI (XAI), Automated Model Documentation",
        "business_outcome": "Saved $2M Account, Customer Retention, ROI Justification",
        "relevant_concepts": "Churn Prevention, Customer Success Management (CSM), Solutions Engineering (SE), Account Management (AM), Value Selling, Regulated Industries Compliance, ML Adoption Velocity"
    }
    ),
    Document(
    page_content="In my role in Performance Engineering at Granulate (acquired by Intel), I handled a challenging customer situation with a major US-based Airline. We had initially saved them tens of millions in compute costs. However, about 4 months post-deployment, the software caused a massive increase in network data egress costs, leading to a datacenter bottleneck and a production outage, impacting end-customer services. Our main point of contact, already cautious about our software, was highly critical and sought to have Granulate removed entirely. My approach was to immediately meet with him one-on-one. I listened to his concerns, explicitly acknowledged that our software was the cause of the increased egress costs, and took full responsibility for both the problem and its resolution. We were able to get their services back online and halt the excessive egress within 25 minutes of the first report. Within one week, we delivered a full Root Cause Analysis (RCA) and deployed a bug fix to limit the agent's data transmission. This transparent and rapid response rebuilt trust. About a month after resuming normal operations with the fix, the same point of contact approved expanding Granulate's deployment to their Databricks clusters, ultimately increasing the account's ARR by 50% within six months of the original deal.",
    metadata={
        "section": "Incident Management Example",
        "interview_question_topic": "Challenging Customer / Handling Failure", # Specific type of story
        "source": "Personal Experience",
        "my_company_at_time": "Granulate (Intel)",
        "my_role": "Performance Engineering",
        "customer_industry": "Airline",
        "customer_location": "US-based",
        "situation": "Production Outage & Service Degradation caused by Deployed Software (Excessive Network Egress)",
        "challenge_type": "Technical Failure (Software Bug), Customer Relationship Crisis",
        "customer_reaction": "Wary, Critical, Demanded Uninstallation",
        "resolution_strategy": "Direct Communication (1-on-1), Empathy, Accountability (Taking Responsibility), Acknowledgment of Fault, Rapid Technical Response (25 min stabilization), Full Root Cause Analysis (RCA), Permanent Bug Fix (1 week)",
        "key_technologies": "Granulate Software, Performance Engineering, Network Egress Monitoring, Databricks",
        "initial_benefit_achieved": "$10M+ Compute Cost Savings",
        "negative_impact_caused": "Increased Network Egress Cost, Datacenter Bottleneck, Production Outage",
        "outcome": "Issue Resolved (<30 min stabilization, <1 wk permanent fix), Trust Rebuilt, Account Expansion (Databricks), 50% ARR Increase (within 6 months of deal close)",
        "relevant_concepts": "Incident Response, Crisis Management, Customer Relationship Management, Accountability, Root Cause Analysis (RCA), Bug Fixing, Performance Tradeoffs (Compute vs Network), Trust Building, Account Expansion, ARR Growth"
    }
),
Document(
    page_content="While LLMs are capturing the attention of technology enthusiasts and lay persons, for good reason, I believe that LLMs are just a small part of the larger AI systems that will inevitably change every aspect of how we humans engage with the world. For business applications, there is still a place for traditional predictive models (fraud detection, spam filters, marketing cross-sell/upsell, loan worthiness, etc) that rely on structured data. LLMs are a great next step to make AI more conversational. The latest generation of foundational models with reasoning do an impressive job at replacing some of those more traditional models. \nHowever, LLMs have their challenges in application, and true ROI is yet to be seen in many enterprise applications. As I look to AI leaders in the industry, I am compelled to agree with Yann LeCun who is lead research at Meta on new architectures like JEPA that will once again transform the definition of 'AI'. \nI make the analogy that LLMs are to AI what the command line interface (like MS-DOS) was to early personal computers. Just as MS-DOS gave people a way to interact with computers using typed commands—making computers useful, but still technical and niche—LLMs have made AI accessible through natural language, opening it up to non-experts for the first time. \nHowever, it wasn’t until the graphical user interface (GUI) and later the Internet came along that personal computing became truly ubiquitous—integrated into daily life, with intuitive apps and seamless connectivity. Similarly, while LLMs are the breakthrough interface that brings AI into the public eye, the real transformation will happen when AI is smarter, more autonomous, and deeply integrated into real-world systems (like supply chains, finance, healthcare, infrastructure). At that point, AI won’t just be a tool you talk to—it will be a co-pilot that understands context, takes initiative, and acts across systems in meaningful ways.",
    metadata={
        "section": "AI Perspectives",
        "source": "Personal Thoughts",
        "main_topic": "Future of Artificial Intelligence",
        "sub_topics": [
            "Limitations of LLMs",
            "Role of Traditional Machine Learning",
            "Enterprise AI ROI",
            "Future AI Architectures (beyond LLMs)",
            "AI Integration & Autonomy"
        ],
        "key_concepts": [
            "LLMs",
            "Traditional ML",
            "Predictive Models",
            "Structured Data",
            "Conversational AI",
            "Foundational Models",
            "Reasoning",
            "ROI",
            "Enterprise AI",
            "Yann LeCun",
            "Meta AI",
            "JEPA (Joint Embedding Predictive Architecture)",
            "AI Integration",
            "Autonomous Systems",
            "AI Co-pilot"
        ],
        "analogy_used": "LLMs : AI Evolution :: Command Line (MS-DOS) : PC Evolution (GUI/Internet)",
        "stance_on_llms": "Important interface/accessibility breakthrough, but not the ultimate form of AI; challenges remain (e.g., enterprise ROI).",
        "future_ai_vision": "Smarter, autonomous, deeply integrated AI co-pilots acting across real-world systems.",
        "influences_mentioned": "Yann LeCun (Meta AI)",
        "architectures_mentioned": "JEPA"
    }
)
] 