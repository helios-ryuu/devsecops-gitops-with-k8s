# BÁO CÁO ĐỒ ÁN MÔN HỌC NT548

> Tài liệu này chứa toàn bộ nội dung hoàn chỉnh kèm vị trí chèn hình ảnh, bảng biểu và hướng dẫn chụp ảnh minh họa để người dùng rà soát và đưa trực tiếp vào tệp báo cáo Word trên WPS Writer.

---

## TRANG BÌA

ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH
TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN
KHOA MẠNG MÁY TÍNH VÀ TRUYỀN THÔNG

**BÁO CÁO ĐỒ ÁN MÔN HỌC**

**MÔN HỌC: CÔNG NGHỆ DEVOPS VÀ ỨNG DỤNG (NT548)**

**ĐỀ TÀI:**
**XÂY DỰNG HỆ THỐNG DEVSECOPS VÀ GITOPS TỰ ĐỘNG HÓA TRIỂN KHAI, BẢO MẬT VÀ GIÁM SÁT ỨNG DỤNG TRÊN HẠ TẦNG KUBERNETES HYBRID**

- **Giảng viên hướng dẫn:** ThS. Lê Anh Tuấn *(Lưu ý: kiểm tra và điều chỉnh lại học vị của Thầy nếu cần)*
- **Lớp:** NT548.R12 (Học kỳ 1, năm học 2026-2027)
- **Nhóm thực hiện:** Nhóm 6
  - Ngô Tiến Sỹ (MSSV: 23521367)
  - Trần Hồng Phúc (MSSV: 23521222)
  - Điền Quốc Huy (MSSV: 23520600)
  - Đặng Thế Long (MSSV: 22520804)

TP. HỒ CHÍ MINH, NĂM 2026

---

## NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN

........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................
........................................................................................................................................

TP.HCM, ngày ... tháng ... năm 2026

**Giảng viên hướng dẫn**
*(Ký tên và ghi rõ họ tên)*

---

## LỜI CẢM ƠN

Lời đầu tiên, nhóm em xin gửi lời cảm ơn chân thành và sâu sắc đến Thầy Lê Anh Tuấn, giảng viên phụ trách môn Công nghệ DevOps và Ứng dụng, người đã trực tiếp giảng dạy và tận tình đồng hành cùng nhóm trong suốt học kỳ vừa qua. Nhờ sự tâm huyết trong từng bài giảng cùng cách truyền đạt gần gũi, dễ hiểu của Thầy, nhóm em đã có được nền tảng vững chắc để tự tin bắt tay vào nghiên cứu và thực hiện đồ án môn học này.

Trong suốt quá trình lên ý tưởng, triển khai và hoàn thiện đồ án, nhóm em đã gặp không ít khó khăn và vướng mắc. Tuy nhiên, nhờ những định hướng kịp thời, sự giải đáp tận tình cùng những lời khuyên và góp ý chân thành từ Thầy, nhóm em đã dần tháo gỡ được các vấn đề, khắc phục những hạn chế và từng bước hoàn thành đồ án cũng như báo cáo một cách suôn sẻ.

Thông qua quá trình học tập và thực hiện đồ án dưới sự hướng dẫn của Thầy, nhóm em không chỉ củng cố thêm nhiều kiến thức bổ ích mà còn rèn luyện được tư duy giải quyết vấn đề, tinh thần chủ động tìm tòi và kỹ năng làm việc nhóm hiệu quả hơn. Đây đều là những trải nghiệm và hành trang hết sức quý giá, giúp từng thành viên trong nhóm trưởng thành hơn cho chặng đường học tập cũng như công việc sau này.

Mặc dù cả nhóm đã nỗ lực hết mình và đầu tư nghiêm túc, nhưng do kiến thức cũng như kinh nghiệm thực tế vẫn còn nhiều hạn chế, đồ án và báo cáo này khó tránh khỏi những điểm thiếu sót, bất cập. Vì vậy, nhóm em rất mong nhận được những nhận xét, đánh giá và góp ý quý báu từ Thầy để nhóm có thể rút kinh nghiệm và hoàn thiện hơn trong thời gian tới.

Nhóm em xin kính chúc Thầy luôn dồi dào sức khỏe, hạnh phúc và gặt hái được nhiều thành công trong sự nghiệp giảng dạy. Nhóm em xin chân thành cảm ơn Thầy!

**Nhóm sinh viên thực hiện**

---

## MỤC LỤC

> *Ghi chú cho WPS Writer: Khi đưa nội dung vào Word, dùng chức năng References -> Table of Contents để sinh số trang tự động dựa trên các Heading dưới đây.*

- LỜI CẢM ƠN
- DANH MỤC BẢNG
- DANH MỤC HÌNH ẢNH
- TỪ NGỮ VIẾT TẮT VÀ THUẬT NGỮ
- **CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI**
  - 1.1. Đặt vấn đề và lý do chọn đề tài
  - 1.2. Mục tiêu và phạm vi thực hiện
  - 1.3. Tổ chức nhóm và tiến trình thực hiện
- **CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG**
  - 2.1. Phương pháp luận vận hành hiện đại
  - 2.2. Ảo hóa container và điều phối Kubernetes
  - 2.3. Hạ tầng mạng, cổng biên và lưu trữ phân tán
  - 2.4. Tự động hóa CI/CD, quản lý bí mật và chính sách bảo mật
  - 2.5. Hệ thống quan sát và ngăn xếp ứng dụng mẫu
- **CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ KIẾN TRÚC HỆ THỐNG**
  - 3.1. Mô hình kiến trúc hai tầng tách biệt
  - 3.2. Thiết kế hạ tầng lai và hai ranh giới mạng
  - 3.3. Thiết kế bảo mật đa lớp theo chiều sâu
  - 3.4. Thiết kế ứng dụng mẫu và đường ống CI/CD GitOps
  - 3.5. Quy hoạch hạ tầng, ngân sách tài nguyên và đánh đổi thiết kế
- **CHƯƠNG 4: TRIỂN KHAI VÀ KIỂM THỬ HỆ THỐNG**
  - 4.1. Dựng nền tảng mạng WireGuard và cụm Kubernetes Hybrid
  - 4.2. Triển khai các dịch vụ nền tảng cốt lõi (Tầng 1)
  - 4.3. Đóng gói ứng dụng mẫu, kích hoạt CI/CD và triển khai Tầng 2
  - 4.4. Kiểm thử hệ thống qua 6 kịch bản thực nghiệm
    - 4.4.1. Kịch bản 1: Kiểm chứng cổng bảo mật CI DevSecOps
    - 4.4.2. Kịch bản 2: Kiểm chứng lớp chặn Kyverno tại tầng tiếp nhận Kubernetes
    - 4.4.3. Kịch bản 3: Kiểm chứng phát hành liên tục RollingUpdate không gián đoạn và hoàn tác qua Git
    - 4.4.4. Kịch bản 4: Kiểm chứng cô lập mạng Redis và quan sát luồng bị chặn trên Hubble UI
    - 4.4.5. Kịch bản 5: Kiểm chứng quét CVE ban đêm, chịu lỗi Traefik HA và chuyển đổi dự phòng Longhorn
    - 4.4.6. Kịch bản 6: Kiểm chứng phục hồi HashiCorp Vault sau eviction và đồng bộ ESO
  - 4.5. Kết quả quan sát và đánh giá vận hành hệ thống
- **CHƯƠNG 5: TỔNG KẾT**
  - 5.1. Kết quả đạt được
  - 5.2. Hạn chế của đồ án
  - 5.3. Hướng phát triển trong tương lai
- TÀI LIỆU THAM KHẢO

---

## DANH MỤC BẢNG

- Bảng 0.1: Bảng từ ngữ viết tắt và thuật ngữ
- Bảng 1.1: Phân công nhiệm vụ các thành viên Nhóm 6
- Bảng 3.1: Tổng hợp quy hoạch hạ tầng, địa chỉ mạng và tên miền hệ thống

---

## DANH MỤC HÌNH ẢNH

- Hình 2.1: Logo nền tảng đóng gói container Docker
- Hình 2.2: Logo hệ thống điều phối container Kubernetes
- Hình 2.3: Logo giao thức mạng riêng ảo WireGuard
- Hình 2.4: Logo hệ thống mạng và bảo mật Cilium eBPF
- Hình 2.5: Logo bộ định tuyến biên Traefik và lưu trữ phân tán Longhorn
- Hình 2.6: Logo nền tảng GitOps ArgoCD
- Hình 2.7: Logo hệ thống quản lý bí mật HashiCorp Vault và chính sách Kyverno
- Hình 2.8: Logo bộ công cụ giám sát Prometheus và Grafana
- Hình 3.1: Sơ đồ kiến trúc tổng thể hệ thống DevSecOps và GitOps trên Kubernetes Hybrid
- Hình 3.2: Sơ đồ luồng đường ống CI/CD DevSecOps, GitOps ArgoCD và quét CVE định kỳ ban đêm
- Hình 4.1: Kết quả kiểm tra thông mạng WireGuard wg0 và độ trễ LAN trực tiếp giữa hai nodes Worker
- Hình 4.2: Trạng thái cụm Kubernetes v1.37.1 với ba nodes Ready và Cilium eBPF hoạt động ổn định
- Hình 4.3: Giao diện Longhorn UI xác nhận hai nodes Worker và dung lượng lưu trữ phân tán
- Hình 4.4: Trạng thái HashiCorp Vault đã mở khóa và các ExternalSecret đồng bộ thành công qua ESO
- Hình 4.5: Trạng thái triển khai Traefik HA hai bản sao nhận địa chỉ External IP từ Cilium LoadBalancer
- Hình 4.6: Danh sách bốn ValidatingPolicy của Kyverno và các ServiceMonitor giám sát toàn cụm
- Hình 4.7: Kết quả chạy thành công quy trình CI & DevSecOps Gate trên GitHub Actions
- Hình 4.8: Trạng thái đồng bộ ứng dụng app-prod ở mức Synced và Healthy trên giao diện ArgoCD
- Hình 4.9: Giao diện ứng dụng mẫu Web Next.js tích hợp bộ đếm Redis và lớp xác thực Cloudflare Zero Trust
- Hình 4.10: Giao diện hướng dẫn kiểm thử hệ thống từ script scripts/test.sh
- Hình 4.11: Kịch bản 1, đường ống GitHub Actions chặn thành công commit chứa thư viện có lỗ hổng CVE
- Hình 4.12: Kịch bản 2, Kubernetes API Server từ chối tạo Pod vi phạm chính sách Kyverno
- Hình 4.13: Kịch bản 3, quá trình cập nhật RollingUpdate không gián đoạn và hoàn tác nhanh bằng Git
- Hình 4.14: Kịch bản 4, kết nối trái phép từ Pod lạ tới Redis bị chặn ở tầng mạng
- Hình 4.15: Kịch bản 4, luồng gói tin bị chặn (DROPPED) hiển thị trực quan trên giao diện Hubble UI
- Hình 4.16: Kịch bản 5, kết quả chạy quy trình quét CVE ban đêm, xóa nóng Pod Traefik và chuyển đổi dự phòng Redis trên Longhorn
- Hình 4.17: Kịch bản 6, mở khóa HashiCorp Vault sau khi chuyển node và xác nhận ESO đồng bộ thành công
- Hình 4.18: Bảng điều khiển Grafana theo dõi mức sử dụng CPU, RAM và lưu lượng của ba nodes trong cụm
- Hình 4.19: Kết quả quét cổng mạng biên bằng nmap xác nhận chỉ mở các cổng dịch vụ cần thiết

