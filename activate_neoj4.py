from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH)
with driver.session() as session:
    result = session.run("RETURN 'AuraDB Free OK' AS msg")
    print(result.single()["msg"])
driver.close()