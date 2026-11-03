"use client"

import { useRef } from "react"

const KEYS = [
  { label: "Tab", text: "    " }, { label: ":", text: ":" }, { label: "(", text: "(" }, { label: ")", text: ")" },
  { label: "[", text: "[" }, { label: "]", text: "]" }, { label: "{", text: "{" }, { label: "}", text: "}" },
  { label: "\"", text: "\"" }, { label: "'", text: "'" }, { label: "=", text: "=" }, { label: "_", text: "_" },
  { label: "#", text: "#" }, { label: ",", text: "," }, { label: ".", text: "." },
]

// Touch keyboards handle a plain textarea far better than Monaco, and phones skip Monaco's download.
export function MobileCodeEditor({ code, onChange }: { code: string; onChange: (value: string) => void }) {
  const input = useRef<HTMLTextAreaElement>(null)

  function insert(text: string) {
    const target = input.current
    if (!target) return
    target.setRangeText(text, target.selectionStart, target.selectionEnd, "end")
    onChange(target.value)
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Tab") {
      event.preventDefault()
      insert("    ")
    } else if (event.key === "Enter" && !event.nativeEvent.isComposing) {
      // Keep Python's indentation, and step in after a block opener.
      const target = event.currentTarget
      const line = target.value.slice(target.value.lastIndexOf("\n", target.selectionStart - 1) + 1, target.selectionStart)
      event.preventDefault()
      insert(`\n${line.match(/^\s*/)?.[0] ?? ""}${line.trimEnd().endsWith(":") ? "    " : ""}`)
    }
  }

  return <div className="flex min-h-0 flex-1 flex-col">
    {/* Keep focus in the editor so these keys do not dismiss the keyboard. */}
    <div onMouseDown={(event) => event.preventDefault()} className="flex shrink-0 gap-1 overflow-x-auto border-b border-border/70 bg-muted/30 px-2 py-1.5" role="group" aria-label="Python symbols">
      {KEYS.map((key) => <button key={key.label} type="button" onClick={() => insert(key.text)} className="h-9 min-w-9 shrink-0 rounded-md border border-border bg-card px-2.5 font-mono text-sm active:bg-muted">{key.label}</button>)}
    </div>
    <textarea
      ref={input}
      value={code}
      onChange={(event) => onChange(event.target.value)}
      onKeyDown={handleKeyDown}
      aria-label="Python code"
      wrap="off"
      spellCheck={false}
      autoCapitalize="off"
      autoCorrect="off"
      autoComplete="off"
      className="learn-mobile-editor min-h-0 w-full flex-1 resize-none overflow-auto whitespace-pre bg-white p-3 font-mono text-base leading-6 text-foreground outline-none dark:bg-[#1e1e1e]"
    />
  </div>
}
