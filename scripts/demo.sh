#!/usr/bin/env bash
# ==============================================================================
# SCRIPT HƯỚNG DẪN DEMO: DEVSECOPS & GITOPS TRÊN K3S HYBRID (ĐỒ ÁN NT548)
# Chức năng: Chỉ hiển thị các bước và câu lệnh mẫu, chỉ thực hiện thao tác ĐỌC.
# Không tự ý chạy bất kỳ lệnh xóa hay thay đổi nào trên cụm.
# ==============================================================================

set -e

# Màu sắc hiển thị terminal
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

NAMESPACE="production-app"
DEPLOYMENT="web-deployment"

clear 2>/dev/null || true
echo -e "${CYAN}====================================================================${NC}"
echo -e "${CYAN}    HƯỚNG DẪN KỊCH BẢN DEMO: DEVSECOPS & GITOPS (K3S HYBRID)        ${NC}"
echo -e "${CYAN}====================================================================${NC}"
echo -e "Chọn kịch bản demo bạn muốn hiển thị:"
echo -e "  ${GREEN}1)${NC} [GitOps] Kịch bản 1: Kiểm chứng Self-healing (Tự phục hồi Pod/Deployment)"
echo -e "  ${GREEN}2)${NC} [GitOps] Kịch bản 2: Kiểm chứng Tự động Rollback qua Git Revert"
echo -e "  ${GREEN}3)${NC} [DevSecOps] Kịch bản 3: Kiểm chứng Trivy Security Gate (Chặn CVE)"
echo -e "  ${GREEN}4)${NC} [Giám sát] Kiểm tra nhanh trạng thái toàn cụm (Read-only)"
echo -e "  ${RED}0)${NC} Thoát"
echo -e "${CYAN}--------------------------------------------------------------------${NC}"
read -rp "Nhập lựa chọn của bạn (0-4): " choice

