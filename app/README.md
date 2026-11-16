# NT548 Web Service (Next.js 16 Standalone + Redis)

Ứng dụng web 2 tầng chạy trên `node:26.13.0-alpine3.23` (non-root `UID:GID 10001:10001`), kết nối Redis qua TCP client thuần (`node:net`) tại [src/lib/redis.ts](./src/lib/redis.ts).

## Endpoints & Biến môi trường

- `/` — Giao diện hiển thị bộ đếm lượt truy cập Redis, `APP_ENV`, `APP_VERSION`, Pod/Node runtime identity.
- `/healthz` — Liveness probe trả `HTTP 200`.
- `/ready` — Readiness probe kiểm tra `PING` tới Redis (`HTTP 200` khi sẵn sàng, `503` khi mất kết nối).
- Biến môi trường: `APP_ENV`, `APP_VERSION`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`.

## Chạy cục bộ

```bash
pnpm install
pnpm dev
```
