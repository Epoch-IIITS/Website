const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const { spawnSync } = require('node:child_process')
const ts = require('typescript')

const root = path.join(__dirname, '..')
const pack = JSON.parse(fs.readFileSync(path.join(root, 'lib/learn/packs.generated.json')))['factorial-validated']
const privateTests = JSON.parse(fs.readFileSync(path.join(root, 'executor/tests.generated.json')))['factorial-validated'].tests
const nextServer = { NextResponse: { json: (body, options = {}) => ({ body: JSON.parse(JSON.stringify(body)), status: options.status || 200, headers: options.headers }) } }
const req = body => ({ json: async () => body, headers: new Map() })

function load(file, mocks = {}, globals = {}) {
  const source = fs.readFileSync(path.join(root, file), 'utf8')
  const { outputText } = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, esModuleInterop: true } })
  const context = { exports: {}, require: name => name in mocks ? mocks[name] : require(name), ...globals }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}

test('problem page payload excludes the reference solution until Reveal', () => {
  const publicPack = load('lib/learn/public-pack.ts', {
    'server-only': {}, '@/lib/learn/local-compat.generated.json': { [pack.slug]: true },
  }).publicProblemPack(pack)
  assert.equal(publicPack.solution, undefined)
  assert.equal(publicPack.solutionExplanation, undefined)
  assert.equal(publicPack.localEligible, true)
  assert.equal(publicPack.visibleTests.length, 3)
})

test('Learn request validation enforces known packs and the code-size limit', async () => {
  const parser = load('lib/learn/request.ts', {
    '@/lib/learn/executor': { MAX_CODE_BYTES: 16000 },
    '@/lib/learn/pack': { packBySlug: slug => slug === pack.slug ? pack : undefined },
  }, { Buffer })
  assert.equal(await parser.parseLearnRequest(req({ slug: pack.slug, code: 'x'.repeat(16001) })), null)
  assert.equal(await parser.parseLearnRequest(req({ slug: 'unknown', code: 'print(1)' })), null)
  assert.equal((await parser.parseLearnRequest(req({ slug: pack.slug, code: 'print(1)' }))).slug, pack.slug)
})

test('visible local harness runs the first supplied cases and labels real failures', () => {
  const worker = fs.readFileSync(path.join(root, 'public/learn/pyodide-worker.mjs'), 'utf8')
  const context = { self: {} }
  vm.runInNewContext(worker + '\nglobalThis.python = runVisibleTests', context)
  const run = code => {
    const payload = JSON.stringify({ code, packages: [], tests: pack.visibleTests })
    const python = spawnSync('python3', ['-B', '-c', 'import os\npayload_json=os.environ["LEARN_PAYLOAD"]\n' + context.python + '\nprint(json.dumps(response))'], { encoding: 'utf8', env: { ...process.env, LEARN_PAYLOAD: payload }, timeout: 5000 })
    assert.equal(python.status, 0, python.stderr)
    return JSON.parse(python.stdout)
  }
  assert.deepEqual([run(pack.solution).passed, run(pack.starter).passed], [3, 0])
})

test('local harness runs whole-program steps with stdin and test-module helpers', () => {
  const packs = JSON.parse(fs.readFileSync(path.join(root, 'lib/learn/packs.generated.json')))
  const worker = fs.readFileSync(path.join(root, 'public/learn/pyodide-worker.mjs'), 'utf8')
  const context = { self: {} }
  vm.runInNewContext(worker + '\nglobalThis.python = runVisibleTests', context)
  const run = (target, code) => {
    const payload = JSON.stringify({ code, packages: [], tests: target.visibleTests, prelude: target.localPrelude, kind: target.kind })
    const python = spawnSync('python3', ['-B', '-c', 'import os\npayload_json=os.environ["LEARN_PAYLOAD"]\n' + context.python + '\nprint(json.dumps(response))'], { encoding: 'utf8', env: { ...process.env, LEARN_PAYLOAD: payload }, timeout: 5000 })
    assert.equal(python.status, 0, python.stderr)
    return JSON.parse(python.stdout)
  }
  for (const slug of ['input-output', 'conditionals']) {
    const target = packs[slug]
    assert.equal(target.kind, 'script')
    assert.ok(target.localPrelude.length > 0 || slug === 'input-output')
    assert.deepEqual([run(target, target.solution).passed, run(target, target.starter).passed < 3], [3, true])
  }
})

