# RUNBOOK TRIỂN KHAI HỆ THỐNG TỪ ĐẦU ĐẾN KẾT THÚC (ĐỒ ÁN NT548)

Tài liệu hướng dẫn thao tác từng bước để dựng hoàn chỉnh hạ tầng mạng WireGuard, cụm Kubernetes Hybrid (`kubeadm v1.37.1`), **Tầng 1 (Platform Core Infrastructure)** rồi mới đưa mã nguồn lên GitHub kích hoạt CI/CD, image GHCR, đồng bộ GitOps ArgoCD và triển khai **Tầng 2 (Project NT548 — RollingUpdate Continuous Delivery)** từ máy quản trị **Fedora (`laptop`)**.

> Tài liệu tham khảo: [ARCHITECTURE.md](./ARCHITECTURE.md) • [README.md](./README.md) • [wireguard/README.md](./wireguard/README.md) • [platform-core/vault/README.md](./platform-core/vault/README.md)

---

## Bảng tham chiếu nhanh

| Thành phần | Node / Giá trị | Thông số & Ghi chú |
|---|---|---|
| Control Plane (VPS Ubuntu) | `server-01` (`heliosvps`) | User `helios` • SSH **`61022/tcp`** • **6GB RAM** (~5.3–5.5GB khả dụng) • Public IP `<VPS_PUBLIC_IP>` • `A`: `vps.helios.id.vn` (DNS Only) • `wg0`: `10.100.0.1/24` |
| Worker 1 (On-Prem Ubuntu) | `worker-01` | User `helios` • SSH **`61122/tcp`** (LAN `10.10.0.0/24` & `wg0`) • **8GB RAM** (~7.3–7.5GB khả dụng) • `wg0`: `10.100.0.2/24` • Longhorn `/var/lib/longhorn` (`199GB`) |
| Worker 2 (On-Prem Ubuntu) | `worker-02` | User `helios` • SSH **`61222/tcp`** (LAN `10.10.0.0/24` & `wg0`) • **8GB RAM** (~7.3–7.5GB khả dụng) • `wg0`: `10.100.0.3/24` • Longhorn `/` (`461GB` trống) |
| Máy quản trị (Fedora) | `laptop` | `wg0`: `10.100.0.10/32` • Chạy `kubectl`, `helm`, `cilium`, `jq`, `ssh` |
| Pod CIDR / Service CIDR | `10.42.0.0/16` / `10.43.0.0/16` | Cilium VXLAN `MTU 1340` • CoreDNS `10.43.0.10` |
| Tên miền Public | `nt548.helios.id.vn` | `CNAME -> vps.helios.id.vn` (Cloudflare Proxied, SSL `Full (Strict)`) |
| Tên miền Quản trị | `argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn` | `CNAME -> vps.helios.id.vn` (Cloudflare Proxied + Zero Trust `K8s Admin` Email OTP) |

---

## Pha 0: Chuẩn bị Hạ tầng, Tắt Host Firewall An toàn SSH & Công cụ Quản trị

### 0.1. Bảo vệ phiên SSH đang chạy & Xác nhận cổng SSH thực tế

Trên từng node (`server-01` = `heliosvps`, `worker-01`, `worker-02`, user `helios`), kiểm tra cổng `sshd` thực sự đang lắng nghe:

```bash
# Xác nhận sshd đang lắng nghe đúng cổng:
# server-01 (heliosvps): 61022 | worker-01: 61122 | worker-02: 61222
sudo ss -tlnp | grep -E 'sshd|ssh'
grep -R -E '^(Port|ListenStream)' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/ 2>/dev/null || true
```

### 0.2. Làm sạch `kubeconfig`

Trên `laptop` (Fedora), sao lưu và xóa `~/.kube/config` cũ nếu tồn tại:

```bash
rm -f ~/.kube/config
```

> [!NOTE]
> Nếu tái sử dụng máy đã có sẵn cụm Kubernetes, Longhorn hoặc VPN khác (như Tailscale), reset sạch trạng thái cũ trước khi sang **Bước 0.3** *(tuyệt đối không chạy mù `iptables -F`/`iptables -X` khi `INPUT` đang ở `DROP` để tránh tự ngắt SSH)*:
>
> ```bash
> # Tùy chọn — chỉ chạy khi tái sử dụng host từ cụm/VPN cũ
> sudo kubeadm reset -f 2>/dev/null || true
> sudo systemctl disable --now tailscaled 2>/dev/null || true
> sudo apt-get purge -y tailscale 2>/dev/null || true
> sudo umount -lf /var/lib/kubelet/pods/*/volumes/*/* /var/lib/longhorn* 2>/dev/null || true
> sudo rm -rf /etc/kubernetes /var/lib/etcd /var/lib/kubelet /etc/cni /var/lib/cni /opt/cni /var/lib/longhorn /var/lib/tailscale
> for iface in cilium_host cilium_net cilium_vxlan flannel.1 flannel-v6.1 cni0 kube-ipvs0; do
>   sudo ip link del "$iface" 2>/dev/null || true
> done
> ```

### 0.3. Tắt `ufw` / `firewalld` trên 3 Node & Xác minh Chính sách Mạng

Mô hình bảo mật biên của cụm tách bạch khỏi nhân Linux trên từng host:
- **Lý do tắt `ufw` và `firewalld`:** Trong cụm Kubernetes dùng **Cilium eBPF (`kubeProxyReplacement: true`)** và **WireGuard (`wg0`)**, bật song song `ufw`/`firewalld` dễ làm xóa hoặc xung đột bảng luật định tuyến của Cilium, đồng thời chain `FORWARD` mặc định của `ufw` chặn lưu lượng Pod/VXLAN. Do `wg0` là giao diện tầng L3 (không có Ethernet header), **Cilium `hostFirewall`** cũng không được bật để tránh rớt gói `UnknownEthernetType`.
- **Phân tầng bảo vệ thay thế (nằm ngoài OS):**
  - Trên **VPS (`server-01` / `heliosvps`)**: Mọi cổng nội bộ/nhạy cảm (`6443/tcp`, `9100/tcp`, `10250/tcp`, `8472/udp`) được chặn hoàn toàn tại **Cloud Firewall (NSG)** của nhà cung cấp VPS (cấu hình ở **Bước 0.5**).
  - Trên **2 Worker tại nhà (`worker-01` & `worker-02` trong `10.10.0.0/24`)**: Tin cậy **Router NAT** (không mở port-forwarding từ WAN vào LAN) kết hợp **SSH Key-only** (`PasswordAuthentication no`, cổng `61122`/`61222`). *(Khuyến nghị: Nếu LAN nhà có nhiều thiết bị IoT/khách không tin cậy, hãy tách 2 worker vào VLAN hoặc tách Wi-Fi khách trên Router.)*

