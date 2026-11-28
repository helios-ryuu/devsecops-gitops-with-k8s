#!/usr/bin/env bash
# ==============================================================================
# SCRIPT IN HƯỚNG DẪN KIỂM THỬ HỆ THỐNG: PLATFORM ENGINEERING & DEVSECOPS (ĐỒ ÁN NT548)
# Chức năng: CHỈ IN RA CÁC BƯỚC VÀ CÂU LỆNH MẪU ĐỂ THỰC HIỆN KIỂM THỬ HỆ THỐNG.
# Không thực thi bất kỳ câu lệnh nào lên Git hay cụm Kubernetes.
# ==============================================================================

set -euo pipefail

CYAN=$'\033[0;36m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
RED=$'\033[0;31m'
NC=$'\033[0m'

print_scenario_1() {
  cat <<EOF

${YELLOW}=== KỊCH BẢN 1: CI DEVSECOPS GATE (GITLEAKS, TRIVY, KUBECONFORM & TRIVY CONFIG) ===${NC}
${BLUE}Mục tiêu:${NC} Chứng minh pipeline GitHub Actions chặn mọi commit rò rỉ secret, dính CVE
          hoặc manifest K8s cấu hình không an toàn trước khi build & push lên GHCR.

${GREEN}[Bước 1] Mô phỏng vi phạm CVE trên app (ví dụ thêm lodash 4.17.20):${NC}
  $ cd app && pnpm add lodash@4.17.20 && cd ..
  $ git commit --only app/package.json app/pnpm-lock.yaml -m "test(security): inject vulnerable dependency lodash@4.17.20"
  $ git push origin main

${GREEN}[Bước 2] Hoặc mô phỏng kiểm tra manifest YAML thuần cục bộ (kubeconform & trivy config):${NC}
  $ kubeconform -strict -ignore-missing-schemas -summary project-nt548/k8s-manifests platform-core/kyverno/policies platform-core/monitoring/servicemonitors
  $ trivy config project-nt548/k8s-manifests --severity HIGH,CRITICAL --exit-code 1

${GREEN}[Bước 3] Quan sát trên tab GitHub Actions:${NC}
  - Job '2. Source CVE Scanning (Trivy FS)' hoặc '3. Kubernetes Manifest & Config Gate' dừng với Exit Code 1.
  - Job '4. Build, Trivy Image Gate & Deploy app-prod' bị bỏ qua -> app-prod trên cụm an toàn tuyệt đối.

${GREEN}[Bước 4] Dọn trạng thái test an toàn (chỉ khôi phục 2 file app/, không đụng local changes khác):${NC}
  $ git checkout HEAD~1 -- app/package.json app/pnpm-lock.yaml
  $ git commit --only app/package.json app/pnpm-lock.yaml -m "revert(security): remove vulnerable dependency lodash [skip ci]"
  $ git push origin main
  - (Tùy chọn) Đồng bộ lại node_modules cục bộ: cd app && pnpm install --frozen-lockfile && cd ..

EOF
}

print_scenario_2() {
  cat <<EOF

${YELLOW}=== KỊCH BẢN 2: KYVERNO ADMISSION POLICY ENFORCE (NHÃN policy-tier=hardened) ===${NC}
${BLUE}Mục tiêu:${NC} Chứng minh Kubernetes API Server từ chối ngay tại tầng Admission mọi Pod chạy quyền root,
          thiếu resource limits, dùng tag ':latest' hoặc từ registry không được cấp phép.

${GREEN}[Bước 1] Kiểm tra 4 ValidatingPolicy đang bật Enforce (Deny):${NC}
  $ kubectl get validatingpolicy
  $ kubectl get namespace app-prod --show-labels

${GREEN}[Bước 2] Thử tạo Pod vi phạm (image :latest, không securityContext, không limits):${NC}
  $ kubectl run test-violation -n app-prod --image=nginx:latest --restart=Never

${GREEN}[Bước 3] Kết quả kiểm chứng kỳ vọng:${NC}
  - Admission Webhook của Kyverno trả lỗi từ chối ngay lập tức, Pod không thể được lên lịch.

${GREEN}[Bước 4] Thử chạy lại một image không nằm trong whitelist (ví dụ alpine:3.20):${NC}
  $ kubectl run test-registry -n app-prod --image=alpine:3.20 --restart=Never -- sleep 30

EOF
}