test('catalogue follows the curriculum path, with FastAPI after pandas', () => {
  const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'lib/learn/catalogue.generated.json')))
  const slugs = catalogue.topics.map(topic => topic.slug)
  assert.equal(slugs.indexOf('fastapi'), slugs.indexOf('pandas') + 1)
  assert.equal(catalogue.problems.filter(problem => !problem.optional).length, catalogue.topics.reduce((sum, topic) => sum + topic.problemCount, 0))
  assert.equal(catalogue.projects.length, catalogue.topics.reduce((sum, topic) => sum + topic.projectCount, 0))
  assert.equal(catalogue.problems[0].slug, 'hello-print')
})

test('container runner grades all supplied tests and separates practice from submit', () => {
  const run = (mode, code) => {
    const process = spawnSync('python3', ['-B', path.join(root, 'executor/runner.py')], { input: JSON.stringify({ mode, code, tests: privateTests }), encoding: 'utf8', timeout: 60000 })
    assert.equal(process.status, 0, process.stderr)
    // A warm container announces READY after its imports, then prints one JSON result.
    const lines = process.stdout.trim().split('\n')
    assert.equal(lines[0], 'READY')
    return JSON.parse(lines.at(-1))
  }
  assert.deepEqual([run('run', pack.solution).passed, run('submit', pack.solution).passed, run('submit', pack.starter).passed], [3, pack.testCount, 0])
  assert.deepEqual(run('submit', pack.solution).failed, [])
  const failed = run('submit', pack.starter).failed
  assert.equal(failed.length, pack.testCount)
  assert.ok(failed.every(name => /^test_\w+$/.test(name)))
})

function runRoute(session, result, calls = []) {
  return load('app/api/learn/run/route.ts', {
    'next/server': nextServer, 'next-auth': { getServerSession: async () => session }, '@/lib/auth': { authOptions: {} },
    '@/lib/learn/request': { parseLearnRequest: async () => ({ slug: pack.slug, code: pack.solution }) },
    '@/lib/learn/executor': {
      executeOnVps: async (...args) => { calls.push(args); return result },
      EXECUTION_UNAVAILABLE: 'Python execution is currently unavailable.',
      isRateLimited: value => Boolean(value && value.rateLimited),
      rateLimitMessage: value => `Too many requests. Try again in ${value.retryAfter} s.`,
    },
  })
}

test('fallback Run returns an unavailable state when the executor is absent', async () => {
  const response = await runRoute({ user: { id: 'member-1' } }, null).POST(req({}))
  assert.equal(response.status, 503)
  assert.equal(response.body.error, 'Python execution is currently unavailable.')
})

test('server Run requires sign-in and passes the user to the executor', async () => {
  const calls = []
  const signedOut = await runRoute(null, { passed: 3, total: 3, status: 'passed' }, calls).POST(req({}))
  assert.equal(signedOut.status, 401)
  assert.equal(signedOut.body.error, 'Sign in to run this problem.')
  assert.equal(calls.length, 0)
  const ok = await runRoute({ user: { id: 'member-1' } }, { passed: 3, total: 3, status: 'passed' }, calls).POST(req({}))
  assert.equal(ok.status, 200)
  assert.deepEqual(calls[0].slice(0, 2).concat(calls[0][3]), ['run', pack.slug, 'member-1'])
})

test('rate-limited Run and Submit return 429 and never save', async () => {
  const limited = { rateLimited: true, retryAfter: 12, inFlight: false }
  const run = await runRoute({ user: { id: 'member-1' } }, limited).POST(req({}))
  assert.equal(run.status, 429)
  assert.equal(run.headers['Retry-After'], '12')
  assert.match(run.body.error, /Try again in 12 s/)
  let writes = 0
  const submit = await submitRoute({ user: { id: 'member-1' } }, limited, async () => { writes++ }).POST(req({}))
  assert.equal(submit.status, 429)
  assert.equal(writes, 0)
})

function submitRoute(session, result, create) {
  return load('app/api/learn/submit/route.ts', {
    'next/server': nextServer, 'next-auth': { getServerSession: async () => session }, '@/lib/auth': { authOptions: {} },
    '@/lib/learn/request': { parseLearnRequest: async () => ({ slug: pack.slug, code: pack.solution }) },
    '@/lib/learn/executor': {
      executeOnVps: async () => result, EXECUTION_UNAVAILABLE: 'Python execution is currently unavailable.',
      isRateLimited: value => Boolean(value && value.rateLimited),
      rateLimitMessage: value => `Too many requests. Try again in ${value.retryAfter} s.`,
    },
    '@/lib/mongodb': async () => {}, '@/models/LearnSubmission': { create },
  })
}