---

## TỪ NGỮ VIẾT TẮT VÀ THUẬT NGỮ

*Bảng 0.1: Bảng từ ngữ viết tắt và thuật ngữ*

| STT | Từ ngữ, thuật ngữ | Ý nghĩa |
| :---: | :--- | :--- |
| 1 | API | Application Programming Interface (Giao diện lập trình ứng dụng) |
| 2 | CEL | Common Expression Language (Ngôn ngữ biểu thức viết luật kiểm tra nhanh trong Kubernetes) |
| 3 | CI/CD | Continuous Integration / Continuous Delivery (Tích hợp liên tục và Phân phối liên tục) |
| 4 | CNI | Container Network Interface (Giao diện chuẩn kết nối mạng cho container trong Kubernetes) |
| 5 | CVE | Common Vulnerabilities and Exposures (Danh mục lỗ hổng bảo mật đã công bố) |
| 6 | DevOps | Development and Operations (Kết hợp phát triển phần mềm và vận hành hệ thống) |
| 7 | DevSecOps | Development, Security and Operations (Tích hợp bảo mật xuyên suốt vòng đời phát triển và vận hành) |
| 8 | DNS | Domain Name System (Hệ thống phân giải tên miền) |
| 9 | eBPF | Extended Berkeley Packet Filter (Công nghệ chạy chương trình an toàn trong nhân Linux để xử lý mạng và quan sát) |
| 10 | ESO | External Secrets Operator (Thành phần đồng bộ bí mật từ kho ngoài vào Kubernetes) |
| 11 | GHCR | GitHub Container Registry (Kho lưu trữ container image của GitHub) |
| 12 | GitOps | Mô hình lấy kho mã nguồn Git làm nguồn trạng thái chuẩn duy nhất để đồng bộ hạ tầng |
| 13 | HA | High Availability (Tính sẵn sàng cao, hạn chế gián đoạn khi có sự cố) |
| 14 | HTTP/HTTPS | HyperText Transfer Protocol / Secure (Giao thức truyền tải siêu văn bản và bản bảo mật TLS) |
| 15 | MTU | Maximum Transmission Unit (Kích thước gói tin tối đa qua một giao diện mạng) |
| 16 | NAT | Network Address Translation (Chuyển đổi địa chỉ IP giữa mạng nội bộ và mạng ngoài) |
| 17 | NSG | Network Security Group (Tường lửa ở tầng hạ tầng đám mây) |
| 18 | PVC | PersistentVolumeClaim (Yêu cầu cấp phát lưu trữ bền vững trong Kubernetes) |
| 19 | RBAC | Role-Based Access Control (Kiểm soát truy cập dựa trên vai trò) |
| 20 | RPO | Recovery Point Objective (Mức dữ liệu tối đa chấp nhận mất khi gặp sự cố) |
| 21 | RWO | ReadWriteOnce (Chế độ gắn ổ đĩa cho phép đọc ghi trên một node tại một thời điểm) |
| 22 | SPOF | Single Point of Failure (Điểm lỗi đơn có thể gây gián đoạn nếu gặp sự cố) |
| 23 | SSH | Secure Shell (Giao thức điều khiển máy chủ từ xa có mã hóa) |
| 24 | TLS | Transport Layer Security (Giao thức mã hóa đường truyền mạng) |
| 25 | VPN | Virtual Private Network (Mạng riêng ảo kết nối an toàn qua Internet) |
| 26 | VXLAN | Virtual Extensible LAN (Kỹ thuật đóng gói tạo mạng phủ ảo cho cụm máy chủ) |
| 27 | YAML | YAML Ain't Markup Language (Định dạng văn bản có cấu trúc dùng viết cấu hình) |

---

# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI

## 1.1. Đặt vấn đề và lý do chọn đề tài

Trong cách làm phần mềm truyền thống, lập trình và vận hành thường tách biệt nhau. Mã nguồn sau khi viết xong được bàn giao để cài đặt thủ công lên máy chủ, dễ dẫn đến lỗi sai khác môi trường, khó kiểm soát lịch sử thay đổi và tốn thời gian khôi phục khi bản cập nhật gặp trục trặc. Song song đó, nếu chỉ kiểm tra bảo mật ở giai đoạn cuối trước khi phát hành, những rủi ro phổ biến như vô tình để lộ mật khẩu trong Git, dùng thư viện chứa lỗ hổng nghiêm trọng hay chạy container bằng quyền quản trị cao nhất sẽ rất tốn công xử lý lại.

Bên cạnh yếu tố kỹ thuật, chi phí hạ tầng cũng là bài toán thực tế với sinh viên và các nhóm nhỏ. Nếu thuê toàn bộ cụm máy chủ đủ mạnh trên đám mây để chạy trọn vẹn hệ thống điều phối, lưu trữ phân tán, quản lý bí mật và giám sát, chi phí duy trì sẽ khá cao. Ngược lại, nếu chỉ đặt máy chủ trong mạng gia đình, hệ thống lại thiếu địa chỉ IP công cộng ổn định để tiếp nhận truy cập an toàn từ Internet.

Xuất phát từ nhu cầu đó, nhóm chọn giải pháp **Kubernetes Hybrid** kết hợp một máy chủ ảo đám mây (VPS) có IP công cộng làm node điều khiển và tiếp nhận lưu lượng biên, ghép nối với hai máy tính vật lý tại mạng nội bộ gia đình (On-Premises) có tài nguyên RAM và đĩa lớn hơn để chạy dịch vụ nền và ứng dụng. Trên hạ tầng lai này, nhóm áp dụng trọn vẹn quy trình **DevSecOps** (kiểm tra bảo mật từ lúc viết mã đến khi vận hành) cùng **GitOps** (đồng bộ tự động từ kho Git), vừa tối ưu chi phí vừa bảo đảm an toàn và tính sẵn sàng cho hệ thống.

## 1.2. Mục tiêu và phạm vi thực hiện

Mục tiêu tổng thể của đồ án là thiết kế, triển khai và kiểm chứng một nền tảng vận hành ứng dụng hoàn chỉnh trên cụm Kubernetes lai ba nodes theo hướng tự động hóa, an toàn nhiều lớp và dễ tái sử dụng. Cụ thể, hệ thống hướng tới bốn mục tiêu chính:

- **Xây dựng hạ tầng lai ổn định:** Kết nối VPS và hai máy tại chỗ qua mạng riêng ảo mã hóa, tối ưu luồng dữ liệu nội bộ đi thẳng qua mạng LAN thay vì đi vòng qua Internet.
- **Tự động hóa kiểm tra và đóng gói an toàn:** Thiết lập quy trình CI quét rò rỉ bí mật, kiểm tra lỗ hổng mã nguồn, rà soát chuẩn tệp cấu hình và quét ảnh container trước khi lưu trữ.
- **Triển khai GitOps không gián đoạn và phòng thủ đa lớp:** Tách riêng hạ tầng nền tảng cố định với ứng dụng đồ án, cập nhật ứng dụng không rớt kết nối và bảo vệ từ lớp biên Internet đến từng tiến trình container.
- **Quan sát trực quan và kiểm chứng thực tế:** Theo dõi tài nguyên, lưu lượng mạng theo thời gian thực và kiểm thử toàn bộ cơ chế bảo vệ, chịu lỗi qua sáu kịch bản cụ thể.

Về phạm vi, đồ án tập trung vào mảng kỹ thuật nền tảng (Platform Engineering), bảo mật và tự động hóa triển khai trên phần cứng gồm một VPS 6 GB RAM và hai máy tại chỗ 8 GB RAM mỗi máy. Nhóm sử dụng một ứng dụng web hai tầng gọn nhẹ (Next.js và Redis) làm đối tượng kiểm chứng xuyên suốt thay cho một phần mềm nghiệp vụ phức tạp. Các cấu hình mở rộng tốn nhiều tài nguyên như cụm Control Plane nhiều nodes hay cụm Redis phân mảnh nhiều bản sao nằm ngoài phạm vi triển khai phần cứng nhưng được phân tích rõ ở phần đánh đổi thiết kế.

## 1.3. Tổ chức nhóm và tiến trình thực hiện

Nhóm 6 gồm bốn thành viên, phân công rõ ràng giữa mảng hạ tầng vận hành, phát triển ứng dụng kiểm chứng, quan sát hệ thống và kiểm thử tổng hợp báo cáo.

*Bảng 1.1: Phân công nhiệm vụ các thành viên Nhóm 6*

| STT | MSSV | Họ và tên | Vai trò và nhiệm vụ chính |
| :---: | :---: | :--- | :--- |
| 1 | 23521367 | Ngô Tiến Sỹ | Trưởng nhóm, phụ trách hạ tầng và DevOps: thiết kế và vận hành mạng WireGuard, cụm Kubernetes Hybrid (`kubeadm`), Cilium eBPF và Hubble UI, Traefik HA, lưu trữ phân tán Longhorn, Vault và ESO, chính sách Kyverno, đồng bộ ArgoCD, hệ thống giám sát Prometheus/Grafana và đường ống GitHub Actions CI/CD. |
| 2 | 23521222 | Trần Hồng Phúc | Phát triển ứng dụng mẫu: xây dựng ứng dụng Web Next.js 16 kết nối Redis đếm lượt truy cập, hiển thị biến môi trường phiên bản, hoàn thiện các điểm kiểm tra sức khỏe (`/healthz`, `/ready`) và đóng gói container chạy quyền không đặc quyền (`UID 10001`). |
| 3 | 23520600 | Điền Quốc Huy | Quan sát hệ thống: khai thác giao diện Grafana và Hubble UI để theo dõi tài nguyên CPU, RAM, lưu lượng Traefik và luồng mạng bị chặn, thu thập ảnh minh chứng trực quan phục vụ báo cáo và bài trình bày. |
| 4 | 22520804 | Đặng Thế Long | Tài liệu và kiểm thử hệ thống: phối hợp chạy bộ sáu kịch bản kiểm thử (`scripts/test.sh`), thu thập nhật ký và ảnh minh chứng, chủ trì biên soạn báo cáo đồ án, vẽ sơ đồ kiến trúc và hoàn thiện slide thuyết trình. |

Đồ án được thực hiện trong sáu tuần (từ 25/10/2026 đến 05/12/2026) qua năm giai đoạn nối tiếp:

