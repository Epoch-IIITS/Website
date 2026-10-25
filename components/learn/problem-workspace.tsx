"use client"

import { useEffect, useRef, useState } from "react"
import dynamic from "next/dynamic"
import Link from "next/link"
import { useTheme } from "next-themes"
import { useSession } from "next-auth/react"
import { ArrowRight, Check, ChevronDown, CircleHelp, Eye, EyeOff, Lightbulb, Play, RotateCcw, Send, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"
import type { LearnExecutionResult, PublicProblemPack } from "@/lib/learn/types"

const MonacoCodeEditor = dynamic(() => import("@/components/learn/monaco-code-editor").then((module) => module.MonacoCodeEditor), { ssr: false, loading: () => <div className="flex h-full min-h-0 items-center justify-center text-xs text-muted-foreground">Loading Python editor…</div> })
let localRunCount = 0

const MonacoCodeView = dynamic(() => import("@/components/learn/monaco-code-editor").then((module) => module.MonacoCodeView), { ssr: false, loading: () => <div className="p-4 text-xs text-muted-foreground">Loading solution code…</div> })

type Pane = "concept" | "problem"
type ConsoleTab = "tests" | "output" | "feedback"

function errorSummary(message: string) {
  const lines = message.split(/\r?\n/).map((line) => line.trim()).filter(Boolean)
  const exception = lines.findLast((line) => /^(?:[\w.]+(?:Error|Exception|Warning|Exit|Interrupt)|Failed):/.test(line))
  return exception ?? lines.findLast((line) => !/^[?+-]\s/.test(line)) ?? "Test failed"
}

function ExecutionResult({ result, source, submitted, advice }: { result: LearnExecutionResult; source: string; submitted: boolean; advice: Map<string, string> }) {
  return <div className="space-y-3">
    <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border/70 pb-3">
      <div>
        <p className="text-[11px] text-muted-foreground">{source}</p>
        <p className="mt-1 text-sm font-semibold">{result.passed} / {result.total} tests passed</p>
      </div>
      <span className={`rounded-full border px-2.5 py-0.5 text-[11px] font-medium ${result.status === "passed" ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-700 dark:text-emerald-400" : "border-red-500/30 bg-red-500/5 text-red-700 dark:text-red-400"}`}>
        {result.status === "passed" ? "Passed" : "Needs work"}
      </span>
    </div>
    {result.tests?.length ? <ul className="space-y-2" aria-label="Test results">
      {result.tests.map((test) => {
        const message = test.message?.trim()
        const summary = message ? errorSummary(message) : null
        return <li key={test.name} className="rounded-md border border-border/80 bg-muted/20 p-3">
          <div className="flex items-start gap-2">
            {test.passed ? <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-700 dark:text-emerald-400" aria-hidden="true" /> : <X className="mt-0.5 h-3.5 w-3.5 shrink-0 text-red-700 dark:text-red-400" aria-hidden="true" />}
            <code className="min-w-0 break-all font-mono text-xs font-semibold text-foreground">{test.name}</code>
            <span className={`ml-auto shrink-0 text-[10px] font-medium ${test.passed ? "text-emerald-700 dark:text-emerald-400" : "text-red-700 dark:text-red-400"}`}>{test.passed ? "Passed" : "Failed"}</span>
          </div>
          {message && <div className="mt-3 border-t border-border/70 pt-2.5">
            <p className="break-words font-mono text-xs leading-5 text-red-700 dark:text-red-300">{summary}</p>
            {message.includes("\n") && <details className="mt-2">
              <summary className="w-fit cursor-pointer text-[11px] font-medium text-muted-foreground hover:text-foreground">Show traceback</summary>
              <pre className="mt-2 max-h-56 overflow-auto whitespace-pre-wrap break-all rounded-md border border-border/70 bg-background p-3 font-mono text-[11px] leading-5 text-foreground">{message}</pre>
            </details>}
          </div>}
        </li>
      })}
    </ul> : null}
    {result.failedTests?.length ? <div className="space-y-2" aria-label="Failed checks">
      <p className="text-muted-foreground">Checks that failed. Hidden checks show their name and a hint, not their code.</p>
      <ul className="space-y-2">{result.failedTests.map((name) => <li key={name} className="rounded-md border border-red-500/30 bg-red-500/5 p-3">
        <div className="flex items-start gap-2"><X className="mt-0.5 h-3.5 w-3.5 shrink-0 text-red-700 dark:text-red-400" aria-hidden="true" /><code className="min-w-0 break-all font-mono text-xs font-semibold text-foreground">{name}</code></div>
        <p className="mt-2 text-xs leading-5 text-muted-foreground">{advice.get(name) ?? "Re-read the task for the exact expected behaviour, including output formatting and edge cases."}</p>
      </li>)}</ul>
    </div> : null}
    {result.output && <pre className="whitespace-pre-wrap break-words rounded-md border border-border/70 bg-muted/20 p-3 font-mono text-[11px] text-muted-foreground">{result.output}</pre>}
    {submitted && <p className="text-muted-foreground">Submission saved. <Link href="/learn/progress" className="text-primary underline">View progress</Link></p>}
  </div>
}

export function ProblemWorkspace({ pack, articleHtml, statementHtml }: {
  pack: PublicProblemPack
  articleHtml: string
  statementHtml: string
}) {
  const { resolvedTheme } = useTheme()
  const { status: sessionStatus } = useSession()
  const signedOut = sessionStatus === "unauthenticated"
  const [isMac, setIsMac] = useState<boolean | null>(null)
  const [pane, setPane] = useState<Pane>("concept")
  const [consoleTab, setConsoleTab] = useState<ConsoleTab>("tests")
  const [code, setCode] = useState(pack.starter)
  const [hintCount, setHintCount] = useState(0)
  const [solutionOpen, setSolutionOpen] = useState(false)
  const [action, setAction] = useState<"run" | "submit" | null>(null)
  const [resetNotice, setResetNotice] = useState(false)
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<LearnExecutionResult | null>(null)
  const [resultSource, setResultSource] = useState("")
  const [error, setError] = useState("")
  const [solution, setSolution] = useState<{ solution: string; explanationHtml: string } | null>(null)
  const [solutionLoading, setSolutionLoading] = useState(false)
  const [solutionError, setSolutionError] = useState("")
  const [python, setPython] = useState<"preparing" | "ready" | "unavailable" | null>(null)
  const advice = new Map(pack.failureFeedback.map((item) => [item.test, item.advice]))
  const edited = useRef(false)
  const generation = useRef(0)
  const worker = useRef<Worker | null>(null)

  useEffect(() => {
    setIsMac(/Mac|iPhone|iPad|iPod/i.test(navigator.platform || navigator.userAgent))
  }, [])

  useEffect(() => {
    setPane("concept")
    setConsoleTab("tests")
    setCode(pack.starter)
    setHintCount(0)
    setSolutionOpen(false)
    setAction(null)
    setResetNotice(false)
    setResult(null)
    setError("")
    setSolution(null)
    edited.current = false
    generation.current++
  }, [pack.id, pack.starter])

  useEffect(() => {
    let cancelled = false
    fetch(`/api/learn/submissions?slug=${encodeURIComponent(pack.slug)}`, { cache: "no-store" })
      .then((response) => response.ok ? response.json() : null)
      .then((data) => {
        if (cancelled || edited.current || typeof data?.latest?.code !== "string") return
        setCode(data.latest.code)
        if (Number.isInteger(data.latest.passed) && Number.isInteger(data.latest.total) && ["passed", "failed"].includes(data.latest.status)) {
          setResult({ passed: data.latest.passed, total: data.latest.total, status: data.latest.status })
          setResultSource("Previous trusted submission")
          setAction("submit")
          setConsoleTab("output")
        }
      }).catch(() => {})
    return () => { cancelled = true }
  }, [pack.slug])

  useEffect(() => {
    if (pane !== "concept") return
    const diagrams = Array.from(document.querySelectorAll<HTMLElement>(".learn-diagram"))
    if (!diagrams.length) return
    let cancelled = false
    import("mermaid").then(async ({ default: mermaid }) => {
      if (cancelled) return
      mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: resolvedTheme === "dark" ? "dark" : "default", flowchart: { htmlLabels: false } })
      for (const diagram of diagrams) {
        const source = diagram.dataset.source ?? diagram.textContent ?? ""
        diagram.dataset.source = source
        diagram.textContent = source
        diagram.removeAttribute("data-processed")
      }
      await mermaid.run({ nodes: diagrams, suppressErrors: true })
    }).catch(() => { /* Keep readable diagram source if rendering fails. */ })
    return () => { cancelled = true }
  }, [articleHtml, pane, resolvedTheme])

  // Start Pyodide when the page opens so the first Run does not wait for it; keep it for later Runs.
  function startWorker() {
    worker.current?.terminate()
    worker.current = null
    let created: Worker
    try { created = new Worker("/learn/pyodide-worker.mjs", { type: "module" }) }
    catch { setPython("unavailable"); return null }
    worker.current = created
    setPython("preparing")
    created.addEventListener("message", (event: MessageEvent<{ type: string; unavailable?: boolean }>) => {
      if (event.data.type === "ready" && worker.current === created) setPython(event.data.unavailable ? "unavailable" : "ready")
    })
    created.addEventListener("error", () => { if (worker.current === created) setPython("unavailable") })
    created.postMessage({ type: "prepare", packages: pack.allowedPackages })
    return created
  }

  useEffect(() => {
    if (!pack.localEligible) { setPython(null); return }
    startWorker()
    return () => { worker.current?.terminate(); worker.current = null }
  }, [pack.slug, pack.localEligible])

  function runLocal(): Promise<LearnExecutionResult | null> {
    return new Promise((resolve) => {
      const target = worker.current ?? startWorker()
      if (!target) { resolve(null); return }
      const id = String(++localRunCount)
      let settled = false
      const finish = (value: LearnExecutionResult | null, restart = false) => {
        if (settled) return
        settled = true
        clearTimeout(timeout)
        target.removeEventListener("message", onMessage)
        target.removeEventListener("error", onError)
        // A stuck or broken run cannot be interrupted, so replace the worker for the next Run.
        if (restart && worker.current === target) startWorker()
        resolve(value)
      }
      const onMessage = (event: MessageEvent<{ type: string; id?: string; result?: LearnExecutionResult; unavailable?: boolean }>) => {
        if (event.data.type === "result" && event.data.id === id) finish(event.data.unavailable ? null : event.data.result ?? null, event.data.unavailable)
      }
      const onError = () => finish(null, true)
      const timeout = setTimeout(() => finish(null, true), 45000)
      target.addEventListener("message", onMessage)
      target.addEventListener("error", onError)
      target.postMessage({ type: "run", id, code, tests: pack.visibleTests, packages: pack.allowedPackages, prelude: pack.localPrelude, classes: pack.localClasses, kind: pack.kind })
    })
  }

  async function execute(kind: "run" | "submit") {
    if (busy) return
    if (new TextEncoder().encode(code).byteLength > 16000 || !code.trim()) {
      setError("Enter Python code under 16 KB before running it.")
      setResult(null)
      setConsoleTab("output")
      return
    }
    // The server grades Submit and runs problems that cannot run in the browser; both need an account.
    if (signedOut && (kind === "submit" || !pack.localEligible)) {
      setAction(kind)
      setResult(null)
      setError(kind === "submit" ? "Sign in to submit this problem." : "Sign in to run this problem.")
      setConsoleTab("output")
      return
    }
    setAction(kind)
    setResetNotice(false)
    setConsoleTab("output")
    setBusy(true)
    edited.current = true
    const runId = ++generation.current
    setError("")
    setResult(null)
    try {
      if (kind === "run" && pack.localEligible) {
        const local = await runLocal()
        if (local) {
          if (generation.current !== runId) return
          setResult(local)
          setResultSource("Local practice result · visible tests only")
          return
        }
      }
      const response = await fetch(`/api/learn/${kind === "run" ? "run" : "submit"}`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ slug: pack.slug, code }),
      })
      const data = await response.json().catch(() => null)
      if (!response.ok) throw new Error(typeof data?.error === "string" ? data.error : "Python execution is currently unavailable.")
      if (generation.current !== runId) return
      setResult(data as LearnExecutionResult)
      setResultSource(kind === "run" ? "VPS practice result · visible tests only" : "Trusted submission · all supplied tests")
    } catch (caught) {
      if (generation.current === runId) setError(caught instanceof Error ? caught.message : "Python execution is currently unavailable.")
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => {
    function handleShortcut(event: KeyboardEvent) {
      if (event.isComposing || event.repeat || event.altKey || event.shiftKey || !(event.metaKey || event.ctrlKey)) return
      const kind = event.key === "'" || event.code === "Quote" ? "run" : event.key === "Enter" ? "submit" : null
      if (!kind) return
      event.preventDefault()
      event.stopPropagation()
      void execute(kind)
    }
    // Monaco has its own keybindings, so intercept these before they reach the editor.
    window.addEventListener("keydown", handleShortcut, true)
    return () => window.removeEventListener("keydown", handleShortcut, true)
  })

  async function revealSolution() {
    if (solutionOpen) { setSolutionOpen(false); return }
    setSolutionOpen(true)
    if (solution) return
    setSolutionLoading(true)
    setSolutionError("")
    try {
      const response = await fetch(`/api/learn/solution/${encodeURIComponent(pack.slug)}`, { cache: "no-store" })
      if (!response.ok) throw new Error("Unable to load the worked solution.")
      const data = await response.json()
      if (typeof data.solution !== "string" || typeof data.explanationHtml !== "string") throw new Error("Unable to load the worked solution.")
      setSolution(data)
    } catch (caught) {
      setSolutionError(caught instanceof Error ? caught.message : "Unable to load the worked solution.")
    } finally {
      setSolutionLoading(false)
    }
  }

  function resetCode() {
    edited.current = true
    generation.current++
    setCode(pack.starter)
    setAction(null)
    setResetNotice(true)
    setResult(null)
    setError("")
    setConsoleTab("output")
  }

  function updateCode(value: string) {
    edited.current = true
    generation.current++
    setCode(value)
    setResult(null)
    setError("")
    setAction(null)
  }

  return <ResizablePanelGroup direction="horizontal" autoSaveId="learn-workspace-columns" className="min-h-0 flex-1">
      <ResizablePanel defaultSize={45} minSize={32} maxSize={55} className="min-h-0 min-w-0">
      <section className="flex h-full min-w-0 flex-col overflow-hidden rounded-lg border border-border/80 bg-card" aria-label="Learning material">
        <div className="flex shrink-0 items-center border-b border-border/70 px-3" role="tablist" aria-label="Learning material tabs">
          {(["concept", "problem"] as const).map((tab) => <button key={tab} type="button" role="tab" aria-selected={pane === tab} onClick={() => setPane(tab)} className={`border-b-2 px-4 py-3 text-xs font-medium transition-colors ${pane === tab ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground"}`}>{tab === "concept" ? "Concept" : "Problem"}</button>)}
          <Dialog>
            <DialogTrigger asChild>
              <button type="button" aria-label="Learning outcomes" title="Learning outcomes" className="ml-auto mr-1 inline-flex h-8 w-8 items-center justify-center rounded-full text-muted-foreground transition-colors hover:bg-muted hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"><CircleHelp className="h-4 w-4" /></button>
            </DialogTrigger>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>Learning outcomes</DialogTitle>
                <DialogDescription>{pack.title} · <span className="capitalize">{pack.difficulty}</span></DialogDescription>
              </DialogHeader>
              <ul className="space-y-2.5">{pack.objectives.map((item, index) => <li key={item} className="flex gap-3 text-sm leading-6"><span className="tabular-nums text-primary">{String(index + 1).padStart(2, "0")}</span><span>{item}</span></li>)}</ul>
            </DialogContent>
          </Dialog>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto px-6 py-6 xl:px-7">
          {pane === "concept" ? <>
            <article className="learn-prose" dangerouslySetInnerHTML={{ __html: articleHtml }} />
            <Button variant="outline" className="mt-8 rounded-md" onClick={() => setPane("problem")}>Go to problem <ArrowRight className="ml-2 h-4 w-4" /></Button>
          </> : <>
            <article className="learn-prose" dangerouslySetInnerHTML={{ __html: statementHtml }} />
            <section className="mt-8 border-t border-border/70 pt-6"><div className="flex items-center gap-2"><Lightbulb className="h-4 w-4 text-primary" /><h2 className="text-sm font-semibold">Progressive hints</h2></div><p className="mt-1 text-xs text-muted-foreground">Reveal one hint at a time.</p><div className="mt-4">{pack.hints.slice(0, hintCount).map((hint, index) => <div key={index} className="border-t border-border/70 py-3 first:border-t-0"><p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-primary">Hint {index + 1}</p><p className="mt-1 text-sm leading-6">{hint}</p></div>)}</div>{hintCount < pack.hints.length ? <Button variant="outline" size="sm" className="rounded-md" onClick={() => setHintCount(hintCount + 1)}>Reveal hint {hintCount + 1}<ChevronDown className="ml-2 h-3.5 w-3.5" /></Button> : <p className="text-xs text-muted-foreground">All hints revealed.</p>}</section>
            <section className="mt-7 border-t border-border/70 pt-6"><div className="flex items-center justify-between gap-3"><div><h2 className="text-sm font-semibold">Worked solution</h2><p className="mt-1 text-xs text-muted-foreground">Compare your approach when you are ready.</p></div><Button variant="outline" size="sm" className="rounded-md" onClick={revealSolution}>{solutionOpen ? <EyeOff className="mr-1.5 h-3.5 w-3.5" /> : <Eye className="mr-1.5 h-3.5 w-3.5" />}{solutionOpen ? "Hide" : "Reveal"}</Button></div>{solutionOpen && <div className="mt-5">{solutionLoading ? <p className="text-xs text-muted-foreground">Loading solution…</p> : solutionError ? <p role="alert" className="text-xs text-destructive">{solutionError}</p> : solution ? <><article className="learn-prose" dangerouslySetInnerHTML={{ __html: solution.explanationHtml }} /><div className="mt-4 overflow-hidden rounded-md border border-border/70 bg-white dark:bg-[#1e1e1e]"><MonacoCodeView code={solution.solution} dark={resolvedTheme === "dark"} /></div></> : null}</div>}</section>
          </>}
        </div>
      </section>
      </ResizablePanel>
      <ResizableHandle withHandle aria-label="Resize learning material and Python workspace" className="w-2 bg-border/60 transition-colors hover:bg-primary/30" />
      <ResizablePanel defaultSize={55} minSize={45} className="min-h-0 min-w-0">
      <section className="flex h-full min-w-0 flex-col overflow-hidden rounded-lg border border-border/80 bg-card" aria-label="Python workspace">
        <div className="flex shrink-0 items-center justify-between border-b border-border/70 pl-4 pr-3"><div className="flex items-center gap-3"><span className="border-b-2 border-primary px-2 py-3 text-xs font-medium">starter.py</span><span className="text-[11px] text-muted-foreground" role="status">{python === "preparing" ? "Preparing Python…" : "Python 3"}</span></div><div className="flex items-center gap-1.5"><button type="button" onClick={resetCode} title="Reset starter code" aria-label="Reset starter code" className="rounded-md p-2 text-muted-foreground hover:bg-muted hover:text-foreground"><RotateCcw className="h-3.5 w-3.5" /></button><Button size="sm" variant="outline" title={isMac === null ? "Run" : `Run (${isMac ? "⌘" : "Ctrl"}+')`} className="h-8 rounded-md px-3 text-xs" onClick={() => execute("run")} disabled={busy}><Play className="mr-1.5 h-3.5 w-3.5" />Run</Button><Button size="sm" title={isMac === null ? "Submit" : `Submit (${isMac ? "⌘+Return" : "Ctrl+Enter"})`} className="h-8 rounded-md px-3 text-xs" onClick={() => execute("submit")} disabled={busy}><Send className="mr-1.5 h-3.5 w-3.5" />Submit</Button></div></div>
        {signedOut && !pack.localEligible && <div role="note" className="flex shrink-0 items-center gap-2 border-b border-border/70 bg-muted/30 px-4 py-2 text-xs"><span className="text-muted-foreground">This problem runs on the course server.</span><Link href={`/auth/signin?callbackUrl=${encodeURIComponent(`/learn/problems/${pack.slug}`)}`} className="font-medium text-primary underline">Sign in</Link><span className="text-muted-foreground">to run or submit this problem.</span></div>}
        <ResizablePanelGroup direction="vertical" autoSaveId="learn-workspace-split" className="min-h-0 flex-1">
          <ResizablePanel defaultSize={74} minSize={25} className="min-h-0 min-w-0">
            <div className="h-full min-h-0 bg-white dark:bg-[#1e1e1e]"><MonacoCodeEditor code={code} onChange={updateCode} dark={resolvedTheme === "dark"} /></div>
          </ResizablePanel>
          <ResizableHandle withHandle aria-label="Resize editor and results" className="h-2 bg-border/60 transition-colors hover:bg-primary/30" />
          <ResizablePanel defaultSize={26} minSize={15} maxSize={70} className="min-h-0 min-w-0">
            <div className="flex h-full min-h-0 flex-col">
              <div className="flex items-center border-b border-border/70 px-2" role="tablist" aria-label="Workspace feedback">{([{"id":"tests","label":"Test cases"},{"id":"output","label":"Output"},{"id":"feedback","label":"Feedback"}] as const).map((tab) => <button key={tab.id} role="tab" aria-selected={consoleTab === tab.id} onClick={() => setConsoleTab(tab.id)} className={`border-b-2 px-3 py-2.5 text-xs font-medium ${consoleTab === tab.id ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground"}`}>{tab.label}</button>)}<span className="ml-auto pr-3 text-[11px] text-muted-foreground">{pack.testCount} supplied tests</span></div>
              <div className="min-h-0 flex-1 overflow-y-auto px-5 py-4 text-xs leading-5">{consoleTab === "tests" ? <><p className="text-muted-foreground">Visible cases from the supplied pack. In snippets, <code>S</code> means the implementation being tested.</p><div className="mt-3">{pack.visibleTests.map((test) => <div key={test.name} className="border-t border-border/70 py-3 first:border-t-0 first:pt-0"><p className="font-medium">{test.name}</p><pre className="mt-1 overflow-x-auto text-[11px] text-muted-foreground"><code>{test.code || "See the problem statement for example behaviour."}</code></pre></div>)}</div></> : consoleTab === "output" ? <div role="status">{busy ? <p className="font-medium">{action === "run" ? "Running visible tests…" : "Grading submission…"}</p> : error ? <p role="alert" className="font-medium text-destructive">{error}{error.includes("Sign in") && <span className="ml-2"><Link href={`/auth/signin?callbackUrl=${encodeURIComponent(`/learn/problems/${pack.slug}`)}`} className="underline">Sign in</Link></span>}</p> : result ? <ExecutionResult result={result} source={resultSource} submitted={action === "submit"} advice={advice} /> : <><p className="font-medium">{resetNotice ? "Starter restored" : "Ready to practise"}</p><p className="mt-2 text-muted-foreground">{resetNotice ? "The supplied starter code is back in the editor." : "Run checks visible tests for practice. Submit grades all supplied tests and saves your result when signed in."}</p>{signedOut && pack.localEligible && <p className="mt-3 text-foreground">Run works in your browser without an account. <Link href={`/auth/signin?callbackUrl=${encodeURIComponent(`/learn/problems/${pack.slug}`)}`} className="font-medium text-primary underline">Sign in</Link> to submit this problem.</p>}</>}</div> : <><p className="text-muted-foreground">Guidance from the supplied pack. These are possible checks, not results from your code.</p><div className="mt-3">{pack.failureFeedback.map((item) => <div key={item.test} className="border-t border-border/70 py-3 first:border-t-0 first:pt-0"><p className="font-medium">{item.test}</p><p className="mt-1 text-muted-foreground">{item.advice}</p></div>)}</div></>}</div>
            </div>
          </ResizablePanel>
        </ResizablePanelGroup>
      </section>
      </ResizablePanel>
  </ResizablePanelGroup>
}