Thực hiện lần lượt trên **cả 3 node** (`server-01` SSH `61022`, `worker-01` SSH `61122`, `worker-02` SSH `61222`):

```bash
# 1. Kiểm tra chắc chắn SSH chỉ cho phép Key (PasswordAuthentication no)
sudo sshd -T | grep -iE 'port|passwordauthentication|pubkeyauthentication'

# 2. Tắt hoàn toàn ufw và firewalld (nếu có) trên OS
sudo ufw disable || true
sudo systemctl disable --now ufw 2>/dev/null || true
sudo systemctl disable --now firewalld 2>/dev/null || true

# 3. Xác minh host firewall đã tắt và bảng iptables sạch (policy ACCEPT)
sudo ufw status || true
sudo iptables -L -n
```

> [!IMPORTANT]
> Kỳ vọng `sudo ufw status` trả về `Status: inactive` và `sudo iptables -L -n` hiển thị `Chain INPUT (policy ACCEPT)`, `Chain FORWARD (policy ACCEPT)`, `Chain OUTPUT (policy ACCEPT)`, không còn chain `ufw-*` chặn luồng. Hoàn tất khóa Cloud Firewall (NSG) tại **Bước 0.5** trước khi mở các dịch vụ cụm ở Pha 2.

### 0.4. Cài công cụ trên `laptop` (Fedora) & Khai báo biến tạm `VPS_PUBLIC_IP`

```bash
sudo dnf install -y wireguard-tools curl jq git vim
```

Cài `kubectl` (`v1.37.1`), `helm` và `cilium` CLI vào `/usr/local/bin/` (theo phiên bản ổn định tương ứng) và kiểm tra tại thư mục repository:

```bash
cd /path/to/devsecops-gitops-with-k8s
kubectl version --client
helm version
jq --version
```

Khai báo tạm biến `VPS_PUBLIC_IP` trên phiên terminal `laptop`:

```bash
export VPS_PUBLIC_IP="<IP_PUBLIC_VPS_THUC_TE>"
```

### 0.5. Đặt IP LAN tĩnh, Cloud Firewall VPS & Cloudflare DNS / Origin TLS

1. **Router & Static IP LAN (`10.10.0.0/24`):** Giới hạn dải DHCP động trên Router (`10.10.0.50` – `10.10.0.254`) và cấu hình **Static IP (`netplan`)** nằm ngoài vùng DHCP cho `<WORKER_01_LAN_IP>` (`worker-01`) và `<WORKER_02_LAN_IP>` (`worker-02`).
2. **Cloud Firewall (NSG) của nhà cung cấp VPS (`server-01`):**
   - Khóa biên ngoài của VPS ngay tại tầng hạ tầng Cloud theo thứ tự **thêm rule mới trước — xóa rule wildcard sau** để bảo toàn phiên SSH `61022` đang chạy:
   - **Bước 2a — Thêm 4 rule Ingress IPv4 chuẩn (giữ `Ingress IPv4 ICMP` và toàn bộ `Egress` mở):**

     | Direction | Ether Type | Protocol | From Port / To Port | CIDR | Mục đích |
     | :--- | :--- | :--- | :--- | :--- | :--- |
     | Ingress | IPv4 | `TCP` | `61022` – `61022` | `0.0.0.0/0` | SSH Admin (`heliosvps`) |
     | Ingress | IPv4 | `TCP` | `80` – `80` | `0.0.0.0/0` | HTTP Public (Cloudflare $\rightarrow$ Traefik) |
     | Ingress | IPv4 | `TCP` | `443` – `443` | `0.0.0.0/0` | HTTPS Public (Cloudflare Origin TLS $\rightarrow$ Traefik) |
     | Ingress | IPv4 | `UDP` | `51820` – `51820` | `0.0.0.0/0` | WireGuard Hub (`wg0`) |

   - **Bước 2b — Xóa bỏ toàn bộ rule Ingress wildcard cũ (`Ingress IPv4 TCP 0.0.0.0/0`, `Ingress IPv4 UDP 0.0.0.0/0`, `Ingress IPv6 ::/0`):** Bảo đảm mọi cổng nội bộ (`6443/tcp`, `9100/tcp`, `10250/tcp`, `8472/udp`) bị chặn tuyệt đối từ Internet.
   - **Bước 2c — Kiểm tra SSH mới qua Terminal #2:** Mở **Terminal #2** trên `laptop` chạy `ssh -p 61022 helios@vps.helios.id.vn` trước khi chuyển sang Pha 1.
3. **Cloudflare DNS (`helios.id.vn`):**
   - Tạo bản ghi **`A`**: `vps.helios.id.vn` $\rightarrow$ **`<VPS_PUBLIC_IP>`** với trạng thái **DNS Only (đám mây xám)** để WireGuard `:51820/udp` và SSH `:61022/tcp` đi trực tiếp tới VPS.
   - Tạo các bản ghi **`CNAME`** với trạng thái **Proxied (đám mây cam)** trỏ tới `vps.helios.id.vn`:
     - Public App: `nt548.helios.id.vn`
     - Admin UIs: `argocd.helios.id.vn`, `grafana.helios.id.vn`, `hubble.helios.id.vn`
