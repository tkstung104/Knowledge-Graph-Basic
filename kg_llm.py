from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Kết nối Neo4j database
graph = Neo4jGraph(
    url=URI,
    username=AUTH[0],
    password=AUTH[1]
)

# Khởi tạo LLM với temperature thấp cho tốc độ nhanh hơn
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,  # Giảm randomness để nhanh hơn
    max_tokens=500  # Giới hạn độ dài response
)

# Tạo chain với GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    return_direct=True,
    allow_dangerous_requests=True
)

while True:
    print("Gõ 'exit' hoặc 'quit' để thoát")
    query = input(f"Query: ")
    if query.lower() in {"exit", "quit"}:
        break
    print("=" * 50)

    result = chain.invoke({"query": query})

    # Sử dụng pandas để in ra kết quả dưới dạng bảng
    df = pd.DataFrame(result['result'])
    print(df)
    print("=" * 50)