from neo4j import GraphDatabase
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

graph = Neo4jGraph(
    url=URI,
    username=AUTH[0],
    password=AUTH[1]
)

query = """
    MATCH (p:Product)
    RETURN p.productId AS id, p.name AS name, p.price AS price
    ORDER BY p.price DESC
    LIMIT 5
    """
result = graph.query(query)
# print(result)
df = pd.DataFrame(result)
print(df)

# driver = GraphDatabase.driver(URI, auth=AUTH)

# with driver.session() as session:
#     query = """
#     MATCH (p:Product)
#     RETURN p.productId AS id, p.name AS name, p.price AS price
#     ORDER BY p.price DESC
#     LIMIT 5
#     """
#     result = graph.query(query)
#     print(result)
#     df = pd.DataFrame(result)
#     print(df)

# driver.close()
