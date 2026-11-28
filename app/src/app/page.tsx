import { Suspense } from "react";
import { connection } from "next/server";
import { incrementVisitCounter } from "@/lib/redis";

async function LiveClusterPanel() {
  await connection();

  const appEnv = (process.env.APP_ENV || "production").toUpperCase();
  const appVersion = process.env.APP_VERSION || "local";
  const podName = process.env.HOSTNAME || "localhost";
  const nodeName = process.env.NODE_NAME || "local-node";
  const namespace = process.env.POD_NAMESPACE || "local";
  const renderedAt = new Date().toISOString();

  const visit = await incrementVisitCounter();

  return (
    <div
      className="w-full rounded-2xl border border-sky-500/30 bg-gradient-to-br from-sky-500/10 to-cyan-500/5 bg-slate-900/80 p-6 sm:p-8 shadow-2xl"
    >
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <p className="font-mono text-xs uppercase tracking-widest text-slate-400">
            NT548.R12 - Platform Engineering & DevSecOps
          </p>
          <h1 className="mt-2 text-2xl sm:text-3xl font-bold tracking-tight text-white">
            Kubernetes Hybrid Web + Redis Service
          </h1>
        </div>
        <span
          className="inline-flex items-center gap-2 rounded-full border border-sky-500/40 bg-sky-500/15 px-3.5 py-1.5 font-mono text-xs font-semibold text-sky-300"
        >
          <span className="h-2 w-2 rounded-full bg-current animate-pulse" />
          {`${appEnv} (${appVersion})`}
        </span>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-5 sm:col-span-1">
          <p className="font-mono text-xs uppercase tracking-wider text-slate-400">
            Redis Visit Counter
          </p>
          <p className="mt-2 font-mono text-4xl font-bold text-white">
            {visit.connected && visit.count !== null ? visit.count : "N/A"}
          </p>
          <p className="mt-2 text-xs text-slate-400">
            {visit.connected
              ? `Longhorn PVC • ${visit.latencyMs}ms (${visit.host})`
              : `Redis offline: ${visit.error ?? "unreachable"}`}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-5 sm:col-span-2">
          <p className="font-mono text-xs uppercase tracking-wider text-slate-400">
            Runtime Identity
          </p>
          <dl className="mt-3 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-slate-500">Pod (HOSTNAME)</dt>
              <dd className="font-mono text-slate-200 break-all">{podName}</dd>
            </div>
            <div>
              <dt className="text-slate-500">Worker Node</dt>
              <dd className="font-mono text-slate-200">{nodeName}</dd>
            </div>
            <div>
              <dt className="text-slate-500">Namespace</dt>
              <dd className="font-mono text-slate-200">{namespace}</dd>
            </div>
            <div>
              <dt className="text-slate-500">Rendered At (UTC)</dt>
              <dd className="font-mono text-slate-200">{renderedAt}</dd>
            </div>
          </dl>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-slate-800 pt-5 text-xs text-slate-400">
        <div className="flex flex-wrap items-center gap-2 font-mono">
          <span className="rounded bg-slate-800 px-2.5 py-1 text-slate-300">
            WireGuard wg0 + Cilium eBPF
          </span>
          <span className="rounded bg-slate-800 px-2.5 py-1 text-slate-300">
            Traefik HA + ArgoCD + Kyverno
          </span>
          <span className="rounded bg-slate-800 px-2.5 py-1 text-slate-300">
            Non-root UID 10001
          </span>
        </div>
        <div className="flex items-center gap-4 font-mono">
          <a href="/healthz" className="text-cyan-400 hover:underline">
            /healthz
          </a>
          <a href="/ready" className="text-cyan-400 hover:underline">
            /ready
          </a>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-4xl flex-1 items-center justify-center px-4 py-12">
      <Suspense
        fallback={
          <div className="w-full rounded-2xl border border-slate-800 bg-slate-900/60 p-8 text-center font-mono text-sm text-slate-400">
            Connecting to Redis & Kubernetes Runtime...
          </div>
        }
      >
        <LiveClusterPanel />
      </Suspense>
    </main>
  );
}
