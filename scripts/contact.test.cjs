const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const ts = require('typescript')

// Exercise the real route handlers with isolated database/session boundaries.
function load(file, mocks = {}) {
  const source = fs.readFileSync(path.join(__dirname, '..', file), 'utf8')
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true },
  })
  const context = { exports: {}, require: name => name in mocks ? mocks[name] : require(name) }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}
const schemas = load('lib/validations.ts')
const nextServer = { NextResponse: { json: (body, options = {}) => ({ body: JSON.parse(JSON.stringify(body)), status: options.status || 200, headers: options.headers }) } }
const valid = { firstName: ' Ada ', lastName: ' Lovelace ', email: ' ADA@example.com ', subject: ' Workshop idea ', message: ' Could we host a workshop? ' }
const request = body => ({ json: async () => body })

function publicRoute(create, connect = async () => {}, session = { user: { email: 'ADA@example.com' } }) {
  return load('app/api/contact/route.ts', {
    'next/server': nextServer, '@/lib/mongodb': connect,
    '@/models/ContactQuery': { create }, '@/lib/validations': schemas,
    'next-auth': { getServerSession: async () => session }, '@/lib/auth': { authOptions: {} },
  })
}

test('contact submission normalizes fields, strips extra fields, and waits for persistence', async () => {
  let saved
  const route = publicRoute(async data => { saved = data })
  const response = await route.POST(request({ ...valid, role: 'admin' }))
  assert.equal(response.status, 201)
  assert.deepEqual(JSON.parse(JSON.stringify(saved)), { firstName: 'Ada', lastName: 'Lovelace', email: 'ada@example.com', subject: 'Workshop idea', message: 'Could we host a workshop?' })
  assert.equal(response.body.email, undefined)
})

test('signed-in submissions use the session email even when a different email is submitted', async () => {
  let saved
  const route = publicRoute(async data => { saved = data }, undefined, { user: { email: 'member@example.com' } })
  assert.equal((await route.POST(request({ ...valid, email: 'someone-else@example.com' }))).status, 201)
  assert.equal(saved.email, 'member@example.com')
})

test('signed-in submissions can omit email', async () => {
  const { email, ...body } = valid
  let saved
  const route = publicRoute(async data => { saved = data }, undefined, { user: { email: 'member@example.com' } })
  assert.equal((await route.POST(request(body))).status, 201)
  assert.equal(saved.email, 'member@example.com')
})

test('signed-out users and sessions without an email cannot submit even with a valid body', async () => {
  let writes = 0
  for (const session of [null, { user: {} }]) {
    const route = publicRoute(async () => { writes++ }, undefined, session)
    assert.equal((await route.POST(request(valid))).status, 401)
  }
  assert.equal(writes, 0)
})

test('invalid, blank, oversized, and malformed submissions never reach the database', async () => {
  let writes = 0
  const route = publicRoute(async () => { writes++ })
  for (const body of [{}, { ...valid, message: '   ' }, { ...valid, message: 'x'.repeat(5001) }, { ...valid, subject: 'x'.repeat(201) }]) {
    assert.equal((await route.POST(request(body))).status, 400)
  }
  assert.equal((await route.POST({ json: async () => { throw new SyntaxError() } })).status, 400)
  assert.equal(writes, 0)
})

test('storage failures return an error instead of a false success', async () => {
  const route = publicRoute(async () => { throw new Error('private database details') })
  const response = await route.POST(request(valid))
  assert.equal(response.status, 500)
  assert.doesNotMatch(response.body.error, /private database/)
})

function inboxRoute(session, model, connect = async () => {}) {
  return load('app/api/admin/queries/route.ts', {
    'next/server': nextServer, 'next-auth': { getServerSession: async () => session },
    '@/lib/auth': { authOptions: {} }, '@/lib/mongodb': connect, '@/models/ContactQuery': model,
  })
}
const pageRequest = page => ({ nextUrl: new URL(`http://localhost/api/admin/queries?page=${page}`) })

