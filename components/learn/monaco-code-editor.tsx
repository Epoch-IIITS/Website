"use client"

import { useEffect, useRef } from "react"
import * as monaco from "monaco-editor"

// This module is loaded only by the problem workspace. Use the installed editor
// assets so the editor does not depend on a CDN at runtime.
if (typeof self !== "undefined") {
  self.MonacoEnvironment = {
    getWorker() {
      return new Worker(new URL("monaco-editor/editor/editor.worker.js", import.meta.url), { type: "module" })
    },
  }
}

const BASE_OPTIONS: monaco.editor.IStandaloneEditorConstructionOptions = {
  language: "python", minimap: { enabled: false }, fontSize: 13, lineHeight: 21, scrollBeyondLastLine: false,
  automaticLayout: true, tabSize: 4, fontFamily: "'SFMono-Regular', Consolas, 'Liberation Mono', monospace",
}

// Each mount creates its own editor and disposes it on unmount. Owning the lifecycle here (rather than
// through a wrapper that reuses its instance) keeps the editor valid when React remounts the workspace,
// for example when moving between problems or when development mode re-runs effects.
function useMonaco(container: React.RefObject<HTMLDivElement | null>, code: string, dark: boolean,
  options: monaco.editor.IStandaloneEditorConstructionOptions, onChange?: (value: string) => void) {
  const editor = useRef<monaco.editor.IStandaloneCodeEditor | null>(null)
  const change = useRef(onChange)
  const applying = useRef(false)
  change.current = onChange

  useEffect(() => {
    if (!container.current) return
    const instance = monaco.editor.create(container.current, { ...BASE_OPTIONS, ...options, value: code, theme: dark ? "vs-dark" : "vs" })
    const subscription = instance.onDidChangeModelContent(() => {
      if (!applying.current) change.current?.(instance.getValue())
    })
    editor.current = instance
    return () => {
      subscription.dispose()
      instance.getModel()?.dispose()
      instance.dispose()
      editor.current = null
    }
    // The editor is created once per mount; later prop changes are applied by the effects below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const instance = editor.current
    if (!instance || instance.getValue() === code) return
    // Updates from props (reset, a loaded submission) are not learner edits.
    applying.current = true
    instance.setValue(code)
    applying.current = false
  }, [code])

  useEffect(() => {
    monaco.editor.setTheme(dark ? "vs-dark" : "vs")
  }, [dark])
}

export function MonacoCodeEditor({ code, onChange, dark }: { code: string; onChange: (value: string) => void; dark: boolean }) {
  const container = useRef<HTMLDivElement>(null)
  useMonaco(container, code, dark, { padding: { top: 18 }, wordWrap: "on" }, onChange)
  return <div ref={container} className="h-full w-full" />
}

// Read-only, syntax-highlighted view sized to its content (used for worked solutions).
export function MonacoCodeView({ code, dark }: { code: string; dark: boolean }) {
  const container = useRef<HTMLDivElement>(null)
  useMonaco(container, code, dark, {
    readOnly: true, domReadOnly: true, padding: { top: 14, bottom: 14 }, wordWrap: "off", renderLineHighlight: "none",
    folding: false, contextmenu: false, scrollbar: { alwaysConsumeMouseWheel: false },
  })
  const height = Math.min(code.split("\n").length, 60) * 21 + 40  // room for padding and a horizontal scrollbar
  return <div ref={container} style={{ height }} className="w-full" />
}
