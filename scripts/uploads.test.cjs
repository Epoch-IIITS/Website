const { test } = require("node:test")
const assert = require("node:assert/strict")
const fs = require("node:fs")
const path = require("node:path")
const vm = require("node:vm")
const ts = require("typescript")

function load(file, mocks = {}, globals = {}) {
  const { outputText } = ts.transpileModule(fs.readFileSync(path.join(__dirname, "..", file), "utf8"), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true },
  })
  const context = {
    exports: {}, File, Blob, FormData, Response, URL, Buffer, Error,
    console: { error() {} },
    require: (name) => name in mocks ? mocks[name] : require(name),
    ...globals,
  }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}

const policy = load("lib/image-upload.ts")
const photo = (size = 3, type = "image/jpeg") => new File([new Uint8Array(size)], "photo.jpg", { type })
const imageUrl = "https://res.cloudinary.com/test/image/upload/epoch/gallery/photo.jpg"
const client = (fetch) => load("lib/image-upload.ts", {}, { fetch })

test("oversized, empty and unsupported images fail before any request is sent", async () => {
  let requests = 0
  const { uploadImage } = client(async () => { requests++; return Response.json({ url: imageUrl }) })
  await assert.rejects(uploadImage(photo(policy.IMAGE_UPLOAD_MAX_BYTES + 1), "gallery"), /4 MB/)
  await assert.rejects(uploadImage(photo(0), "blog"), /empty/)
  await assert.rejects(uploadImage(photo(3, "image/svg+xml"), "event"), /JPEG, PNG, GIF or WebP/)
  await assert.rejects(uploadImage(photo(3, "image/gif"), "team"), /JPG, PNG or WebP/)
  assert.equal(requests, 0)
  assert.equal(policy.validateImageUpload(photo(policy.IMAGE_UPLOAD_MAX_BYTES)), null)
  assert.equal(policy.validateImageUpload(photo(3, "image/gif")), null)
})

test("a plain-text hosting 413 becomes a size error without parsing JSON", async () => {
  const { uploadImage } = client(async () => new Response("Request Entity Too Large", { status: 413 }))
  await assert.rejects(uploadImage(photo(), "gallery"), /Choose an image of 4 MB or less/)
})

test("HTTP failures have actionable messages even when the response is HTML or empty", async () => {
  for (const [status, expected] of [
    [401, /Sign in again/], [403, /permission/], [408, /timed out/], [429, /Wait a moment/],
    [500, /temporarily unavailable/], [502, /temporarily unavailable/], [504, /timed out/],
    [400, /Image upload failed/], [404, /Image upload failed/],
  ]) {
    for (const body of ["<html>Proxy error</html>", ""]) {
      const { uploadImage } = client(async () => new Response(body, { status }))
      await assert.rejects(uploadImage(photo(), "gallery"), expected)
    }
  }
})

test("structured validation messages are preserved and unexpected error shapes are safe", async () => {
  const { uploadImage } = client(async () => Response.json({ error: "Choose a PNG image." }, { status: 415 }))
  await assert.rejects(uploadImage(photo(), "gallery"), /Choose a PNG image/)
  for (const body of [null, [], { error: {} }, { error: "" }]) {
    const api = client(async () => Response.json(body, { status: 400 }))
    await assert.rejects(api.uploadImage(photo(), "blog"), /Image upload failed/)
  }
})

test("network errors do not leak low-level fetch errors", async () => {
  const { uploadImage } = client(async () => { throw new TypeError("Failed to fetch") })
  await assert.rejects(uploadImage(photo(), "project"), /Check your connection/)
})

test("malformed success responses never produce a saved image URL", async () => {
  for (const body of ["<html>Sign in</html>", "", "null", "{}", '{"url":42}', '{"url":""}', '{"url":"javascript:alert(1)"}']) {
    const { uploadImage } = client(async () => new Response(body))
    await assert.rejects(uploadImage(photo(), "gallery"), /invalid upload response/)
  }
})