case $choice in
  1)
    echo -e "\n${YELLOW}=== KỊCH BẢN 1: GITOPS SELF-HEALING (TỰ PHỤC HỒI KHI CÓ SAI LỆCH) ===${NC}"
    echo -e "${BLUE}Mục tiêu:${NC} Chứng minh ArgoCD liên tục đối chiếu trạng thái thực tế với Git."
    echo -e "          Khi quản trị viên cố tình xóa tài nguyên trực tiếp trên K8s,"
    echo -e "          ArgoCD sẽ tự động tái tạo lại ngay lập tức (Zero-Touch Reconciliation).\n"

    echo -e "${GREEN}[Bước 1] Kiểm tra trạng thái Deployment đang chạy bình thường:${NC}"
    echo -e "  $ kubectl get deployment ${DEPLOYMENT} -n ${NAMESPACE}\n"
    kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" 2>/dev/null || echo -e "  (Chưa triển khai hoặc chưa kết nối cluster)\n"

    echo -e "${GREEN}[Bước 2] Lệnh mô phỏng sự cố (Copy lệnh này chạy thủ công):${NC}"
    echo -e "  ${RED}$ kubectl delete deployment ${DEPLOYMENT} -n ${NAMESPACE}${NC}\n"

    echo -e "${GREEN}[Bước 3] Lệnh quan sát ArgoCD tự phục hồi trong vòng 5-10 giây:${NC}"
    echo -e "  $ kubectl get pods -n ${NAMESPACE} -l app=web -w"
    echo -e "  $ kubectl get deployment ${DEPLOYMENT} -n ${NAMESPACE}\n"

    echo -e "${BLUE}Gợi ý thuyết trình:${NC} Mở đồng thời giao diện Web UI ArgoCD để khán giả thấy"
    echo -e "cây ứng dụng nhấp nháy OutOfSync sang Synced màu xanh lá cây trong vài giây."
    ;;

  2)
    echo -e "\n${YELLOW}=== KỊCH BẢN 2: GITOPS ROLLBACK AN TOÀN QUA GIT REVERT ===${NC}"
    echo -e "${BLUE}Mục tiêu:${NC} Chứng minh mọi thay đổi phiên bản đều truy vết trên Git."
    echo -e "          Khi cần hoàn tác, chỉ cần 'git revert' là ArgoCD tự động kéo phiên bản cũ về.\n"

    echo -e "${GREEN}[Bước 1] Kiểm tra image và commit tag hiện tại của Pod:${NC}"
    echo -e "  $ kubectl get deployment ${DEPLOYMENT} -n ${NAMESPACE} -o jsonpath='{.spec.template.spec.containers[0].image}'\n"
    CURRENT_IMG=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null || echo "")
    if [ -n "$CURRENT_IMG" ]; then
      echo -e "  Image hiện tại: ${CYAN}${CURRENT_IMG}${NC}\n"
    fi

    echo -e "${GREEN}[Bước 2] Lệnh thực hiện Rollback qua Git (Chạy từ terminal):${NC}"
    echo -e "  $ git revert HEAD --no-edit"
    echo -e "  $ git push origin main\n"

    echo -e "${GREEN}[Bước 3] Lệnh theo dõi quá trình Rolling Update phiên bản cũ:${NC}"
    echo -e "  $ kubectl rollout status deployment/${DEPLOYMENT} -n ${NAMESPACE}"
    echo -e "  $ kubectl get deployment ${DEPLOYMENT} -n ${NAMESPACE} -o jsonpath='{.spec.template.spec.containers[0].image}'\n"

    echo -e "${BLUE}Gợi ý thuyết trình:${NC} Nhấn mạnh việc không ai dùng lệnh 'kubectl set image' thủ công"
    echo -e "trên production, mà toàn bộ tuân thủ nguyên tắc GitOps Declarative."
    ;;

  3)
    echo -e "\n${YELLOW}=== KỊCH BẢN 3: DEVSECOPS SECURITY GATE (CHẶN COMMIT DÍNH CVE) ===${NC}"
    echo -e "${BLUE}Mục tiêu:${NC} Chứng minh pipeline CI tự động đóng vai trò chốt chặn bảo mật."
    echo -e "          Mã nguồn dính CVE hoặc rò rỉ secret sẽ bị chặn ngay lập tức, không cho phép đóng gói image.\n"

    echo -e "${GREEN}[Bước 1] Thêm một thư viện chứa lỗ hổng nghiêm trọng vào app (Ví dụ: lodash 4.17.20):${NC}"
    echo -e "  $ cd app && pnpm add lodash@4.17.20 && cd ..\n"

    echo -e "${GREEN}[Bước 2] Commit và đẩy lên GitHub để kích hoạt CI Pipeline:${NC}"
    echo -e "  $ git add app/package.json app/pnpm-lock.yaml"
    echo -e "  $ git commit -m \"test(security): inject vulnerable dependency lodash@4.17.20\""
    echo -e "  $ git push origin main\n"

    echo -e "${GREEN}[Bước 3] Quan sát Security Gate chặn quá trình phát hành:${NC}"
    echo -e "  1. Mở tab GitHub Actions trên repo."
    echo -e "  2. Job '2. Source CVE Scanning (Trivy FS)' sẽ quét thấy lỗ hổng CRITICAL/HIGH và trả về Exit Code 1 (Fail)."
    echo -e "  3. Toàn bộ các bước sau (Build Docker, Push GHCR, Update Tag) bị CANCEL/FAILED."
    echo -e "  4. Cụm K8s và ArgoCD hoàn toàn an toàn, không bị cập nhật phiên bản lỗi này."
    ;;

  4)
    echo -e "\n${YELLOW}=== KIỂM TRA NHANH TRẠNG THÁI HỆ THỐNG (READ-ONLY) ===${NC}\n"
    echo -e "${CYAN}[1] Danh sách Nodes:${NC}"
    kubectl get nodes -o wide 2>/dev/null || echo "Không kết nối được cluster"
    echo -e "\n${CYAN}[2] Toàn bộ Pods trong production-app:${NC}"
    kubectl get pods -n "$NAMESPACE" -o wide 2>/dev/null || echo "Namespace chưa tồn tại"
    echo -e "\n${CYAN}[3] Ingress đang hoạt động:${NC}"
    kubectl get ingress -A 2>/dev/null || echo "Chưa có Ingress"
    ;;

  0)
    echo -e "\nThoát."
    exit 0
    ;;

  *)
    echo -e "\n${RED}Lựa chọn không hợp lệ.${NC}"
    exit 1
    ;;
esac