- **Giai đoạn 1 (25/10/2026 đến 31/10/2026): Khởi động dự án.** Chốt đề tài, thống nhất bộ công nghệ phù hợp với cấu hình RAM thực tế và phân chia nhiệm vụ cho bốn thành viên.
- **Giai đoạn 2 (01/11/2026 đến 05/11/2026): Phân tích và thiết kế.** Lập bảng phân rã công việc (WBS), thiết kế kiến trúc hai tầng, tổ chức kho mã nguồn Monorepo và quy hoạch địa chỉ mạng.
- **Giai đoạn 3 (06/11/2026 đến 20/11/2026): Triển khai hạ tầng và tích hợp CI/CD.** Dựng mạng WireGuard, cụm Kubernetes `v1.37.1`, cài đặt toàn bộ dịch vụ nền tảng Tầng 1, đóng gói ứng dụng mẫu, xây dựng quy trình GitHub Actions, viết luật Kyverno và kích hoạt ArgoCD.
- **Giai đoạn 4 (21/11/2026 đến 28/11/2026): Giám sát và kiểm thử hệ thống.** Cài đặt bộ giám sát Prometheus/Grafana, chụp ảnh quan sát trên Grafana và Hubble UI, đồng thời thực nghiệm sáu kịch bản kiểm thử qua `scripts/test.sh`.
- **Giai đoạn 5 (26/11/2026 đến 05/12/2026): Hoàn thiện báo cáo và nghiệm thu.** Biên soạn báo cáo hoàn chỉnh, hoàn thiện sơ đồ Draw.io, slide thuyết trình và rà soát tính sẵn sàng của cụm trước ngày 05/12/2026.

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG

Chương này trình bày nền tảng lý thuyết theo năm nhóm từ tư duy vận hành đến công cụ thực thi, giải thích rõ vai trò của từng công nghệ trong bức tranh chung của đồ án.

## 2.1. Phương pháp luận vận hành hiện đại

- **DevOps:** Là phương pháp gắn kết quá trình phát triển phần mềm và vận hành hệ thống thông qua tự động hóa. Thay vì bàn giao thủ công, các bước kiểm tra, đóng gói và phát hành được chuẩn hóa thành quy trình lặp lại tin cậy, giúp cập nhật ứng dụng nhanh và ít lỗi hơn.
- **DevSecOps:** Mở rộng từ DevOps bằng cách đưa bảo mật vào xuyên suốt vòng đời phần mềm theo nguyên tắc dịch chuyển bảo mật sang trái (Shift Left). Các lỗ hổng mã nguồn, rò rỉ khóa bí mật hay sai sót cấu hình được phát hiện ngay lúc lập trình viên đẩy mã lên Git, kết hợp cùng các chốt chặn tại cụm máy chủ và quét lại định kỳ khi ứng dụng đang chạy.
- **GitOps:** Lấy kho mã nguồn Git làm nguồn chân lý duy nhất mô tả trạng thái mong muốn của hạ tầng và ứng dụng. Thay vì để hệ thống CI bên ngoài đẩy lệnh thẳng vào cụm (vốn tiềm ẩn rủi ro lộ quyền quản trị cụm), một bộ điều phối nằm bên trong cụm sẽ chủ động kéo cấu hình từ Git về đối chiếu và tự động sửa lệch nếu trạng thái thực tế bị thay đổi.
- **Zero Trust:** Nguyên tắc an ninh "không mặc định tin cậy bất kỳ kết nối nào", kể cả khi lưu lượng đã đi vào bên trong mạng nội bộ. Mọi truy cập tới trang quản trị hay giao tiếp giữa các dịch vụ trong cụm đều phải xác thực danh tính, giới hạn quyền tối thiểu và chỉ đi qua đúng cổng được cấp phép.

## 2.2. Ảo hóa container và điều phối Kubernetes

**Container** là phương pháp đóng gói ứng dụng kèm đầy đủ thư viện phụ thuộc thành một đơn vị độc lập. Khác với máy ảo phải giả lập cả một hệ điều hành nặng nề, container chia sẻ chung nhân Linux của máy chủ nên khởi động rất nhanh và tiết kiệm bộ nhớ. Trong đồ án, **Docker** được dùng trong bước đóng gói ảnh container qua tệp `Dockerfile`, còn trên các máy chủ cụm Kubernetes sử dụng **containerd**, trình thực thi container chuẩn công nghiệp gọn nhẹ và ổn định hơn.

> **[Vị trí chèn Hình 2.1]**
> *Hướng dẫn lấy/chụp ảnh:* Tải logo chính thức của Docker (PNG nền trong suốt hoặc nền trắng).
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Biểu tượng cá voi Docker và tên thương hiệu rõ nét.

*Hình 2.1: Logo nền tảng đóng gói container Docker*

Khi chạy nhiều container trên nhiều máy chủ, **Kubernetes** đóng vai trò bộ não điều phối: node điều khiển (Control Plane) giữ trạng thái hệ thống và lập lịch, còn các nodes thực thi (Worker) trực tiếp chạy ứng dụng bên trong các đơn vị gọi là Pod. Nhóm sử dụng **`kubeadm`** để tự dựng cụm chuẩn gốc nhằm kiểm soát sâu cấu hình mạng và mã hóa dữ liệu, kết hợp cùng **Helm** (trình quản lý gói cho Kubernetes) để cài đặt và nâng cấp nhanh các thành phần nền tảng phức tạp.

> **[Vị trí chèn Hình 2.2]**
> *Hướng dẫn lấy/chụp ảnh:* Tải logo chính thức của Kubernetes (biểu tượng bánh lái màu xanh dương).
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Bánh lái bảy nan và chữ Kubernetes rõ nét.

*Hình 2.2: Logo hệ thống điều phối container Kubernetes*

## 2.3. Hạ tầng mạng, cổng biên và lưu trữ phân tán

- **WireGuard:** Là giao thức mạng riêng ảo (VPN) hiện đại chạy trực tiếp trong nhân Linux với mã nguồn gọn nhẹ và hiệu năng mã hóa cao. WireGuard giúp nối thông VPS công cộng với hai máy tại chỗ thành một mạng nội bộ thống nhất, đồng thời cho phép cấu hình tuyến đi thẳng giữa hai máy trong cùng mạng LAN.

> **[Vị trí chèn Hình 2.3]**
> *Hướng dẫn lấy/chụp ảnh:* Tải logo chính thức của WireGuard từ wireguard.com.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Biểu tượng rồng đỏ cách điệu và chữ WireGuard rõ nét.

*Hình 2.3: Logo giao thức mạng riêng ảo WireGuard*

- **Cilium eBPF và Hubble:** Cilium là thành phần mạng (CNI) cho Kubernetes sử dụng công nghệ **eBPF** để xử lý gói tin trực tiếp trong nhân Linux, thay thế hoàn toàn `kube-proxy` truyền thống với tốc độ nhanh hơn và khả năng thực thi luật chặn mạng linh hoạt. Đi kèm với Cilium là **Hubble**, cung cấp giao diện trực quan theo dõi từng luồng kết nối và các gói tin bị chặn theo thời gian thực.

> **[Vị trí chèn Hình 2.4]**
> *Hướng dẫn lấy/chụp ảnh:* Tải logo chính thức của Cilium từ cilium.io.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Biểu tượng tổ ong Cilium rõ nét.

*Hình 2.4: Logo hệ thống mạng và bảo mật Cilium eBPF*

- **Traefik, Cloudflare và Longhorn:** **Traefik** đóng vai trò bộ định tuyến biên (Ingress Controller) tiếp nhận lưu lượng web vào cụm, giải mã TLS và chia tải về các Pod ứng dụng. Phía trước Traefik là **Cloudflare**, đảm nhiệm phân giải tên miền, cung cấp chứng chỉ Origin TLS và hàng rào xác thực **Cloudflare Zero Trust Access** bảo vệ các trang quản trị. Ở tầng dữ liệu, **Longhorn** gom không gian ổ đĩa trên các nodes Worker thành hệ thống lưu trữ khối phân tán, tự động nhân bản dữ liệu qua mạng LAN để tránh mất mát khi một máy Worker gặp sự cố.

> **[Vị trí chèn Hình 2.5]**
> *Hướng dẫn lấy/chụp ảnh:* Ghép logo Traefik và Longhorn đặt cạnh nhau cân đối trong một ảnh ngang.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Hai logo đều rõ chữ và cân xứng kích thước.

*Hình 2.5: Logo bộ định tuyến biên Traefik và lưu trữ phân tán Longhorn*

## 2.4. Tự động hóa CI/CD, quản lý bí mật và chính sách bảo mật

- **GitHub Actions và bộ công cụ kiểm tra sớm:** GitHub Actions tự động hóa toàn bộ quy trình kiểm tra, đóng gói và đẩy ảnh lên kho **GHCR** mỗi khi mã nguồn thay đổi. Trong đó, **Gitleaks** rà soát khóa bí mật bị lộ trong lịch sử Git; **Trivy** quét lỗ hổng CVE trong thư viện mã nguồn, tệp cấu hình Kubernetes và ảnh container; còn **`kubeconform`** kiểm tra chuẩn cú pháp YAML trước khi triển khai.
- **ArgoCD:** Là công cụ GitOps theo dõi liên tục thư mục cấu hình trên Git để tự động đồng bộ trạng thái xuống cụm Kubernetes và hiển thị cây tài nguyên trực quan.

> **[Vị trí chèn Hình 2.6]**
> *Hướng dẫn lấy/chụp ảnh:* Tải logo chính thức của ArgoCD từ argoproj.github.io.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Biểu tượng ArgoCD màu cam rõ nét trên nền sáng.

*Hình 2.6: Logo nền tảng GitOps ArgoCD*

- **HashiCorp Vault, External Secrets Operator (ESO) và Kyverno:** **Vault** lưu trữ tập trung và mã hóa mọi mật khẩu, chứng chỉ nhạy cảm thay vì đưa lên Git. **ESO** tự động đồng bộ bí mật từ Vault vào Kubernetes thông qua danh tính ngắn hạn của từng không gian tên (Kubernetes Auth), bảo đảm không tồn tại khóa tĩnh. Cuối cùng, **Kyverno** hoạt động như chốt gác cổng tại Kubernetes API Server, dùng ngôn ngữ biểu thức **CEL** để từ chối tức thì mọi Pod thiếu cấu hình an toàn trước khi được chạy.

> **[Vị trí chèn Hình 2.7]**
> *Hướng dẫn lấy/chụp ảnh:* Ghép logo HashiCorp Vault và Kyverno cạnh nhau trong một ảnh ngang.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Logo hai công cụ rõ nét, kích thước hài hòa.

*Hình 2.7: Logo hệ thống quản lý bí mật HashiCorp Vault và chính sách Kyverno*

## 2.5. Hệ thống quan sát và ngăn xếp ứng dụng mẫu

Để theo dõi sức khỏe hạ tầng, nhóm kết hợp **Prometheus** (thu thập và lưu trữ chỉ số chuỗi thời gian về CPU, RAM, lưu lượng mạng, trạng thái đĩa) với **Grafana** (hiển thị bảng điều khiển trực quan từ dữ liệu của Prometheus). Song song đó, nhóm xây dựng ứng dụng web hai tầng gọn nhẹ gồm **Next.js 16** (App Router) và **Redis** (lưu bộ đếm lượt truy cập) làm đối tượng kiểm chứng thực tế cho quy trình phát hành, cô lập mạng và phục hồi dữ liệu.

