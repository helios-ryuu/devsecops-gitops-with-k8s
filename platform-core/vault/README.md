# Hướng dẫn quản lý Bí mật tập trung bằng HashiCorp Vault & External Secrets Operator (ESO)

Hệ thống quản lý toàn bộ bí mật tập trung bằng **HashiCorp Vault** (self-hosted trên Longhorn PVC `2Gi`, `replicas: 2` qua LAN `1Gbps`) kết hợp **External Secrets Operator (ESO)** sử dụng **Kubernetes Auth Method** (**Zero Static Secret**):

- Không lưu mật khẩu/chứng chỉ mã hóa tĩnh trên Git và không lưu `VAULT_TOKEN` dài hạn trong cụm.
- Mỗi namespace (`traefik`, `monitoring`, `app-prod`) có riêng 1 `ServiceAccount` (`eso-vault-auth`, `automountServiceAccountToken: false`), 1 `SecretStore` (namespace-scoped), 1 Vault Policy và 1 Vault Role chỉ đọc được đúng nhánh bí mật của namespace đó (`Least Privilege`).
- Vault UI **không expose ra Internet**, chỉ truy cập nội bộ từ máy quản trị (`laptop` qua WireGuard `wg0`) bằng `kubectl port-forward`.

---

## 1. Khởi tạo & Unseal Vault (1 khóa duy nhất)

Sau khi cài Vault bằng `platform-core/vault/values.yaml` và Pod `vault-0` ở trạng thái `Running`:

```bash
# Khởi tạo Vault với 1 khóa duy nhất (phù hợp mô hình homelab/đồ án 1 người vận hành)
kubectl exec -n vault vault-0 -- vault operator init -key-shares=1 -key-threshold=1 \
  > ~/vault-init-keys.txt
chmod 600 ~/vault-init-keys.txt
cat ~/vault-init-keys.txt
```

> **BẮT BUỘC:** Sao lưu `~/vault-init-keys.txt` (chứa `Unseal Key 1` và `Initial Root Token`) vào trình quản lý mật khẩu ngoại tuyến; **tuyệt đối không commit lên Git**.

Mở khóa Vault bằng 1 lệnh duy nhất:

```bash
kubectl exec -n vault vault-0 -- vault operator unseal "<UNSEAL_KEY>"
kubectl -n vault get pods
# Kỳ vọng: vault-0 chuyển sang 1/1 Ready
```

> **Lưu ý khi khởi động lại Worker:** Nếu `vault-0` bị restart sau khi reboot node hoặc bảo trì, các `Secret` Kubernetes đã sync trước đó vẫn tồn tại trong `etcd` để ứng dụng tiếp tục chạy bình thường, nhưng Vault sẽ về trạng thái `Sealed`. Chạy lại lệnh `vault operator unseal "<UNSEAL_KEY>"` để ESO tiếp tục đồng bộ/rotate bí mật.

---

## 2. Cấu hình KV v2, Nạp 3 Secret & Phân quyền Kubernetes Auth (Từng bước tường minh)

Khai báo biến môi trường tạm cho phiên làm việc hiện tại:

```bash
export VAULT_TOKEN="<INITIAL_ROOT_TOKEN>"
export GRAFANA_USER="admin"
export GRAFANA_PASS="<STRONG_GRAFANA_PASSWORD>"
export REDIS_PASS="<STRONG_REDIS_PROD_PASSWORD>"
```

### 2.1. Bật Secret Engine KV v2 & Kubernetes Auth

```bash
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" vault secrets enable -path=secret kv-v2
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" vault auth enable kubernetes
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443"
```

### 2.2. Nạp 3 Secret chuẩn vào Vault KV v2

```bash
# 1. Cloudflare Origin TLS (đọc từ secrets/tls.crt & secrets/tls.key qua jq để giữ nguyên định dạng PEM nhiều dòng)
jq -n --rawfile crt secrets/tls.crt --rawfile key secrets/tls.key '{"tls.crt": $crt, "tls.key": $key}' | \
  kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault kv put secret/traefik/cloudflare-origin-tls -

# 2. Grafana Admin
jq -n --arg user "$GRAFANA_USER" --arg pass "$GRAFANA_PASS" '{"admin-user": $user, "admin-password": $pass}' | \
  kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault kv put secret/monitoring/grafana-admin -

# 3. Redis Auth (app-prod)
jq -n --arg pass "$REDIS_PASS" '{"password": $pass}' | \
  kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
    vault kv put secret/app-prod/redis-auth -
```

