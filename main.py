import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Neo4jVector
from langchain_groq import ChatGroq  # Groq for fast Llama inference
from langchain_openai import OpenAIEmbeddings  # OpenAI for embeddings
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
import streamlit as st
import tempfile
from neo4j import GraphDatabase

def main():
    st.set_page_config(
        layout="wide",
        page_title="BioGraphRAG | Real-time Biomedical Knowledge Graph",
        page_icon="🧬",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for professional black and blue styling
    st.markdown("""
        <style>
        .main {
            background-color: #000000;
        }
        .stApp {
            max-width: 100%;
            background-color: #000000;
        }
        h1 {
            color: #60a5fa;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        h2 {
            color: #3b82f6;
            font-weight: 600;
        }
        h3 {
            color: #60a5fa;
            font-weight: 500;
        }
        p, label, div {
            color: #e5e7eb;
        }
        .stButton>button {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            transform: translateY(-2px);
        }
        .upload-section {
            background: #1a1a1a;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(37, 99, 235, 0.3);
            border: 1px solid #2563eb;
            margin: 1rem 0;
        }
        .info-box {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        .success-box {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        }
        .metric-card {
            background: #1a1a1a;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
            border: 1px solid #2563eb;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Professional Header - White and Blue
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
                    padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem;
                    box-shadow: 0 8px 24px rgba(30, 58, 138, 0.15);'>
            <h1 style='color: white; margin: 0; font-size: 2.8rem; text-align: center;'>
                🧬 BioGraphRAG
            </h1>
            <p style='color: #e0e7ff; margin: 0.8rem 0 0 0; font-size: 1.2rem; text-align: center;'>
                Real-time <span style='color: white; font-weight: 600;'>Biomedical</span> Knowledge Graph Engineering
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 System Information")

        st.markdown("---")

        st.markdown("#### 🎯 Supported Entities")
        with st.expander("Clinical Entities", expanded=False):
            st.markdown("""
            <div style='color: #475569;'>
            <p>👤 <span style='color: #2563eb; font-weight: 600;'>Patient</span> - Demographics & identifiers</p>
            <p>🦠 <span style='color: #2563eb; font-weight: 600;'>Disease</span> - Diagnoses & conditions</p>
            <p>💊 <span style='color: #2563eb; font-weight: 600;'>Medication</span> - Drugs & dosages</p>
            <p>🩺 <span style='color: #2563eb; font-weight: 600;'>Symptom</span> - Clinical manifestations</p>
            <p>👨‍⚕️ <span style='color: #2563eb; font-weight: 600;'>Doctor</span> - Healthcare providers</p>
            <p>🧪 <span style='color: #2563eb; font-weight: 600;'>Test</span> - Lab results & values</p>
            <p>🏥 <span style='color: #2563eb; font-weight: 600;'>Procedure</span> - Medical interventions</p>
            <p>🫀 <span style='color: #2563eb; font-weight: 600;'>Anatomy</span> - Body parts & organs</p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Research Entities", expanded=False):
            st.markdown("""
            <div style='color: #475569;'>
            <p>🧬 <span style='color: #2563eb; font-weight: 600;'>Gene</span> - Genetic markers</p>
            <p>🔬 <span style='color: #2563eb; font-weight: 600;'>Protein</span> - Protein expressions</p>
            <p>📈 <span style='color: #2563eb; font-weight: 600;'>Biomarker</span> - Clinical biomarkers</p>
            <p>🔬 <span style='color: #2563eb; font-weight: 600;'>ClinicalTrial</span> - Research studies</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("#### ⚙️ Technology Stack")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                    padding: 1rem; border-radius: 8px; border-left: 4px solid #2563eb;'>
            <p style='margin: 0; color: #1e3a8a;'><strong>LLM:</strong> Llama 3.3 70B Versatile</p>
            <p style='margin: 0.3rem 0; color: #1e3a8a;'><strong>Database:</strong> Neo4j Aura</p>
            <p style='margin: 0; color: #1e3a8a;'><strong>Framework:</strong> LangChain</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("#### 📚 Use Cases")
        st.markdown("""
        <div style='color: #475569;'>
        <p>✅ Clinical case reports</p>
        <p>✅ Research papers</p>
        <p>✅ Patient records</p>
        <p>✅ Laboratory reports</p>
        <p>✅ Medical literature</p>
        </div>
        """, unsafe_allow_html=True)

    load_dotenv()

    # Load credentials from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    groq_api_key = os.getenv('GROQ_API_KEY')
    neo4j_url = os.getenv('NEO4J_URI')
    neo4j_username = os.getenv('NEO4J_USERNAME')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    neo4j_database = os.getenv('NEO4J_DATABASE', 'neo4j')

    # Validate that credentials are loaded
    if not openai_api_key:
        st.error("OpenAI API Key not found. Please set OPENAI_API_KEY in your .env file.")
        st.stop()

    if not groq_api_key:
        st.error("Groq API Key not found. Please set GROQ_API_KEY in your .env file.")
        st.stop()

    if not all([neo4j_url, neo4j_username, neo4j_password]):
        st.error("Neo4j credentials not found. Please set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD in your .env file.")
        st.stop()

    # Initialize models: OpenAI for embeddings, Groq for LLM
    if 'embeddings' not in st.session_state:
        # OpenAI Embeddings (text-embedding-ada-002)
        embeddings = OpenAIEmbeddings()

        # Groq with Llama 3.3 70B Versatile (recommended for tool use)
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",  # Supports function calling
            temperature=0,
            groq_api_key=groq_api_key
        )

        st.session_state['embeddings'] = embeddings
        st.session_state['llm'] = llm
        st.sidebar.success("✅ AI Models Initialized")
    else:
        embeddings = st.session_state['embeddings']
        llm = st.session_state['llm']

    # Connect to Neo4j
    if 'graph' not in st.session_state:
        try:
            graph = Neo4jGraph(
                url=neo4j_url,
                username=neo4j_username,
                password=neo4j_password
            )
            st.session_state['graph'] = graph
            st.session_state['neo4j_url'] = neo4j_url
            st.session_state['neo4j_username'] = neo4j_username
            st.session_state['neo4j_password'] = neo4j_password
            st.sidebar.success("✅ Neo4j Connected: Realtime_Graph")
        except Exception as e:
            st.sidebar.error(f"❌ Neo4j Connection Failed")
            st.error(f"**Database Connection Error:** {e}")
            st.stop()
    else:
        graph = st.session_state['graph']
        neo4j_url = st.session_state['neo4j_url']
        neo4j_username = st.session_state['neo4j_username']
        neo4j_password = st.session_state['neo4j_password']

    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 1rem;'>
                <h3 style='color: #1e40af; margin: 0;'>📄 Document Processing</h3>
                <p style='color: #64748b; margin: 0.5rem 0 0 0;'>
                    Upload a <span style='color: #2563eb; font-weight: 600;'>biomedical</span> PDF document to build the knowledge graph
                </p>
            </div>
        """, unsafe_allow_html=True)

    # File uploader with custom styling
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload clinical reports, research papers, patient records, or lab reports"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None and 'qa' not in st.session_state:
        # Show processing status
        st.markdown(f"""
            <div class='info-box'>
                <h3 style='color: white; margin: 0;'>⚙️ Processing: {uploaded_file.name}</h3>
                <p style='color: white; margin: 0.5rem 0 0 0;'>
                    Extracting <strong>biomedical</strong> entities and building knowledge graph...
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>📥 Loading PDF document...</p>", unsafe_allow_html=True)
        progress_bar.progress(10)

        with st.spinner("Processing the PDF..."):
            # Save uploaded file to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # Load and split the PDF
            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>📖 Extracting text from PDF pages...</p>", unsafe_allow_html=True)
            progress_bar.progress(20)
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load_and_split()

            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>✂️ Chunking text for optimal processing...</p>", unsafe_allow_html=True)
            progress_bar.progress(30)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
            docs = text_splitter.split_documents(pages)

            lc_docs = []
            for doc in docs:
                lc_docs.append(Document(page_content=doc.page_content.replace("\n", ""),
                metadata={'source': uploaded_file.name}))

            # Clear the graph database
            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>🗑️ Clearing existing graph data...</p>", unsafe_allow_html=True)
            progress_bar.progress(40)
            cypher = """
              MATCH (n)
              DETACH DELETE n;
            """
            graph.query(cypher)

            # Define allowed nodes and relationships for Clinical Research
            allowed_nodes = [
                "Patient", "Disease", "Medication", "Test", "Symptom", "Doctor",
                "Procedure", "Anatomy", "Gene", "Protein", "Biomarker", "ClinicalTrial"
            ]
            allowed_relationships = [
                "HAS_DISEASE", "TAKES_MEDICATION", "UNDERWENT_TEST", "HAS_SYMPTOM", "TREATED_BY",
                "EXPRESSES", "MUTATES", "TARGETS", "ENROLLED_IN", "AFFECTS", "UNDERWENT_PROCEDURE"
            ]

            # Transform documents into graph documents
            # Enable properties to capture dosages, dates, test values, etc.
            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>🤖 AI extracting entities and relationships...</p>", unsafe_allow_html=True)
            progress_bar.progress(50)

            transformer = LLMGraphTransformer(
                llm=llm,
                allowed_nodes=allowed_nodes,
                allowed_relationships=allowed_relationships,
                node_properties=True,  # Enable to capture quantitative data
                relationship_properties=True  # Enable to capture relationship metadata
            )

            graph_documents = transformer.convert_to_graph_documents(lc_docs)

            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>💾 Storing graph in Neo4j database...</p>", unsafe_allow_html=True)
            progress_bar.progress(70)
            graph.add_graph_documents(graph_documents, include_source=True)

            # Use the stored connection parameters
            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>🔍 Creating vector embeddings for semantic search...</p>", unsafe_allow_html=True)
            progress_bar.progress(85)

            index = Neo4jVector.from_existing_graph(
                embedding=embeddings,
                url=neo4j_url,
                username=neo4j_username,
                password=neo4j_password,
                database="neo4j",
                node_label="Patient",  # Adjust node_label as needed
                text_node_properties=["id", "text"],
                embedding_node_property="embedding",
                index_name="vector_index",
                keyword_index_name="entity_index",
                search_type="hybrid"
            )

            status_text.markdown("<p style='color: #1e40af; font-weight: 600;'>⚡ Finalizing knowledge graph...</p>", unsafe_allow_html=True)
            progress_bar.progress(95)

            # Retrieve the graph schema
            schema = graph.get_schema

            # Set up the QA chain with improved prompt
            template = """
            Task: Generate a Cypher query to retrieve information from a Neo4j graph database.

            Use ONLY the provided schema and relationship types.

            Schema:
            {schema}

            Instructions:
            1. Generate syntactically correct Cypher queries
            2. Use only node labels and relationship types from the schema
            3. For questions about entities, use MATCH patterns to find them
            4. Use RETURN to specify what information to retrieve
            5. Keep queries simple and focused

            Examples:
            - "What medications?" → MATCH (p:Patient)-[:TAKES_MEDICATION]->(m:Medication) RETURN m.id
            - "What diseases?" → MATCH (d:Disease) RETURN d.id
            - "What symptoms?" → MATCH (s:Symptom) RETURN s.id

            Question: {question}

            Cypher Query:"""

            question_prompt = PromptTemplate(
                template=template,
                input_variables=["schema", "question"]
            )

            # Response generation prompt for natural answers
            response_template = """Based on the question and database results, provide a natural, conversational answer.

Question: {question}
Database Results: {context}

Instructions:
1. Write in a natural, conversational tone
2. If results show medications/diseases/symptoms, explain them clearly
3. Provide context and relevant details from the data
4. If no results, say "I couldn't find that information in the document"
5. Keep it concise but informative

Answer:"""

            response_prompt = PromptTemplate(
                template=response_template,
                input_variables=["question", "context"]
            )

            qa = GraphCypherQAChain.from_llm(
                llm=llm,
                graph=graph,
                cypher_prompt=question_prompt,
                qa_prompt=response_prompt,
                verbose=True,
                return_intermediate_steps=True,
                allow_dangerous_requests=True,
                top_k=10
            )
            st.session_state['qa'] = qa

            # Complete
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()

            # Success message with stats
            st.markdown(f"""
                <div class='success-box'>
                    <h3 style='color: white; margin: 0;'>✅ Knowledge Graph Ready!</h3>
                    <p style='color: white; margin: 0.5rem 0 0 0;'>
                        Successfully processed: <strong>{uploaded_file.name}</strong>
                    </p>
                </div>
            """, unsafe_allow_html=True)

    if 'qa' in st.session_state:
        st.markdown("---")

        # Query interface
        st.markdown("### 💬 Query Knowledge Graph")
        st.markdown('<p style="color: #64748b;">Ask questions in natural language about the extracted <span style="color: #2563eb; font-weight: 600;">biomedical</span> information</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            question = st.text_input(
                "Your Question",
                placeholder="e.g., What medications does the patient take? What genes are mutated?",
                label_visibility="collapsed"
            )

        with col2:
            submit_button = st.button("🔍 Search", use_container_width=True)

        # Example questions
        with st.expander("💡 Example Questions"):
            st.markdown("""
            <div style='color: #1e3a8a;'>
                <p style='color: #2563eb; font-weight: 600; margin-bottom: 0.5rem;'>Clinical:</p>
                <ul style='color: #475569; margin-top: 0;'>
                    <li>What medications does the patient take?</li>
                    <li>What symptoms does the patient have?</li>
                    <li>Which doctor is treating the patient?</li>
                </ul>

                <p style='color: #2563eb; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;'>Research:</p>
                <ul style='color: #475569; margin-top: 0;'>
                    <li>What genes are mutated in this patient?</li>
                    <li>What proteins does the disease affect?</li>
                    <li>Is the patient enrolled in any clinical trials?</li>
                </ul>

                <p style='color: #2563eb; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;'>Complex:</p>
                <ul style='color: #475569; margin-top: 0;'>
                    <li>What medications target the expressed proteins?</li>
                    <li>What procedures were performed on which anatomy?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        if submit_button and question:
            with st.spinner("🤖 AI is analyzing the knowledge graph..."):
                try:
                    res = st.session_state['qa'].invoke({"query": question})

                    # Display answer with styling
                    st.markdown("### 📊 Answer")
                    st.markdown(f"""
                        <div style='background: white; padding: 1.5rem; border-radius: 10px;
                                    border-left: 4px solid #2563eb; box-shadow: 0 2px 6px rgba(0,0,0,0.08);'>
                            <p style='font-size: 1.1rem; line-height: 1.6; margin: 0; color: #1e293b;'>
                                {res['result']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Show debug information
                    with st.expander("🔧 Debug Information"):
                        if 'intermediate_steps' in res and res['intermediate_steps']:
                            st.write("**Generated Cypher Query:**")
                            cypher_query = res['intermediate_steps'][0]['query'] if res['intermediate_steps'] else "No query generated"
                            st.code(cypher_query, language='cypher')

                            st.write("**Query Results:**")
                            context = res['intermediate_steps'][0].get('context', 'No results')
                            # Handle both string and dict/list results
                            if isinstance(context, str):
                                st.write(context)  # Display as text if string
                            else:
                                st.json(context)  # Display as JSON if dict/list
                        else:
                            st.warning("No intermediate steps available. Enable return_intermediate_steps=True")

                        st.write("**Full Response:**")
                        st.json(res)

                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")
                    st.write("**Error Details:**")
                    st.exception(e)

if __name__ == "__main__":
    main()



