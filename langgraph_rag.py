from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase
from typing import List, Any, Optional

# Neo4j config
NEO4J_URL = ""
NEO4J_USER = ""
NEO4J_PASSWORD = ""

driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, NEO4J_PASSWORD))

# LLM config
llm = ChatOpenAI(temperature=0)

# Cypher prompt for LLM
cypher_prompt_template = PromptTemplate.from_template("""
Bạn là một trợ lý AI truy vấn hệ thống đồ thị Neo4j lưu thông tin điện thoại.

Dưới đây là một số ví dụ:
Câu hỏi: các điện thoại nào có cân nặng 194g.
Cypher query:
MATCH (p:Model)-[:HAS_WEIGHT]->(w:Weight)
WHERE w.value = "194g"
RETURN p.name

Câu hỏi: Điện thoại nào của Samsung có RAM 8GB?
Cypher query:
MATCH (m:Model)-[:HAS_COMPANY_NAME]->(c:Company {{name: "Samsung"}})
MATCH (m)-[:HAS_RAM]->(r:RAM {{size: "8GB"}})
RETURN m.name

Câu hỏi: Các mẫu iPhone ra mắt năm 2024?
Cypher query:
MATCH (m:Model)-[:HAS_COMPANY_NAME]->(c:Company {{name: "Apple"}})
MATCH (m)-[:HAS_YEAR]->(y:Year {{year: 2024}})
RETURN m.name

Câu hỏi: Điện thoại nào có camera sau 50MP?
Cypher query:
MATCH (m:Model)-[:HAS_BACK_CAMERA]->(c:Camera {{name: "50MP", type: "Back"}})
RETURN m.name

Câu hỏi: Điện thoại nào có giá tại Pakistan là PKR 200,000?
Cypher query:
MATCH (m:Model)-[:HAS_PAKISTAN_PRICE]->(p:Price {{value: "PKR 200,000", country: "Pakistan"}})
RETURN m.name

Câu hỏi: Điện thoại nào có pin 5000mAh?
Cypher query:
MATCH (m:Model)-[:HAS_BATTERY]->(b:Battery {{capacity: "5000mAh"}})
RETURN m.name

Câu hỏi: Điện thoại nào có màn hình 6.7 inches?
Cypher query:
MATCH (m:Model)-[:HAS_SCREEN]->(s:Screen {{size: "6.7 inches"}})
RETURN m.name

Câu hỏi: Điện thoại nào có processor Snapdragon 8 Gen 2?
Cypher query:
MATCH (m:Model)-[:HAS_PROCESSOR]->(p:Processor {{name: "Snapdragon 8 Gen 2"}})
RETURN m.name

Câu hỏi: Giá trung quốc của điện thoại iPhone 15 Pro 128GB là bao nhiêu?
Cypher query:
MATCH (m:Model {{name: 'iPhone 15 Pro 128GB'}}) - [:HAS_CHINA_PRICE] -> (p:Price)
RETURN p.value

Câu hỏi: Thông tin chi tiết điện thoại iPhone 15 Pro 128GB.
Cypher query:
MATCH (m:Model {{name: 'iPhone 15 Pro 128GB'}})-[:HAS_RAM]->(r:RAM),       (m)-[:HAS_WEIGHT]->(w:Weight),       (m)-[:HAS_SCREEN]->(s:Screen),       (m)-[:HAS_COMPANY_NAME]->(c:Company),       (m)-[:HAS_FRONT_CAMERA]->(cam:Camera),       (m)-[p:HAS_USA_PRICE]->(price)
RETURN m.name AS model, r.size AS ram, w.value AS weight, s.size AS screen, c.name AS company, cam.name AS camera, price.value AS price

Câu hỏi: {query}
Cypher query:
""")

def run_cypher_query(cypher_query: str):
    cypher_query = str(cypher_query)  # Đảm bảo là chuỗi
    with driver.session() as session:
        result = session.run(cypher_query)  # type: ignore
        return [record.data() for record in result]

