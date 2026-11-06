# Web App — AI Agent Office Monitor

[Về mục lục dự án](../README.md)

Web App kết hợp phần ứng dụng phục vụ đồ án NT548 với đề xuất giao diện quan sát hoạt động agents/tasks mô phỏng. Phạm vi bắt buộc và phần mở rộng có điều kiện được xác định trong [BRD Official](official/BRD.md).

## Chọn đúng bộ tài liệu

| Bạn cần | Đọc tại |
|---|---|
| Hiểu mục tiêu, yêu cầu, thiết kế, dữ liệu và định hướng migration | [Official Documentation](official/README.md) |
| Xem bài thử nghiệm thực tế đã dùng làm nguồn biên tập | [Practical test](validation/practical-test/evaluation-report.md) |
| Xem lần smoke test và các bằng chứng kiểm thử Skills trước đó | [Validation/Test Documentation](validation/README.md) |

## Cấu trúc

```text
web-app/
├── README.md
├── official/
│   ├── README.md
│   ├── BRD.md
│   ├── FRD.md
│   ├── api-contract.yaml
│   ├── architecture.md
│   ├── data-contract.md
│   └── migration-plan.md
└── validation/
    ├── smoke/
    ├── practical-test/
    └── báo cáo, evidence và scripts kiểm thử
```

Sáu bản `practical-test/01…06` được giữ nguyên làm snapshot nguồn. Sáu tài liệu tại `official/` là bản biên tập dùng cho phát triển; từ đây các cập nhật nghiệp vụ và kỹ thuật được thực hiện tại bản Official, không ghi đè lịch sử kiểm thử.
