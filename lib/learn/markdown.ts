import "server-only"
import { Marked } from "marked"
import markedKatex from "marked-katex-extension"
import sanitizeHtml from "sanitize-html"

// Static lesson diagrams are inline SVG. Only drawing elements and presentation attributes are
// allowed: no scripts, event handlers, links, styles or foreign content.
const svgTags = ["svg", "title", "g", "line", "polyline", "polygon", "path", "rect", "circle", "ellipse", "text", "tspan"]
const svgAttributes = ["viewbox", "xmlns", "width", "height", "role", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "d", "points",
  "fill", "stroke", "stroke-width", "stroke-dasharray", "stroke-linecap", "stroke-linejoin", "opacity", "font-size", "font-weight", "text-anchor", "dominant-baseline", "transform"]

const mathMarkdown = new Marked(markedKatex({ throwOnError: false, nonStandard: true }))

function normalizeDisplayMath(markdown: string) {
  return markdown.split(/(```[\s\S]*?```)/g).map((part, index) => index % 2
    ? part
    : part.replace(/\$\$([\s\S]*?)\$\$/g, (_match, formula: string) => `\n\n$$\n${formula.trim()}\n$$\n\n`)
  ).join("")
}

export function markdownHtml(markdown: string) {
  const rendered = mathMarkdown.parse(normalizeDisplayMath(markdown), { async: false }) as string
  const safeHtml = sanitizeHtml(rendered, {
    allowedTags: [...sanitizeHtml.defaults.allowedTags, ...svgTags, "img", "math", "semantics", "annotation", "mrow", "mi", "mo", "mn", "mtext", "mfrac", "msqrt", "mroot", "msub", "msup", "msubsup", "munder", "mover", "munderover", "mtable", "mtr", "mtd", "mspace", "menclose", "mpadded", "mstyle"],
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      code: ["class"], a: ["href", "title", "target", "rel"], span: ["class", "style", "aria-hidden"],
      math: ["xmlns", "display"], annotation: ["encoding"], "*": ["aria-label"],
      ...Object.fromEntries(svgTags.map((tag) => [tag, svgAttributes])),
    },
    allowedSchemes: ["http", "https", "mailto"],
    // External links (lesson references and further reading) open in a new tab.
    transformTags: {
      a: (tagName, attribs) => /^https?:\/\//i.test(attribs.href ?? "")
        ? { tagName, attribs: { ...attribs, target: "_blank", rel: "noopener noreferrer" } }
        : { tagName, attribs },
    },
  })
  return safeHtml.replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, (_match, diagram: string) => `<div class="learn-diagram mermaid" role="img" aria-label="Concept diagram">${diagram}</div>`)
}