4. **Cloudflare SSL/TLS:**
   - **SSL/TLS -> Overview:** chọn chế độ **Full (Strict)**.
   - **SSL/TLS -> Origin Server -> Create Certificate:** cấp chứng chỉ cho `*.helios.id.vn, helios.id.vn`, lưu cục bộ tại `secrets/tls.crt` và `secrets/tls.key` (đã nằm trong `.gitignore`, tuyệt đối không commit lên Git).

---

## Pha 1: Hạ tầng mạng WireGuard (`wg0`) & Chuẩn bị Host Longhorn

Thực hiện theo chi tiết trong [wireguard/README.md](./wireguard/README.md).

### 1.1. Cài gói phụ thuộc & cấu hình `sysctl` (`90-k8s.conf`) trên cả 3 node (`server-01`, `worker-01`, `worker-02`)

```bash
sudo apt-get update && sudo apt-get install -y wireguard wireguard-tools curl jq vim

# Nạp module br_netfilter ngay và tự động nạp sau khi reboot
sudo modprobe br_netfilter
echo "br_netfilter" | sudo tee /etc/modules-load.d/k8s.conf

# Ghi cấu hình mạng chuẩn cho Kubernetes + Cilium + WireGuard vào /etc/sysctl.d/90-k8s.conf
cat <<'EOF' | sudo tee /etc/sysctl.d/90-k8s.conf
net.ipv4.ip_forward = 1
net.ipv4.conf.all.forwarding = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.conf.all.rp_filter = 0
net.ipv4.conf.default.rp_filter = 0
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system
# Xác minh giá trị thực tế đang hiệu lực trong kernel (kỳ vọng lần lượt: 1, 0, 0, 1)
sysctl net.ipv4.ip_forward net.ipv4.conf.all.rp_filter net.ipv4.conf.default.rp_filter net.bridge.bridge-nf-call-iptables
```

### 1.2. Cài đặt thành phần Longhorn trên 2 Worker (`worker-01` & `worker-02`)

```bash
sudo apt-get install -y open-iscsi nfs-common
sudo modprobe iscsi_tcp
echo "iscsi_tcp" | sudo tee /etc/modules-load.d/longhorn-iscsi.conf
sudo systemctl enable --now iscsid
```

> Cả `worker-01` (`199GB`) và `worker-02` (`461GB` trống trên `/`) đều dùng trực tiếp thư mục mặc định `/var/lib/longhorn` trên phân vùng `/`.

### 1.3. Sinh khóa, kích hoạt `wg0` & Kiểm chứng SSH qua `wg0`

*(Cloud Firewall NSG của `server-01` đã mở `51820/udp` ở Bước `0.5` và host firewall trên cả 3 node đã tắt từ Bước `0.3`.)*

Trên từng máy (`server`, `client-01`, `client-02`, `client-fedora` và tạo cặp khóa mới trên app WireGuard cho `client-phone`):

```bash
umask 077
sudo mkdir -p /etc/wireguard
wg genkey | sudo tee /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
```

Điền khóa, `Endpoint = vps.helios.id.vn:51820` và IP LAN thực tế (`10.10.0.x`) vào `/etc/wireguard/wg0.conf`:
- `server` (`heliosvps` / `server-01` — `.1`): [wireguard/wg0.server.conf.example](./wireguard/wg0.server.conf.example)
- `client-01` (`worker-01` — `.2`): [wireguard/wg0.client-01.conf.example](./wireguard/wg0.client-01.conf.example) *(Peer `client-02` dùng `<WORKER_02_LAN_IP>:51820` và `AllowedIPs = 10.100.0.3/32`)*
- `client-02` (`worker-02` — `.3`): [wireguard/wg0.client-02.conf.example](./wireguard/wg0.client-02.conf.example) *(Peer `client-01` dùng `<WORKER_01_LAN_IP>:51820` và `AllowedIPs = 10.100.0.2/32`)*
- `client-fedora` (`laptop` — `.10`): [wireguard/wg0.client-fedora.conf.example](./wireguard/wg0.client-fedora.conf.example)
- `client-phone` (`phone` — `.11`): [wireguard/wg0.client-phone.conf.example](./wireguard/wg0.client-phone.conf.example)

Bật `wg0` trên `server`, `client-01`, `client-02`, `client-fedora` và bật tunnel trên `client-phone`:

```bash
sudo vim /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf
sudo systemctl enable --now wg-quick@wg0
sudo wg show
```

Trên `client-fedora` (`laptop`), mở giao tiếp nội bộ cho riêng interface `wg0` trong `firewalld` để 4 máy còn lại có thể ping/kết nối ngược tới `10.100.0.10`:

```bash
sudo firewall-cmd --zone=trusted --add-interface=wg0 --permanent
sudo firewall-cmd --reload
```

