const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const ts = require("typescript");

function load(file, mocks = {}) {
  const source = fs.readFileSync(path.join(__dirname, "..", file), "utf8");
  const { outputText } = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.ReactJSX,
      esModuleInterop: true,
    },
  });
  const context = {
    exports: {},
    Buffer,
    Response,
    URL,
    AbortSignal,
    fetch,
    Error,
    Date,
    require: (name) => (name in mocks ? mocks[name] : require(name)),
  };
  vm.runInNewContext(outputText, context, { filename: file });
  return context.exports;
}
const schemas = load("lib/team-validation.ts");
const next = {
  NextResponse: {
    json: (body, options = {}) => ({
      body: JSON.parse(JSON.stringify(body)),
      status: options.status || 200,
    }),
  },
};
const id = "123456789012345678901234";
const personId = "123456789012345678901235";
const yearId = "123456789012345678901236";
const profile = {
  name: "Ada Lovelace",
  linkedin: "https://www.linkedin.com/in/ada",
  currentRole: "Researcher",
  organization: "Institute",
  photo: "",
  tagline: "Building with curiosity.",
};
const appointment = {
  personId,
  yearId,
  groupId: "domain",
  por: "NLP Lead",
  order: 0,
  published: true,
};
const query = (value) => ({
  session() {
    return this;
  },
  lean: async () => value,
  sort() {
    return this;
  },
  select() {
    return this;
  },
  then(resolve, reject) {
    return Promise.resolve(value).then(resolve, reject);
  },
});
function adminRoute(models = {}, role = "admin", transaction) {
  return load("app/api/admin/team/route.ts", {
    "next/server": next,
    "next-auth": {
      getServerSession: async () => (role ? { user: { id, role } } : null),
    },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/Team": { ...models, ensureTeamStorage: async () => {} },
    "@/lib/team-validation": schemas,
    mongoose: {
      connection: { transaction: transaction || (async (fn) => fn({})) },
    },
  });
}
const req = (value) => ({ json: async () => value });

test("team validation rejects unsafe URLs, invalid years, duplicate group identifiers, and missing consent", () => {
  assert.equal(
    schemas.profileSchema.safeParse({
      ...profile,
      linkedin: "javascript:alert(1)",
    }).success,
    false,
  );
  assert.equal(
    schemas.profileSchema.safeParse({
      ...profile,
      photo: "http://localhost/private",
    }).success,
    false,
  );
  assert.equal(
    schemas.yearSchema.safeParse({
      year: 2026,
      published: false,
      groups: [
        { id: "x", name: "A" },
        { id: "x", name: "B" },
      ],
    }).success,
    false,
  );
  assert.equal(
    schemas.yearSchema.safeParse({
      year: 1,
      published: false,
      groups: [{ id: "x", name: "A" }],
    }).success,
    false,
  );
  assert.equal(
    schemas.requestSchema.safeParse({
      ...profile,
      year: 2026,
      group: "",
      por: "Lead",
      notes: "",
      consent: false,
    }).success,
    false,
  );
});

test("appointments and requests accept empty or omitted POR through validation and persistence", async () => {
  const models = load("models/Team.ts");
  for (const por of ["", "   ", undefined]) {
    const parsed = schemas.appointmentSchema.parse({ ...appointment, por });
    assert.equal(parsed.por, "");
    await new models.TeamAppointment(parsed).validate();
    let saved;
    const response = await requestRoute({ create: async value => { saved = value; } }).POST(req({ ...profile, year: 2026, group: "Learners", por, notes: "", consent: true }));
    assert.equal(response.status, 201);
    assert.equal(saved.por, "");
    await new models.TeamRequest(saved).validate();
  }
});

test("all admin reads and writes deny anonymous and ordinary members", async () => {
  for (const role of [null, "user"]) {
    const route = adminRoute({}, role, () => {
      throw new Error("must not access storage");
    });
    assert.equal((await route.GET()).status, 403);
    assert.equal(
      (
        await route.POST(
          req({ action: "settings", value: schemas.defaultSettings }),
        )
      ).status,
      403,
    );
  }
});

