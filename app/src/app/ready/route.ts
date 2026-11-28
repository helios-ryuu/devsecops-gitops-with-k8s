import { connection } from "next/server";
import { pingRedis } from "@/lib/redis";

export async function GET() {
  await connection();
  const version = process.env.APP_VERSION || "local";
  const pod = process.env.HOSTNAME || "localhost";
  const redis = await pingRedis();

  if (!redis.ok) {
    return Response.json(
      {
        status: "not_ready",
        redis: "error",
        version,
        pod,
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
      version,
      pod,
      latencyMs: redis.latencyMs,
      timestamp: new Date().toISOString(),
    },
    { status: 200 }
  );
}
