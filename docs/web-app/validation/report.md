# Báo cáo kiểm thử BA Documentation Skills

| Document ID | Version | Status | Date | Owner role | Sources | Upstream |
|---|---|---|---|---|---|---|
| TEST-REPORT | 0.1.0 | draft | 2026-11-05 | Codex thực hiện; người dùng review | E-01..E-14; yêu cầu phiên hiện tại | Project `2110edd`; skill bundle `3f0127b`; sáu smoke docs 0.1.0 |

Change log 0.1.0: ghi kết quả guided smoke test; chỉ tài liệu validation. Tài liệu giữ trạng thái draft và không phải chứng nhận độc lập hoặc approval cho official BA.

## Kết luận trong phạm vi test

Nhánh `ba/documentation` tạo từ `origin/main` đã fetch, tại `2110eddec91bc3e34137c86fef693095c4afb677`. Working tree ban đầu sạch, nhánh chưa tồn tại trong danh sách được kiểm tra; không có overwrite/reset/stash/rebase. Các tài liệu thử nghiệm ở riêng `docs/web-app/validation/`; file baseline được giữ nguyên. Không commit/push/merge trong lượt này.

**PASS**: runtime catalog của phiên có đủ sáu BA Skills trước khi đọc manifests; sáu workflow được áp dụng có hướng dẫn, tuần tự từ BRD, tạo draft có evidence/gaps. **FAIL**: baseline README/WBS/source/config còn lệch hoặc thiếu rõ vai trò component, namespace, Node version và GitOps source mode. **BLOCKED**: chưa thể tuyên bố bộ BA đầy đủ/baseline-ready, blind skill routing, runtime feature readiness hoặc migration readiness.

Đây là kết quả của nhiều đối tượng khác nhau. Source inconsistency FAIL không tự quy thành lỗi Skill; Skill xử lý thiếu đầu vào đúng không làm sản phẩm hoặc migration PASS. Cần người dùng review trước mọi bước tài liệu chính thức.

## Bằng chứng nhận diện và provenance

[runtime-discovery.json](runtime-discovery.json) chép đúng sáu tên/mô tả/path từ **Available skills catalog do runtime đưa vào context phiên**, khác với filesystem scan hoặc đọc SKILL.md. PASS chỉ cho discovery ở phiên này. Không có raw registry API export hoặc chụp UI `/skills`; bản chép có nhãn provenance rõ. Không có fresh-session explicit invocation hoặc blind implicit selection eval; hai hạng mục này BLOCKED/chưa chạy.

Bundle local có remote `https://github.com/Nobita534/BA-skill-documentation.git`, pin `3f0127b33bc6612f743c1aec4862079eea3adb9e`. Các file dưới `skills/` khớp HEAD; repo bundle có thay đổi sẵn ngoài đó và được giữ nguyên. Không xác nhận đây là remote bundle mới nhất. Không lấy notes, patch/PR riêng hoặc báo cáo cũ của bundle làm kết quả test mới hay authority sản phẩm.

## Kết quả từng Skill

