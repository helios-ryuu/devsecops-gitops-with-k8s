import { connection } from "next/server";
import { pingRedis } from "@/lib/redis";

export async function GET() {
  await connection();
  const redis = await pingRedis();

  if (!redis.ok) {
    return Response.json(
      {
        status: "not_ready",
        redis: "error",
        error: redis.error ?? "Redis unreachable",
        timestamp: new Date().toISOString(),
      },
      { status: 503 }
    );
  }

  return Response.json(
    {
      status: "ready",
      redis: "ok",
      latencyMs: redis.latencyMs,
      timestamp: new Date().toISOString(),
    },
    { status: 200 }
  );
}
