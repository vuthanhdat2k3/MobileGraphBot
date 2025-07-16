# Chatbot Tư Vấn Mua Điện Thoại Dựa Trên Neo4j

## Mô tả dự án

Chatbot này sử dụng mô hình ngôn ngữ lớn (LLM) kết hợp với cơ sở dữ liệu đồ thị Neo4j để hỗ trợ khách hàng tìm kiếm, so sánh và tư vấn các sản phẩm điện thoại di động. Dữ liệu sản phẩm được chuẩn hóa thành các thực thể (Model, Company, RAM, Camera, Price, Year, ...) và các mối quan hệ (HAS_COMPANY_NAME, HAS_RAM, HAS_WEIGHT, ...), giúp truy vấn linh hoạt và thông minh.

## Tính năng chính
- Hiểu câu hỏi tự nhiên của người dùng về điện thoại (hãng, cấu hình, giá, năm ra mắt, ...)
- Sinh truy vấn Cypher tự động để lấy dữ liệu từ Neo4j
- Định dạng kết quả trả về rõ ràng, dễ hiểu
- Có các template truy vấn mẫu cho các nhu cầu phổ biến
- Dễ dàng mở rộng thêm thuộc tính, mối quan hệ, loại truy vấn

## Hướng dẫn sử dụng
1. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
2. Đảm bảo đã import dữ liệu và các mối quan hệ vào Neo4j (sử dụng các file Cypher đã sinh).
3. Chạy chatbot:
   ```bash
   python app.py
   ```
4. Đặt câu hỏi về điện thoại, ví dụ:
   - "Các điện thoại nào có cân nặng 194g?"
   - "Điện thoại Samsung nào có RAM 8GB?"
   - "Các mẫu iPhone ra mắt năm 2024?"
   - "Điện thoại nào giá dưới PKR 200,000?"

## Hướng phát triển & cải tiến
- **Tích hợp đa kênh:** Kết nối chatbot với website, Facebook, Zalo, v.v. để hỗ trợ khách hàng mọi lúc mọi nơi.
- **Cá nhân hóa:** Gợi ý sản phẩm dựa trên lịch sử tìm kiếm, sở thích, ngân sách của từng khách hàng.
- **So sánh sản phẩm:** Cho phép người dùng so sánh nhiều mẫu điện thoại theo các tiêu chí khác nhau.
- **Tư vấn thông minh:** Đề xuất sản phẩm phù hợp dựa trên nhu cầu (chơi game, chụp ảnh, pin trâu, ...).
- **Tích hợp giỏ hàng & đặt mua:** Cho phép khách hàng thêm sản phẩm vào giỏ, đặt mua trực tiếp qua chatbot.
- **Phản hồi & đánh giá:** Thu thập ý kiến, đánh giá sản phẩm và dịch vụ để cải thiện trải nghiệm.
- **Phân tích dữ liệu:** Sử dụng dữ liệu truy vấn để phân tích xu hướng, nhu cầu thị trường.
- **Đa ngôn ngữ:** Hỗ trợ tiếng Việt, Anh, và các ngôn ngữ khác.

## Đóng góp & phát triển
- Đóng góp thêm dữ liệu, template truy vấn, hoặc cải tiến code đều được hoan nghênh!
- Liên hệ: [Your Contact/Email Here] 