test("a populated hierarchy group cannot be removed and the current year cannot be unpublished", async () => {
  const route = adminRoute({
    TeamSettings: { findById: () => query({ currentYearId: yearId }) },
    TeamAppointment: { exists: () => query(true) },
  });
  const value = {
    year: 2026,
    published: false,
    groups: [{ id: "other", name: "Other" }],
  };
  assert.match(
    (await route.POST(req({ action: "year", id: yearId, value }))).body.error,
    /current year/,
  );
  assert.match(
    (
      await route.POST(
        req({
          action: "year",
          id: yearId,
          value: { ...value, published: true },
        }),
      )
    ).body.error,
    /Move members/,
  );
});

test("current team selection rejects draft or nonexistent years", async () => {
  const route = adminRoute({ TeamYear: { findOne: () => query(null) } });
  assert.match(
    (await route.POST(req({ action: "current", id: yearId }))).body.error,
    /Publish the year/,
  );
});

test("appointment must reference an existing person and a group belonging to its year", async () => {
  const route = adminRoute({
    TeamYear: { findById: () => query({ groups: [{ id: "other" }] }) },
  });
  assert.match(
    (await route.POST(req({ action: "appointment", value: appointment }))).body
      .error,
    /Select a group/,
  );
});

test("request approval is transactional, preserves an existing profile, and cannot repeat", async () => {
  let savedAppointment,
    reviews = 0,
    txCount = 0;
  const record = {
    status: "pending",
    save: async () => {
      reviews++;
    },
  };
  const route = adminRoute(
    {
      TeamRequest: {
        findOne: () => query(record.status === "pending" ? record : null),
      },
      TeamPerson: { exists: () => query(true) },
      TeamYear: { findById: () => query({ groups: [{ id: "domain" }] }) },
      TeamAppointment: {
        findOneAndUpdate: async (filter, update) => {
          savedAppointment = { filter, update };
          return { _id: id };
        },
      },
    },
    "admin",
    async (fn) => {
      txCount++;
      await fn({});
    },
  );
  const body = {
    action: "review",
    id,
    decision: "approve",
    personId,
    profile,
    appointment,
  };
  assert.equal((await route.POST(req(body))).status, 200);
  assert.equal(savedAppointment.filter.personId, personId);
  assert.equal(savedAppointment.filter.yearId, yearId);
  assert.equal(record.status, "approved");
  assert.equal((await route.POST(req(body))).status, 400);
  assert.equal(reviews, 1);
  assert.equal(txCount, 2);
});

test("rejection requires feedback and never creates a public appointment", async () => {
  const record = { status: "pending", save: async () => {} };
  const route = adminRoute({ TeamRequest: { findOne: () => query(record) } });
  assert.equal(
    (
      await route.POST(
        req({ action: "review", id, decision: "reject", reason: "" }),
      )
    ).status,
    400,
  );
  assert.equal(
    (
      await route.POST(
        req({
          action: "review",
          id,
          decision: "reject",
          reason: "Please verify your academic year.",
        }),
      )
    ).status,
    200,
  );
  assert.equal(record.status, "rejected");
  assert.equal(record.reason, "Please verify your academic year.");
});