> **[Vị trí chèn Hình 2.8]**
> *Hướng dẫn lấy/chụp ảnh:* Ghép logo Prometheus và Grafana đặt cạnh nhau trong một ảnh ngang.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Biểu tượng ngọn lửa Prometheus và biểu tượng Grafana sắc nét.

*Hình 2.8: Logo bộ công cụ giám sát Prometheus và Grafana*

---

# CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ KIẾN TRÚC HỆ THỐNG

Từ nền tảng các công nghệ ở Chương 2, chương này giải thích cách nhóm tổ chức kiến trúc hai tầng, nối thông mạng lai, xếp lớp phòng thủ và cân đối tài nguyên phần cứng thực tế.

## 3.1. Mô hình kiến trúc hai tầng tách biệt

Thay vì gộp chung hạ tầng dùng chung với tài nguyên của ứng dụng vào cùng một vòng lặp đồng bộ, nhóm thiết kế kho mã nguồn Monorepo theo **hai tầng độc lập**:

- **Tầng 1, Hạ tầng nền tảng (`platform-core/`, `wireguard/`, `kubeadm-config/`):** Gồm toàn bộ thành phần cố định dùng lâu dài như WireGuard, cụm Kubernetes `kubeadm`, Cilium eBPF, Longhorn, HashiCorp Vault, ESO, Traefik HA, hệ thống giám sát, Kyverno và ArgoCD. Tầng này được dựng một lần và quản trị trực tiếp bằng `kubeadm`, `helm` và `kubectl`.
- **Tầng 2, Tài nguyên đồ án (`app/`, `.github/workflows/`, `project-nt548/`):** Chỉ chứa mã nguồn ứng dụng mẫu, đường ống CI/CD và các tệp YAML thuần triển khai vào không gian tên `app-prod`, do đối tượng `Application` tên `app-prod` trên ArgoCD tự động quản lý.

Cách phân tách này giúp ArgoCD không bị quá tải bởi hạ tầng lõi, đồng thời cho phép thu hồi sạch toàn bộ ứng dụng đồ án chỉ bằng hai lệnh xóa `app-prod` và namespace `app-prod` mà không ảnh hưởng tới cụm nền. Trong Monorepo, quy trình CI dùng bộ lọc đường dẫn (`paths`) để chỉ chạy khi có thay đổi liên quan tới ứng dụng hoặc chính sách, và đính kèm `[skip ci]` khi tự cập nhật thẻ ảnh mới vào Git nhằm tránh lặp vô hạn.

## 3.2. Thiết kế hạ tầng lai và hai ranh giới mạng

Thách thức lớn nhất khi kết hợp một VPS đám mây (`server-01`, 6 GB RAM) với hai máy trạm nội bộ đặt tại mạng gia đình (`worker-01` và `worker-02`, mỗi máy 8 GB RAM, kết nối mạng LAN `10.10.0.0/24` 1 Gbps phía sau Router NAT) là làm sao giữ thông mạng an toàn mà không làm lưu lượng giữa hai Worker phải đi vòng qua VPS ngoài Internet.

> **[Vị trí chèn Hình 3.1]**
> *Hướng dẫn lấy/chụp ảnh:* Chèn trực tiếp tệp sơ đồ kiến trúc có sẵn tại `images/diagrams/architecture-4x.png`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Hai ranh giới mạng WireGuard `wg0` và Cilium VXLAN, tuyến truyền LAN `/32` giữa hai Worker, luồng từ người dùng qua Cloudflare tới VPS và luồng GitHub Actions/ArgoCD.

*Hình 3.1: Sơ đồ kiến trúc tổng thể hệ thống DevSecOps và GitOps trên Kubernetes Hybrid*

Như thể hiện ở Hình 3.1, hạ tầng mạng được tổ chức thành **hai ranh giới lồng nhau**:

- **Ranh giới 1, Mạng lưới mã hóa WireGuard (`wg0`, dải `10.100.0.0/24`, MTU `1420`, cổng `51820/udp`):** Kết nối năm thiết bị gồm `server-01` (`.1`), `worker-01` (`.2`), `worker-02` (`.3`) cùng hai máy quản trị `client-fedora` (`.10`) và `client-phone` (`.11`). Trên hai Worker, ngoài kết nối về VPS (`10.100.0.0/24`), nhóm khai báo thêm peer ngang hàng trực tiếp tới IP LAN tĩnh của Worker đối diện với dải hẹp `10.100.0.3/32` hoặc `10.100.0.2/32`. Nhờ quy tắc ưu tiên tiền tố dài hơn của bảng định tuyến (Longest-Prefix Match, `/32` ưu tiên hơn `/24`), toàn bộ lưu lượng nhân bản ổ đĩa Longhorn và trao đổi giữa hai Worker đi thẳng qua dây LAN 1 Gbps với độ trễ khoảng 0.3 ms.
- **Ranh giới 2, Mạng phủ Cilium VXLAN (Pod `10.42.0.0/16`, Service `10.43.0.0/16`, MTU `1340`):** Chạy lồng bên trong `wg0` để nối thông các Pod và Service của ba nodes Kubernetes. Giá trị `MTU 1340` được chọn để trừ hao phần tiêu đề gói VXLAN bên trong khung `wg0` (`MTU 1420`), tránh phân mảnh gói tin gây treo kết nối. Hai thiết bị quản trị `.10` và `.11` đứng ngoài mạng phủ này để giữ ranh giới quản trị tách bạch.

Hành trình một truy cập từ trình duyệt vào `https://nt548.*` diễn ra theo bốn bước: người dùng đi qua **Cloudflare Edge** (Proxied, SSL `Full Strict`) tới cổng `443` trên giao diện công cộng `eth0` của `server-01`; Cilium LoadBalancer IP Pool (`<VPS_PUBLIC_IP>/32`) tiếp nhận và đóng gói qua đường hầm VXLAN trên `wg0` gửi về một trong hai Pod **Traefik HA** đang chạy trên Worker; Traefik chấm dứt TLS bằng chứng chỉ Cloudflare Origin rồi chuyển tiếp vào `web-service` tới Pod ứng dụng.

## 3.3. Thiết kế bảo mật đa lớp theo chiều sâu

Hệ thống triển khai năm lớp phòng thủ nối tiếp từ ngoài Internet vào tận tiến trình container:

1. **Lớp biên Cloudflare:** Tên miền ứng dụng chạy qua Proxy ẩn địa chỉ gốc, bắt buộc HTTPS chuẩn `Full (Strict)`, còn ba tên miền quản trị (`argocd.*`, `grafana.*`, `hubble.*`) bị chặn bởi chính sách **Cloudflare Zero Trust Access (`Kubernetes Cluster Admin`)** yêu cầu xác thực mã OTP qua email.
2. **Lớp tường lửa đám mây và an toàn máy chủ:** Trên VPS, tường lửa hạ tầng đám mây (**Cloud NSG**) chỉ mở `61022/tcp` (SSH), `80/tcp`, `443/tcp` (Web) và `51820/udp` (WireGuard), chặn tuyệt đối từ Internet các cổng nội bộ (`6443`, `9100`, `10250`, `8472/udp`). Trên hệ điều hành cả ba nodes, nhóm tắt `ufw`/`firewalld` và tắt `Cilium hostFirewall` để tránh xung đột chuỗi chuyển tiếp `FORWARD` hoặc rớt gói trên giao diện tầng 3 `wg0`; hai Worker tại nhà được bảo vệ bởi Router NAT và chế độ SSH chỉ dùng khóa công khai (`61122`, `61222`).
3. **Lớp mã hóa trạng thái và quản lý bí mật không khóa tĩnh:** API Server bật mã hóa `aescbc` cho mọi `Secret` lưu trong `etcd`. Các bí mật thực tế (`cloudflare-origin-tls`, `grafana-admin-secret`, `redis-auth-secret`) lưu tập trung trong **HashiCorp Vault** (giao diện chỉ mở nội bộ qua `port-forward`). **ESO** dùng xác thực **Kubernetes Auth** (TTL 15 phút) với `ServiceAccount` và `SecretStore` tách riêng cho từng namespace, bảo đảm hoàn toàn không lưu khóa tĩnh trong Git hay cụm.
4. **Lớp kiểm soát cổng tiếp nhận (Kyverno):** Bốn chính sách `ValidatingPolicy` (ngôn ngữ CEL, chế độ `Deny`) chỉ áp dụng lên không gian tên gắn nhãn `policy-tier: hardened` (tự động gắn trên `app-prod`): bắt buộc chạy non-root với `seccompProfile: RuntimeDefault`, tắt leo thang đặc quyền và gỡ mọi capabilities (`ALL`); bắt buộc khai báo đủ `requests` và `limits` CPU/RAM; cấm thẻ `:latest` hoặc thiếu thẻ; và chỉ cho phép kéo ảnh từ `ghcr.io/helios-ryuu/*` hoặc `docker.io/library/redis:*`.
5. **Lớp cô lập mạng nội bộ (Cilium NetworkPolicy):** Luật `allow-web-to-redis` trong `app-prod` chỉ cho phép Pod mang nhãn `app: web` truy cập cổng `6379/TCP` của Redis. Ở tầng nền, Longhorn chỉ mở cổng số liệu `9500` cho Pod `prometheus`, còn số liệu Traefik tách thành `ClusterIP` cổng `9100` nội bộ.

## 3.4. Thiết kế ứng dụng mẫu và đường ống CI/CD GitOps

Ứng dụng mẫu trong `app/` xây dựng trên Next.js `16.4.6` App Router (`output: standalone`), kết nối Redis bằng trình khách viết thuần trên mô đun `node:net` (tự xử lý giao thức RESP) nhằm loại bỏ các thư viện ngoài dễ dính lỗ hổng CVE. Ứng dụng dùng `<Suspense>` và `connection()` để đóng gói ảnh không cần Redis chạy sẵn, đồng thời tách hai đường dẫn kiểm tra sức khỏe: `/healthz` (Liveness) và `/ready` (Readiness kiểm tra thực tế `PING` tới Redis). Trong `app/Dockerfile`, quá trình đóng gói ba giai đoạn chạy trên nền `node:26.13.1-alpine3.24`, xóa bỏ `npm`/`npx`/`corepack` ở ảnh cuối và ép chạy dưới người dùng số `USER 10001:10001`, kết hợp `readOnlyRootFilesystem: true` cùng hai vùng nhớ tạm `emptyDir` giới hạn dung lượng (`/tmp` 32 MiB, `/app/.next/cache` 64 MiB).

> **[Vị trí chèn Hình 3.2]**
> *Hướng dẫn lấy/chụp ảnh:* Dùng Draw.io (trích từ nhánh CI/CD của `images/diagrams/architecture.drawio`, tệp xuất sẵn `images/diagrams/github-action-workflow.png`) vẽ sơ đồ luồng gồm: Developer push Git -> `ci.yml` gọi `security-scan.yml` (Gitleaks, Trivy FS, kubeconform & Trivy Config) -> `build-deploy.yml` (Buildx, `yq` cập nhật manifest, Trivy Image Gate, Push GHCR, Commit `[skip ci]`) -> ArgoCD `RollingUpdate` xuống `app-prod`, cùng nhánh `nightly-audit.yml` chạy hằng đêm.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Các cổng kiểm tra nối tiếp, cơ chế chặn khi có lỗi và hướng đồng bộ từ Git vào cụm.