| Thứ tự / Skill | Discovery ở phiên | Guided application | Evidence / actual content checked | Giới hạn tài liệu |
|---|---|---|---|---|
| 1. brd-authoring | PASS E-12 | PASS trong smoke | [BRD](smoke/BRD.md): outcome trước stack; BR-01..03 có sources, success evidence, scope/proposed; BR-03 là non-software outcome | Authority/rubric/targets thiếu Q-01; full baseline BLOCKED |
| 2. frd-authoring | PASS E-12 | PASS trong smoke | [FRD](smoke/FRD.md): valid parents, RULE/AC/NFR; current probes khác target; counter/metrics failure/concurrency gaps giữ visible | AC-01/02/07/08 và NFR targets chưa đầy đủ, BLOCKED |
| 3. api-contract-design | PASS E-12 | PASS cho partial draft | [API](smoke/api-contract.yaml): hai operations có x-fr-ids, 200/schema/time code-aligned; không bịa counter/error/auth/SSE | Full API/OAS-aware validation/access policy/runtime BLOCKED |
| 4. architecture-design | PASS E-12 | PASS cho evidence separation | [Architecture](smoke/architecture.md): current/planned diagrams, NFR controls/gaps, source/config/live boundaries; Redis namespace có offline render | Full NFR achievement/live/diagram render BLOCKED; baseline namespace agreement FAIL |
| 5. data-contract-design | PASS E-12 | PASS cho bounded mapping | [Data](smoke/data-contract.md): đủ 5 transient probe fields; API là canonical; counter key/TTL/lifecycle không bị fabricate | ENT-03 consistency/recovery/TTL BLOCKED |
| 6. backend-migration-planning | PASS E-12 | PAS`S về handling missing inputs | [Migration](smoke/migration-plan.md): không nhầm Next thành Express; source/target/gates/parity/post-write rollback limits rõ | Plan completeness, implementation/parity và cutover readiness đều BLOCKED |

[execution-log.json](execution-log.json) ghi sequence, upstream/output hashes và recording times. Đây là agent-authored record về việc áp dụng trong cùng phiên; không là independent model invocation trace. [test-plan.md](test-plan.md) lưu các prompts áp dụng và expected behavior trước outputs; trigger/boundary prompts chỉ được review thủ công.

## Các checks đã chạy

| Check | Result | Evidence / limits |
|---|---|---|
| Bundle checker chạy lại bằng Bun 1.4.3 | 22 PASS, 0 FAIL | [bundle-results.json](bundle-results.json); bundle/Queue Board fixtures, không là test app NT548 |
| Tài liệu NT548: controls/links/Git scope/sequence/trace/source-schema/examples/mutations | 28 PASS, 0 FAIL, 6 BLOCKED | [document-checks.json](document-checks.json); có 11 mutation cases và 5 invalid samples được phát hiện; không general semantic/OAS certification |
| Kustomize offline render | PASS về evidence cấu hình | [kustomize-render.yaml](kustomize-render.yaml): 7 resources cùng production-app, không gọi API server/apply |
| Manual cross-document review | PASS probe slice; full coverage BLOCKED | [traceability.md](traceability.md); cùng agent tự review, không reviewer độc lập |
| Fresh-session invocation / blind routing | BLOCKED, chưa chạy | Không dùng guided invocation hoặc file read làm PASS |
| Full OpenAPI-aware validation | BLOCKED, chưa chạy | Default Python thiếu yaml/jsonschema/openapi_spec_validator; đã dùng Bun parse + targeted subset checks |
| Mermaid render / HTTP / Redis / load / cluster / migration parity | BLOCKED, chưa chạy | Không suy kết quả từ source, manifests hoặc fixtures |

Lượt QA đầu có **26 PASS, 2 FAIL, 6 BLOCKED**, giữ nguyên ở [document-checks.initial.json](document-checks.initial.json). Hai lỗi artifact: Architecture thiếu heading Validation tường minh dù có bảng findings; Migration viết gọn AC/ENT IDs khiến inventory khó tra cứu. Đã bổ sung heading và viết đầy đủ IDs trong cùng initial draft 0.1.0, rồi chạy lại đạt kết quả ở trên. [Execution log](execution-log.json) giữ hashes lúc tạo và hai review revisions; không xóa lịch sử FAIL hoặc đổi yêu cầu kỹ thuật để qua test. Đây là sửa output thử nghiệm, không sửa Skill bundle.

## Vai trò stack và source findings

Next.js là implementation quan sát được trong `app/`: frontend starter và hai route probes. Express Backend/API là intent trong README; chưa thấy entry/package/router trong snapshot được pin. Redis có manifests/service/env, chưa có app client hoặc counter integration quan sát được. Có thể dùng đồng thời Next frontend + Express backend + Redis; Next source không chứng minh Express đã bị thay thế. Target boundary và backend location vẫn Q-04.

| Finding / result | Evidence / implication | Đề xuất / owner |
|---|---|---|
| C-01 FAIL, source role/version wording chưa nhất quán | README Express/Node24 vs WBS/README-tree Next; source chỉ chứng minh Next | Tách intended roles/as-observed và link backend ref thật / Web + Documentation |
| C-02 evidence gap; Redis-ready claim FAIL nếu có | `/ready` chỉ ready/200, không kiểm tra Redis | Chốt Q-03 rồi review FRD/API/Architecture/consumer impacts; không sửa handler trong lượt này |
| C-03/C-05 BLOCKED | Counter/metrics/client/TTL/persistence/concurrency chưa có evidence | Chốt Q-02/Q-05/Q-07; giữ draft, không cam kết no expiry/durable/exactly-once |
| C-04 FAIL, namespace claim | README namespace database vs offline render production-app | Sửa mô tả hoặc quyết định kiến trúc tại owner sau review; không đổi manifests |
| C-06/C-07 FAIL, docs/config agreement | README directory recurse/Node24; Kustomize config và Next Dockerfile node26 string | Cập nhật source-aware wording theo component; runtime/build vẫn cần test |
| C-08 BLOCKED verification | WBS future dates có complete status nhưng chưa có log bằng chứng | Tách planned/actual date và đính evidence completion; không suy trạng thái triển khai từ lịch |

Location/IDs/severity/expected-vs-observed/impact/correction/owner đầy đủ tại [evidence-register.md](evidence-register.md). Các finding được giữ lại; baseline README/WBS không bị sửa để làm kết quả đẹp hơn.

## Đề xuất cải thiện bộ Skills và lần kiểm thử tiếp theo

1. Giữ quy tắc evidence/scope/commitment/implementation độc lập của shared standard; chúng giúp lộ gaps thay vì tạo fact từ templates. Bundle hiện chưa thấy lỗi cấu trúc trong checks đã chạy.
2. Thêm automated fresh-session trigger eval cho mỗi Skill: explicit invocation, natural-language positive prompts và negative/boundary prompts. Lưu selected skill/trace/output với runtime/version pin; không chỉ kiểm tra file tồn tại.
3. Thêm fixture riêng cho Next frontend + Express backend intended nhưng source thiếu, Redis configured nhưng chưa client; assert Skill không coi Next là backend replacement, không gọi `/ready` là Redis-ready, không bịa counter keys/TTL.
4. Thêm OpenAPI-aware validator và JSON Schema validator đầy đủ trong môi trường test, rồi xác minh examples/status/required/null/time. Giữ targeted mutations và bổ sung semantic regressions từ các findings thực tế; không biến checker keyword thành semantic certification.
5. Thêm migration missing-input fixture có target TBD/source mismatch/post-cutover writes, phân biệt plan completeness với cutover readiness. Có thể thêm nhánh template “partial discovery response” để người đọc không hiểu bảng gates là runnable runbook.
6. Đóng gói `_ba-shared` cùng sáu folders, pin/hash bundle và ghi trạng thái dirty của context ngoài skills. Sau khi resolved nguồn, review ngữ nghĩa độc lập và render diagrams trước official baseline.

Các mục trên là **đề xuất**, chưa chỉnh sửa global Skill bundle. Câu hỏi cần trước tài liệu chính thức: authority/rubric Q-01; counter semantics Q-02; ready criteria Q-03; Express/component ownership Q-04; Data lifecycle Q-05; migration intent Q-06 nếu thực sự cần; NFR/metrics targets Q-07.

## Điểm dừng

Hoàn tất phạm vi test/sandbox và để người dùng review. Chưa tạo/thay bộ BA chính thức; chưa sửa application code, Dockerfile, CI/CD, Kubernetes manifests; chưa merge vào main. Những BLOCKED ở đây được giao lại như prerequisites, không tự triển khai để đóng finding trong nhiệm vụ docs-only.
