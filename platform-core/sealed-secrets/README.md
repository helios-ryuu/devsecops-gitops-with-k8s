# Hướng dẫn quản lý Bí mật bằng Bitnami Sealed Secrets (`kubeseal`)

## 1. Sao lưu Master Key ngay sau khi cài đặt controller

```bash
kubectl get secret -n kube-system \
  -l sealedsecrets.bitnami.com/sealed-secrets-key \
  -o yaml > ~/sealed-secrets-master-key.yaml
chmod 600 ~/sealed-secrets-master-key.yaml
```

> Lưu tệp `~/sealed-secrets-master-key.yaml` ở máy cá nhân hoặc trình quản lý mật khẩu; không commit tệp này lên Git. Vì controller mặc định tự xoay khóa mỗi 30 ngày (`720h`), nếu sau này chạy `kubeseal` lại hãy xuất cập nhật tệp backup và lưu thêm 3 giá trị gốc trong trình quản lý mật khẩu.

## 2. Niêm phong & áp dụng Secrets Tầng 1 — Cụm chuẩn (chạy ở Pha 2.5)

```bash
# Tạo sẵn 2 namespace nền tảng (riêng app-prod thuộc Tầng 2 để ArgoCD tự tạo kèm nhãn policy-tier=hardened ở Pha 5)
kubectl create namespace traefik monitoring --dry-run=client -o yaml | kubectl apply -f -

# 2.1 Cloudflare Origin TLS Secret (namespace traefik)
kubectl create secret tls cloudflare-origin-tls \
  --cert=secrets/tls.crt \
  --key=secrets/tls.key \
  -n traefik --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml \
  > platform-core/traefik/cloudflare-origin-tls-sealedsecret.yaml
kubectl apply -f platform-core/traefik/cloudflare-origin-tls-sealedsecret.yaml

# 2.2 Grafana Admin Secret (namespace monitoring)
kubectl create secret generic grafana-admin-secret \
  --from-literal=admin-user=admin \
  --from-literal=admin-password='<STRONG_GRAFANA_PASSWORD>' \
  -n monitoring --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml \
  > platform-core/monitoring/grafana-admin-sealedsecret.yaml
kubectl apply -f platform-core/monitoring/grafana-admin-sealedsecret.yaml
```

## 3. Niêm phong Secret Tầng 2 — Dự án NT548 (chạy ở Pha 5.1, trước khi apply `app-prod.yaml`)

```bash
# 3.1 Redis Auth Secret cho app-prod (không cần tạo namespace app-prod trước; push [skip ci] để ArgoCD tự sync & giải mã)
kubectl create secret generic redis-auth-secret \
  --from-literal=password='<STRONG_REDIS_PROD_PASSWORD>' \
  -n app-prod --dry-run=client -o yaml | \
  kubeseal --controller-name=sealed-secrets-controller --controller-namespace=kube-system --format yaml \
  > project-nt548/k8s-manifests/redis-auth-sealedsecret.yaml
```