*Hình 3.2: Sơ đồ luồng đường ống CI/CD DevSecOps, GitOps ArgoCD và quét CVE định kỳ ban đêm*

Như minh họa tại Hình 3.2, quy trình tự động hóa được tách mô đun rõ ràng qua `workflow_call`:
- **Giai đoạn kiểm tra sớm (`security-scan.yml`):** Thực thi `Gitleaks` (quét toàn bộ lịch sử Git), `Trivy FS` (quét CVE mức `HIGH,CRITICAL` trong `app/`) và `kubeconform -strict` kèm `Trivy Config` (kiểm tra chuẩn cấu hình manifest). Nếu bất kỳ cổng nào báo lỗi, pipeline dừng ngay lập tức.
- **Giai đoạn đóng gói và cập nhật GitOps (`build-deploy.yml`):** Chỉ chạy khi mọi cổng an toàn đạt chuẩn. Workflow dựng ảnh gắn thẻ `<git-sha>`, dùng `yq` cập nhật trước tên ảnh và `APP_VERSION` vào `project-nt548/k8s-manifests/deployment.yaml`, chạy **Trivy Image Gate** quét toàn bộ ảnh trong thư mục manifest rồi mới đẩy lên GHCR và tạo commit `[skip ci]` lên nhánh `main` qua khóa `GITOPS_TOKEN`.
- **Phát hành liên tục và quét ban đêm:** ArgoCD nhận biết thay đổi trên Git và áp dụng chiến lược `RollingUpdate` (`maxUnavailable: 0`, `maxSurge: 1`) trên hai bản sao đặt tách node (`podAntiAffinity`), chờ `/ready` xanh trước khi tắt Pod cũ để đạt 0% downtime, đồng thời cho phép hoàn tác ngay bằng `git revert`. Tác vụ `nightly-audit.yml` tách riêng chạy lúc `00:00 UTC` mỗi đêm trên GitHub Runner để quét lại ảnh đang triển khai mà không tốn tài nguyên của cụm.

## 3.5. Quy hoạch hạ tầng, ngân sách tài nguyên và đánh đổi thiết kế

Toàn bộ địa chỉ mạng, cổng SSH và tên miền được quy hoạch thống nhất như Bảng 3.1 (ẩn IP công cộng và IP LAN thật bằng ký hiệu đại diện để bảo đảm an toàn trên kho công khai).

*Bảng 3.1: Tổng hợp quy hoạch hạ tầng, địa chỉ mạng và tên miền hệ thống*

| Thành phần | Giao diện hoặc loại | Địa chỉ / Tên miền | Cổng và ghi chú quy hoạch |
| :--- | :--- | :--- | :--- |
| `server-01` (VPS 6 GB RAM) | `eth0` và `wg0` | `<VPS_PUBLIC_IP>` và `10.100.0.1/24` | Control Plane; SSH `61022/tcp`; API `10.100.0.1:6443`; cấp VIP `<VPS_PUBLIC_IP>/32` |
| Bản ghi `A` máy chủ VPS | Cloudflare (DNS Only) | `vps.*` | Trỏ `<VPS_PUBLIC_IP>`, tắt Proxy cho WireGuard UDP `51820` và SSH `61022` |
| `worker-01` (On-Prem 8 GB) | `wg0` và LAN | `10.100.0.2/24` và `<WORKER_01_LAN_IP>` | SSH `61122/tcp`; IP tĩnh ngoài DHCP `.50` đến `.254`; Longhorn `158 Gi` khả dụng (tổng `226 Gi`, 30% Reserved tại `/var/lib/longhorn`) |
| `worker-02` (On-Prem 8 GB) | `wg0` và LAN | `10.100.0.3/24` và `<WORKER_02_LAN_IP>` | SSH `61222/tcp`; IP tĩnh ngoài DHCP `.50` đến `.254`; Longhorn `347 Gi` khả dụng (tổng `496 Gi`, 30% Reserved tại `/var/lib/longhorn`) |
| Máy quản trị (`client-fedora`, `client-phone`) | `wg0` | `10.100.0.10/32` và `10.100.0.11/32` | Chạy `kubectl`, `helm`, `cilium`, `ssh` qua Hub `vps.*:51820` |
| Mạng phủ cụm (Overlay) | Cilium VXLAN | Pod `10.42.0.0/16`, Svc `10.43.0.0/16` | `MTU 1340`; CoreDNS `10.43.0.10` chạy trên 2 Worker |
| Tên miền ứng dụng | Cloudflare Proxy | `nt548.*` | `CNAME` tới `vps.*` (Proxied), SSL `Full (Strict)` |
| Tên miền quản trị | Cloudflare Zero Trust | `argocd.*`, `grafana.*`, `hubble.*` | `CNAME` tới `vps.*` (Proxied) kèm chính sách `Kubernetes Cluster Admin` (Email OTP) |

Để toàn bộ ngăn xếp DevSecOps chạy vừa vặn trên 1 VPS 6 GB và 2 Worker 8 GB (khả dụng thực tế khoảng 5.78 GiB trên VPS và khoảng 14.7 GB tổng 2 Worker), nhóm tối ưu ngân sách RAM theo năm điểm chính:
- Giữ `server-01` với nhãn `NoSchedule` chỉ chạy Control Plane và tác nhân mạng (~1.9 đến 2.0 GiB RAM, còn dư ~3.8 đến 3.9 GiB).
- Đặt `replicas: 1` cho các dịch vụ nền đơn lẻ (`Prometheus`, `Grafana`, `ArgoCD`, `Vault`, `ESO`, `Kyverno`) và khóa về `zone=onprem-lan`; riêng `Traefik` chạy 2 bản sao để bảo đảm HA.
- Tắt các mô đun chưa cần thiết: tắt `Envoy` trên Cilium, tắt `dex`/`notifications`/`alertmanager`, đặt `applicationSet.replicas: 0`, tắt `Vault injector` và tắt bộ tạo báo cáo nền của Kyverno.
- Giữ bốn giao diện nội bộ (Vault UI `:8200`, Longhorn UI `:8080`, Prometheus UI `:9090`, Traefik Dashboard `:9000`) ở chế độ truy cập qua `kubectl port-forward`.
- Đẩy tác vụ quét CVE hằng đêm ra GitHub Runner (`0 MB` RAM cụm). Tổng mức dùng thực tế trên cả 2 Worker đạt khoảng 5.7 đến 7.9 GB (trung bình 2.85 đến 3.95 GB mỗi máy), còn dư hơn 50% RAM dự phòng.

Về **đánh đổi thiết kế (Trade-offs)** trong giới hạn đồ án: node `server-01` là điểm lỗi đơn (SPOF) cho Control Plane và VIP biên; `redis-0` chạy đơn bản sao với ổ đĩa `RWO` ưu tiên bảo toàn dữ liệu (`RPO = 0`) nên chấp nhận gián đoạn ngắn 30 đến 60 giây khi chuyển node; Monorepo kết hợp `[skip ci]` giúp gọn cho nhóm nhỏ; và Vault cấu hình 1 khóa mở nên cần 1 lệnh `unseal` thủ công sau khi máy chủ khởi động lại.

---

# CHƯƠNG 4: TRIỂN KHAI VÀ KIỂM THỬ HỆ THỐNG

Quá trình triển khai được thực hiện theo trình tự từ hạ tầng mạng và nhân cụm Kubernetes, tới các dịch vụ nền Tầng 1, rồi mới kích hoạt CI/CD, đưa ứng dụng Tầng 2 lên chạy thật và kiểm thử bằng sáu kịch bản thực nghiệm.

## 4.1. Dựng nền tảng mạng WireGuard và cụm Kubernetes Hybrid

Ở bước chuẩn bị (Pha 0), nhóm xác nhận cổng SSH thực tế (`61022`, `61122`, `61222`) và tắt đăng nhập mật khẩu (`PasswordAuthentication no`). Trên cả ba nodes, nhóm tắt `ufw`/`firewalld` giữ `iptables` ở `policy ACCEPT`, đồng thời khóa Cloud NSG trên `server-01` theo thứ tự thêm bốn luật cho phép (`61022/tcp`, `80/tcp`, `443/tcp`, `51820/udp` cùng ICMP) trước rồi mới xóa luật mở rộng cũ. Tại nhà, Router giới hạn dải DHCP `.50` đến `.254` để cố định IP LAN tĩnh cho hai Worker. Trên Cloudflare, nhóm trỏ bản ghi `A` (DNS Only) cho `vps.*`, bốn bản ghi `CNAME` (Proxied) và xuất chứng chỉ Cloudflare Origin lưu cục bộ ngoài Git.

Tiếp đó (Pha 1), nhóm nạp `br_netfilter`, cấu hình `/etc/sysctl.d/90-k8s.conf` (`ip_forward=1`, `rp_filter=0`, `bridge-nf-call-iptables=1`) trên cả ba nodes, cài `open-iscsi` và `nfs-common` trên hai Worker cho Longhorn. Sau khi sinh khóa và kích hoạt `wg-quick@wg0` trên năm thiết bị, nhóm kiểm tra thông mạng hai chiều, đo độ trễ tuyến LAN `/32` giữa hai Worker dưới 1 ms và khởi động lại cả ba máy để xác nhận `wg0` tự phục hồi.

> **[Vị trí chèn Hình 4.1]**
> *Hướng dẫn lấy/chụp ảnh:* Chạy `sudo wg show` và `ping -c 3 10.100.0.3` (hoặc `mtr -c 5 10.100.0.3`) từ `worker-01` (che khóa công khai và IP thật nếu cần).
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Năm peer WireGuard kết nối thành công và RTT giữa hai Worker dưới 1 ms qua IP LAN.

*Hình 4.1: Kết quả kiểm tra thông mạng WireGuard wg0 và độ trễ LAN trực tiếp giữa hai nodes Worker*

Sang Pha 2, nhóm tắt Swap vĩnh viễn, nạp `overlay`, cài `containerd.io 2.3.6` (`SystemdCgroup = true`) cùng `kubelet`, `kubeadm`, `kubectl` `v1.37.1` và khóa nâng cấp tự động. Trên `server-01`, nhóm tạo khóa mã hóa `etcd` (`aescbc`) tại `/etc/kubernetes/enc/enc.yaml`, chạy `kubeadm init` bỏ qua `kube-proxy`, rồi đưa hai Worker vào cụm bằng `kubeadm join` kèm nhãn `zone=onprem-lan` và `node.longhorn.io/create-default-disk=true`. Từ máy quản trị, nhóm cài Cilium eBPF (`MTU 1340`, bật Hubble UI) cùng `CiliumLoadBalancerIPPool`, sau đó vá `deployment/coredns` đưa hai Pod CoreDNS từ VPS về chạy trên hai Worker LAN nhằm giảm độ trễ phân giải DNS nội bộ từ ~30 đến 45 ms xuống dưới 1 ms.

