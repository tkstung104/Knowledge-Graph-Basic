from neo4j import GraphDatabase

URI = "neo4j+s://94667836.databases.neo4j.io"
AUTH = ("neo4j", "qu6Mhe1D89mCZ_umoy5JKwItShKB-cuKh2Cf7Ig9vcU")

driver = GraphDatabase.driver(URI, auth=AUTH)
with driver.session() as session:
    result = session.run("RETURN 'AuraDB Free OK' AS msg")
    print(result.single()["msg"])
driver.close()