test('anonymous and member sessions cannot access messages or query the database', async () => {
  let connected = false
  for (const [session, expected] of [[null, 401], [{ user: { role: 'user' } }, 403]]) {
    const route = inboxRoute(session, {}, async () => { connected = true })
    assert.equal((await route.GET(pageRequest(1))).status, expected)
  }
  assert.equal(connected, false)
})

test('invalid pagination is rejected before querying the database', async () => {
  let connected = false
  const route = inboxRoute({ user: { role: 'admin' } }, {}, async () => { connected = true })
  for (const page of ['0', '-1', '1.2', 'NaN', '100001']) assert.equal((await route.GET(pageRequest(page))).status, 400)
  assert.equal(connected, false)
})

test('admin inbox uses bounded newest-first pagination and private uncached responses', async () => {
  const calls = {}
  const chain = {
    select(value) { calls.select = value; return this },
    sort(value) { calls.sort = JSON.parse(JSON.stringify(value)); return this },
    skip(value) { calls.skip = value; return this },
    limit(value) { calls.limit = value; return this },
    async lean() { return [{ subject: 'Hello', message: 'A community question' }] },
  }
  const route = inboxRoute({ user: { role: 'admin' } }, { find: () => chain, countDocuments: async () => 21 })
  const response = await route.GET(pageRequest(2))
  assert.equal(response.status, 200)
  assert.equal(calls.skip, 20)
  assert.equal(calls.limit, 20)
  assert.deepEqual(calls.sort, { createdAt: -1, _id: -1 })
  assert.deepEqual(response.body.pagination, { page: 2, total: 21, pages: 2 })
  assert.equal(response.headers['Cache-Control'], 'no-store')
  assert.equal(response.body.queries[0].message, 'A community question')
})

test('inbox storage errors return a recoverable error', async () => {
  const route = inboxRoute({ user: { role: 'admin' } }, {}, async () => { throw new Error('offline') })
  assert.equal((await route.GET(pageRequest(1))).status, 500)
})

function deleteRoute(session, model, connect = async () => {}) {
  return load('app/api/admin/queries/[id]/route.ts', {
    'next/server': nextServer, 'next-auth': { getServerSession: async () => session },
    '@/lib/auth': { authOptions: {} }, '@/lib/mongodb': connect, '@/models/ContactQuery': model,
  })
}
const queryId = '507f1f77bcf86cd799439011'
const deleteContext = id => ({ params: Promise.resolve({ id }) })

test('query deletion rejects anonymous and member sessions before accessing storage', async () => {
  let connected = false
  for (const [session, status] of [[null, 401], [{ user: { role: 'user' } }, 403]]) {
    const route = deleteRoute(session, {}, async () => { connected = true })
    assert.equal((await route.DELETE({}, deleteContext(queryId))).status, status)
  }
  assert.equal(connected, false)
})

test('query deletion validates IDs before accessing storage', async () => {
  let connected = false
  const route = deleteRoute({ user: { role: 'admin' } }, {}, async () => { connected = true })
  for (const id of ['invalid', '', '507f1f77bcf86cd79943901z']) assert.equal((await route.DELETE({}, deleteContext(id))).status, 400)
  assert.equal(connected, false)
})

test('admin deletion removes only the requested record without returning message contents', async () => {
  const ids = []
  const route = deleteRoute({ user: { role: 'admin' } }, { findByIdAndDelete: async id => { ids.push(id); return { _id: id, message: 'Private text' } } })
  const response = await route.DELETE({}, deleteContext(queryId))
  assert.equal(response.status, 200)
  assert.deepEqual(ids, [queryId])
  assert.deepEqual(response.body, { message: 'Query deleted' })
})

test('deleting a missing record returns 404 and database failures return 500', async () => {
  const session = { user: { role: 'admin' } }
  assert.equal((await deleteRoute(session, { findByIdAndDelete: async () => null }).DELETE({}, deleteContext(queryId))).status, 404)
  const response = await deleteRoute(session, { findByIdAndDelete: async () => { throw new Error('Private database details') } }).DELETE({}, deleteContext(queryId))
  assert.equal(response.status, 500)
  assert.doesNotMatch(response.body.error, /Private database/)
})
