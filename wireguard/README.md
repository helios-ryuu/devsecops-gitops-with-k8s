# Cấu hình WireGuard (`wg0`) & Chuẩn bị Host

Mạng `wg0` (`10.100.0.0/24`, UDP `51820`, `MTU 1420`) dùng quy ước tên **`server`** (VPS Hub) và **`client`** (4 máy kết nối: `client-01`, `client-02`, `client-fedora`, `client-phone`) theo mô hình Hub-and-Spoke kết hợp Direct LAN giữa `client-01` $\leftrightarrow$ `client-02` để cả 5 máy đều nhìn thấy và giao tiếp hai chiều với nhau.

## 1. Quy hoạch IP

| WireGuard Role | Host / Kubernetes Role | `wg0` IP | SSH (`helios`) | File mẫu & Định tuyến |
|---|---|---|---|---|
| `server` | `heliosvps` (`server-01`, 6GB RAM) | `10.100.0.1/24` | `61022/tcp` | [wg0.server.conf.example](./wg0.server.conf.example) — Hub (`<VPS_PUBLIC_IP>`, `vps.helios.id.vn:51820` DNS Only) |
| `client-01` | `worker-01` (8GB RAM, `199GB`) | `10.100.0.2/24` | `61122/tcp` | [wg0.client-01.conf.example](./wg0.client-01.conf.example) — Hub `10.100.0.0/24` + Direct LAN `client-02` (`/32`) |
| `client-02` | `worker-02` (8GB RAM, `461GB`) | `10.100.0.3/24` | `61222/tcp` | [wg0.client-02.conf.example](./wg0.client-02.conf.example) — Hub `10.100.0.0/24` + Direct LAN `client-01` (`/32`) |
| `client-fedora` | `laptop` (Fedora, `kubectl`) | `10.100.0.10/32` | — | [wg0.client-fedora.conf.example](./wg0.client-fedora.conf.example) — Hub `10.100.0.0/24` |
| `client-phone` | `phone` (Mobile / Termius) | `10.100.0.11/32` | — | [wg0.client-phone.conf.example](./wg0.client-phone.conf.example) — Hub `10.100.0.0/24` |

## 2. Chuẩn bị Gói phụ thuộc & Sysctl trên Host

Trên **cả 3 node** (`server-01`, `worker-01`, `worker-02`), cài gói phụ thuộc, nạp module `br_netfilter` và thiết lập thông số kernel chuẩn trong `/etc/sysctl.d/90-k8s.conf` *(bảo đảm không có file `*.conf` khác trong `/etc/sysctl.d/` đặt `rp_filter = 1` ghi đè theo thứ tự chữ cái)*:

```bash
sudo apt-get update && sudo apt-get install -y wireguard wireguard-tools curl jq vim

sudo modprobe br_netfilter
echo "br_netfilter" | sudo tee /etc/modules-load.d/k8s.conf

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
sysctl net.ipv4.ip_forward net.ipv4.conf.all.rp_filter net.ipv4.conf.default.rp_filter net.bridge.bridge-nf-call-iptables
```

Riêng trên **2 Worker (`worker-01` & `worker-02`)** để chuẩn bị Longhorn:

```bash
sudo apt-get install -y open-iscsi nfs-common
sudo modprobe iscsi_tcp
echo "iscsi_tcp" | sudo tee /etc/modules-load.d/longhorn-iscsi.conf
sudo systemctl enable --now iscsid
```

Cả **`worker-01`** và **`worker-02`** đều dùng trực tiếp đường dẫn mặc định `/var/lib/longhorn` trên phân vùng `/` (`461GB` trống trên `worker-02`, `199GB` trên `worker-01`).

## 3. Chính sách Host Firewall, Cloud NSG & Bảo mật LAN

> Xem quy trình thực thi an toàn SSH tại [RUNBOOK.md](../RUNBOOK.md) (Bước `0.3` tắt host firewall trên OS, Bước `0.5` khóa VPS Cloud NSG và Bước `1.4` kiểm chứng lại trước khi cài `kubeadm`).

