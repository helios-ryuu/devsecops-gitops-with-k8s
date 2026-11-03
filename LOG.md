# Nhật ký triển khai (Deployment Log)

Các bước thực hiện thiết lập hạ tầng thực tế:

1. **Cài đặt Tailscale**
   - Cài đặt và cấu hình Tailscale trên các node (`server-01` VPS, `worker-01`, `worker-02` on-prem) tạo mạng mesh VPN riêng.

2. **Cài đặt K3s Cluster**
   - **Cấu hình & Cài đặt Server Node (`server-01` VPS):**
     Tạo file `/etc/rancher/k3s/config.yaml`:
     ```yaml
     # --- Định danh & Mạng Node ---
     node-name: "server-01"
     bind-address: "<MASTER_TAILSCALE_IP>"
     advertise-address: "<MASTER_TAILSCALE_IP>"
     node-ip: "<MASTER_TAILSCALE_IP>"
     node-external-ip: "<MASTER_TAILSCALE_IP>"

     # --- SANs cho TLS Certificate ---
     tls-san:
       - "<MASTER_TAILSCALE_IP>"
       - "127.0.0.1"
       - "localhost"

     # --- Cấu hình CNI Mạng Flannel qua Tailscale ---
     flannel-iface: "tailscale0"
     flannel-backend: "vxlan"

     # --- Cấu hình Taints ---
     node-taint:
       - "node-role.kubernetes.io/control-plane:NoSchedule"

     # --- Tinh chỉnh Dịch vụ & Add-ons ---
     disable:
       - "traefik"
       - "servicelb"
   
     # --- Bảo mật & Phân quyền ---
     secrets-encryption: true
     write-kubeconfig-mode: "0644"
     debug: false
     ```
     Phân quyền cho file cấu hình & Chạy lệnh cài đặt K3s Server và lấy token:
     ```bash
     # Phân quyền cho file cấu hình (0644 giúp user thường chạy kubectl không bị cảnh báo permission denied)
     sudo chmod 755 /etc/rancher/k3s
     sudo chmod 644 /etc/rancher/k3s/config.yaml

     curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.37.1+k3s1" sh -
     sudo cat /var/lib/rancher/k3s/server/node-token
     ```

   - **Cấu hình & Cài đặt Worker Nodes (`worker-01`, `worker-02` on-prem):**
     Tạo file `/etc/rancher/k3s/config.yaml` trên từng worker:
     ```yaml
     server: "https://<MASTER_TAILSCALE_IP>:6443"
     token: "<NODE_TOKEN>"
     node-name: "worker-01"   # Đặt tương ứng worker-01 hoặc worker-02
     node-ip: "<WORKER_TAILSCALE_IP>"
     node-external-ip: "<WORKER_TAILSCALE_IP>"
     flannel-iface: "tailscale0"
     ```
     Chạy lệnh cài đặt K3s Agent:
     ```bash
     curl -sfL https://get.k3s.io | sh -s - agent
     ```

3. **Đồng bộ Kubeconfig về máy quản trị**
   - Sao chép file `/etc/rancher/k3s/k3s.yaml` từ `server-01` về máy local (`~/.kube/config`) và phân quyền cho config: `chmod 600 ~/.kube/config`.
   - Cập nhật địa chỉ `server` trỏ về Tailscale IP của `server-01` nếu cần.

4. **Xác nhận trạng thái Nodes**
   - Kiểm tra kết nối cụm:
     ```bash
     kubectl get nodes -o wide
     ```
   - Đảm bảo tất cả 3 node đều ở trạng thái `Ready`.