**Kiểm tra thông mạng 5 máy & SSH qua `wg0` (bắt buộc mở Terminal #2 và chạy đạt trước khi sang Bước 1.4):**

```bash
# 1. Xác nhận cả 5 máy thấy nhau qua wg0 (.1 server, .2 client-01, .3 client-02, .10 client-fedora, .11 client-phone)
for ip in 10.100.0.1 10.100.0.2 10.100.0.3 10.100.0.10 10.100.0.11; do
  ping -c 2 -W 1 "$ip"
done

# 2. Từ client-01 kiểm tra đường LAN trực tiếp tới client-02: RTT < 1ms
ping -c 3 10.100.0.3
traceroute -n 10.100.0.3

# 3. Từ client-fedora kiểm tra SSH tới server, client-01 & client-02 qua wg0
ssh -p 61022 helios@10.100.0.1 "hostname && free -h"
ssh -p 61122 helios@10.100.0.2 "hostname && free -h"
ssh -p 61222 helios@10.100.0.3 "hostname && free -h"
```

### 1.4. Kiểm chứng Host Firewall, Khởi động lại Node & Lọc cổng Cloud NSG

1. **Mở phiên SSH qua `wg0` tới 3 node để xác minh `ufw`, `ip_forward`, `FORWARD ACCEPT` và các cổng đang lắng nghe:**

```bash
# Trên laptop (Fedora): mở 3 terminal/tab SSH trực tiếp qua wg0
ssh -p 61022 helios@10.100.0.1   # server-01
ssh -p 61122 helios@10.100.0.2   # worker-01
ssh -p 61222 helios@10.100.0.3   # worker-02
```

Chạy kiểm tra bên trong từng phiên SSH vừa mở:

```bash
sudo ufw status || true
cat /proc/sys/net/ipv4/ip_forward
sudo iptables -L FORWARD -n | head -n 5
sudo ss -tlnp
```

2. **Khởi động lại các node Linux (`server-01`, `worker-01`, `worker-02`) và `laptop` để kiểm chứng tự phục hồi sau reboot:**

```bash
sudo reboot
```

3. **Kiểm chứng sau khi các máy khởi động lại:**

Nạp lại `export VPS_PUBLIC_IP="<IP_PUBLIC_VPS_THUC_TE>"` trên `laptop`, kiểm tra `sudo wg show` và `lsmod | grep -E "br_netfilter|iscsi_tcp"` trên worker, sau đó xác minh thông mạng `wg0` và Cloud NSG:

```bash
# 1. Xác nhận wg0 tự bật lại và cả 5 peer thấy nhau hai chiều
for ip in 10.100.0.1 10.100.0.2 10.100.0.3 10.100.0.10 10.100.0.11; do
  ping -c 2 -W 1 "$ip"
done

# 2. Kiểm tra Cloud Firewall (NSG) VPS từ laptop:
# Kỳ vọng: 61022 open; 80,443 closed (Traefik cài ở Pha 3); 6443,9100,10250 filtered
nmap -Pn -p 61022,80,443,6443,9100,10250 vps.helios.id.vn
```

---

## Pha 2: Khởi tạo Kubernetes `v1.37.1` (`kubeadm`) & Cilium eBPF + Hubble UI

### 2.1. Tắt Swap, Nạp `overlay`, Cài `containerd.io` `2.3.6` & Gói Kubernetes `v1.37.1` (Cả 3 Node)

Thực hiện tuần tự các lệnh sau trên **tất cả 3 node** (`server-01`, `worker-01`, `worker-02`):

1. **Tắt Swap vĩnh viễn** (`kubelet` yêu cầu tắt hoàn toàn Swap để lập lịch chính xác):

```bash
sudo swapoff -a
sudo sed -i '/\bswap\b/ s/^/#/' /etc/fstab
free -h
# Kỳ vọng dòng Swap hiển thị: 0B
```

2. **Nạp module kernel `overlay` cùng `br_netfilter`** và lưu cấu hình tự nạp sau reboot:

```bash
sudo modprobe overlay
sudo modprobe br_netfilter
printf "overlay\nbr_netfilter\n" | sudo tee /etc/modules-load.d/k8s.conf
```

3. **Cài đặt `containerd.io` `2.3.6` (tương thích Kubernetes `v1.37`), khóa nâng cấp tự động và bật `SystemdCgroup = true`:**

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg apt-transport-https
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
apt-cache madison containerd.io | grep "2.3.6"
sudo apt-get install -y --allow-downgrades containerd.io=2.3.6-*
sudo apt-mark hold containerd.io

# Sinh cấu hình mặc định cho containerd 2.x (version = 3) và bật SystemdCgroup = true
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl enable --now containerd
sudo systemctl restart containerd

# Xác minh phiên bản 2.3.6 và SystemdCgroup = true
containerd --version
grep -n "SystemdCgroup" /etc/containerd/config.toml
```

4. **Cài đặt `kubelet`, `kubeadm`, `kubectl` `v1.37.1` từ kho chính thức `pkgs.k8s.io` và khóa nâng cấp tự động:**

```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.37/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.37/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

sudo apt-get update
apt-cache madison kubeadm | grep "1.37.1"
sudo apt-get install -y kubelet=1.37.1-* kubeadm=1.37.1-* kubectl=1.37.1-*
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable kubelet
```

### 2.2. Tạo khóa mã hóa `etcd` (`aescbc`) & Khởi tạo Control Plane (`kubeadm init`) trên `server-01`

1. **Trên `server-01` — Sinh khóa `EncryptionConfiguration` (`aescbc`) bảo vệ `Secret` lưu trong `etcd`:**

Tham khảo mẫu [kubeadm-config/encryption-config.example.yaml](./kubeadm-config/encryption-config.example.yaml), sinh khóa ngẫu nhiên 32-byte và ghi ra `/etc/kubernetes/enc/enc.yaml` (*tuyệt đối không commit khóa thật lên Git và phải sao lưu bản sao ra ngoài `laptop`*):

```bash
# Trên server-01
sudo mkdir -p /etc/kubernetes/enc
head -c 32 /dev/urandom | base64
# Copy nội dung mẫu từ kubeadm-config/encryption-config.example.yaml vào /etc/kubernetes/enc/enc.yaml
# và thay <BASE64_32_BYTE_KEY> bằng chuỗi base64 vừa sinh
sudo vim /etc/kubernetes/enc/enc.yaml
sudo chmod 600 /etc/kubernetes/enc/enc.yaml
```

2. **Trên `laptop` — Xuất file [kubeadm-config/init-server-01.yaml](./kubeadm-config/init-server-01.yaml) đã điền `$VPS_PUBLIC_IP`:**

```bash
# Trên laptop (nếu mở terminal mới: export VPS_PUBLIC_IP="<IP_PUBLIC_VPS_THUC_TE>")
sed "s|<VPS_PUBLIC_IP>|${VPS_PUBLIC_IP:?Can export VPS_PUBLIC_IP truoc}|g" kubeadm-config/init-server-01.yaml
```

3. **Trên `server-01` — Nạp `/etc/kubernetes/kubeadm-init.yaml`, chạy `kubeadm init` (`kubeadm.k8s.io/v1beta4`, bỏ `kube-proxy` cho Cilium) & chuẩn bị `kubeconfig`:**

```bash
# Trên server-01: dán nội dung vừa xuất vào /etc/kubernetes/kubeadm-init.yaml
sudo mkdir -p /etc/kubernetes
sudo vim /etc/kubernetes/kubeadm-init.yaml

# Tải trước các image hệ thống v1.37.1 và khởi tạo Control Plane
sudo kubeadm config images pull --config=/etc/kubernetes/kubeadm-init.yaml
sudo kubeadm init --config=/etc/kubernetes/kubeadm-init.yaml

# Xuất admin.conf sang ~/.kube/config cho user hiện tại trên server-01
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Lấy token & CA hash để dùng cho Bước 2.3 (join workers)
kubeadm token create --print-join-command
```

### 2.3. Join Worker Nodes (`worker-01` & `worker-02`), Kéo `kubeconfig` & Gán nhãn Longhorn

1. **Trên `worker-01` và `worker-02` — Tạo `/etc/kubernetes/kubeadm-join.yaml` và join cụm:**

Sao chép [kubeadm-config/join-worker-01.yaml](./kubeadm-config/join-worker-01.yaml) (cho `worker-01`) hoặc [kubeadm-config/join-worker-02.yaml](./kubeadm-config/join-worker-02.yaml) (cho `worker-02`), thay `<BOOTSTRAP_TOKEN>` và `<DISCOVERY_CA_CERT_HASH>` lấy từ `kubeadm token create --print-join-command`, sau đó chạy `kubeadm join`:

```bash
# Trên worker-01 và worker-02
sudo mkdir -p /etc/kubernetes
sudo vim /etc/kubernetes/kubeadm-join.yaml
sudo kubeadm join --config=/etc/kubernetes/kubeadm-join.yaml
```

> [!NOTE]
> Nhãn Longhorn `node.longhorn.io/create-default-disk=true` được cấp qua `kubectl` ở bước kế tiếp để tuân thủ `NodeRestriction` plugin.

2. **Trên `laptop` (Fedora) — Kéo `kubeconfig` an toàn, gán nhãn Longhorn & kiểm tra Node:**

```bash
# Trên laptop
mkdir -p ~/.kube
ssh -p 61022 helios@10.100.0.1 "cat ~/.kube/config" > ~/.kube/config
chmod 600 ~/.kube/config

# Gán nhãn tạo disk mặc định cho Longhorn trên 2 worker
kubectl label node worker-01 worker-02 node.longhorn.io/create-default-disk=true --overwrite

# Xác nhận node đã join (trạng thái NotReady là đúng vì chưa cài CNI Cilium)
kubectl get nodes -o wide --show-labels
```

### 2.4. Cài đặt Cilium eBPF CNI/LB & Hubble UI

Từ `laptop` Fedora (chạy tại thư mục gốc repository):

```bash
helm repo add cilium https://helm.cilium.io/
helm repo update

helm install cilium cilium/cilium \
  --namespace kube-system \
  -f platform-core/cilium/values.yaml

kubectl -n kube-system rollout status ds/cilium --timeout=300s
# (Nếu mở terminal mới: export VPS_PUBLIC_IP="<IP_PUBLIC_VPS_THUC_TE>")
sed "s|<VPS_PUBLIC_IP>|${VPS_PUBLIC_IP:?Can export VPS_PUBLIC_IP truoc}|g" platform-core/cilium/lb-ip-pool.yaml | kubectl apply -f -
```

**Kiểm tra:**

```bash
kubectl get nodes -o wide
cilium status
# Xác nhận 3/3 Ready, INTERNAL-IP là 10.100.0.1..3,
# server-01 có taint node-role.kubernetes.io/control-plane:NoSchedule và kubeProxyReplacement active
```

---

## Pha 3: Distributed Storage (Longhorn), HashiCorp Vault + ESO & Edge Gateway (Traefik HA)

### 3.1. Cài đặt Longhorn Distributed Block Storage

Cài đặt Longhorn trước để cấp phát PVC `longhorn` (`replicas: 2` qua LAN 1Gbps) cho HashiCorp Vault, Prometheus, Grafana và Redis:

```bash
# Đảm bảo 2 worker có đủ nhãn zone (global.nodeSelector) và nhãn tạo disk mặc định (idempotent)
kubectl label node worker-01 worker-02 \
  topology.kubernetes.io/zone=onprem-lan \
  node.longhorn.io/create-default-disk=true --overwrite

helm repo add longhorn https://charts.longhorn.io
helm repo update

helm install longhorn longhorn/longhorn \
  --namespace longhorn-system \
  --create-namespace \
  -f platform-core/longhorn/values.yaml

kubectl -n longhorn-system get pods -w
kubectl -n longhorn-system get pods -o wide
```

Mở tạm Longhorn UI để kiểm tra nhận diện IP Node & Ổ đĩa:

```bash
kubectl port-forward svc/longhorn-frontend 8080:80 -n longhorn-system
```

Truy cập `http://127.0.0.1:8080` -> mục **Node**: xác nhận `worker-01` có IP `10.100.0.2` (`199GB`), `worker-02` có IP `10.100.0.3` (`461GB` trên `/var/lib/longhorn`), trạng thái **Schedulable / Ready**.

### 3.2. Cài đặt HashiCorp Vault, Bootstrap Kubernetes Auth & External Secrets Operator (ESO)

1. **Cài HashiCorp Vault (Standalone, Longhorn PVC `2Gi`, tắt `injector`) & Khởi tạo 1 khóa duy nhất:**

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  -f platform-core/vault/values.yaml

# Đợi vault-0 ở trạng thái 0/1 Running (bình thường khi chưa init/unseal) rồi kiểm tra status
kubectl -n vault get pods -w
kubectl exec -n vault vault-0 -- vault status || true

# Khởi tạo Vault với 1 khóa duy nhất (-key-shares=1 -key-threshold=1) và lưu ngoại tuyến
kubectl exec -n vault vault-0 -- vault operator init -key-shares=1 -key-threshold=1 \
  > ~/vault-init-keys.txt
chmod 600 ~/vault-init-keys.txt
cat ~/vault-init-keys.txt
```

> **BẮT BUỘC:** Sao lưu `~/vault-init-keys.txt` (`Unseal Key 1` và `Initial Root Token`) vào trình quản lý mật khẩu ngoại tuyến; **tuyệt đối không commit lên Git**.

Mở khóa Vault (chỉ 1 lệnh duy nhất), bật KV v2 & Kubernetes Auth, nạp 3 bí mật (`traefik`, `monitoring`, `app-prod`) và tạo 3 cặp Policy/Role tách biệt theo từng namespace:

```bash
kubectl exec -n vault vault-0 -- vault operator unseal "<UNSEAL_KEY>"
kubectl -n vault wait --for=condition=Ready pod/vault-0 --timeout=120s

export VAULT_TOKEN="<INITIAL_ROOT_TOKEN>"
export GRAFANA_USER="admin"
export GRAFANA_PASS="<STRONG_GRAFANA_PASSWORD>"
export REDIS_PASS="<STRONG_REDIS_PROD_PASSWORD>"

# 1. Bật KV v2 (secret/) & Kubernetes Auth
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" vault secrets enable -path=secret kv-v2
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" vault auth enable kubernetes
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443"

# 2. Nạp 3 Secret chuẩn vào Vault KV v2
jq -n --rawfile crt secrets/tls.crt --rawfile key secrets/tls.key '{"tls.crt": $crt, "tls.key": $key}' | \
  kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault kv put secret/traefik/cloudflare-origin-tls -

jq -n --arg user "$GRAFANA_USER" --arg pass "$GRAFANA_PASS" '{"admin-user": $user, "admin-password": $pass}' | \
  kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault kv put secret/monitoring/grafana-admin -

jq -n --arg pass "$REDIS_PASS" '{"password": $pass}' | \
  kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault kv put secret/app-prod/redis-auth -

# 3. Tạo 3 Vault Policy tách biệt (Least-Privilege)
kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault policy write eso-traefik-policy - <<'EOF'
path "secret/data/traefik/*" { capabilities = ["read"] }
EOF

kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault policy write eso-monitoring-policy - <<'EOF'
path "secret/data/monitoring/*" { capabilities = ["read"] }
EOF

kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault policy write eso-app-prod-policy - <<'EOF'
path "secret/data/app-prod/*" { capabilities = ["read"] }
EOF

# 4. Tạo 3 Kubernetes Auth Role gắn chặt ServiceAccount & Namespace
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault write auth/kubernetes/role/eso-traefik \
    bound_service_account_names=eso-vault-auth \
    bound_service_account_namespaces=traefik \
    policies=eso-traefik-policy ttl=15m

kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault write auth/kubernetes/role/eso-monitoring \
    bound_service_account_names=eso-vault-auth \
    bound_service_account_namespaces=monitoring \
    policies=eso-monitoring-policy ttl=15m

kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault write auth/kubernetes/role/eso-app-prod \
    bound_service_account_names=eso-vault-auth \
    bound_service_account_namespaces=app-prod \
    policies=eso-app-prod-policy ttl=15m

unset VAULT_TOKEN GRAFANA_USER GRAFANA_PASS REDIS_PASS
```

> Vault UI không expose ra Internet; khi cần xem/sửa/rotate secret qua Web UI, dùng `kubectl port-forward -n vault svc/vault 8200:8200` (chi tiết xem tại [platform-core/vault/README.md](./platform-core/vault/README.md)).

2. **Cài External Secrets Operator (ESO) qua OCI Registry (`ghcr.io`) & Đồng bộ 2 Secret Tầng 1 (`traefik`, `monitoring`):**

```bash
helm install external-secrets oci://ghcr.io/external-secrets/charts/external-secrets \
  --namespace external-secrets \
  --create-namespace \
  -f platform-core/external-secrets/values.yaml

kubectl -n external-secrets rollout status deploy/external-secrets --timeout=180s
kubectl -n external-secrets rollout status deploy/external-secrets-webhook --timeout=180s
kubectl -n external-secrets rollout status deploy/external-secrets-cert-controller --timeout=180s

# Tạo sẵn 2 namespace nền tảng và apply ServiceAccount + SecretStore + ExternalSecret
kubectl create namespace traefik --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -f platform-core/traefik/vault-secretstore.yaml \
  -f platform-core/traefik/cloudflare-origin-tls-externalsecret.yaml
kubectl apply -f platform-core/monitoring/vault-secretstore.yaml \
  -f platform-core/monitoring/grafana-admin-externalsecret.yaml

# Xác nhận ESO đã đồng bộ thành công 2 Secret Tầng 1 (STATUS = SecretSynced, READY = True)
kubectl get secretstore,externalsecret -A
kubectl get secret cloudflare-origin-tls -n traefik
kubectl get secret grafana-admin-secret -n monitoring
```

### 3.3. Cài đặt Traefik HA (`replicas: 2`)

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update

helm install traefik traefik/traefik \
  --namespace traefik \
  -f platform-core/traefik/values.yaml

kubectl apply -f platform-core/traefik/tlsstore.yaml
kubectl apply -f platform-core/traefik/metrics-service.yaml
kubectl get svc,pods -n traefik -o wide
```

> Xác nhận Service `traefik` nhận `TYPE=LoadBalancer` và `EXTERNAL-IP` khớp với `$VPS_PUBLIC_IP` (`<VPS_PUBLIC_IP>`), đồng thời 2 Pod Traefik chạy trên 2 worker khác nhau (`worker-01` và `worker-02`).

---

## Pha 4: Monitoring Stack, Kyverno Policy, ArgoCD & Kích hoạt CI/GHCR

### 4.1. Cài đặt Monitoring Stack (`kube-prometheus-stack`), Kyverno (`ValidatingPolicies`) & ArgoCD

1. **Cài Monitoring Stack & `traefik-metrics` ServiceMonitor** (namespace `monitoring` đã có sẵn `grafana-admin-secret` đồng bộ từ Vault qua ESO ở Pha `3.2`):

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f platform-core/monitoring/values.yaml

kubectl -n monitoring rollout status deploy/monitoring-grafana --timeout=300s
kubectl -n monitoring get pods -o wide
kubectl apply -f platform-core/monitoring/servicemonitors/
```

2. **Cài Kyverno Engine (`admissionController`) & 4 `ValidatingPolicy`** (Chart `3.10.0` / Kyverno `v1.20.0`, dùng biểu thức CEL trên `policies.kyverno.io/v1`; chỉ `Deny` trên namespace có nhãn `policy-tier=hardened`, không chặn các namespace hệ thống):

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

helm install kyverno kyverno/kyverno \
  --version 3.10.0 \
  --namespace kyverno \
  --create-namespace \
  -f platform-core/kyverno/values.yaml

kubectl -n kyverno rollout status deploy/kyverno-admission-controller --timeout=300s
kubectl -n kyverno get pods -o wide
kubectl apply -f platform-core/kyverno/policies/
kubectl get validatingpolicy
```

3. **Cài ArgoCD (chuyên trách GitOps cho Tầng 2 `app-prod`) & lấy mật khẩu `admin`:**

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  -f platform-core/argocd/values.yaml

kubectl -n argocd rollout status deploy/argocd-server --timeout=300s
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
```

### 4.2. Bật `ServiceMonitor` trên Cilium/Hubble, Longhorn & ArgoCD

Vì `kube-prometheus-stack` đã cài xong Prometheus CRDs (`monitoring.coreos.com/v1`) ở bước `4.1`, chạy `helm upgrade` bật `serviceMonitor.enabled=true`:

```bash
# Cilium + Hubble ServiceMonitors
helm upgrade cilium cilium/cilium \
  --namespace kube-system \
  -f platform-core/cilium/values.yaml \
  --set prometheus.serviceMonitor.enabled=true \
  --set hubble.metrics.serviceMonitor.enabled=true

# Longhorn ServiceMonitor
helm upgrade longhorn longhorn/longhorn \
  --namespace longhorn-system \
  -f platform-core/longhorn/values.yaml \
  --set metrics.serviceMonitor.enabled=true

# ArgoCD ServiceMonitors
helm upgrade argocd argo/argo-cd \
  --namespace argocd \
  -f platform-core/argocd/values.yaml \
  --set server.metrics.serviceMonitor.enabled=true \
  --set controller.metrics.serviceMonitor.enabled=true \
  --set repoServer.metrics.serviceMonitor.enabled=true
```

**Kiểm tra Monitoring & Kyverno:**

```bash
kubectl -n monitoring get pods,pvc -o wide
kubectl get servicemonitor -A
kubectl get validatingpolicy
# Xác nhận 4 ValidatingPolicy của Kyverno đã áp dụng (validationActions: Deny)
```

### 4.3. Đẩy mã nguồn lên Public GitHub & Kích hoạt CI/GHCR (`ci.yml`)

Sau khi toàn bộ Platform Core Tầng 1 (`0.1` $\rightarrow$ `4.2`) đã vận hành ổn định, đẩy mã nguồn lên GitHub remote để kích hoạt CI build image đầu tiên cho Tầng 2 (`app-prod`):

1. Trên GitHub Repository (`https://github.com/helios-ryuu/devsecops-gitops-with-k8s`), vào **Settings -> Actions -> General -> Workflow permissions**:
   - Chọn **Read and write permissions** (bắt buộc để `ci.yml` đẩy image lên GHCR và pull image khi quét định kỳ).
2. Cấu hình **Fine-grained PAT (`GITOPS_TOKEN`)** để bước cập nhật tag `[skip ci]` vượt qua Ruleset nhánh `main` theo đúng nguyên tắc tối thiểu đặc quyền:
   - Trên tài khoản GitHub Admin, vào **Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token**:
     - **Token name \*:** `devsecops-gitops-ci-push` *(tên mô tả trên GitHub, có thể đặt tùy ý)*.
     - **Expiration \*:** `90 days` *(hoặc chọn mốc thời gian phù hợp kỳ bảo vệ đồ án)*.
     - **Repository access:** chọn **Only select repositories** $\rightarrow$ `devsecops-gitops-with-k8s`.
     - **Repository permissions:** đặt **Contents: Read and write** *(giữ `Metadata: Read-only`)*.
   - Lưu token vừa tạo vào Repository **Settings -> Secrets and variables -> Actions -> New repository secret** với tên **`GITOPS_TOKEN`**.
   - Trong **Settings -> Rules -> Rulesets** của nhánh `main`, giữ rule bảo vệ PR (*Require a pull request before merging*) và đảm bảo **Bypass list** có **Repository admin** (*Always allow*) để tài khoản Admin và `GITOPS_TOKEN` đẩy commit tag `[skip ci]` hợp lệ.
3. Kiểm tra `git status` để chắc chắn không chứa IP VPS thật hay các tệp nhạy cảm trong `secrets/` (`tls.crt`, `tls.key`) và `~/vault-init-keys.txt` *(các manifest `SecretStore`/`ExternalSecret` chỉ chứa tham chiếu đường dẫn Vault, hoàn toàn an toàn khi lưu trên Git)*, sau đó stage toàn bộ thay đổi, commit và push lên nhánh `main`:

```bash
git status
git add -A
git commit -m "feat(platform): complete phase 0-4 hybrid k8s core & devsecops pipeline"
git push -u origin main
```

4. Kiểm tra tab **Actions -> `CI & DevSecOps Gate`** chạy thành công *(nếu commit vừa push không sửa file thuộc `paths` kích hoạt của `ci.yml`, bấm **Run workflow** trên workflow này)*:
   - Pipeline tự kiểm tra Gitleaks, Trivy FS, `kubeconform` + Trivy Config, build & push image `ghcr.io/helios-ryuu/devsecops-gitops-with-k8s:<NEW_SHA>` lên GHCR, quét Trivy Image Gate (`HIGH,CRITICAL`) và tự động cập nhật `image:` + `APP_VERSION` vào `project-nt548/k8s-manifests/deployment.yaml`.
   - Kiểm tra tab **Packages -> `devsecops-gitops-with-k8s` -> Package settings -> Change visibility -> Public** (bắt buộc nếu package mới tạo ở chế độ Private, vì `deployment.yaml` không dùng `imagePullSecrets`).
   - Kéo commit tag mới về máy quản trị:

```bash
git pull --rebase origin main
```

---

## Pha 5: Triển khai Tầng 2 (`project-nt548`), Zero Trust & Vận hành CI/CD

### 5.1. Kích hoạt Application Tầng 2 (`app-prod`) & Đồng bộ `redis-auth-secret` từ Vault

Vì `secret/app-prod/redis-auth` và role `eso-app-prod` đã được cấu hình sẵn trong Vault ở Pha `3.2`, bạn chỉ cần kích hoạt Application Tầng 2 — ArgoCD sẽ tự tạo namespace `app-prod` kèm nhãn `policy-tier=hardened`, đồng bộ toàn bộ `project-nt548/k8s-manifests/` (bao gồm `ServiceAccount/eso-vault-auth`, `SecretStore/vault-backend` và `ExternalSecret/redis-auth-secret`), và ESO sẽ tự đồng bộ `redis-auth-secret` từ Vault:

```bash
kubectl apply -f project-nt548/app-prod.yaml
kubectl get applications -n argocd -w
kubectl get ns app-prod --show-labels
# Xác nhận namespace app-prod mang nhãn policy-tier=hardened
kubectl -n app-prod get secretstore,externalsecret,secret,pods,pvc,svc,ingress
```

*(ArgoCD đồng bộ `app-prod` với image `<NEW_SHA>` đã build từ Bước `4.3` cùng `redis-auth-externalsecret.yaml`; nếu thấy Pod báo `CreateContainerConfigError` trong vài giây đầu lúc chờ ESO đồng bộ Secret từ Vault, kubelet sẽ tự khởi động lại và lên `Running`.)*

### 5.2. Bảo vệ tên miền quản trị với Cloudflare Zero Trust Access

Trong **Cloudflare Zero Trust -> Access -> Applications**:
1. Tạo Access Policy `K8s Admin` (Action: **Allow**, Include: Emails nhóm quản trị viên, Authentication: **One-time PIN**).
2. Gán policy lên 3 tên miền quản trị:
   - `argocd.helios.id.vn`
   - `grafana.helios.id.vn`
   - `hubble.helios.id.vn`

### 5.3. Vận hành Phát hành Continuous Delivery (`RollingUpdate`) & Nightly GHCR Audit (`0 0 * * *`)

1. **Cập nhật & Rollback ứng dụng (`ci.yml` + ArgoCD `RollingUpdate`):**
   - Mỗi khi push cập nhật trong `app/` lên `main`, `ci.yml` chạy đầy đủ DevSecOps Gates, đẩy image `<NEW_SHA>` lên GHCR và cập nhật `image:` + `APP_VERSION` trong `project-nt548/k8s-manifests/deployment.yaml`.
   - ArgoCD tự động đồng bộ `web-deployment` (`replicas: 2`, `RollingUpdate` `maxUnavailable: 0, maxSurge: 1`) giúp nâng cấp zero-downtime:
     ```bash
     kubectl -n app-prod rollout status deploy/web-deployment
     curl -i https://nt548.helios.id.vn/ready
     ```
   - **Rollback tức thì:** Chạy `git pull --rebase origin main && git revert HEAD --no-edit && git push` để ArgoCD đưa `web-deployment` quay về phiên bản ổn định trước đó.
2. **Nightly GHCR Image Audit (`nightly-audit.yml`, `0 0 * * *`, `0 MB` RAM cụm):** Hằng đêm lúc `00:00 UTC` (hoặc chạy tay từ **Actions -> `Nightly Active GHCR & Base Image Audit` -> Run workflow**), workflow tách riêng tự pull các image đang chạy trong `deployment.yaml` & `redis-statefulset.yaml` về runner và quét Trivy CVE `HIGH,CRITICAL`.

---

## Pha 6: Kiểm chứng tổng thể, Demo & Thu hồi Tầng 2

### 6.1. Checklist kiểm chứng trước khi bảo vệ đồ án

```bash
# 1. Kiểm tra RAM thực tế còn trống trên VPS (6GB) & 2 Worker (8GB/máy)
ssh -p 61022 helios@10.100.0.1 "free -h"
ssh -p 61122 helios@10.100.0.2 "free -h"
ssh -p 61222 helios@10.100.0.3 "free -h"
kubectl top nodes

# 2. Kiểm tra bảo mật cổng từ bên ngoài Internet
nmap -Pn -p 61022,80,443,6443,9100,10250 vps.helios.id.vn

# 3. Kiểm tra toàn cụm Core & Project
kubectl get nodes -o wide
kubectl get applications -n argocd
kubectl get validatingpolicy
kubectl get deployments,pods,svc,networkpolicy,ingress -n app-prod

# 4. Kiểm tra web thực tế
curl -i https://nt548.helios.id.vn/healthz
curl -i https://nt548.helios.id.vn/ready
```

### 6.2. Trình diễn 5 kịch bản Demo cho Hội đồng

```bash
./scripts/demo.sh        # Menu chọn từng kịch bản 1..5 hoặc 'a'
./scripts/demo.sh --all  # In toàn bộ 5 kịch bản
```

### 6.3. Thu hồi sạch Tầng 2 sau khi bảo vệ đồ án (giữ nguyên Tầng 1 Platform Core)

```bash
kubectl delete -f project-nt548/app-prod.yaml
kubectl delete namespace app-prod
kubectl get ns | grep app-prod
# Xóa Application trước để ArgoCD dừng reconcile và xóa tài nguyên con,
# sau đó xóa namespace app-prod để dọn sạch PVC Longhorn (1Gi) và Secret còn lại;
# toàn bộ cụm chuẩn Tầng 1 (Cilium, Longhorn, HashiCorp Vault + ESO, Traefik HA + cloudflare-origin-tls,
# Monitoring + grafana-admin-secret, ArgoCD, Kyverno) vẫn giữ nguyên 100%.
```

*(Tùy chọn trên Cloudflare DNS: xóa hoặc tắt bản ghi CNAME `nt548.helios.id.vn` sau khi thu hồi Tầng 2.)*