> **[Vị trí chèn Hình 4.2]**
> *Hướng dẫn lấy/chụp ảnh:* Chạy `kubectl get nodes -o wide`, `cilium status` và `kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Ba nodes đạt `Ready` (`10.100.0.1` đến `.3`), Cilium khỏe mạnh và hai Pod CoreDNS chạy tách trên hai Worker.

*Hình 4.2: Trạng thái cụm Kubernetes v1.37.1 với ba nodes Ready và Cilium eBPF hoạt động ổn định*

## 4.2. Triển khai các dịch vụ nền tảng cốt lõi (Tầng 1)

Trên nền cụm Kubernetes sẵn sàng, nhóm triển khai tuần tự các dịch vụ Tầng 1:

- **Longhorn Storage:** Cài vào `longhorn-system` với `replicas: 2` trên hai Worker. Truy cập Longhorn UI qua `port-forward` xác nhận cả hai Worker đạt trạng thái `Schedulable / Ready`. Do lưu trữ dùng chung phân vùng `/` nên Longhorn mặc định giữ lại 30% dung lượng dự phòng cho hệ điều hành (`Reserved`): `worker-01` còn `158 Gi` khả dụng (tổng `226.03 Gi`, `67.8 Gi` Reserved) và `worker-02` còn `347 Gi` khả dụng (tổng `496.24 Gi`, `149 Gi` Reserved), với 4 bản sao (`18 Gi` đã cấp phát cho các PVC của Prometheus, Grafana, Vault và Redis) trên mỗi Worker. Địa chỉ `10.42.x.x` hiển thị bên dưới tên mỗi node trên giao diện Longhorn là Pod IP của `longhorn-manager` trong mạng phủ Cilium.

> **[Vị trí chèn Hình 4.3]**
> *Hướng dẫn lấy/chụp ảnh:* Mở Longhorn UI qua `kubectl port-forward -n longhorn-system svc/longhorn-frontend 8080:80` và chụp mục **Nodes**.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Hai Worker ở trạng thái `Schedulable` và `Ready`, cột `Allocated` là `18 / 158.22 Gi` và `18 / 347.37 Gi` (4 Replicas mỗi node), cột `Size` hiển thị `158 Gi` (`+67.8 Gi Reserved`) và `347 Gi` (`+149 Gi Reserved`).

*Hình 4.3: Giao diện Longhorn UI xác nhận hai nodes Worker và dung lượng lưu trữ phân tán*

- **HashiCorp Vault và ESO:** Cài Vault (PVC Longhorn `2Gi`), khởi tạo 1 khóa duy nhất sao lưu ngoại tuyến, mở khóa, bật `kv-v2` và `kubernetes` auth, nạp ba bí mật (`cloudflare-origin-tls`, `grafana-admin`, `redis-auth`) cùng ba cặp Policy/Role tối thiểu đặc quyền. Sau khi cài ESO từ `ghcr.io` và áp dụng `SecretStore`/`ExternalSecret` cho `traefik` và `monitoring`, hai Secret nền tảng tự đồng bộ đạt `SecretSynced`.

> **[Vị trí chèn Hình 4.4]**
> *Hướng dẫn lấy/chụp ảnh:* Chạy `kubectl exec -n vault vault-0 -- vault status` và `kubectl get secretstore,externalsecret -A`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Vault báo `Sealed: false` và các `ExternalSecret` đạt `SecretSynced` / `True`.

*Hình 4.4: Trạng thái HashiCorp Vault đã mở khóa và các ExternalSecret đồng bộ thành công qua ESO*

- **Traefik HA:** Cài vào `traefik` (`replicas: 2` tách trên hai Worker), gắn `TLSStore` mặc định và tách `traefik-metrics` (`ClusterIP: 9100`). Service `LoadBalancer` nhận đúng địa chỉ ngoài `<VPS_PUBLIC_IP>` từ Cilium.

> **[Vị trí chèn Hình 4.5]**
> *Hướng dẫn lấy/chụp ảnh:* Chạy `kubectl get svc,pods -n traefik -o wide` (che IP công cộng thật nếu cần).
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Service `traefik` kiểu `LoadBalancer` có `EXTERNAL-IP` và hai Pod nằm trên hai Worker khác nhau.

*Hình 4.5: Trạng thái triển khai Traefik HA hai bản sao nhận địa chỉ External IP từ Cilium LoadBalancer*

- **Monitoring, Kyverno và ArgoCD:** Cài `kube-prometheus-stack` (Prometheus `10Gi`, Grafana `5Gi` chiến lược `Recreate`), cài Kyverno chart `3.10.0` kèm bốn `ValidatingPolicy` (`Deny`), cài ArgoCD chuyên trách Tầng 2, rồi chạy `helm upgrade` bật `ServiceMonitor` cho Cilium/Hubble, Longhorn và ArgoCD.

> **[Vị trí chèn Hình 4.6]**
> *Hướng dẫn lấy/chụp ảnh:* Chạy `kubectl get validatingpolicy` và `kubectl get servicemonitor -A`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Đủ bốn luật Kyverno và danh sách `ServiceMonitor` toàn cụm.

*Hình 4.6: Danh sách bốn ValidatingPolicy của Kyverno và các ServiceMonitor giám sát toàn cụm*

## 4.3. Đóng gói ứng dụng mẫu, kích hoạt CI/CD và triển khai Tầng 2

Trên GitHub, nhóm bật quyền `Read and write` cho `GITHUB_TOKEN` và tạo Fine-grained PAT `GITOPS_TOKEN` (chỉ cấp `Contents: Read and write` cho đúng repository kết hợp ngoại lệ Ruleset nhánh `main`) để workflow tự ghi được commit `[skip ci]`. Sau khi kiểm tra sạch bí mật cục bộ và đẩy mã nguồn lên nhánh `main`, quy trình `CI & DevSecOps Gate` chạy qua tất cả các bước kiểm tra an toàn, đẩy ảnh non-root `UID 10001` lên GHCR (chế độ Public) và cập nhật thẻ SHA vào `deployment.yaml`.

> **[Vị trí chèn Hình 4.7]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp màn hình một lần chạy thành công của workflow `CI & DevSecOps Gate` trong tab **Actions** trên GitHub.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Hai nhóm job `Security Gates` và `Build, Scan & GitOps Deploy` đều đạt dấu tích xanh.

*Hình 4.7: Kết quả chạy thành công quy trình CI & DevSecOps Gate trên GitHub Actions*

Tiếp theo, nhóm áp dụng `project-nt548/app-prod.yaml`. ArgoCD tự khởi tạo không gian tên `app-prod` mang nhãn `policy-tier: hardened`, đồng bộ toàn bộ tài nguyên Tầng 2, và ESO tự kéo `redis-auth-secret` từ Vault để Pod `redis-0` cùng hai Pod `web-deployment` khởi chạy khỏe mạnh.

> **[Vị trí chèn Hình 4.8]**
> *Hướng dẫn lấy/chụp ảnh:* Mở giao diện ArgoCD (`https://argocd.*`) vào chi tiết ứng dụng `app-prod`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Trạng thái `Synced` và `Healthy` cùng cây tài nguyên `web-deployment`, `redis-0`, `ExternalSecret`, `NetworkPolicy`, `Ingress`.

*Hình 4.8: Trạng thái đồng bộ ứng dụng app-prod ở mức Synced và Healthy trên giao diện ArgoCD*

Cuối cùng, nhóm gán chính sách Cloudflare Zero Trust `Kubernetes Cluster Admin` (Email OTP) cho ba tên miền quản trị và kiểm tra trang web công cộng tại `https://nt548.*`.

> **[Vị trí chèn Hình 4.9]**
> *Hướng dẫn lấy/chụp ảnh:* Ghép ảnh giao diện trang web `https://nt548.*` với màn hình xác thực OTP Cloudflare Zero Trust khi truy cập trang quản trị.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Bộ đếm Redis, phiên bản `APP_VERSION`, danh tính Pod/Worker và màn hình chặn Zero Trust.

*Hình 4.9: Giao diện ứng dụng mẫu Web Next.js tích hợp bộ đếm Redis và lớp xác thực Cloudflare Zero Trust*

## 4.4. Kiểm thử hệ thống qua 6 kịch bản thực nghiệm

Nhằm bảo đảm quá trình kiểm thử lặp lại an toàn và nhất quán, nhóm xây dựng công cụ hướng dẫn `scripts/test.sh` chỉ in câu lệnh mẫu và các bước kiểm chứng ra màn hình mà không tự ý sửa đổi Git hay cụm Kubernetes.

> **[Vị trí chèn Hình 4.10]**
> *Hướng dẫn lấy/chụp ảnh:* Chạy `./scripts/test.sh` trên terminal và chụp giao diện menu 6 kịch bản kiểm thử.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Danh sách 6 kịch bản và dòng thông báo script chỉ in hướng dẫn an toàn.

*Hình 4.10: Giao diện hướng dẫn kiểm thử hệ thống từ script scripts/test.sh*

### 4.4.1. Kịch bản 1: Kiểm chứng cổng bảo mật CI DevSecOps

- **Mục tiêu:** Chứng minh đường ống GitHub Actions chặn tức thì commit rò rỉ thông tin bí mật, chứa thư viện dính lỗ hổng CVE hoặc tệp cấu hình Kubernetes không hợp chuẩn trước khi đóng gói và đẩy ảnh lên GHCR.
- **Quy trình thực hiện:** Nhóm mô phỏng vi phạm CVE bằng cách cài tạm thư viện cũ `lodash@4.17.20` vào `app/`, chỉ commit riêng hai tệp cấu hình gói bằng lệnh `git commit --only app/package.json app/pnpm-lock.yaml` rồi đẩy lên `main` để không ảnh hưởng tới các thay đổi tài liệu cục bộ. Song song đó, nhóm kiểm tra cục bộ các tệp cấu hình YAML bằng `kubeconform -strict` và `trivy config --severity HIGH,CRITICAL --exit-code 1`. Sau khi kiểm chứng xong trên GitHub Actions, nhóm khôi phục sạch hai tệp về phiên bản trước bằng `git checkout HEAD~1 -- app/package.json app/pnpm-lock.yaml` kèm commit gắn thẻ `[skip ci]`.
- **Kết quả và phân tích:** Trên tab GitHub Actions, job `2. Source CVE Scanning (Trivy FS)` phát hiện ngay lỗ hổng nghiêm trọng của `lodash@4.17.20` và dừng với mã thoát `1`; toàn bộ bước sau đó là `4. Build, Trivy Image Gate & Deploy app-prod` bị bỏ qua hoàn toàn, bảo đảm môi trường `app-prod` đang chạy không bị tác động.

> **[Vị trí chèn Hình 4.11]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp nhật ký GitHub Actions khi chèn `lodash@4.17.20`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Trivy FS báo đỏ mã lỗi 1 và Job build/deploy bị skipped.

*Hình 4.11: Kịch bản 1, đường ống GitHub Actions chặn thành công commit chứa thư viện có lỗ hổng CVE*

### 4.4.2. Kịch bản 2: Kiểm chứng lớp chặn Kyverno tại tầng tiếp nhận Kubernetes