def run_cypher_query_from_nl(query: str):
    cypher_query = llm.invoke(cypher_prompt_template.format(query=query)).content
    print("🔎 Generated Cypher:\n", cypher_query)
    # Kiểm tra Cypher hợp lệ
    if not str(cypher_query).strip().lower().startswith(("match", "call", "return", "with", "create")):
        return [], cypher_query
    try:
        results = run_cypher_query(str(cypher_query))
        return results, cypher_query
    except Exception as e:
        print("❌ Cypher error:", e)
        return [], cypher_query

def format_product_result(records):
    # Nếu records là list các dict, hiển thị dạng bảng
    if not records:
        return "Không tìm thấy kết quả phù hợp."
    if isinstance(records, list) and isinstance(records[0], dict):
        keys = records[0].keys()
        lines = [" | ".join(keys)]
        lines.append("-" * (len(lines[0])))
        for rec in records:
            lines.append(" | ".join(str(rec[k]) for k in keys))
        return "\n".join(lines)
    # Nếu là list các giá trị đơn
    if isinstance(records, list):
        return "\n".join(str(r) for r in records)
    return str(records)

# Một số Cypher template mẫu cho các truy vấn phổ biến
cypher_templates = {
    "find_by_company": lambda company: f"""
        MATCH (m:Model)-[:HAS_COMPANY_NAME]->(c:Company {{name: '{company}'}})
        RETURN m.name AS model, c.name AS company LIMIT 10
    """,
    "find_by_ram": lambda ram: f"""
        MATCH (m:Model)-[:HAS_RAM]->(r:RAM {{size: '{ram}'}})
        RETURN m.name AS model, r.size AS ram LIMIT 10
    """,
    "find_by_price": lambda price: f"""
        MATCH (m:Model)-[:HAS_PAKISTAN_PRICE]->(p:Price)
        WHERE p.value CONTAINS '{price}'
        RETURN m.name AS model, p.value AS price LIMIT 10
    """,
    "find_by_year": lambda year: f"""
        MATCH (m:Model)-[:HAS_YEAR]->(y:Year {{year: {year}}})
        RETURN m.name AS model, y.year AS year LIMIT 10
    """,
}

def answer_general_question(query: str, history: Optional[List[Any]] = None) -> str:
    # Tạo prompt có lịch sử hội thoại
    if history is None:
        history = []
    # Ghép lịch sử thành đoạn hội thoại
    history_text = ""
    for turn in history:
        if isinstance(turn, dict):
            # Nếu lưu dạng dict {"user": "...", "bot": "..."}
            history_text += f"User: {turn.get('user', '')}\nBot: {turn.get('bot', '')}\n"
        else:
            history_text += f"{turn}\n"
    prompt = f"{history_text}User: {query}\nBot:"
    response = llm.invoke(prompt)
    if hasattr(response, "content"):
        return str(response.content)
    return str(response)

def chat(query: str, history: Optional[List[Any]] = None):
    if history is None:
        history = []
    try:
        cypher_query = run_cypher_query_from_nl(query)
        if isinstance(cypher_query, tuple):
            cypher_query = cypher_query[1] if len(cypher_query) > 1 else cypher_query[0]
        if isinstance(cypher_query, str) and cypher_query:
            records = run_cypher_query(cypher_query)
            if records:
                answer = format_product_result(records)
                # Lưu vào history
                history.append({"user": query, "bot": answer})
                return answer
    except Exception as e:
        pass
    # Nếu không có kết quả, trả lời tự do và lưu vào history
    answer = answer_general_question(query, history)
    history.append({"user": query, "bot": answer})
    return answer

# Hàm chat sử dụng Cypher trực tiếp (nếu muốn)
def chat_neo4j(cypher_query: str):
    results = run_cypher_query(cypher_query)
    return format_product_result(results)
