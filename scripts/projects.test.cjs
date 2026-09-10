const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const ts = require('typescript')
const mongoose = require('mongoose')

function load(file, mocks = {}) {
  const source = fs.readFileSync(path.join(__dirname, '..', file), 'utf8')
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true },
  })
  const context = { exports: {}, Error, require: name => name in mocks ? mocks[name] : require(name) }
  vm.runInNewContext(outputText, context, { filename: file })
  return context.exports
}
// Use the real Mongoose schema/query machinery, stubbing only database I/O.
// This catches strictPopulate failures for relationships absent from the schema.
const Project = load('models/Project.ts').default
const schemas = load('lib/validations.ts')
const id = new mongoose.Types.ObjectId()
const existing = { _id: id, title: 'Club website', description: 'Community project', techStack: ['Next.js'], featured: false }
const context = { params: Promise.resolve({ id: id.toString() }) }

function route(session = null) {
  return load('app/api/projects/[id]/route.ts', {
    'next/server': { NextResponse: { json: (body, options = {}) => ({ body: JSON.parse(JSON.stringify(body)), status: options.status || 200 }) } },
    '@/lib/mongodb': async () => {},
    '@/models/Project': Project,
    '@/lib/validations': schemas,
    'next-auth': { getServerSession: async () => session },
    '@/lib/auth': { authOptions: {} },
  })
}

test('an existing project loads through its real schema without nonexistent author population', async () => {
  Project.collection.findOne = async () => existing
  const response = await route().GET({}, context)
  assert.equal(response.status, 200)
  assert.equal(response.body._id, id.toString())
  assert.equal(response.body.title, existing.title)
})

test('a genuinely missing project returns 404', async () => {
  Project.collection.findOne = async () => null
  const response = await route().GET({}, context)
  assert.equal(response.status, 404)
  assert.equal(response.body.error, 'Project not found')
})

test('a database failure returns 500 rather than a missing-project response', async () => {
  Project.collection.findOne = async () => { throw new Error('Database unavailable') }
  assert.equal((await route().GET({}, context)).status, 500)
})

test('an admin can save a project without a nonexistent createdBy relationship', async () => {
  let saved
  Project.collection.findOneAndUpdate = async (filter, update) => {
    saved = update.$set
    return { ...existing, ...saved }
  }
  const response = await route({ user: { role: 'admin', email: 'admin@example.com' } }).PUT({ json: async () => ({ ...existing, title: 'Updated website' }) }, context)
  assert.equal(response.status, 200)
  assert.equal(response.body.title, 'Updated website')
  assert.equal(saved.createdBy, undefined)
})

test('non-admin users cannot update projects', async () => {
  let writes = 0
  Project.collection.findOneAndUpdate = async () => { writes++; return existing }
  for (const session of [null, { user: { role: 'user' } }]) {
    assert.equal((await route(session).PUT({ json: async () => existing }, context)).status, 401)
  }
  assert.equal(writes, 0)
})
