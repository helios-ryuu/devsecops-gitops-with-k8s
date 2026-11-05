# Kiểm thử BA Skills — NT548

> **SANDBOX / TÀI LIỆU THỬ NGHIỆM.** Không phải bộ BA chính thức; không phê duyệt yêu cầu, kiến trúc hay migration.

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| TEST-INDEX | 0.1.0 | draft | 2026-11-05 | Người dùng review; người thực hiện Codex | Yêu cầu phiên hiện tại; E-01..E-12 | Project commit `2110eddec91bc3e34137c86fef693095c4afb677` |

Thay đổi 0.1.0: tạo bộ thử nghiệm trên `ba/documentation`, bắt đầu từ `brd-authoring`. Chỉ thư mục này được thêm. Không commit, push, merge hoặc tạo tài liệu BA ở ngoài sandbox trong lượt này.

Đọc [báo cáo kết quả](report.md), [kế hoạch kiểm thử](test-plan.md), [bằng chứng và vấn đề](evidence-register.md), [traceability](traceability.md). Bằng chứng máy đọc được: [Git/source/skill hashes](evidence.json), [catalog của phiên](runtime-discovery.json), [kết quả bundle](bundle-results.json), [nhật ký áp dụng và review revisions](execution-log.json), [QA đầu](document-checks.initial.json), [kiểm tra tài liệu sau sửa](document-checks.json).

Thứ tự áp dụng trong cùng một phiên, có sử dụng đầu ra của bước trước:

1. `brd-authoring` → [BRD thử nghiệm](smoke/BRD.md).
2. `frd-authoring` → [FRD thử nghiệm](smoke/FRD.md).
3. `api-contract-design` → [OpenAPI thử nghiệm](smoke/api-contract.yaml).
4. `architecture-design` → [Architecture thử nghiệm](smoke/architecture.md).
5. `data-contract-design` → [Data contract thử nghiệm](smoke/data-contract.md).
6. `backend-migration-planning` → [Migration draft có điều kiện](smoke/migration-plan.md).

Phân biệt ba kết luận: **nhận diện Skill trong catalog**, **áp dụng có hướng dẫn trong phiên này**, **đánh giá chọn Skill tự động trong phiên độc lập**. Hai kết luận đầu có bằng chứng riêng; kết luận thứ ba chưa được kiểm thử. Đọc `SKILL.md` và chạy checker cấu trúc không tự chứng minh nhận diện hoặc chọn Skill.

Các tài liệu là lát cắt giới hạn: hiển thị lượt xem, probes, metrics và ràng buộc vận hành liên quan. Chúng không cố bao phủ toàn bộ đồ án, không đưa AI workspace/SSE/Three.js vào phạm vi, và không biến Laravel thành yêu cầu hiện tại.

Tái kiểm tra bằng các lệnh chỉ ghi trong sandbox:

```powershell
bun.cmd run C:/Users/84352/.agents/skills/business-analyst-skill/scripts/validate-bundle.mjs
python docs/web-app/validation/validate_documents.py
```

`capture_evidence.py` chỉ dành cho lần chụp đầu; dùng chế độ tạo file mới và từ chối ghi đè baseline. Checker tài liệu không chạy ứng dụng, không kiểm tra cluster và không thay thế review ngữ nghĩa độc lập. Xem giới hạn và câu hỏi Q-01..Q-07 trong evidence register trước khi dùng kết quả.
