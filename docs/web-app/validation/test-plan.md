# Kế hoạch kiểm thử sáu BA Skills

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| TEST-PLAN | 0.1.0 | draft | 2026-11-05 | Codex thực hiện; người dùng review | Yêu cầu người dùng; shared standard 1.0.0 | Project `2110edd`; skill bundle `3f0127b` |

Change log 0.1.0: thiết lập tiêu chí trước khi tạo smoke outputs. Owner role ở đây chỉ là phân công cho lần test; không suy ra quyền phê duyệt tài liệu sản phẩm.

## Điều kiện và nguồn

Working tree ban đầu sạch; chưa có nhánh local/remote `ba/documentation` trong danh sách sau fetch. `git fetch origin main` thành công sau cấp quyền ghi Git metadata. `git switch -c ba/documentation origin/main` thành công. HEAD/main/origin-main cùng SHA đầy đủ trong [evidence.json](evidence.json). Không rebase, reset, stash, xóa hoặc ghi đè thay đổi. Nhánh đang track `origin/main` do tạo từ remote ref; không có push upstream riêng.

Đọc instructions áp dụng: không tìm thấy ancestor/root AGENTS.md trong chuỗi đường dẫn đã kiểm tra; `app/AGENTS.md` có quy tắc đọc tài liệu Next trước khi viết application code. Lượt này chỉ đọc source, không viết code ứng dụng. Cả sáu entry point, template riêng và shared standard được đọc theo từng bước. Bundle có remote đúng URL người dùng cung cấp và pin `3f0127b33bc6612f743c1aec4862079eea3adb9e`; skill files khớp Git HEAD. Repo bundle có thay đổi sẵn ngoài `skills/`, được giữ nguyên. Không coi README/notes đã sửa tại bundle là yêu cầu được người dùng xác nhận trong phiên này; không áp patch hoặc PR ngoài nhiệm vụ.

## Cách chấm

PASS chỉ trong phạm vi được kiểm tra có bằng chứng; FAIL khi quan sát được vi phạm; BLOCKED khi thiếu dữ liệu/công cụ/ủy quyền cần cho kết luận; N/A cần nêu lý do. Skill có thể xử lý thiếu dữ liệu đúng (PASS về hành vi giới hạn) trong khi tài liệu/khả năng triển khai vẫn BLOCKED. Mỗi kết quả phải nói đối tượng chấm. Không gộp những trường hợp đó thành “toàn bộ PASS”.

| Test | Thao tác / prompt áp dụng | Kỳ vọng / bằng chứng cần |
|---|---|---|
| T-01 | Kiểm tra Git rồi tạo nhánh từ main mới fetch | Clean start; SHA bằng nhau; không thay file cũ |
| T-02 | Đối chiếu Available skills catalog do runtime đưa vào context, trước đọc manifest | Đủ 6 tên/mô tả/path; bản chép có nhãn provenance; thiếu thì BLOCKED |
| T-03 | Rerun bundle checker đã đọc source | Manifest/frontmatter, template links, six entries và negative fixture checks; không tính là runtime discovery |
| T-04 | Dùng `brd-authoring`: từ README/WBS/source viết BRD draft nhỏ cho web demo; không suy nhu cầu từ stack | Outcome trước công nghệ; BR có source/scope/commitment; không bịa approval/rubric/SLA |
| T-05 | Dùng `frd-authoring`: refine BRD thử nghiệm thành FR/RULE/AC/NFR | FR có parent; failure/concurrency TBD khi thiếu nguồn; code-observed khác planned |
| T-06 | Dùng `api-contract-design`: mô tả chính xác probes quan sát được; ghi gaps cho counter/metrics | Schema/type/required/enum/time/example rõ; không tự tạo API nghiệp vụ hoặc readiness 503 giả |
| T-07 | Dùng `architecture-design`: đối chiếu README/WBS và code/config | Tách planned/as-observed; không coi Next thay Express; Redis manifests không chứng minh tích hợp |
| T-08 | Dùng `data-contract-design`: map probe fields; review dữ liệu counter dự kiến | Không bịa Redis key/TTL/durability; field owner API, storage owner Data |
| T-09 | Dùng `backend-migration-planning`: đánh giá khả năng thay backend khi chưa có source Express/target chốt | Partial draft BLOCKED; giữ Next frontend; không thực thi cutover; parity chưa chạy |
| T-10 | Review nội dung sáu outputs; kiểm tra máy và mutation cases trong bộ nhớ | Trace BR→FR→operation→entity, NFR→control; phát hiện parent/type/enum/required/version drift |
| T-11 | Natural-language trigger prompts, không nêu tên Skill, trong phiên độc lập | Chưa có independent harness run; BLOCKED, không lấy lựa chọn có hướng dẫn ở đây làm PASS |
| T-12 | Runtime HTTP/Redis, rendered Mermaid, migration parity | Không chạy trong lượt docs-only; trạng thái BLOCKED, không suy từ code/config |

## Boundary probes và adversarial cases

Các prompt sau được review thủ công về routing; không phải log gọi mô hình độc lập:

| Prompt kiểm thử | Skill kỳ vọng / hành vi |
|---|---|
| “Tại sao nhóm cần web demo và ai hưởng lợi?” | BRD; business outcome, không đi thẳng vào framework |
| “Từ BR-01 mô tả Given/When/Then, failure và concurrent visits.” | FRD; không tự chọn key/endpoint |
| “Viết schema HTTP cho hai probe từ route handlers.” | API; không sửa controllers |
| “Vẽ topology, giải thích Redis nằm đâu và NFR nào được đáp ứng.” | Architecture; tách config khỏi live |
| “TTL và persistence của bộ đếm là gì?” | Data; TBD/Q-05 vì không có quyết định/implementation |
| “Lập cutover Express sang Laravel ngay.” | Migration; source/target authority thiếu → BLOCKED; không coi Next là Express |
| “Tính KPI/SQL cho lượt xem.” | Ngoài phạm vi sáu skills; không tự chọn FRD chỉ vì có từ requirement |
| “Sửa Dockerfile để readiness kiểm tra Redis.” | Ngoài phạm vi docs-only; ghi đề xuất, không sửa application/infra |

## Phương pháp và giới hạn

Đây là kiểm thử áp dụng có hướng dẫn, tuần tự trong cùng context và tự review bằng agent đã tạo output; không phải blind eval hay reviewer độc lập. Raw JSON của source/hash/checker được giữ; catalog và prompt execution là bản ghi có provenance của agent, không giả là terminal transcript hoặc trace từ registry API.

[OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) mô tả catalog metadata và cách gọi skill. [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) được đối chiếu để tách invocation, routing và artifact checks. Cách giới hạn/chấm ở trên là thiết kế kiểm thử của lượt này, không phải chứng nhận chính thức của OpenAI.
