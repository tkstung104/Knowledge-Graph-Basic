# Knowledge Graph (KG) Folder

This folder contains scripts for working with Neo4j Knowledge Graph and LangChain.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with Neo4j connection information:
```env
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

## How to run files

### 1. Test Neo4j connection
```bash
python activate_neoj4.py
```
- Test connection to Neo4j database
- Print "AuraDB Free OK" message if connection is successful

### 2. Basic query
```bash
python kg_basic.py
```
- Execute basic Cypher query
- Display top 5 products with highest prices

### 3. LLM interaction
```bash
python kg_llm.py
```
- Run interactive chatbot with Knowledge Graph
- Use GPT-4o-mini to answer questions
- Type 'exit' or 'quit' to exit

### 4. Specific query example
```bash
python kg_neo4jgraph.py
```
- Demo query for customer c009's product information
- Compare results between LLM and direct query

## Notes

- Ensure Neo4j database is initialized with sample data
- Valid OpenAI API key is required
- CSV files in the `others/` folder contain sample data for Neo4j import