- **Mục tiêu:** Chứng minh ngay cả khi thao tác trực tiếp qua `kubectl`, Kyverno vẫn chặn đứng mọi Pod vi phạm chính sách trong namespace mang nhãn `policy-tier=hardened`.
- **Quy trình thực hiện:** Chạy hai lệnh tạo Pod vi phạm trên `app-prod`:
  ```bash
  kubectl run test-violation -n app-prod --image=nginx:latest --restart=Never
  kubectl run test-registry -n app-prod --image=alpine:3.20 --restart=Never -- sleep 30
  ```
- **Kết quả và phân tích:** Kubernetes API Server lập tức trả lỗi từ chối từ webhook của Kyverno (vi phạm quyền non-root, thiếu `limits`, dùng thẻ `:latest` hoặc registry ngoài danh sách cho phép), không có Pod vi phạm nào được lập lịch xuống Worker.

> **[Vị trí chèn Hình 4.12]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp terminal kết quả hai lệnh `kubectl run` bị từ chối trong `app-prod`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Thông báo `admission webhook "validate.kyverno.svc-fail" denied the request`.

*Hình 4.12: Kịch bản 2, Kubernetes API Server từ chối tạo Pod vi phạm chính sách Kyverno*

### 4.4.3. Kịch bản 3: Kiểm chứng phát hành liên tục RollingUpdate không gián đoạn và hoàn tác qua Git

- **Mục tiêu:** Kiểm chứng quy trình cập nhật ứng dụng qua CI và ArgoCD đạt 0% rớt kết nối với `RollingUpdate` (`maxUnavailable: 0, maxSurge: 1`, `minReadySeconds: 5` kết hợp `lifecycle.preStop` chờ 5 giây để đồng bộ gỡ EndpointSlice với Traefik) và hoàn tác tức thì qua Git.
- **Quy trình thực hiện:** Mở một terminal chạy vòng lặp kiểm tra liên tục endpoint `https://nt548.*/ready` (mỗi 0.5 giây, ghi nhận mốc thời gian, mã HTTP, độ trễ, bộ đếm `ok/fail` cùng phản hồi JSON chứa `version` và `pod`); đẩy riêng một chỉnh sửa nhỏ trong `app/` lên `main` bằng `git commit --only`, dùng `git pull --ff-only origin main` lấy thẻ ảnh mới do CI cập nhật và theo dõi `kubectl -n app-prod rollout status deploy/web-deployment`. Cuối cùng, nhóm hoàn tác tệp `deployment.yaml` về phiên bản trước bằng `git checkout HEAD~1 -- project-nt548/k8s-manifests/deployment.yaml` kèm `git commit --only ... [skip ci]` và đẩy lên `main`.
- **Kết quả và phân tích:** Trong suốt thời gian thay thế Pod cũ bằng Pod mới, vòng lặp kiểm tra ghi nhận `HTTP=200` liên tục với `fail=0`, đồng thời thể hiện rõ thời điểm trường `version` và `pod` trong JSON phản hồi chuyển tiếp mượt mà sang mã SHA mới. Khi hoàn tác trên Git, ArgoCD tiếp tục điều phối một đợt `RollingUpdate` tương tự để đưa hệ thống về phiên bản cũ mà không làm gián đoạn truy cập.

> **[Vị trí chèn Hình 4.13]**
> *Hướng dẫn lấy/chụp ảnh:* Ghép ảnh vòng lặp kiểm tra `/ready` giữ nguyên `HTTP=200` (`fail=0`, thấy rõ `version` và `pod` chuyển từ bản cũ sang bản mới), trạng thái `rollout status` thành công và giao diện web hiển thị `APP_VERSION` mới.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Dòng log `HTTP=200`, `fail=0`, trường `version` đổi sang mã SHA mới và thông báo rollout hoàn tất.

*Hình 4.13: Kịch bản 3, quá trình cập nhật RollingUpdate không gián đoạn và hoàn tác nhanh bằng Git*

### 4.4.4. Kịch bản 4: Kiểm chứng cô lập mạng Redis và quan sát luồng bị chặn trên Hubble UI

- **Mục tiêu:** Chứng minh NetworkPolicy `allow-web-to-redis` chỉ cho phép Pod mang nhãn `app: web` kết nối cổng `6379` của Redis và ghi nhận trực quan luồng bị chặn trên Hubble UI.
- **Quy trình thực hiện:** Kiểm tra `/ready` của Pod Web vẫn đạt HTTP 200, sau đó khởi chạy Pod `intruder` trong cùng `app-prod` (tuân thủ đủ 4 luật Kyverno để được phép chạy, nhưng mang nhãn `app=intruder`) thử kết nối TCP tới `redis-service.app-prod.svc.cluster.local:6379` trong lúc theo dõi Hubble UI (`Verdict = DROPPED`).
- **Kết quả và phân tích:** Kết nối từ `intruder` hết thời gian chờ và báo `DROPPED/TIMEOUT`, đồng thời xuất hiện luồng màu đỏ `DROPPED` từ `intruder` tới `redis-0:6379` trên Hubble UI. Điều này chứng minh dù kẻ tấn công chạy được container hợp chuẩn trong cùng namespace, họ vẫn bị cô lập khỏi dữ liệu Redis.

> **[Vị trí chèn Hình 4.14]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp terminal chạy lệnh kiểm tra `/ready` (200 OK) và lệnh tạo Pod `intruder` trả về `DROPPED/TIMEOUT`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Sự đối lập giữa kết nối thành công của Pod `web` và bị chặn của Pod `intruder`.

*Hình 4.14: Kịch bản 4, kết nối trái phép từ Pod lạ tới Redis bị chặn ở tầng mạng*

> **[Vị trí chèn Hình 4.15]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp giao diện Hubble UI (`https://hubble.*`) ở namespace `app-prod` với bộ lọc `Verdict = DROPPED`.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Dòng lưu lượng màu đỏ từ `intruder` tới `redis-0:6379` mang trạng thái `DROPPED`.

*Hình 4.15: Kịch bản 4, luồng gói tin bị chặn (DROPPED) hiển thị trực quan trên giao diện Hubble UI*

### 4.4.5. Kịch bản 5: Kiểm chứng quét CVE ban đêm, chịu lỗi Traefik HA và chuyển đổi dự phòng Longhorn

- **Mục tiêu:** Kiểm chứng quy trình quét CVE ban đêm không tốn RAM cụm, khả năng chịu lỗi zero-downtime của Traefik HA và khả năng chuyển node bảo toàn dữ liệu (`RPO = 0`) của Redis trên Longhorn.
- **Quy trình thực hiện:** Kích hoạt tay workflow `nightly-audit.yml` trên GitHub Actions; chạy vòng lặp `curl` vào `/healthz` đồng thời xóa nóng một Pod Traefik; ghi nhận số đếm Redis trên web rồi chạy `kubectl drain <NODE_NAME> --ignore-daemonsets --delete-emptydir-data` với node chứa `redis-0`, đợi `redis-0` sang Worker còn lại rồi tải lại trang web và chạy `kubectl uncordon <NODE_NAME>`.
- **Kết quả và phân tích:** Workflow ban đêm quét sạch ảnh trên GitHub Runner mà không dùng RAM cụm; khi xóa nóng một Pod Traefik, bản sao còn lại tiếp tục trả về HTTP `200` liên tục (0% rớt kết nối); và sau khi `drain` node chứa `redis-0`, Longhorn tháo và gắn lại ổ đĩa `RWO` sang Worker còn lại trong khoảng 30 đến 60 giây với số đếm truy cập giữ nguyên vẹn (`RPO = 0`).

> **[Vị trí chèn Hình 4.16]**
> *Hướng dẫn lấy/chụp ảnh:* Ghép minh chứng gồm workflow `nightly-audit.yml` chạy xanh, vòng lặp `curl` giữ nguyên `200` khi xóa Pod Traefik, và `redis-0` chuyển sang Worker còn lại giữ nguyên bộ đếm.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Ba kết quả kiểm chứng khớp với ba phần của Kịch bản 5.

*Hình 4.16: Kịch bản 5, kết quả chạy quy trình quét CVE ban đêm, xóa nóng Pod Traefik và chuyển đổi dự phòng Redis trên Longhorn*

### 4.4.6. Kịch bản 6: Kiểm chứng phục hồi HashiCorp Vault sau eviction và đồng bộ ESO

- **Mục tiêu:** Tận dụng trạng thái `vault-0` bị chuyển khỏi node bảo trì sau lệnh `kubectl drain` ở Kịch bản 5 để chứng minh hai tính chất: ứng dụng và Traefik vẫn vận hành bình thường khi Vault đang bị khóa (`Sealed: true`) nhờ các Kubernetes `Secret` đã đồng bộ sẵn; đồng thời dữ liệu mật khẩu lưu trên ổ đĩa Longhorn `2Gi` vẫn nguyên vẹn, chỉ cần một lệnh mở khóa là Vault hoạt động lại và ESO duy trì trạng thái đồng bộ.
- **Quy trình thực hiện:** Ngay sau khi `vault-0` được lập lịch sang node Worker còn lại ở trạng thái `0/1 Running`, nhóm chạy `kubectl exec -n vault vault-0 -- vault status` để xác nhận `Sealed: true`, kiểm tra trang `/ready` và `kubectl get externalsecret -A` để chứng minh dịch vụ không bị ảnh hưởng. Tiếp theo, nhóm thực hiện mở khóa bằng khóa đơn đã sao lưu ngoại tuyến:
  ```bash
  kubectl exec -n vault vault-0 -- vault operator unseal "<UNSEAL_KEY>"
  ```
  Sau cùng, nhóm kiểm tra lại `kubectl get pods -n vault -o wide` và `kubectl get externalsecret -A`.
- **Kết quả và phân tích:** Trong lúc Vault tạm thời ở trạng thái `Sealed: true`, ứng dụng web và chứng chỉ TLS của Traefik vẫn hoạt động ổn định nhờ các `Secret` đã được đồng bộ trước đó trên cụm. Ngay sau lệnh `vault operator unseal`, trạng thái `Sealed` chuyển về `false` (`Initialized: true`, `HA Enabled: false`), Pod `vault-0` đạt `1/1 Running` và toàn bộ các `ExternalSecret` của `app-prod`, `monitoring` và `traefik` giữ vững trạng thái `SecretSynced` (`READY: True`). Kết quả chứng minh mô hình Vault kết hợp Longhorn PVC và ESO bảo toàn dữ liệu bí mật qua biến cố chuyển node và có quy trình phục hồi đơn giản, đúng như đánh đổi thiết kế ở Chương 3.

> **[Vị trí chèn Hình 4.17]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp terminal hiển thị `vault-0` sau khi chạy `kubectl exec -n vault vault-0 -- vault operator unseal` chuyển từ `Sealed: true` sang `Sealed: false`, kèm kết quả `kubectl get pods -n vault` (`1/1 Running`) và `kubectl get externalsecret -A` (`SecretSynced`).
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Thông báo `Sealed: false` của Vault và trạng thái `SecretSynced` của cả ba `ExternalSecret`.