### Tắt `ufw` / `firewalld` trên cả 3 Node (`server-01`, `worker-01`, `worker-02`)

Không chạy `ufw`/`firewalld` song song với Cilium eBPF và WireGuard `wg0` để tránh xung đột bảng luật nhân Linux và không làm rơi gói ở chain `FORWARD`. Đồng thời giữ tắt `Cilium hostFirewall` do `wg0` là giao diện L3.

```bash
sudo sshd -T | grep -iE 'port|passwordauthentication|pubkeyauthentication'
sudo ufw disable || true
sudo systemctl disable --now ufw 2>/dev/null || true
sudo systemctl disable --now firewalld 2>/dev/null || true
sudo ufw status || true
sudo iptables -L -n
```

### Bảo vệ biên ngoài thay thế Host Firewall

1. **VPS `server` (`heliosvps` / `server-01`, SSH `61022/tcp`) — Khóa tại Cloud Firewall (NSG):**
   - **Chỉ mở Ingress IPv4 (`0.0.0.0/0`):** `61022/tcp` (SSH Admin), `80/tcp` (HTTP), `443/tcp` (HTTPS), `51820/udp` (WireGuard `wg0`) và `ICMP`.
   - **Xóa sạch wildcard Ingress cũ** (`IPv4 TCP 0.0.0.0/0`, `IPv4 UDP 0.0.0.0/0`, `IPv6 ::/0`) và giữ **Egress** mở. Các cổng `6443/tcp`, `9100/tcp`, `10250/tcp`, `8472/udp` bị chặn từ Internet tại tầng Cloud NSG.
2. **2 Worker tại nhà `client-01` (`worker-01`, `61122/tcp`) & `client-02` (`worker-02`, `61222/tcp`) trong LAN `10.10.10.0/24`:**
   - Tin cậy **Router NAT** (không port-forward WAN vào 2 worker), đặt **DHCP Reservation** trong `10.10.10.0/24` và bật **SSH Key-only** (`PasswordAuthentication no`).
   - *(Tùy chọn)* Có thể tách 2 worker sang VLAN hoặc dùng Wi-Fi khách riêng trên Router nếu mạng LAN nhà có nhiều thiết bị IoT/khách không tin cậy.

## 4. Sinh cặp khóa, Kích hoạt `wg0` & Thông mạng 5 Node

Thực hiện sinh khóa trên cả 4 máy Linux (`server`, `client-01`, `client-02`, `client-fedora`) và trên ứng dụng WireGuard của `client-phone`:

```bash
umask 077
sudo mkdir -p /etc/wireguard
wg genkey | sudo tee /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
# Copy file wg0.<role>.conf.example tương ứng và điền khóa + IP LAN bằng vim (hoặc import trên client-phone)
sudo vim /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf
sudo systemctl enable --now wg-quick@wg0
sudo wg show
```

> [!TIP]
> Trên `client-fedora` (Fedora Workstation dùng `firewalld` mặc định), đưa interface `wg0` vào vùng `trusted` để `server`, `client-01`, `client-02` và `client-phone` có thể ping/kết nối ngược vào `10.100.0.10`:
> ```bash
> sudo firewall-cmd --zone=trusted --add-interface=wg0 --permanent
> sudo firewall-cmd --reload
> ```

Xác minh 5 node thấy nhau (`server` `.1`, `client-01` `.2`, `client-02` `.3`, `client-fedora` `.10`, `client-phone` `.11`):

```bash
for ip in 10.100.0.1 10.100.0.2 10.100.0.3 10.100.0.10 10.100.0.11; do
  ping -c 2 -W 1 "$ip"
done
```

> [!NOTE]
> Sau khi mạng `wg0` và SSH tới `10.100.0.1..3` đã thông suốt, thực hiện **Bước `1.4`** trong [RUNBOOK.md](../RUNBOOK.md) để kiểm chứng firewall/`sysctl`, khởi động lại các node Linux & `laptop` và kiểm tra cổng Cloud NSG trước khi cài `kubeadm`.
