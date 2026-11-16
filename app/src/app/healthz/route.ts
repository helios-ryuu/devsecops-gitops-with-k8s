import { connection } from "next/server";

export async function GET() {
  await connection();
  return Response.json(
    {
      status: "ok",
      uptime: process.uptime(),
      timestamp: new Date().toISOString(),
    },
    { status: 200 }
  );
}
