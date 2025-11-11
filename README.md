# BioGraphRAG: Biomedical Knowledge Graph System

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0+-018bff.svg)](https://neo4j.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-00C58E.svg)](https://langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An advanced GraphRAG system for extracting and querying biomedical knowledge from scientific literature**

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Usage](#usage) • [Docker](#docker-deployment) • [Architecture](#architecture)

</div>

---

## Overview

BioGraphRAG is a state-of-the-art Graph Retrieval-Augmented Generation (GraphRAG) application designed specifically for biomedical research. It combines the power of large language models, knowledge graphs, and vector search to transform unstructured biomedical documents into queryable knowledge bases.

The system automatically extracts entities, relationships, and properties from PDF documents, constructs a comprehensive knowledge graph in Neo4j, and enables natural language querying with conversational AI responses.

### Key Capabilities

- **Intelligent Entity Extraction**: Automatically identifies 12+ biomedical entity types from scientific literature
- **Property Extraction**: Captures quantitative data including dosages, dates, measurements, and test values
- **Knowledge Graph Construction**: Builds rich, interconnected knowledge graphs in Neo4j
- **Natural Language Querying**: Ask questions in plain English and receive contextual, conversational answers
- **Hybrid Search**: Combines vector similarity and keyword matching for accurate information retrieval
- **Production Ready**: Docker support, health checks, and enterprise-grade deployment options

---

## Features

### Comprehensive Biomedical Schema

BioGraphRAG extracts and organizes information across 12 specialized entity types:

| Entity Type | Description | Properties Extracted |
|-------------|-------------|---------------------|
| **Patient** | Patient demographics and identifiers | ID, age, gender, medical history |
| **Disease** | Diseases, conditions, and diagnoses | Name, type, severity, stage |
| **Medication** | Drugs and therapeutic agents | Name, dosage, frequency, route |
| **Test** | Diagnostic and laboratory tests | Type, values, units, dates |
| **Symptom** | Clinical symptoms and manifestations | Description, severity, onset |
| **Doctor** | Healthcare providers | Name, specialty, affiliation |
| **Procedure** | Medical procedures and interventions | Type, date, outcome, duration |
| **Anatomy** | Anatomical structures and systems | Location, affected areas |
| **Gene** | Genetic markers and mutations | Gene name, variants, expression |
| **Protein** | Proteins and biomolecules | Name, function, interactions |
| **Biomarker** | Biological markers | Type, values, significance |
| **ClinicalTrial** | Clinical trial information | ID, phase, status, endpoints |

### Relationship Extraction

The system automatically identifies and maps 11 types of relationships:

- `HAS_DISEASE` - Patient-disease associations
- `TAKES_MEDICATION` - Medication regimens
- `UNDERWENT_TEST` - Diagnostic testing
- `HAS_SYMPTOM` - Symptom presentations
- `TREATED_BY` - Provider relationships
- `EXPRESSES` - Gene expression patterns
- `MUTATES` - Genetic mutations
- `TARGETS` - Drug-target interactions
- `ENROLLED_IN` - Clinical trial participation
- `AFFECTS` - Disease-anatomy relationships
- `UNDERWENT_PROCEDURE` - Medical interventions

### Advanced Query Capabilities

- **Simple Queries**: "What medications are mentioned?"
- **Relationship Queries**: "What medications does the patient take?"
- **Complex Queries**: "What medications target specific proteins affected by the disease?"
- **Natural Language Responses**: Conversational, contextual answers instead of raw data

---

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/biographrag.git
cd biographrag

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the application
docker-compose up --build

# Access at http://localhost:8501
```

### Using Python Virtual Environment

```bash
# Clone and navigate to project
git clone https://github.com/yourusername/biographrag.git
cd biographrag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run application
streamlit run main.py
```

---

## Installation

### Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Neo4j Aura Account** - [Sign up for Neo4j Aura](https://neo4j.com/cloud/aura/)
- **OpenAI API Key** - [Get API key](https://platform.openai.com/api-keys)
- **Groq API Key** - [Get API key](https://console.groq.com/)
- **Docker** (optional) - [Install Docker](https://docs.docker.com/get-docker/)

### Environment Configuration

Create a `.env` file in the project root:

```env
# Neo4j Configuration
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password

# OpenAI Configuration (for embeddings)
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Groq Configuration (for LLM)
GROQ_API_KEY=gsk_your-groq-api-key
```

### Dependencies

All dependencies are listed in `requirements.txt`:

```
langchain==0.1.0
langchain-community==0.0.10
langchain-experimental==0.0.47
langchain-openai==0.0.2
langchain-groq==0.0.1
sentence-transformers==2.2.2
neo4j==5.14.1
pypdf==3.17.1
python-dotenv==1.0.0
streamlit==1.28.1
```

---

## Usage

### 1. Upload a Biomedical Document

- Launch the application
- Use the file uploader to select a PDF document
- Click "Process Document" to begin extraction

### 2. Processing Pipeline

The system executes the following steps:

1. **Document Loading**: PDF text extraction with page segmentation
2. **Text Chunking**: Smart chunking with overlap for context preservation
3. **Entity Extraction**: AI-powered identification of biomedical entities
4. **Property Extraction**: Quantitative data capture (dosages, dates, values)
5. **Relationship Mapping**: Automatic relationship discovery
6. **Graph Storage**: Neo4j knowledge graph construction
7. **Vector Indexing**: Hybrid search index creation
8. **QA Chain Setup**: Natural language query interface initialization

**Processing Time**: 30-90 seconds for typical biomedical documents

### 3. Query the Knowledge Graph

#### Simple Entity Queries
```
What medications are mentioned in the document?
What diseases are discussed?
What genes or proteins are mentioned?
```

#### Relationship Queries
```
What medications does the patient take?
Which doctor treated the patient?
What procedures were performed?
```

#### Complex Medical Queries
```
What medications are used to treat the disease?
What genes are affected by the disease?
What medications target specific proteins?
Is the patient enrolled in any clinical trials?
```

### 4. Interpreting Results

Answers are provided in natural, conversational language with:
- Context from the source document
- Relevant details and explanations
- Clear indication when information is not found

---

## Docker Deployment

### Quick Deploy with Docker Compose

```bash
docker-compose up --build
```

Access the application at `http://localhost:8501`

### Manual Docker Build

```bash
# Build image
docker build -t biographrag:latest .

# Run container
docker run -d \
  --name biographrag-app \
  -p 8501:8501 \
  --env-file .env \
  biographrag:latest

# View logs
docker logs -f biographrag-app
```

### Production Deployment

For production environments, see [DOCKER_README.md](./DOCKER_README.md) for:
- Resource limits configuration
- SSL/TLS setup with reverse proxy
- Health check monitoring
- Logging and observability
- Scaling strategies

---

## Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq Llama 3.3 70B | Entity extraction & query generation |
| **Embeddings** | OpenAI Ada-002 | Vector representations for hybrid search |
| **Database** | Neo4j Aura | Knowledge graph storage |
| **Framework** | LangChain | RAG orchestration |
| **Interface** | Streamlit | Web application UI |
| **Deployment** | Docker | Containerized deployment |

### System Architecture

```
┌─────────────────┐
│  PDF Document   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Extractor │
│    (PyPDF)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM Transformer │
│  (Groq LLaMA)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│   Neo4j Graph   │◄────│ Cypher Query │
│    Database     │     │  Generator   │
└────────┬────────┘     └──────▲───────┘
         │                     │
         ▼                     │
┌─────────────────┐           │
│ Vector Embeddings│           │
│   (OpenAI Ada)  │           │
└────────┬────────┘           │
         │                     │
         ▼                     │
┌─────────────────────────────┴──┐
│     Natural Language Query     │
│      GraphCypherQAChain        │
└────────────────────────────────┘
```

### Data Flow

1. **Ingestion**: PDF document uploaded via Streamlit interface
2. **Extraction**: PyPDF extracts text, LangChain chunks content
3. **Transformation**: Groq LLaMA extracts entities, relationships, and properties
4. **Storage**: Structured data stored in Neo4j knowledge graph
5. **Indexing**: OpenAI Ada-002 creates vector embeddings for hybrid search
6. **Querying**: Natural language queries converted to Cypher via LLM
7. **Response**: Results formatted into conversational answers

---

## Project Structure

```
biographrag/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration (not in git)
├── .env.example           # Environment template
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker build exclusions
├── README.md              # This file
├── DOCKER_README.md       # Docker deployment guide
└── LICENSE                # MIT License
```

---

## Performance Considerations

### Processing Time Breakdown

| Stage | Time | % of Total |
|-------|------|-----------|
| PDF Loading | 2-5 sec | 5% |
| Text Chunking | 1-3 sec | 3% |
| **Entity Extraction** | 15-40 sec | 50% |
| Property Extraction | 5-10 sec | 10% |
| **Graph Storage** | 5-10 sec | 15% |
| **Vector Indexing** | 8-15 sec | 20% |
| QA Setup | 1-2 sec | 2% |

**Optimization Tips**:
- Use smaller documents (< 50 pages) for faster processing
- Groq API provides fast inference (primary bottleneck is entity extraction volume)
- Neo4j Aura connection speed depends on geographic location
- OpenAI embedding API calls are parallelized where possible

### Resource Requirements

**Minimum**:
- 2 GB RAM
- 1 CPU core
- 500 MB disk space

**Recommended**:
- 4 GB RAM
- 2 CPU cores
- 2 GB disk space

---

## Troubleshooting

### Common Issues

#### Connection Errors

**Neo4j Connection Failed**
```bash
# Verify credentials in .env
# Check Neo4j Aura instance is running
# Confirm URI includes neo4j+s:// protocol
```

**API Key Errors**
```bash
# Verify all API keys in .env are valid
# Check API key permissions and quotas
# Ensure no extra spaces in environment variables
```

#### Processing Errors

**Entity Extraction Fails**
```python
# Error: Model doesn't support function calling
# Solution: Ensure using llama-3.3-70b-versatile (not gpt-oss-20b)
```

**Memory Issues**
```bash
# For large PDFs, increase Docker memory limit:
docker run --memory="4g" --cpus="2" ...
```

### Debug Mode

Enable verbose logging by checking the "Debug Information" expander after each query to view:
- Generated Cypher queries
- Raw database results
- Full LangChain response chain

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black main.py

# Lint code
flake8 main.py
```

---

## Roadmap

- [ ] Support for multiple document formats (DOCX, TXT, XML)
- [ ] Batch document processing
- [ ] Advanced graph visualization
- [ ] Export functionality (JSON, CSV, GraphML)
- [ ] Multi-user session management
- [ ] Graph query history and bookmarks
- [ ] Custom entity type configuration
- [ ] RESTful API endpoints
- [ ] Integration with PubMed and biomedical databases
- [ ] Support for biomedical ontologies (MeSH, SNOMED CT)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Citation

If you use BioGraphRAG in your research, please cite:

```bibtex
@software{biographrag2024,
  title={BioGraphRAG: Biomedical Knowledge Graph System},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/biographrag}
}
```

---

## Acknowledgments

- **LangChain** for the RAG orchestration framework
- **Neo4j** for the graph database platform
- **Groq** for high-performance LLM inference
- **OpenAI** for embedding models
- **Streamlit** for the web application framework

---

## Contact

For questions, issues, or collaboration opportunities:

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/biographrag/issues)
- **Email**: your.email@example.com
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

<div align="center">

**Built with ❤️ for biomedical research**

[⬆ Back to Top](#biographrag-biomedical-knowledge-graph-system)

</div>
