# Data contract thử nghiệm — probes và counter gap

> SANDBOX. Áp dụng `data-contract-design`; không thiết lập Redis schema/key/TTL chính thức.

| Document ID | Version | Status | Date | Owner role | Sources | Upstream versions |
|---|---|---|---|---|---|---|
| TEST-DATA | 0.1.0 | draft | 2026-11-05 | Web Dev + Platform; approval Q-01 | E-05/E-06/E-08/E-09; evidence registry | TEST-FRD, TEST-API, TEST-ARCH đều 0.1.0 |

Change log 0.1.0: map mọi field của hai reports transient; giữ ENT-03 candidate chưa có storage decisions. Schema wire canonical là [API 0.1.0](api-contract.yaml), không tạo schema cạnh tranh ở đây.

## Entities, identity và relationships

| Entity | Meaning / grain / identity | FR / RULE source | Relationships / integrity / deletion | Source of truth | Writer / reader / owner |
|---|---|---|---|---|---|
| ENT-01 | HealthReport, một report cho mỗi lần handler thực thi; không durable ID | FR-02 / RULE-02 / E-05 | Không foreign key hoặc delete nghiệp vụ; không quan hệ với counter | Handler literal + process clock/uptime | Next handler / operational consumer / Web Dev |
| ENT-02 | ReadinessReport, một report cho mỗi lần handler thực thi; không durable ID | FR-03 / RULE-03 / E-06 | Không persisted state machine; không biểu thị Redis readiness | Handler literal + process clock | Next handler / operational consumer / Web Dev |
| ENT-03 | Candidate visit counter, grain/identity/scope TBD Q-02 | FR-01 / RULE-01 / E-01/E-02 | Initial/update/delete/reset/uniqueness TBD Q-02/Q-05 | Redis intended; chưa chốt authoritative hay cache | Writer/reader component boundary TBD Q-04; owner Web/Platform proposed |

Không suy danh tính visitor, IP/session/user table hoặc events từ chữ “counter”. FR-04 metric model chưa được định nghĩa; không tạo bảng analytics hoặc event store.

## Field dictionary và API mapping

Các kiểu/required/null/enums/ranges/time format lấy nguyên canonical pointers của API version 0.1.0. Những ràng buộc local dưới đây mô tả nguồn/đơn vị/lifecycle, không thay đổi wire definitions. Không field nào trong hai reports được lưu ở Redis theo source được đọc.

| Entity | Schema | Field | Source | Serialization | Lifecycle |
|---|---|---|---|---|---|
| ENT-01 | HealthReport | status | Handler literal ok; E-05 | Identity mapping; theo #/components/schemas/HealthReport/properties/status | transient |
| ENT-01 | HealthReport | uptime | process.uptime(); E-05 | Số giây process, có thể fractional; theo #/components/schemas/HealthReport/properties/uptime | derived/transient |
| ENT-01 | HealthReport | timestamp | new Date().toISOString(); E-05 | UTC ISO string; theo #/components/schemas/HealthReport/properties/timestamp | transient |
| ENT-02 | ReadinessReport | status | Handler literal ready; E-06 | Identity mapping; theo #/components/schemas/ReadinessReport/properties/status | transient |
| ENT-02 | ReadinessReport | timestamp | new Date().toISOString(); E-06 | UTC ISO string; theo #/components/schemas/ReadinessReport/properties/timestamp | transient |

`getHealth` → HealthReport → ENT-01 → RULE-02 / AC-03/04. `getReadiness` → ReadinessReport → ENT-02 → RULE-03 / AC-05/06. Required fields đều có nguồn tạo tại handler, không có null/default fallback trong code. Uptime không phải field đếm view và có thể reset khi process restart. Timestamp là response creation time, không phải retained event/cursor và không cần monotonic/equality across replicas.

## Access patterns

| Operation / FR | Read/write | Identity / order / cardinality | Atomic boundary / mechanism | Retry/concurrency/failure |
|---|---|---|---|---|
| getHealth / FR-02 | Đọc process/time; không storage write | Report singleton theo invocation, không pagination/index | Tạo object trong handler; không transaction nhiều fields với Redis | Retry tạo time/uptime mới, không increment counter |
| getReadiness / FR-03 | Đọc time; không storage read/write | Tương tự, không lịch sử | Handler không check dependency | Concurrent reads độc lập; không hứa Redis failure response |
| Counter / FR-01 | Reads/writes TBD Q-02/Q-04 | Counter scope/key cardinality/order TBD | Chưa chọn mechanism; Redis atomic increment chỉ là một option, chưa code/decision | Lost updates/duplicate retry/partial-write handling TBD Q-02/Q-05 |