*Hình 4.17: Kịch bản 6, mở khóa HashiCorp Vault sau khi chuyển node và xác nhận ESO đồng bộ thành công*

## 4.5. Kết quả quan sát và đánh giá vận hành hệ thống

Qua theo dõi vận hành trên Grafana, Hubble UI và kiểm tra biên mạng:

- **Tài nguyên thực tế trên Grafana (`https://grafana.*`):** Node `server-01` tiêu thụ ổn định ~1.9 đến 2.0 GiB trên 5.78 GiB RAM khả dụng; hai nodes Worker dùng trung bình ~2.85 đến 3.95 GB mỗi máy (trên 8 GB), dư hơn 50% bộ nhớ dự phòng. Toàn bộ số liệu từ `node-exporter`, Cilium/Hubble, Traefik, Longhorn (`:9500`) và ArgoCD đều hiển thị đầy đủ.

> **[Vị trí chèn Hình 4.18]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp Dashboard tổng quan tài nguyên Node trên Grafana (`https://grafana.*`).
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Biểu đồ CPU và RAM của ba nodes `server-01`, `worker-01`, `worker-02` ổn định dưới ngưỡng quy hoạch.

*Hình 4.18: Bảng điều khiển Grafana theo dõi mức sử dụng CPU, RAM và lưu lượng của ba nodes trong cụm*

- **Kiểm tra cổng biên và quan sát thực tế:** Quét từ bên ngoài Internet bằng `nmap -Pn -p 61022,80,443,6443,9100,10250 vps.*` xác nhận chỉ các cổng công khai (`61022`, `80`, `443`) ở trạng thái `open`, còn `6443`, `9100` và `10250` bị chặn (`filtered`). Trên Hubble UI, luồng outbound tới `world:443` từ Grafana là tác vụ mặc định kiểm tra phiên bản, còn `argocd-applicationset-controller` được xác nhận duy trì ở `0` bản sao (`0 MB` RAM). Cuối cùng, nhóm chạy thử lệnh thu hồi Tầng 2 (`kubectl delete -f project-nt548/app-prod.yaml && kubectl delete namespace app-prod`) và xác nhận dọn sạch tài nguyên ứng dụng mà vẫn giữ nguyên vẹn 100% hạ tầng Tầng 1.

> **[Vị trí chèn Hình 4.19]**
> *Hướng dẫn lấy/chụp ảnh:* Chụp kết quả lệnh `nmap -Pn -p 61022,80,443,6443,9100,10250 vps.*` chạy từ máy ngoài mạng VPN.
> *Gợi ý nội dung cần thấy rõ trong ảnh:* Cổng `61022`, `80`, `443` ghi `open`; cổng `6443`, `9100`, `10250` ghi `filtered`.

*Hình 4.19: Kết quả quét cổng mạng biên bằng nmap xác nhận chỉ mở các cổng dịch vụ cần thiết*

---

# CHƯƠNG 5: TỔNG KẾT

## 5.1. Kết quả đạt được

Sau hơn năm tuần triển khai và kiểm thử, Nhóm 6 đã hoàn thành đầy đủ các mục tiêu đặt ra:

- **Vận hành thành công hạ tầng Kubernetes Hybrid tối ưu chi phí:** Nối thông 1 VPS 6 GB RAM với 2 máy nội bộ 8 GB RAM qua WireGuard `wg0` và Cilium eBPF, định tuyến trực tiếp `/32` qua LAN 1 Gbps (độ trễ dưới 1 ms) và chuyển CoreDNS về Worker để tăng tốc phân giải DNS nội bộ.
- **Triển khai trọn vẹn kiến trúc hai tầng tiết kiệm tài nguyên:** Tách biệt nền tảng Tầng 1 cố định và ứng dụng Tầng 2 thu hồi sạch, tối ưu toàn bộ hệ sinh thái để tiêu thụ dưới 50% RAM khả dụng trên mỗi Worker.
- **Xây dựng phòng thủ đa lớp khép kín:** Kết hợp cổng CI sớm (`Gitleaks`, `Trivy`, `kubeconform`), Cloudflare Zero Trust, tường lửa Cloud NSG, mã hóa `etcd` (`aescbc`), quản lý bí mật không khóa tĩnh qua Vault và ESO, 4 luật Kyverno CEL và NetworkPolicy cô lập Redis.
- **Kiểm chứng thực nghiệm thành công sáu kịch bản:** Khẳng định khả năng chặn lỗi tự động, cập nhật `RollingUpdate` và hoàn tác qua Git đạt 0% downtime, chịu lỗi Traefik HA, bảo toàn dữ liệu Redis trên Longhorn (`RPO = 0`), mở khóa phục hồi Vault sau eviction kèm đồng bộ ESO và quét CVE ban đêm không tốn RAM cụm.

## 5.2. Hạn chế của đồ án

- **Điểm lỗi đơn tại `server-01`:** Do giới hạn một VPS duy nhất, node này gánh cả Control Plane đơn lẻ lẫn điểm nhận LoadBalancer VIP công cộng.
- **Gián đoạn ngắn ở Redis khi chuyển node:** Với cấu hình một bản sao dùng ổ đĩa Longhorn `RWO`, việc chuyển `redis-0` sang Worker khác gây gián đoạn khoảng 30 đến 60 giây dù bảo toàn dữ liệu.
- **Mở khóa Vault thủ công sau khi khởi động lại:** Vì dùng một khóa mở duy nhất để tiết kiệm RAM, quản trị viên cần chạy một lệnh `vault operator unseal` sau khi máy Worker chứa Vault khởi động lại.
- **Chưa bật cảnh báo tức thời và kiểm thử tải lớn:** `Alertmanager` được tắt để dành bộ nhớ nên chưa gửi cảnh báo chủ động về kênh chat, và đồ án chưa thực hiện các bài đo chịu tải quy mô hàng nghìn kết nối đồng thời.

## 5.3. Hướng phát triển trong tương lai

- **Mở rộng Control Plane HA:** Bổ sung ba nodes Control Plane tạo quorum `etcd`, kết hợp Cloud Load Balancer hoặc Cilium BGP để loại bỏ điểm lỗi đơn ở tầng điều khiển và tầng biên.
- **Nâng cấp tầng dữ liệu HA:** Chuyển Redis sang mô hình **Redis Sentinel** hoặc **Redis Cluster** nhiều bản sao phân tán trên nhiều Worker.
- **Tự động mở khóa Vault:** Chuyển sang Vault HA ba nodes dùng lưu trữ Raft kết hợp dịch vụ Cloud KMS để thực hiện **Auto-Unseal**.
- **Tách kho cấu hình GitOps và mở rộng chiến lược phát hành:** Tách App Repo và GitOps Repo để phân quyền chặt chẽ hơn, kết hợp triển khai **Canary** hoặc **Blue/Green** qua Argo Rollouts.
- **Tăng cường chuỗi cung ứng và cảnh báo tự động:** Bổ sung ký xác thực ảnh bằng **Cosign**, tạo danh mục **SBOM**, bật lại `Alertmanager` kết nối Telegram/Slack và bổ sung kiểm thử chịu tải định kỳ.

---

# TÀI LIỆU THAM KHẢO

[1] Aqua Security Software Ltd., "Trivy Documentation: Vulnerability, Misconfiguration and Secret Scanning," Aqua Security, 2026. [Trực tuyến]. Địa chỉ: https://trivy.dev/docs/.

[2] Argo Project Authors, "Argo CD Documentation: Declarative GitOps Continuous Delivery for Kubernetes," CNCF, 2026. [Trực tuyến]. Địa chỉ: https://argo-cd.readthedocs.io/.

[3] Cilium Authors, "Cilium and Hubble Documentation: eBPF-based Networking, Security, and Observability," CNCF, 2026. [Trực tuyến]. Địa chỉ: https://docs.cilium.io/.

[4] Cloudflare Inc., "Cloudflare Zero Trust and Origin CA Certificates Documentation," Cloudflare Docs, San Francisco, CA, USA, 2026. [Trực tuyến]. Địa chỉ: https://developers.cloudflare.com/cloudflare-one/.

[5] Docker Inc., "Docker Buildx and Multi-Stage Builds Documentation," Docker Documentation, Palo Alto, CA, USA, 2026. [Trực tuyến]. Địa chỉ: https://docs.docker.com/build/.

[6] External Secrets Operator Authors, "External Secrets Operator Documentation: HashiCorp Vault Provider and Kubernetes Auth," CNCF, 2026. [Trực tuyến]. Địa chỉ: https://external-secrets.io/.

[7] GitHub Inc., "GitHub Actions Documentation: Reusing Workflows and GitHub Container Registry," GitHub Docs, San Francisco, CA, USA, 2026. [Trực tuyến]. Địa chỉ: https://docs.github.com/en/actions.

[8] Grafana Labs and Prometheus Authors, "Prometheus and Grafana Observability Stack Documentation," CNCF and Grafana Labs, 2026. [Trực tuyến]. Địa chỉ: https://prometheus.io/docs/.

[9] HashiCorp Inc., "Vault Documentation: KV Secrets Engine v2 and Kubernetes Auth Method," HashiCorp Developer, San Francisco, CA, USA, 2026. [Trực tuyến]. Địa chỉ: https://developer.hashicorp.com/vault/docs.

[10] Kyverno Authors, "Kyverno Documentation: Kubernetes Native Policy Management and CEL ValidatingPolicy," CNCF, 2026. [Trực tuyến]. Địa chỉ: https://kyverno.io/docs/.

[11] Longhorn Authors, "Longhorn Documentation: Cloud Native Distributed Block Storage for Kubernetes," CNCF, 2026. [Trực tuyến]. Địa chỉ: https://longhorn.io/docs/.

[12] Redis Ltd., "Redis Documentation: RESP Protocol Specification and Persistence," Redis.io, Mountain View, CA, USA, 2026. [Trực tuyến]. Địa chỉ: https://redis.io/docs/.

[13] The Kubernetes Authors, "Kubernetes Documentation: Cluster Administration with kubeadm, Network Policies, and Workloads," CNCF, 2026. [Trực tuyến]. Địa chỉ: https://kubernetes.io/docs/.

[14] Traefik Labs, "Traefik Proxy Documentation: Kubernetes Ingress Provider and TLS Configuration," Traefik Labs, Lyon, France, 2026. [Trực tuyến]. Địa chỉ: https://doc.traefik.io/traefik/.

[15] Vercel Inc., "Next.js App Router Documentation: Standalone Output and Dynamic Rendering," Next.js Docs, San Francisco, CA, USA, 2026. [Trực tuyến]. Địa chỉ: https://nextjs.org/docs.

[16] WireGuard Authors, "WireGuard: Fast, Modern, Secure Kernel VPN Tunnel," WireGuard.com, 2026. [Trực tuyến]. Địa chỉ: https://www.wireguard.com/.

[17] Z. Rice and Gitleaks Contributors, "Gitleaks: Detect Hardcoded Secrets in Git Repositories," GitHub Repository, 2026. [Trực tuyến]. Địa chỉ: https://github.com/gitleaks/gitleaks.
