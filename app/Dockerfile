# ==============================================================================
# DOCKERFILE: NEXT.JS STANDALONE MULTI-STAGE BUILD (PNPM)
# Optimized for Kubernetes, Minimal Image Size & Non-Root Security (Trivy Scan)
# ==============================================================================

# --- Stage 1: Install Dependencies ---
FROM node:26.13.0-alpine3.23 AS deps
# Cần thiết cho một số thư viện C++ bindings trên Alpine (libc6-compat)
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Cài đặt pnpm theo đúng version trong package.json
RUN npm install -g pnpm@12.16.1

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml* ./
RUN pnpm i --frozen-lockfile

# --- Stage 2: Build Application ---
FROM node:26.13.0-alpine3.23 AS builder
WORKDIR /app

RUN npm install -g pnpm@12.16.1

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN pnpm run build

# --- Stage 3: Production Runtime ---
FROM node:26.13.0-alpine3.23 AS runner
WORKDIR /app

# Hardening: Gỡ bỏ npm, npx, corepack không cần thiết trong runtime standalone
# Loại bỏ triệt để CVE (như brace-expansion trong bundled npm) và giảm attack surface
RUN rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Non-root user với UID:GID 10001 (khớp với runAsUser / runAsGroup trong K8s manifest)
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# Sao chép public và standalone output với chown số 10001:10001 đồng bộ
COPY --from=builder --chown=10001:10001 /app/public ./public
COPY --from=builder --chown=10001:10001 /app/.next/standalone ./
COPY --from=builder --chown=10001:10001 /app/.next/static ./.next/static

# Khai báo dạng số UID:GID để Trivy Scan và Kubernetes SecurityContext xác thực tuyệt đối
USER 10001:10001
EXPOSE 3000

CMD ["node", "server.js"]
