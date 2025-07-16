import gradio as gr
from langgraph_rag import chat, chat_neo4j

chat_history_memory = []

with gr.Blocks(title="📱 Phone Specs Chatbot") as demo:
    gr.Markdown("## 🤖 Trợ lý AI - Hỏi gì về điện thoại cũng biết!")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Nhập câu hỏi về điện thoại...", label="Bạn hỏi:")
    mode = gr.Radio(["Vector Search (RAG)", "Cypher Query (Graph)"], value="Vector Search (RAG)", label="Chế độ trả lời")
    clear = gr.Button("🧹 Xoá hội thoại")

    def respond(user_input, history_ui, selected_mode):
        global chat_history_memory

        if selected_mode == "Vector Search (RAG)":
            result = chat(user_input, chat_history_memory)
            response = result  # Sửa ở đây
            # chat_history_memory = result["chat_history"]  # Nếu cần lưu history, tự xử lý thêm
        else:  # dùng Cypher
            results = chat_neo4j(user_input)
            if not results:
                response = "Không tìm thấy kết quả phù hợp."
            else:
                response = "\n".join([str(r) for r in results])

        history_ui.append((user_input, response))
        return "", history_ui

    def clear_all():
        global chat_history_memory
        chat_history_memory = []
        return []

    msg.submit(respond, [msg, chatbot, mode], [msg, chatbot])
    clear.click(clear_all, outputs=chatbot)

demo.launch()