print_scenario_3() {
  cat <<EOF

${YELLOW}=== KỊCH BẢN 3: GITOPS CONTINUOUS DELIVERY (ROLLINGUPDATE ZERO-DOWNTIME) & GIT ROLLBACK ===${NC}
${BLUE}Mục tiêu:${NC} Kiểm chứng nâng cấp ứng dụng không gián đoạn với Deployment web-deployment
          (replicas: 2, RollingUpdate maxUnavailable=0, maxSurge=1) và rollback tức thì bằng Git.

${GREEN}[Bước 1] Kiểm tra trạng thái Production hiện tại trong app-prod:${NC}
  $ kubectl get deployments,pods,svc,ingress -n app-prod -o wide
  $ curl -s https://nt548.helios.id.vn | grep -oE 'PRODUCTION \([a-f0-9]+\)'

${GREEN}[Bước 2] Mở terminal theo dõi truy cập liên tục (chứng minh 0% downtime & chuyển đổi version/pod):${NC}
  $ ok=0; fail=0; i=0; while true; do i=\$((i+1)); out=\$(curl -sS --max-time 3 -w "\n%{http_code} %{time_total}" https://nt548.helios.id.vn/ready 2>/dev/null || printf "\n000 0"); body=\$(printf "%s" "\$out" | head -n1); meta=\$(printf "%s" "\$out" | tail -n1); code=\${meta%% *}; ms=\${meta#* }; if [ "\$code" = "200" ]; then ok=\$((ok+1)); else fail=\$((fail+1)); fi; printf "[%s] #%03d HTTP=%s time=%ss ok=%d fail=%d %s\n" "\$(date +%H:%M:%S)" "\$i" "\$code" "\$ms" "\$ok" "\$fail" "\$body"; sleep 0.5; done

${GREEN}[Bước 3] Đẩy cập nhật nhỏ trong app/ lên main để kích hoạt CI -> GitOps RollingUpdate:${NC}
  - Chỉ commit riêng file đã sửa trong app/ để không lẫn local changes khác:
    $ git commit --only <file-trong-app> -m "test(cd): verify rolling update" && git push origin main
  - CI pipeline chạy Gitleaks -> Trivy FS -> Kubeconform & Trivy Config -> Build & Trivy Image -> Commit tag mới vào project-nt548/k8s-manifests/deployment.yaml.
  - Kéo commit từ CI về bằng fast-forward:
    $ git pull --ff-only origin main
  $ kubectl -n app-prod rollout status deploy/web-deployment
  $ kubectl -n app-prod get pods -o wide

${GREEN}[Bước 4] Kiểm thử GitOps Rollback tức thì (Zero-Downtime, không đụng local changes khác):${NC}
  $ git checkout HEAD~1 -- project-nt548/k8s-manifests/deployment.yaml
  $ git commit --only project-nt548/k8s-manifests/deployment.yaml -m "revert(prod): rollback web-deployment to previous version [skip ci]"
  $ git push origin main
  $ kubectl -n app-prod rollout status deploy/web-deployment
  $ curl -s https://nt548.helios.id.vn/ready
  - (Sau khi kiểm chứng xong, khôi phục lại file test trong app/):
    $ git checkout HEAD~2 -- <file-trong-app> && git commit --only <file-trong-app> -m "chore(app): revert test change [skip ci]" && git push origin main

EOF
}

print_scenario_4() {
  cat <<EOF

${YELLOW}=== KỊCH BẢN 4: NETWORKPOLICY CÔ LẬP REDIS & HUBBLE OBSERVABILITY ===${NC}
${BLUE}Mục tiêu:${NC} Chứng minh chỉ Pod mang nhãn app: web mới truy cập được cổng TCP 6379 của Redis;
          mọi Pod lạ trong app-prod bị Cilium eBPF chặn đứng và hiện flow DROPPED trên Hubble UI.

${GREEN}[Bước 1] Kiểm tra NetworkPolicy đang áp dụng:${NC}
  $ kubectl get networkpolicy -n app-prod -o yaml

${GREEN}[Bước 2] Kiểm tra Pod Web hợp lệ truy cập được Redis (/ready):${NC}
  $ curl -i https://nt548.helios.id.vn/ready

${GREEN}[Bước 3] Khởi chạy Pod hợp chuẩn Kyverno trong app-prod nhưng KHÔNG mang nhãn app=web:${NC}
  $ kubectl run intruder -n app-prod --labels="app=intruder" --rm -it --restart=Never \\
      --image=ghcr.io/helios-ryuu/devsecops-gitops-with-k8s:<CURRENT_TAG> \\
      --overrides='{"spec":{"securityContext":{"runAsNonRoot":true,"runAsUser":10001,"runAsGroup":10001,"fsGroup":10001,"seccompProfile":{"type":"RuntimeDefault"}},"containers":[{"name":"intruder","image":"ghcr.io/helios-ryuu/devsecops-gitops-with-k8s:<CURRENT_TAG>","securityContext":{"allowPrivilegeEscalation":false,"readOnlyRootFilesystem":true,"capabilities":{"drop":["ALL"]}},"resources":{"requests":{"cpu":"20m","memory":"32Mi"},"limits":{"cpu":"50m","memory":"64Mi"}},"command":["node","-e","const s=require(\"node:net\").connect(6379,\"redis-service.app-prod.svc.cluster.local\");s.setTimeout(3000,()=>{console.log(\"DROPPED/TIMEOUT\");s.destroy()});s.on(\"connect\",()=>{console.log(\"CONNECTED\");s.destroy()});s.on(\"error\",e=>console.log(\"ERROR:\",e.message))"]}]}}'

${GREEN}[Bước 4] Quan sát trực tiếp trên Hubble UI (https://hubble.helios.id.vn):${NC}
  - Chọn filter Verdict = DROPPED -> hiển thị dòng màu đỏ chặn kết nối từ intruder tới redis-0:6379.

EOF
}

print_scenario_5() {
  cat <<EOF

${YELLOW}=== KỊCH BẢN 5: NIGHTLY GHCR IMAGE AUDIT (0 MB CLUSTER RAM), TRAEFIK HA & LONGHORN FAILOVER ===${NC}
${BLUE}Mục tiêu:${NC} Chứng minh quét CVE định kỳ image đang chạy bằng GitHub Actions (không tốn RAM cụm),
          khả năng chịu lỗi Traefik HA và bảo toàn dữ liệu Redis trên Longhorn khi bảo trì Worker.

${GREEN}[Bước 1] Kiểm tra quét CVE hàng đêm cho các image đang deploy (0 MB RAM cụm):${NC}
  - Vào GitHub Actions -> Workflow 'Nightly Active GHCR & Base Image Audit' (.github/workflows/nightly-audit.yml)
    -> xem lịch cron '0 0 * * *' hoặc bấm Run workflow để kiểm chứng trực tiếp:
  - Runner tự đọc các image tag đang chạy trong deployment.yaml & redis-statefulset.yaml, pull về và chạy Trivy.
  - Mở Grafana (https://grafana.helios.id.vn) để xem dashboard tài nguyên Node, Cilium eBPF và Traefik RPS.

${GREEN}[Bước 2] Kiểm chứng Traefik HA Zero-Downtime trên 2 Worker (worker-01 & worker-02):${NC}
  $ kubectl get pods -n traefik -o wide
  - Chạy vòng lặp tải nhẹ trong 1 terminal khác:
    $ ok=0; fail=0; i=0; while true; do i=\$((i+1)); out=\$(curl -sS --max-time 3 -w "\n%{http_code} %{time_total}" https://nt548.helios.id.vn/healthz 2>/dev/null || printf "\n000 0"); body=\$(printf "%s" "\$out" | head -n1); meta=\$(printf "%s" "\$out" | tail -n1); code=\${meta%% *}; ms=\${meta#* }; if [ "\$code" = "200" ]; then ok=\$((ok+1)); else fail=\$((fail+1)); fi; printf "[%s] #%03d HTTP=%s time=%ss ok=%d fail=%d %s\n" "\$(date +%H:%M:%S)" "\$i" "\$code" "\$ms" "\$ok" "\$fail" "\$body"; sleep 0.5; done
  - Xóa 1 Pod Traefik bất kỳ:
    $ kubectl delete pod -n traefik \$(kubectl get pod -n traefik -l app.kubernetes.io/name=traefik -o jsonpath='{.items[0].metadata.name}')
  -> Quan sát kết quả HTTP 200 liên tục, không rớt kết nối nào.

${GREEN}[Bước 3] Kiểm chứng Longhorn Storage Failover (RPO = 0, không mất bộ đếm Redis):${NC}
  $ kubectl get pods -n app-prod -o wide | grep redis-0
  - Ghi nhận số lượt truy cập hiện tại trên https://nt548.helios.id.vn
  - Drain node đang chứa redis-0 (thay <NODE_NAME> bằng worker-01 hoặc worker-02):
    $ kubectl drain <NODE_NAME> --ignore-daemonsets --delete-emptydir-data
  - Chờ redis-0 khởi chạy lại trên worker còn lại (~30-60s để Longhorn detach/attach PVC RWO), sau đó tải lại web và mở node lại:
    $ kubectl get pods -n app-prod -o wide -w
    $ kubectl uncordon <NODE_NAME>
  -> Lưu ý đánh giá: Traefik đạt Zero-Downtime HA; còn Redis StatefulSet (1 replica, PVC RWO) gián đoạn ngắn lúc chuyển volume và đạt Data Durability (RPO = 0).

EOF
}

print_scenario_6() {
  cat <<EOF

${YELLOW}=== KỊCH BẢN 6: PHỤC HỒI HASHICORP VAULT SAU EVICTION (UNSEAL) & ĐỒNG BỘ ESO ===${NC}
${BLUE}Mục tiêu:${NC} Tận dụng trạng thái vault-0 bị evict sang Worker khác sau lệnh kubectl drain ở Kịch bản 5
          để chứng minh: (1) K8s Secret đã đồng bộ giúp app & Traefik tiếp tục chạy ổn định khi Vault Sealed;
          (2) dữ liệu Vault trên Longhorn PVC 2Gi nguyên vẹn, chỉ cần 1 lệnh unseal để mở khóa và duy trì đồng bộ ESO.

${GREEN}[Bước 1] Kiểm tra vault-0 ở trạng thái 0/1 Running (Sealed: true) sau khi chuyển node:${NC}
  $ kubectl get pods -n vault -o wide
  $ kubectl exec -n vault vault-0 -- vault status || true

${GREEN}[Bước 2] Xác nhận ứng dụng và các Secret đã đồng bộ vẫn hoạt động bình thường khi Vault đang Sealed:${NC}
  $ curl -sS https://nt548.helios.id.vn/ready
  $ kubectl get externalsecret -A

${GREEN}[Bước 3] Mở khóa Vault bằng 1 khóa duy nhất (lưu ngoại tuyến):${NC}
  $ kubectl exec -n vault vault-0 -- vault operator unseal "<UNSEAL_KEY>"

${GREEN}[Bước 4] Xác nhận vault-0 trở lại 1/1 Running (Sealed: false) và ESO duy trì SecretSynced:${NC}
  $ kubectl get pods -n vault -o wide
  $ kubectl get externalsecret -A

EOF
}

print_all() {
  print_scenario_1
  print_scenario_2
  print_scenario_3
  print_scenario_4
  print_scenario_5
  print_scenario_6
}

if [[ "${1:-}" == "--all" ]]; then
  print_all
  exit 0
elif [[ "${1:-}" =~ ^[1-6]$ ]]; then
  "print_scenario_${1}"
  exit 0
fi

clear 2>/dev/null || true
echo -e "${CYAN}========================================================================${NC}"
echo -e "${CYAN}   HƯỚNG DẪN CÁC BƯỚC KIỂM THỬ HỆ THỐNG (ĐỒ ÁN NT548)                  ${NC}"
echo -e "${CYAN}   (Script chỉ in câu lệnh hướng dẫn — không thực thi lên hệ thống)     ${NC}"
echo -e "${CYAN}========================================================================${NC}"
echo -e "Chọn kịch bản kiểm thử bạn muốn xem hướng dẫn:"
echo -e "  ${GREEN}1)${NC} Kịch bản 1: CI DevSecOps Gate (Gitleaks, Trivy, Kubeconform, Trivy Config)"
echo -e "  ${GREEN}2)${NC} Kịch bản 2: Kyverno Admission Policy Enforce (policy-tier=hardened)"
echo -e "  ${GREEN}3)${NC} Kịch bản 3: GitOps Continuous Delivery (RollingUpdate Zero-Downtime) & Rollback"
echo -e "  ${GREEN}4)${NC} Kịch bản 4: NetworkPolicy Cô lập Redis & Hubble Observability (DROPPED)"
echo -e "  ${GREEN}5)${NC} Kịch bản 5: Nightly GHCR CVE Audit (0 MB RAM), Traefik HA & Longhorn Failover"
echo -e "  ${GREEN}6)${NC} Kịch bản 6: Phục hồi HashiCorp Vault sau Eviction (Unseal) & Đồng bộ ESO"
echo -e "  ${GREEN}a)${NC} In toàn bộ 6 kịch bản"
echo -e "  ${RED}0)${NC} Thoát"
echo -e "${CYAN}------------------------------------------------------------------------${NC}"
read -rp "Nhập lựa chọn của bạn (0-6 hoặc a): " choice

case "$choice" in
  1) print_scenario_1 ;;
  2) print_scenario_2 ;;
  3) print_scenario_3 ;;
  4) print_scenario_4 ;;
  5) print_scenario_5 ;;
  6) print_scenario_6 ;;
  a|A) print_all ;;
  0) echo -e "\nThoát."; exit 0 ;;
  *) echo -e "\n${RED}Lựa chọn không hợp lệ.${NC}"; exit 1 ;;
esac