test('Submit requires authentication, and unavailable grading never writes', async () => {
  let writes = 0
  const create = async () => { writes++ }
  assert.equal((await submitRoute(null, { passed: pack.testCount, total: pack.testCount, status: 'passed' }, create).POST(req({}))).status, 401)
  const unavailable = await submitRoute({ user: { id: 'member-1' } }, null, create).POST(req({}))
  assert.equal(unavailable.status, 503)
  assert.equal(unavailable.body.error, 'Python execution is currently unavailable.')
  assert.equal(writes, 0)
})

test('Submit saves only the authenticated owner and the trusted grading result', async () => {
  let saved
  const route = submitRoute({ user: { id: 'member-1' } }, { passed: pack.testCount, total: pack.testCount, status: 'passed' }, async data => { saved = data; return { _id: { toString: () => 'submission-1' } } })
  const response = await route.POST(req({ user: 'another-user', passed: 7 }))
  assert.equal(response.status, 201)
  assert.equal(saved.user, 'member-1')
  assert.equal(saved.problemSlug, pack.slug)
  assert.equal(saved.status, 'passed')
  assert.equal(response.body.submissionId, 'submission-1')
})

test('latest submission query is scoped to the session user', async () => {
  let filter
  const chain = { select() { return this }, sort() { return this }, async lean() { return { code: 'saved', status: 'passed' } } }
  const route = load('app/api/learn/submissions/route.ts', {
    'next/server': nextServer, 'next-auth': { getServerSession: async () => ({ user: { id: 'member-1' } }) }, '@/lib/auth': { authOptions: {} },
    '@/lib/mongodb': async () => {}, '@/models/LearnSubmission': { findOne: value => { filter = value; return chain } },
    '@/lib/learn/data': { problemBySlug: slug => slug === pack.slug ? pack : undefined },
  })
  const response = await route.GET({ nextUrl: new URL('http://localhost/api/learn/submissions?slug=' + pack.slug) })
  assert.equal(response.status, 200)
  assert.equal(filter.user, 'member-1')
  assert.equal(filter.problemSlug, pack.slug)
})

test('progress counts distinct passed problems for the authenticated owner', async () => {
  const chain = { select() { return this }, sort() { return this }, async lean() { return { problemSlug: pack.slug } } }
  const filters = []
  const progress = load('lib/learn/progress.ts', {
    'server-only': {}, '@/lib/mongodb': async () => {},
    '@/models/LearnSubmission': {
      distinct: async (field, filter) => { filters.push(filter); return [pack.slug, pack.slug] },
      findOne: filter => { filters.push(filter); return chain },
      countDocuments: async filter => { filters.push(filter); return 3 },
    },
    '@/lib/learn/data': { topics: [{ slug: 'python', problemCount: 1 }], problems: [{ slug: pack.slug, topicSlug: 'python', id: pack.id, title: pack.title }], requiredProblems: [{ slug: pack.slug, topicSlug: 'python', id: pack.id, title: pack.title }] },
  })
  const data = await progress.getLearnProgress('member-1')
  assert.equal(data.completed, 1)
  assert.equal(data.topicsComplete, 1)
  assert.equal(data.attempts, 3)
  assert.ok(filters.every(filter => filter.user === 'member-1'))
})

