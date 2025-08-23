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
    return_direct=False,
    allow_dangerous_requests=True
)

chain_temp = GraphCypherQAChain.from_llm(
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
    result_temp = chain_temp.invoke({"query": query})

    if result['result'] not in ["I don't know the answer.", "Tôi không biết câu trả lời."]:
        print(result['result'])
    else:
        df = pd.DataFrame(result_temp['result'])
        print(df)
        print("=" * 51)