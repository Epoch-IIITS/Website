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
    process,
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
      headers: { set() {} },
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
  const runTransaction = transaction || (async (fn) => fn({}));
  return load("app/api/admin/team/route.ts", {
    "next/server": next,
    "next-auth": {
      getServerSession: async () => (role ? { user: { id, role } } : null),
    },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/Team": { ...models, ensureTeamStorage: async () => {} },
    "@/lib/team-validation": schemas,
    "@/lib/audit-log": {
      diffAuditFields: () => [],
      runAuditedMutation: async (_session, _request, mutation) =>
        runTransaction(async (databaseSession) =>
          (await mutation(databaseSession)).value),
    },
    "@/lib/media-assets": {
      ensureMediaStorage: async () => {},
      reconcileMediaUrls: async () => [],
      attemptMediaCleanup: async () => {},
    },
    mongoose: {
      connection: { transaction: runTransaction },
    },
  });
}
const req = (value) => ({ json: async () => value });

test("team validation rejects unsafe URLs, invalid years, duplicate group identifiers, and missing consent", () => {
  assert.equal(
    schemas.personSchema.safeParse({ ...profile, email: "not-an-email" }).success,
    false,
  );
  assert.equal(
    schemas.personSchema.parse({ ...profile, email: " ADA@Example.COM " }).email,
    "ada@example.com",
  );
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

test("admins can privately link an existing person profile by account email", async () => {
  let savedUpdate;
  const before = { _id: personId, ...profile, email: "", userId: "old-user" };
  const route = adminRoute({
    TeamPerson: {
      findById: () => query(before),
      findByIdAndUpdate: async (_id, update) => {
        savedUpdate = update;
        return { ...before, ...update.$set };
      },
    },
  });
  const response = await route.POST(
    req({
      action: "person",
      id: personId,
      value: { ...profile, email: " Member@Example.com " },
    }),
  );
  assert.equal(response.status, 200);
  assert.equal(savedUpdate.$set.email, "member@example.com");
  assert.equal(savedUpdate.$unset.userId, 1);
});

test("request approval is transactional, preserves an existing profile, and cannot repeat", async () => {
  let savedAppointment,
    linkedFilter,
    linkedUpdate,
    reviews = 0,
    txCount = 0;
  const record = {
    _id: id,
    userId: id,
    email: "real@example.com",
    status: "pending",
    name: "Ada Lovelace",
    toObject() { return { status: this.status, name: this.name }; },
    save: async () => {
      reviews++;
    },
  };
  const route = adminRoute(
    {
      TeamRequest: {
        findOne: () => query(record.status === "pending" ? record : null),
      },
      TeamPerson: {
        exists: () => query(true),
        findOne: () => query(null),
        findOneAndUpdate: async (filter, update) => {
          linkedFilter = filter;
          linkedUpdate = update;
          return { _id: personId, name: "Ada Lovelace", userId: id };
        },
        findById: () => query({ name: "Ada Lovelace" }),
      },
      TeamYear: { findById: () => query({ year: 2026, groups: [{ id: "domain" }] }) },
      TeamAppointment: {
        findOne: () => query(null),
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
  assert.equal(linkedFilter._id, personId);
  assert.equal(linkedFilter.$or[0].userId, id);
  assert.equal(linkedFilter.$or[1].email, "real@example.com");
  assert.equal(linkedUpdate.$set.email, "real@example.com");
  assert.equal(record.status, "approved");
  assert.equal((await route.POST(req(body))).status, 400);
  assert.equal(reviews, 1);
  assert.equal(txCount, 2);
});

test("rejection requires feedback and never creates a public appointment", async () => {
  const record = {
    _id: id,
    status: "pending",
    name: "Ada Lovelace",
    toObject() { return { status: this.status, name: this.name }; },
    save: async () => {},
  };
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
    "@/lib/media-assets": {
      ensureMediaStorage: async () => {},
      attachMediaUrls: async () => {},
    },
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

function memberProfileRoute({
  models = {},
  session = { user: { id, email: "real@example.com" } },
  transaction = async (fn) => fn({}),
  media = {},
  audit = {},
} = {}) {
  return load("app/api/team/profile/route.ts", {
    "next/server": next,
    "next-auth": { getServerSession: async () => session },
    "@/lib/auth": { authOptions: {} },
    "@/lib/mongodb": async () => {},
    "@/models/Team": { ...models, ensureTeamStorage: async () => {} },
    "@/lib/team-validation": schemas,
    "@/lib/audit-log": {
      diffAuditFields: (before, after, fields) =>
        fields.flatMap((field) =>
          before?.[field] === after?.[field]
            ? []
            : [{ field, before: before?.[field] || null, after: after?.[field] || null }],
        ),
      runAuditedMutation: async (actor, request, mutation) =>
        transaction(async (databaseSession) => {
          const result = await mutation(databaseSession);
          audit.capture?.({ actor, request, logs: result.logs });
          return result.value;
        }),
    },
    "@/lib/media-assets": {
      ensureMediaStorage: async () => {},
      reconcileMediaUrls: async () => [],
      attemptMediaCleanup: async () => {},
      ...media,
    },
    mongoose: { connection: { transaction } },
  });
}

test("team profile endpoint is private and hidden from signed-in nonmembers", async () => {
  let storageTouched = false;
  const anonymous = memberProfileRoute({
    session: null,
    transaction: async () => {
      storageTouched = true;
    },
  });
  assert.equal((await anonymous.GET()).status, 401);
  assert.equal((await anonymous.PUT(req(profile))).status, 401);
  assert.equal(storageTouched, false);

  const nonmember = memberProfileRoute({
    models: {
      TeamPerson: { findOne: () => query(null) },
      TeamRequest: { findOne: () => query(null) },
    },
  });
  const read = await nonmember.GET();
  assert.equal(read.status, 200);
  assert.equal(read.body.member, false);
  assert.equal((await nonmember.PUT(req(profile))).status, 403);
});

test("a linked team member can update only their shared profile fields", async () => {
  const oldPhoto =
    "https://res.cloudinary.com/demo/image/upload/v1/epoch/team/old.jpg";
  const newPhoto =
    "https://res.cloudinary.com/demo/image/upload/v1/epoch/team/new.jpg";
  const person = {
    _id: personId,
    userId: "previous-account-id",
    email: "real@example.com",
    ...profile,
    photo: oldPhoto,
  };
  let updateFilter,
    updateValue,
    reconciled,
    cleaned,
    auditRecord;
  const route = memberProfileRoute({
    models: {
      TeamPerson: {
        findOne: (filter) => {
          assert.equal(filter.email, "real@example.com");
          return query(person);
        },
        findOneAndUpdate: async (filter, update) => {
          updateFilter = filter;
          updateValue = update;
          return { ...person, ...update.$set };
        },
      },
      TeamAppointment: { exists: () => query(true) },
      TeamRequest: { findOne: () => { throw new Error("legacy lookup not expected"); } },
    },
    media: {
      reconcileMediaUrls: async (value) => {
        reconciled = value;
        return ["epoch/team/old"];
      },
      attemptMediaCleanup: async (value) => {
        cleaned = value;
      },
    },
    audit: {
      capture: (value) => {
        auditRecord = value;
      },
    },
  });

  const read = await route.GET();
  assert.equal(read.body.member, true);
  assert.equal(read.body.profile.name, profile.name);

  const changed = {
    ...profile,
    name: "Ada Byron",
    currentRole: "Principal Researcher",
    photo: newPhoto,
    email: "forged@example.com",
    userId: "forged-user",
    personId: "forged-person",
    por: "Forged position",
    published: false,
  };
  const response = await route.PUT(req(changed));
  assert.equal(response.status, 200);
  assert.equal(response.body.profile.name, "Ada Byron");
  assert.equal(updateFilter._id, personId);
  assert.equal(updateFilter.userId, undefined);
  assert.equal(updateValue.$set.currentRole, "Principal Researcher");
  assert.equal(updateValue.$set.userId, id);
  assert.equal(updateValue.$set.email, "real@example.com");
  assert.equal(updateValue.$set.personId, undefined);
  assert.equal(updateValue.$set.por, undefined);
  assert.equal(updateValue.$set.published, undefined);
  assert.equal(auditRecord.actor.user.id, id);
  assert.equal(auditRecord.logs.length, 1);
  assert.equal(auditRecord.logs[0].entityType, "team-person");
  assert.match(auditRecord.logs[0].summary, /Updated own team profile/);
  assert.ok(auditRecord.logs[0].changes.some((change) => change.field === "name"));
  assert.ok(!auditRecord.logs[0].changes.some((change) => change.field === "email"));
  assert.equal(reconciled.beforeUrls[0], oldPhoto);
  assert.equal(reconciled.afterUrls[0], newPhoto);
  assert.equal(cleaned.length, 1);
  assert.equal(cleaned[0], "epoch/team/old");
});

test("an older approved request is resolved without exposing or claiming another account", async () => {
  const legacyPerson = { _id: personId, ...profile };
  const calls = [];
  let requestFilter;
  const route = memberProfileRoute({
    models: {
      TeamPerson: {
        findOne: () => query(null),
        findById: () => query(legacyPerson),
        findOneAndUpdate: async (filter, update) => {
          calls.push({ filter, update });
          return { ...legacyPerson, userId: id, ...update.$set };
        },
      },
      TeamRequest: {
        findOne: (filter) => {
          requestFilter = filter;
          return query({ appointmentId: id });
        },
      },
      TeamAppointment: { findById: () => query({ personId }) },
    },
  });

  const read = await route.GET();
  assert.equal(read.body.member, true);
  assert.equal(calls.length, 0);
  assert.equal(requestFilter.$or[1].email, "real@example.com");

  const response = await route.PUT(req({ ...profile, tagline: "Updated" }));
  assert.equal(response.status, 200);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].filter._id, personId);
  assert.equal(calls[0].update.$set.userId, id);
  assert.equal(calls[0].update.$set.email, "real@example.com");

  let crossAccountMutation = false;
  const alreadyClaimed = memberProfileRoute({
    models: {
      TeamPerson: {
        findOne: () => query(null),
        findById: () =>
          query({
            ...legacyPerson,
            userId: "another-user",
            email: "another@example.com",
          }),
        findOneAndUpdate: () => {
          crossAccountMutation = true;
        },
      },
      TeamRequest: { findOne: () => query({ appointmentId: id }) },
      TeamAppointment: { findById: () => query({ personId }) },
    },
  });
  assert.equal((await alreadyClaimed.GET()).body.member, false);
  assert.equal((await alreadyClaimed.PUT(req(profile))).status, 403);
  assert.equal(crossAccountMutation, false);
});

test("public member lookup hides draft appointments and draft years", async () => {
  let returnedAppointment = null,
    returnedYear = null,
    returnedAppointments = [],
    returnedYears = [];
  const data = load("lib/team-data.ts", {
    "@/lib/mongodb": async () => {},
    "@/lib/team-validation": schemas,
    "@/models/Team": {
      TeamAppointment: {
        findOne: (filter) => {
          assert.equal(filter.published, true);
          return query(returnedAppointment);
        },
        find: (filter) => {
          assert.equal(filter.published, true);
          assert.equal(filter.personId, personId);
          return query(returnedAppointments);
        },
      },
      TeamYear: {
        findOne: (filter) => {
          assert.equal(filter.published, true);
          return query(returnedYear);
        },
        find: (filter) => {
          assert.equal(filter.published, true);
          return query(returnedYears);
        },
      },
      TeamPerson: { findById: () => query(profile) },
    },
  });
  assert.equal(await data.publicMember("invalid"), null);
  assert.equal(await data.publicMember(id), null);
  returnedAppointment = appointment;
  assert.equal(await data.publicMember(id), null);
  const previousYearId = "123456789012345678901237";
  returnedYear = {
    _id: yearId,
    year: 2026,
    groups: [{ id: "domain", name: "Domain Leads" }],
  };
  returnedAppointments = [
    appointment,
    {
      ...appointment,
      yearId: previousYearId,
      groupId: "core",
      por: "Core Member",
    },
  ];
  returnedYears = [
    returnedYear,
    {
      _id: previousYearId,
      year: 2025,
      groups: [{ id: "core", name: "Core Committee" }],
    },
  ];
  const member = await data.publicMember(id);
  assert.equal(member.person.name, profile.name);
  assert.equal(member.positions.length, 2);
  assert.equal(member.positions[0].por, "NLP Lead");
  assert.equal(member.positions[0].group, "Domain Leads");
  assert.equal(member.positions[0].year, 2026);
  assert.equal(member.positions[1].por, "Core Member");
  assert.equal(member.positions[1].year, 2025);
});

test("real Mongoose indexes prevent duplicate person/year appointments and pending requests", () => {
  const models = load("models/Team.ts");
  assert.ok(
    models.TeamPerson.schema
      .indexes()
      .some(
        ([fields, options]) =>
          fields.userId && options.unique && options.sparse,
      ),
  );
  assert.ok(
    models.TeamPerson.schema
      .indexes()
      .some(
        ([fields, options]) =>
          fields.email && options.unique && options.sparse,
      ),
  );
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
  member = {
    ...appointment,
    _id: id,
    person: profile,
    year: { year: 2026 },
    positions: [
      { por: "NLP Lead", group: "Domain Leads", year: 2026 },
      { por: "Core Member", group: "Core Committee", year: 2025 },
    ],
  };
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