test("valid uploads keep their purpose, endpoint, and original filename", async () => {
  for (const purpose of ["blog", "project", "event", "gallery", "team"]) {
    const { uploadImage } = client(async (endpoint, options) => {
      assert.equal(endpoint, purpose === "team" ? "/api/team/upload" : "/api/upload")
      assert.equal(options.method, "POST")
      assert.equal(options.body.get("file").name, purpose === "team" ? "profile.jpg" : "photo.jpg")
      assert.equal(options.body.get("purpose"), purpose === "team" ? null : purpose)
      return Response.json({ url: imageUrl })
    })
    assert.equal((await uploadImage(photo(), purpose, purpose === "team" ? "profile.jpg" : undefined)).url, imageUrl)
  }
})

function route(kind, role = "admin", failRegistration = false) {
  const calls = []
  const result = { url: imageUrl, publicId: "epoch/gallery/photo", assetId: "asset-1", resourceType: "image" }
  const api = load(kind === "team" ? "app/api/team/upload/route.ts" : "app/api/upload/route.ts", {
    "next/server": { NextResponse: Response },
    "next-auth": { getServerSession: async () => role ? { user: { id: "test-user", role } } : null },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => { calls.push("connect") },
    "@/lib/image-upload": policy,
    "@/lib/cloudinary-media": {
      isMediaPurpose: (value) => ["blog", "project", "event", "gallery", "team"].includes(value),
      uploadManagedImage: async () => { calls.push("upload"); return result },
      destroyManagedImage: async () => { calls.push("rollback") },
    },
    "@/lib/media-assets": {
      registerUploadedMedia: async () => {
        calls.push("register")
        if (failRegistration) throw new Error("Database unavailable")
      },
    },
  })
  return { ...api, calls }
}

function request(file, purpose) {
  const body = new FormData()
  if (file !== undefined) body.append("file", file)
  if (purpose !== undefined) body.append("purpose", purpose)
  return new Request("http://localhost/api/upload", { method: "POST", body })
}

test("upload APIs reject malformed files and multipart bodies before touching storage", async () => {
  for (const kind of ["content", "team"]) {
    const api = route(kind)
    for (const [file, status, expected] of [
      [undefined, 400, /No .*received/], ["not a file", 400, /No .*received/],
      [photo(0), 400, /empty/], [photo(policy.IMAGE_UPLOAD_MAX_BYTES + 1), 413, /4 MB/],
      [photo(1, "application/pdf"), 415, /Choose/],
    ]) {
      const result = await api.POST(request(file))
      assert.equal(result.status, status)
      assert.match((await result.json()).error, expected)
    }
    const malformed = await api.POST(new Request("http://localhost/api/upload", { method: "POST", body: "bad multipart" }))
    assert.equal(malformed.status, 400)
    assert.match((await malformed.json()).error, /Could not read the upload/)
    assert.deepEqual(api.calls, [])
  }
})

test("upload API authorization still runs before parsing files or accessing storage", async () => {
  for (const [kind, role, status] of [["content", null, 401], ["content", "member", 403], ["team", null, 401]]) {
    const api = route(kind, role)
    const response = await api.POST({ formData() { throw new Error("must not parse") } })
    assert.equal(response.status, status)
    assert.deepEqual(api.calls, [])
  }
  const member = route("team", "member")
  assert.equal((await member.POST(request(photo()))).status, 200)
  assert.deepEqual(member.calls, ["upload", "connect", "register"])
})

test("both upload APIs accept exactly 4 MB and preserve media registration and rollback", async () => {
  for (const kind of ["content", "team"]) {
    const api = route(kind)
    assert.equal((await api.POST(request(photo(policy.IMAGE_UPLOAD_MAX_BYTES)))).status, 200)
    assert.deepEqual(api.calls, ["upload", "connect", "register"])
    const failing = route(kind, "admin", true)
    assert.equal((await failing.POST(request(photo()))).status, 500)
    assert.deepEqual(failing.calls, ["upload", "connect", "register", "rollback"])
  }
})

test("content purposes and team-specific file formats remain restricted", async () => {
  const content = route("content")
  for (const purpose of ["team", "unknown"]) {
    assert.equal((await content.POST(request(photo(), purpose))).status, 400)
  }
  assert.deepEqual(content.calls, [])
  const team = route("team")
  assert.equal((await team.POST(request(photo(1, "image/gif")))).status, 415)
  assert.deepEqual(team.calls, [])
})
