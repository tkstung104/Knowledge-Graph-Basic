from neo4j import GraphDatabase
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
import pandas as pd

URI = "neo4j+s://94667836.databases.neo4j.io"
AUTH = ("neo4j", "qu6Mhe1D89mCZ_umoy5JKwItShKB-cuKh2Cf7Ig9vcU")

graph = Neo4jGraph(
    url="neo4j+s://94667836.databases.neo4j.io",
    username="neo4j",
    password="qu6Mhe1D89mCZ_umoy5JKwItShKB-cuKh2Cf7Ig9vcU"
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