5. **Tạo Chứng chỉ SSL Cloudflare Origin Server**
   - Tạo Origin Certificate (hạn 1 năm hoặc mặc định 15 năm tối đa) trên Cloudflare Dashboard cho domain `*.helios.id.vn` và `helios.id.vn`.
   - Tải về và lưu cặp file chứng chỉ vào thư mục [secrets/](file:///home/helios/main/projects/devsecops-gitops-with-k8s/secrets/) gồm `tls.crt` và `tls.key`.

6. **Tạo Kubernetes Secret cho TLS**
   - Tạo Kubernetes Secret `cloudflare-origin-tls` trong namespace `traefik` (tạo imperative hoặc encode base64 vào file [traefik/cloudflare-origin-tls-secret.yaml](file:///home/helios/main/projects/devsecops-gitops-with-k8s/traefik/cloudflare-origin-tls-secret.yaml)):
     ```bash
     kubectl create namespace traefik
     kubectl create secret tls cloudflare-origin-tls \
       --cert=secrets/tls.crt \
       --key=secrets/tls.key \
       -n traefik
     ```

7. **Apply TLSStore cho Traefik**
   - Áp dụng cấu hình Default Certificate qua [traefik/tlsstore.yaml](file:///home/helios/main/projects/devsecops-gitops-with-k8s/traefik/tlsstore.yaml):
     ```bash
     kubectl apply -f traefik/tlsstore.yaml
     ```

8. **Thêm Traefik Helm Repository**
   - Cập nhật kho chart của Traefik:
     ```bash
     helm repo add traefik https://traefik.github.io/charts
     helm repo update
     ```

9. **Cài đặt Traefik Ingress Controller Release**
   - Deploy Traefik bằng Helm với file values tùy chỉnh [traefik/values.yaml](file:///home/helios/main/projects/devsecops-gitops-with-k8s/traefik/values.yaml):
     ```bash
     helm install traefik traefik/traefik -n traefik -f traefik/values.yaml
     ```

10. **Thêm ArgoCD Helm Repository**
    - Cập nhật kho chart của ArgoCD:
      ```bash
      helm repo add argo https://argoproj.github.io/argo-helm
      helm repo update
      ```
11. **Cài đặt ArgoCD GitOps Controller Release**
    - Deploy ArgoCD bằng Helm với file values tùy chỉnh [argocd/values.yaml](file:///home/helios/main/projects/devsecops-gitops-with-k8s/argocd/values.yaml):
      ```bash
      helm install argocd argo/argo-cd -n argocd --create-namespace -f argocd/values.yaml
      ```

12. **Lấy mật khẩu admin ArgoCD**
    - Lấy mật khẩu admin từ Secret `argocd-initial-admin-secret`:
      ```bash
      kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode
      ```
13. **Khởi tạo Next.js App Router bằng CLI**
    - Sử dụng pnpm để tạo ứng dụng Next.js:
      ```bash
      pnpm create next-app app \
        --typescript \
        --tailwind \
        --eslint \
        --app \
        --src-dir \
        --import-alias "@/*"
      ```

14. **Cấu hình Standalone & Endpoints kiểm tra sức khỏe**
    - Bật `output: "standalone"` trong [app/next.config.ts](file:///home/helios/main/projects/devsecops-gitops-with-k8s/app/next.config.ts).
    - Tạo các route kiểm tra probe cho Kubernetes:
      - `app/src/app/healthz/route.ts` phục vụ `livenessProbe`.
      - `app/src/app/ready/route.ts` phục vụ `readinessProbe`.

15. **Tối ưu hóa Dockerfile & Bảo mật Non-Root**
    - Tạo [app/Dockerfile](file:///home/helios/main/projects/devsecops-gitops-with-k8s/app/Dockerfile) dạng Multi-Stage build cho pnpm với base image bất biến `node:26.13.0-alpine3.23`.
    - Cấu hình non-root user `10001:10001` và chown đồng bộ cho các thư mục `public`, `standalone`, `static`.
    - Tạo file [app/.dockerignore](file:///home/helios/main/projects/devsecops-gitops-with-k8s/app/.dockerignore) loại trừ các tệp không cần thiết.

16. **Cấu hình quyền Workflow trên GitHub Repository**
    - Truy cập Settings $\rightarrow$ Actions $\rightarrow$ General $\rightarrow$ Workflow permissions.
    - Chọn **Read and write permissions** và tích chọn **Allow GitHub Actions to create and approve pull requests** (đảm bảo CI pipeline có quyền push Git tag mới).