test('executor client requires HTTPS and strips private grader output', async () => {
  const old = process.env.LEARN_EXECUTOR_URL
  const oldToken = process.env.LEARN_EXECUTOR_TOKEN
  try {
    process.env.LEARN_EXECUTOR_URL = 'http://executor.example.com'
    process.env.LEARN_EXECUTOR_TOKEN = 'secret'
    let calls = 0
    const executor = load('lib/learn/executor.ts', {
      'server-only': {}, '@/lib/learn/pack': { packBySlug: () => pack },
    }, { process, fetch: async () => { calls++; return { ok: true } }, URL, AbortSignal, Buffer })
    assert.equal(await executor.executeOnVps('submit', pack.slug, pack.solution, 'member-1'), null)
    assert.equal(calls, 0)
    process.env.LEARN_EXECUTOR_URL = 'https://executor.example.com'
    const sent = []
    const graded = load('lib/learn/executor.ts', {
      'server-only': {}, '@/lib/learn/pack': { packBySlug: () => pack },
    }, { process, fetch: async (url, options) => { sent.push(JSON.parse(options.body)); return { ok: true, status: 200, json: async () => ({ passed: pack.testCount, total: pack.testCount, status: 'passed', output: privateTests, tests: [] }) } }, URL, AbortSignal, Buffer })
    const result = await graded.executeOnVps('submit', pack.slug, pack.solution, 'member-1')
    assert.equal(result.status, 'passed')
    assert.equal(result.output, undefined)
    assert.equal(result.tests, undefined)
    assert.match(sent[0].client, /^[a-f0-9]{64}$/)
    const withFailures = load('lib/learn/executor.ts', {
      'server-only': {}, '@/lib/learn/pack': { packBySlug: () => pack },
    }, { process, fetch: async () => ({ ok: true, status: 200, json: async () => ({ passed: pack.testCount - 1, total: pack.testCount, status: 'failed', failed: ['test_hidden_case'] }) }), URL, AbortSignal, Buffer })
    assert.deepEqual([...(await withFailures.executeOnVps('submit', pack.slug, pack.solution, 'member-1')).failedTests], ['test_hidden_case'])
    const inconsistent = load('lib/learn/executor.ts', {
      'server-only': {}, '@/lib/learn/pack': { packBySlug: () => pack },
    }, { process, fetch: async () => ({ ok: true, status: 200, json: async () => ({ passed: pack.testCount - 1, total: pack.testCount, status: 'failed', failed: ['test_a', 'test_b'] }) }), URL, AbortSignal, Buffer })
    assert.equal((await inconsistent.executeOnVps('submit', pack.slug, pack.solution, 'member-1')).failedTests, undefined)
    assert.ok(!JSON.stringify(sent[0]).includes('member-1'))
    const limited = load('lib/learn/executor.ts', {
      'server-only': {}, '@/lib/learn/pack': { packBySlug: () => pack },
    }, { process, fetch: async () => ({ ok: false, status: 429, json: async () => ({ error: 'Too many requests', retryAfter: 7 }) }), URL, AbortSignal, Buffer })
    assert.deepEqual({ ...(await limited.executeOnVps('run', pack.slug, pack.solution, 'member-1')) }, { rateLimited: true, retryAfter: 7, inFlight: false })
  } finally {
    if (old === undefined) delete process.env.LEARN_EXECUTOR_URL; else process.env.LEARN_EXECUTOR_URL = old
    if (oldToken === undefined) delete process.env.LEARN_EXECUTOR_TOKEN; else process.env.LEARN_EXECUTOR_TOKEN = oldToken
  }
})

test('optional deep dives and project ideas stay out of completion counts', async () => {
  const problem = (slug, optional = false) => ({ slug, topicSlug: 'ml', id: slug, title: slug, tags: [], optional })
  const catalogue = {
    topics: [{ slug: 'ml', problemCount: 2, optionalCount: 1, projectCount: 1 }],
    problems: [problem('library-step'), problem('scratch-step', true), problem('capstone')],
    projects: [{ slug: 'house-prices', id: 'ML-P1', title: 'House prices', topicSlug: 'ml', after: 'scratch-step', tags: [] }],
  }
  const data = load('lib/learn/data.ts', { '@/lib/learn/catalogue.generated.json': catalogue })
  assert.deepEqual(data.topicPath('ml').map(entry => entry.item.slug), ['library-step', 'scratch-step', 'house-prices', 'capstone'])
  assert.deepEqual(data.requiredProblems.map(item => item.slug), ['library-step', 'capstone'])
  assert.equal(data.pathHref(data.topicPath('ml')[2]), '/learn/projects/house-prices')
  const chain = { select() { return this }, sort() { return this }, async lean() { return null } }
  const progress = load('lib/learn/progress.ts', {
    'server-only': {}, '@/lib/mongodb': async () => {}, '@/lib/learn/data': data,
    '@/models/LearnSubmission': { distinct: async () => ['scratch-step', 'library-step'], findOne: () => chain, countDocuments: async () => 2 },
  })
  const result = await progress.getLearnProgress('member-1')
  assert.deepEqual([result.completed, result.total, result.byTopic.ml, result.topicsComplete], [1, 2, 1, 0])
  assert.ok(result.completedSlugs.includes('scratch-step'))
  assert.equal(result.continueProblem.slug, 'capstone')
})

