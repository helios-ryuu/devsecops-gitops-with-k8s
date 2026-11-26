import net from "node:net";

type RespValue = string | number | null;

export interface RedisHealthResult {
  ok: boolean;
  latencyMs: number;
  error?: string;
}

export interface VisitCounterResult {
  count: number | null;
  connected: boolean;
  latencyMs: number;
  host: string;
  error?: string;
}

function getRedisConfig() {
  return {
    host: process.env.REDIS_HOST || "127.0.0.1",
    port: Number.parseInt(process.env.REDIS_PORT || "6379", 10),
    password: process.env.REDIS_PASSWORD || "",
  };
}

function encodeCommand(args: string[]): Buffer {
  const chunks: Buffer[] = [Buffer.from(`*${args.length}\r\n`, "utf8")];
  for (const arg of args) {
    const byteLen = Buffer.byteLength(arg, "utf8");
    chunks.push(Buffer.from(`$${byteLen}\r\n`, "utf8"));
    chunks.push(Buffer.from(arg, "utf8"));
    chunks.push(Buffer.from("\r\n", "utf8"));
  }
  return Buffer.concat(chunks);
}

function tryParseValue(
  buf: Buffer,
  offset: number
): { value: RespValue; nextOffset: number } | null {
  if (offset >= buf.length) return null;
  const lineEnd = buf.indexOf("\r\n", offset);
  if (lineEnd === -1) return null;

  const prefix = String.fromCharCode(buf[offset]);
  const header = buf.toString("utf8", offset + 1, lineEnd);

  if (prefix === "+") {
    return { value: header, nextOffset: lineEnd + 2 };
  }
  if (prefix === ":") {
    return { value: Number.parseInt(header, 10), nextOffset: lineEnd + 2 };
  }
  if (prefix === "-") {
    throw new Error(header);
  }
  if (prefix === "$") {
    const len = Number.parseInt(header, 10);
    if (len === -1) {
      return { value: null, nextOffset: lineEnd + 2 };
    }
    const dataStart = lineEnd + 2;
    const dataEnd = dataStart + len;
    if (buf.length < dataEnd + 2) return null;
    const value = buf.toString("utf8", dataStart, dataEnd);
    return { value, nextOffset: dataEnd + 2 };
  }

  throw new Error(`Unsupported RESP prefix: ${prefix}`);
}

async function executeRedisCommands(
  commands: string[][],
  timeoutMs = 1500
): Promise<RespValue[]> {
  const { host, port, password } = getRedisConfig();
  const pipeline = password ? [["AUTH", password], ...commands] : commands;
  const payload = Buffer.concat(pipeline.map(encodeCommand));

  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ host, port, family: 4 });
    let buffer = Buffer.alloc(0);
    const replies: RespValue[] = [];
    let settled = false;

    const cleanup = () => {
      socket.removeAllListeners();
      if (!socket.destroyed) {
        socket.destroy();
      }
    };

    const fail = (err: Error) => {
      if (settled) return;
      settled = true;
      cleanup();
      reject(err);
    };

    socket.setTimeout(timeoutMs);

    socket.on("connect", () => {
      socket.write(payload);
    });

    socket.on("data", (chunk: Buffer) => {
      buffer = Buffer.concat([buffer, chunk]);
      try {
        let offset = 0;
        while (replies.length < pipeline.length) {
          const parsed = tryParseValue(buffer, offset);
          if (!parsed) break;
          replies.push(parsed.value);
          offset = parsed.nextOffset;
        }
        if (offset > 0) {
          buffer = buffer.subarray(offset);
        }
        if (replies.length === pipeline.length && !settled) {
          settled = true;
          cleanup();
          resolve(password ? replies.slice(1) : replies);
        }
      } catch (err) {
        fail(err instanceof Error ? err : new Error(String(err)));
      }
    });

    socket.on("timeout", () => {
      fail(new Error(`Redis timeout after ${timeoutMs}ms (${host}:${port})`));
    });

    socket.on("error", (err) => {
      fail(err);
    });

    socket.on("close", () => {
      if (!settled) {
        fail(new Error("Redis connection closed before receiving full reply"));
      }
    });
  });
}

export async function pingRedis(): Promise<RedisHealthResult> {
  const start = Date.now();
  try {
    const [reply] = await executeRedisCommands([["PING"]]);
    return {
      ok: reply === "PONG",
      latencyMs: Date.now() - start,
    };
  } catch (err) {
    return {
      ok: false,
      latencyMs: Date.now() - start,
      error: err instanceof Error ? err.message : "Unknown Redis error",
    };
  }
}

export async function incrementVisitCounter(): Promise<VisitCounterResult> {
  const { host, port } = getRedisConfig();
  const start = Date.now();
  try {
    const [count] = await executeRedisCommands([["INCR", "nt548:visits"]]);
    return {
      count: typeof count === "number" ? count : Number(count),
      connected: true,
      latencyMs: Date.now() - start,
      host: `${host}:${port}`,
    };
  } catch (err) {
    return {
      count: null,
      connected: false,
      latencyMs: Date.now() - start,
      host: `${host}:${port}`,
      error: err instanceof Error ? err.message : "Unknown Redis error",
    };
  }
}