function requestRoute(
  model,
  session = { user: { id, email: "real@example.com" } },
) {
  return load("app/api/team/requests/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => session },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/Team": { TeamRequest: model, ensureTeamStorage: async () => {} },
    "@/lib/team-validation": schemas,
  });
}
test("applicant identity is server-owned and submitted status cannot self-approve", async () => {
  let saved;
  const route = requestRoute({
    create: async (value) => {
      saved = value;
    },
  });
  const response = await route.POST(
    req({
      ...profile,
      year: 2026,
      group: "",
      por: "Lead",
      notes: "",
      consent: true,
      userId: "forged",
      email: "forged@example.com",
      status: "approved",
    }),
  );
  assert.equal(response.status, 201);
  assert.equal(saved.userId, id);
  assert.equal(saved.email, "real@example.com");
  assert.equal(saved.status, undefined);
});
test("anonymous requests fail and duplicate pending requests report a conflict", async () => {
  assert.equal((await requestRoute({}, null).POST(req({}))).status, 401);
  const route = requestRoute({
    create: async () => {
      throw Object.assign(new Error(), { code: 11000 });
    },
  });
  assert.match(
    (
      await route.POST(
        req({
          ...profile,
          year: 2026,
          group: "",
          por: "Lead",
          notes: "",
          consent: true,
        }),
      )
    ).body.error,
    /already have a pending/,
  );
});
test("request history is scoped to the authenticated applicant", async () => {
  let filter;
  const route = requestRoute({
    find: (value) => {
      filter = value;
      return query([]);
    },
  });
  assert.equal((await route.GET()).status, 200);
  assert.equal(filter.userId, id);
});

test("public member lookup hides draft appointments and draft years", async () => {
  let returnedAppointment = null,
    returnedYear = null;
  const data = load("lib/team-data.ts", {
    "@/lib/mongodb": async () => {},
    "@/lib/team-validation": schemas,
    "@/models/Team": {
      TeamAppointment: {
        findOne: (filter) => {
          assert.equal(filter.published, true);
          return query(returnedAppointment);
        },
      },
      TeamYear: {
        findOne: (filter) => {
          assert.equal(filter.published, true);
          return query(returnedYear);
        },
      },
      TeamPerson: { findById: () => query(profile) },
    },
  });
  assert.equal(await data.publicMember("invalid"), null);
  assert.equal(await data.publicMember(id), null);
  returnedAppointment = appointment;
  assert.equal(await data.publicMember(id), null);
  returnedYear = { year: 2026 };
  assert.equal((await data.publicMember(id)).person.name, profile.name);
});

test("real Mongoose indexes prevent duplicate person/year appointments and pending requests", () => {
  const models = load("models/Team.ts");
  assert.ok(
    models.TeamAppointment.schema
      .indexes()
      .some(
        ([fields, options]) =>
          fields.personId && fields.yearId && options.unique,
      ),
  );
  assert.ok(
    models.TeamRequest.schema
      .indexes()
      .some(
        ([fields, options]) =>
          fields.userId &&
          fields.year &&
          options.unique &&
          options.partialFilterExpression.status === "pending",
      ),
  );
});

test("share card route renders a real 1200px PNG and unpublished cards return 404", async () => {
  let member = null;
  const route = load("app/team/member/[id]/image/route.tsx", {
    "@/lib/team-data": { publicMember: async () => member },
  });
  const context = { params: Promise.resolve({ id }) };
  const request = {
    nextUrl: new URL(
      "http://localhost/team/member/" + id + "/image?download=1",
    ),
  };
  assert.equal((await route.GET(request, context)).status, 404);
  member = { ...appointment, _id: id, person: profile, year: { year: 2026 } };
  const response = await route.GET(request, context);
  assert.equal(response.headers.get("Content-Type"), "image/png");
  assert.match(response.headers.get("Content-Disposition"), /attachment/);
  const bytes = Buffer.from(await response.arrayBuffer());
  assert.equal(bytes.subarray(1, 4).toString(), "PNG");
  assert.equal(bytes.readUInt32BE(16), 1200);
  assert.equal(bytes.readUInt32BE(20), 1200);
  if (process.env.TEAM_CARD_PREVIEW)
    fs.writeFileSync(process.env.TEAM_CARD_PREVIEW, bytes);
  member.por = "";
  const withoutPor = await route.GET(request, context);
  const blankPorBytes = Buffer.from(await withoutPor.arrayBuffer());
  assert.equal(blankPorBytes.subarray(1, 4).toString(), "PNG");
});