## Redis mapping — configured service, contract chưa chốt

| Entity | Key pattern / escaping | Redis type / contents | Role | Readers/writers | TTL value/unit | Start/reset | Missing/expired | Atomicity/recovery |
|---|---|---|---|---|---|---|---|---|
| ENT-03 candidate | TBD Q-05; không đặt visits hoặc prefix giả | TBD Q-05 | Intended counter store; authoritative/cache chưa chốt | TBD Q-04 | TBD Q-05, **không phải null/no expiry** | TBD | TBD Q-02/Q-05; không tự coi missing là 0 | TBD; không có implementation proof |
| ENT-01/02 | N/A, không persisted | N/A | Transient reports, không Redis cache theo source | Next handler only | N/A vì không Redis key | N/A | N/A | Không có Redis dependency |

E-08/E-09 chỉ chứng minh service/env/configured deployment. Chưa thấy key command/client/persistence config trong code được pin. Không đủ cơ sở tuyên bố multi-key atomicity, slot constraints, reset TTL hoặc no-expiry. Null TTL có nghĩa no expiry khi được quyết định; unknown vẫn là TBD. Không đổi unknown thành 60/3600 giây theo template hoặc kinh nghiệm.

## Lifecycle, consistency và recovery

| Entity | Lifecycle / invariant | Concurrency/visibility | Persistence/eviction/backup/restore | NFR / verification gap |
|---|---|---|---|---|
| ENT-01/02 | Tạo report tại request; không create/update/delete durable entities | Time giữa replicas có thể khác; không yêu cầu equality giữa hai lần request | App không lưu reports trong inspected handlers; retention log/proxy nằm ngoài slice, chưa xác minh | FR-02/03; API shape check và runtime HTTP còn chưa chạy |
| ENT-03 | TBD theo RULE-01 Q-02/Q-05 | Definition global/unique/page count, retries và visibility TBD | Redis manifest không có volume/PVC; không cam kết dataset survive pod/node replacement | NFR-02, CTL-02 BLOCKED; cần concurrency/restart/recovery evidence |

Event replay/SSE N/A: không có yêu cầu/retained event model. Không dùng Pub/Sub như durable history hoặc promise replay từ counters. Probe response không là event envelope.

## Classification và evolution

ENT-01/02 chứa thông tin vận hành process/time, không thấy user identity trong schema; mức nhạy cảm và perimeter access policy vẫn cần nhóm xác định Q-04. Không tự thêm tracking ID/PII. ENT-03 sensitivity phụ thuộc cách đếm Q-02; không suy GDPR hoặc nghĩa vụ pháp lý từ stack khi không có nguồn.

Schema/version 0.1.0 là version tài liệu thử nghiệm. Thêm/bỏ required field, đổi enum/type/time encoding là compatibility impact cần API owner review. Nếu thay backend, giữ field meaning/ranges/time format; uptime/time thực tế không cần bằng byte-for-byte. Không có data transform đã chốt hoặc rollback data boundary được chứng minh. Dual writes không được đề xuất khi chưa biết writers/identity; trước migration cần kiểm tra compatibility readers/writers/TTL và recovery theo MIG gates.

Evidence/A/Q canonical tại [registry](../evidence-register.md). A-02 giới hạn slice; Q-02/Q-04/Q-05 chặn ENT-03 baseline; C-02 ngăn đồng nhất report ready với Redis; C-05 ngăn durability claim. Risk owner: Web/Platform; thay đổi rule phải bắt đầu tại FRD, wire tại API, mapping/lifecycle tại Data.

## Validation

| Finding | Check / severity | Locations + versions / IDs | Expected vs observed | Impact | Correction / owner | Result |
|---|---|---|---|---|---|---|
| VAL-13 | Wire-field mapping / major | API/Data0.1.0, ENT-01/02 | Đủ 5 field mappings, sources transient phù hợp code, không schema drift | Chỉ probe slice đủ nguồn | Giữ canonical API definitions / Web | PASS trong slice |
| VAL-14 | TTL/lifecycle/atomicity / major | FR-01, ENT-03, RULE-01, NFR-02 | Key/TTL/definition/concurrency chưa chốt | Không thể cam kết counter hoặc storage parity | Resolve Q-02/Q-05 / Web + Platform | BLOCKED |
| VAL-15 | Architecture/migration recovery / major | CTL-02, MIG-03/04, Data0.1.0 | Không durable recovery proof hoặc baseline Express | Cutover chưa có recovery/compatibility gate đạt | Thu baseline/tests sau review / Web + Platform | BLOCKED |