test('local harness rebuilds setUp and helper methods of the visible tests\' classes', () => {
  const packs = JSON.parse(fs.readFileSync(path.join(root, 'lib/learn/packs.generated.json')))
  const local = JSON.parse(fs.readFileSync(path.join(root, 'lib/learn/local-compat.generated.json')))
  const worker = fs.readFileSync(path.join(root, 'public/learn/pyodide-worker.mjs'), 'utf8')
  const context = { self: {} }
  vm.runInNewContext(worker + '\nglobalThis.python = runVisibleTests', context)
  for (const slug of ['probability-basics', 'inverse-2x2']) {
    const target = packs[slug]
    assert.equal(local[slug], true)
    assert.ok(target.localClasses.some(source => /def (setUp|assert\w+)\(/.test(source)))
    const run = code => {
      const payload = JSON.stringify({ code, packages: [], tests: target.visibleTests, prelude: target.localPrelude, classes: target.localClasses, kind: target.kind })
      const python = spawnSync('python3', ['-B', '-c', 'import os\npayload_json=os.environ["LEARN_PAYLOAD"]\n' + context.python + '\nprint(json.dumps(response))'], { encoding: 'utf8', env: { ...process.env, LEARN_PAYLOAD: payload }, timeout: 20000 })
      assert.equal(python.status, 0, python.stderr)
      return JSON.parse(python.stdout)
    }
    assert.deepEqual([run(target.solution).passed, run(target.starter).passed < 3], [3, true])
  }
})

function learnersModule(rows, users) {
  return load('lib/learn/learners.ts', {
    'server-only': {}, '@/lib/mongodb': async () => {},
    '@/lib/learn/data': { problems: [{ slug: 'a' }, { slug: 'b' }, { slug: 'c' }] },
    '@/models/LearnSubmission': { aggregate: async pipeline => { learnersModule.pipeline = pipeline; return rows } },
    '@/models/User': { find: () => ({ select() { return this }, async lean() { return users } }) },
  })
}

test('admin learners: batch digits come from institute emails', () => {
  const { emailBatch } = learnersModule([], [])
  assert.equal(emailBatch('lokesh.k23@iiits.in'), '23')
  assert.equal(emailBatch('Asha.R21@IIITS.IN'), '21')
  assert.equal(emailBatch('someone@gmail.com'), null)
  assert.equal(emailBatch('name.k2@iiits.in'), null)
  assert.equal(emailBatch('name.k234@iiits.in'), null)
})

test('admin learners: counts distinct passed problems and filters by batch', async () => {
  const id = value => ({ toString: () => value })
  const rows = [
    { _id: 'u1', slugs: ['a', 'b'], lastSolvedAt: new Date('2026-10-20') },
    { _id: 'u2', slugs: ['a', 'b', 'c'], lastSolvedAt: new Date('2026-10-21') },
    { _id: 'u3', slugs: ['c'], lastSolvedAt: new Date('2026-10-22') },
    { _id: 'gone', slugs: ['a'], lastSolvedAt: new Date('2026-10-22') },
  ]
  const users = [
    { _id: id('u1'), name: 'Asha', email: 'asha.r23@iiits.in', image: 'https://example.com/a.png' },
    { _id: id('u2'), name: 'Bala', email: 'bala.k23@iiits.in' },
    { _id: id('u3'), name: 'Chen', email: 'chen@gmail.com' },
  ]
  const mod = learnersModule(rows, users)
  const all = await mod.getLearners()
  assert.deepEqual(JSON.parse(JSON.stringify(all.learners.map(l => [l.name, l.completed, l.batch]))), [['Bala', 3, '23'], ['Asha', 2, '23'], ['Chen', 1, null]])
  assert.deepEqual([...all.batches], ['23'])
  assert.equal(all.total, 3)
  assert.equal(all.learners[1].image, 'https://example.com/a.png')
  const match = learnersModule.pipeline[0].$match
  assert.equal(match.status, 'passed')
  assert.deepEqual([...match.problemSlug.$in], ['a', 'b', 'c'])
  const batch = await mod.getLearners('23')
  assert.deepEqual([...batch.learners.map(l => l.name)], ['Bala', 'Asha'])
  assert.equal(batch.total, 3)
})

test('admin learners API is admin-only and validates the batch', async () => {
  let calls = 0
  const route = session => load('app/api/admin/learners/route.ts', {
    'next/server': nextServer, 'next-auth': { getServerSession: async () => session }, '@/lib/auth': { authOptions: {} },
    '@/lib/learn/learners': { getLearners: async batch => { calls++; return { learners: [], batches: [], total: 0, batch } } },
  })
  const request = url => ({ nextUrl: new URL(url) })
  assert.equal((await route(null).GET(request('http://x/api/admin/learners'))).status, 401)
  assert.equal((await route({ user: { role: 'user' } }).GET(request('http://x/api/admin/learners'))).status, 401)
  assert.equal(calls, 0)
  assert.equal((await route({ user: { role: 'admin' } }).GET(request('http://x/api/admin/learners?batch=2x'))).status, 400)
  const ok = await route({ user: { role: 'admin' } }).GET(request('http://x/api/admin/learners?batch=23'))
  assert.equal(ok.status, 200)
  assert.equal(ok.body.batch, '23')
})
