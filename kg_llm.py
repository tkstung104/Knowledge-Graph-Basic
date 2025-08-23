from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import pandas as pd
import os
from langchain_core.prompts import PromptTemplate

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

# Khỏi tạo prompt
cypher_prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "Bạn là chuyên gia viết Cypher.\n"
        "- Khi RETURN p.xxx hãy alias thành AS xxx.\n"
        "Ví dụ: RETURN p.name AS name, p.productId AS productId\n\n"
        "Hỏi: {question}\n"
        "Trả về DUY NHẤT câu lệnh Cypher hợp lệ."
    ),
)

qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Bạn là trợ lý dữ liệu. Dựa trên DỮ LIỆU dưới đây, trả lời ngắn gọn bằng tiếng Việt.\n"
        "Nếu là danh sách sản phẩm, hãy in mỗi dòng theo mẫu: - tên (mã)\n"
        "KHÔNG dùng dấu ngoặc nhọn.\n\n"
        "DỮ LIỆU:\n{context}\n\n"
        "CÂU HỎI:\n{question}"
    ),
)

# Tạo chain với GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    # cypher_prompt=cypher_prompt,
    # qa_prompt=qa_prompt,
    return_direct=False,
    allow_dangerous_requests=True
)

while True:
    print("Gõ 'exit' hoặc 'quit' để thoát")
    query = input(f"Query: ")
    if query.lower() in {"exit", "quit"}:
        break
    print("=" * 50)

    result = chain.invoke({"query": query})
    print(chain.return_direct)

    # Sử dụng pandas để in ra kết quả dưới dạng bảng
    if result['result'] not in ["I don't know the answer.", "Tôi không biết câu trả lời."]:
        print(result['result'])
    else:
        # df = pd.DataFrame(chain.return_direct)
        # print(df)
        print("=" * 50)