### 2.3. Tạo 3 Vault Policy tách biệt (Least-Privilege)

```bash
# Policy cho traefik
kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault policy write eso-traefik-policy - <<'EOF'
path "secret/data/traefik/*" {
  capabilities = ["read"]
}
EOF

# Policy cho monitoring
kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault policy write eso-monitoring-policy - <<'EOF'
path "secret/data/monitoring/*" {
  capabilities = ["read"]
}
EOF

# Policy cho app-prod
kubectl exec -i -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault policy write eso-app-prod-policy - <<'EOF'
path "secret/data/app-prod/*" {
  capabilities = ["read"]
}
EOF
```

### 2.4. Tạo 3 Kubernetes Auth Role gắn chặt ServiceAccount & Namespace

```bash
kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault write auth/kubernetes/role/eso-traefik \
    bound_service_account_names=eso-vault-auth \
    bound_service_account_namespaces=traefik \
    policies=eso-traefik-policy \
    ttl=15m

kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault write auth/kubernetes/role/eso-monitoring \
    bound_service_account_names=eso-vault-auth \
    bound_service_account_namespaces=monitoring \
    policies=eso-monitoring-policy \
    ttl=15m

kubectl exec -n vault vault-0 -- env VAULT_TOKEN="$VAULT_TOKEN" \
  vault write auth/kubernetes/role/eso-app-prod \
    bound_service_account_names=eso-vault-auth \
    bound_service_account_namespaces=app-prod \
    policies=eso-app-prod-policy \
    ttl=15m
```

---

## 3. Cấu trúc đường dẫn bí mật & Phân quyền Least-Privilege

| Namespace | ServiceAccount & SecretStore | Vault Role / Policy | Đường dẫn Vault (KV v2) | K8s Secret đích |
|---|---|---|---|---|
| `traefik` | `eso-vault-auth` / `vault-backend` | `eso-traefik` / `eso-traefik-policy` | `secret/traefik/cloudflare-origin-tls` (`tls.crt`, `tls.key`) | `cloudflare-origin-tls` (`kubernetes.io/tls`) |
| `monitoring` | `eso-vault-auth` / `vault-backend` | `eso-monitoring` / `eso-monitoring-policy` | `secret/monitoring/grafana-admin` (`admin-user`, `admin-password`) | `grafana-admin-secret` (`Opaque`) |
| `app-prod` | `eso-vault-auth` / `vault-backend` | `eso-app-prod` / `eso-app-prod-policy` | `secret/app-prod/redis-auth` (`password`) | `redis-auth-secret` (`Opaque`) |

---

## 4. Truy cập Vault UI & Xoay vòng (Rotate) Bí mật

### Mở Vault UI nội bộ (không lộ ra Internet)

```bash
kubectl port-forward -n vault svc/vault 8200:8200
# Mở trình duyệt tại http://127.0.0.1:8200 và đăng nhập bằng Root Token
```

### Quy trình Rotate bí mật (ví dụ `redis-auth-secret`)

1. Cập nhật mật khẩu mới trên Vault UI (`secret/app-prod/redis-auth`) hoặc qua CLI:
   ```bash
   kubectl exec -n vault vault-0 -- env VAULT_TOKEN="<ROOT_TOKEN>" \
     vault kv put secret/app-prod/redis-auth password="<NEW_STRONG_REDIS_PASSWORD>"
   ```
2. Ép ESO đồng bộ ngay lập tức (hoặc chờ theo `refreshInterval`):
   ```bash
   kubectl annotate externalsecret redis-auth-secret -n app-prod \
     force-sync="$(date +%s)" --overwrite
   kubectl get externalsecret redis-auth-secret -n app-prod
   ```
3. Khởi động lại workload để nhận biến môi trường mới:
   ```bash
   kubectl rollout restart statefulset/redis deploy/web-deployment -n app-prod
   ```
