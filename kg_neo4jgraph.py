from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

# Kết nối Neo4j database
graph = Neo4jGraph(
    url="neo4j+s://94667836.databases.neo4j.io",
    username="neo4j",
    password="qu6Mhe1D89mCZ_umoy5JKwItShKB-cuKh2Cf7Ig9vcU"
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

# Test query với customer có sẵn trong database
query = "List all name of products, price and oder id that customer c009 has purchased, and call them 'product_name', 'price', 'order_id'"
print("=" * 50)

result = chain.invoke({"query": query})
df = pd.DataFrame(result['result'])
print(df)

# Thêm query trực tiếp để so sánh
print("\n" + "=" * 50)
print("Query trực tiếp để kiểm tra:")
direct_result = graph.query("""
MATCH (c:Customer {customerId: 'c009'})-[:PLACED_ORDER]->(o:Order)-[:INCLUDES_PRODUCT]->(p:Product)
RETURN p.name as product_name, p.price as price, p.productId as product_id
""")
print(f"Sản phẩm customer c009 đã mua:")
df1 = pd.DataFrame(direct_result)
print(df1)
