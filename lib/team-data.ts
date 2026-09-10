import connectDB from "@/lib/mongodb";
import {
  TeamAppointment,
  TeamPerson,
  TeamSettings,
  TeamYear,
} from "@/models/Team";
import { defaultSettings, idSchema } from "@/lib/team-validation";

export async function publicTeam() {
  await connectDB();
  const [years, settings] = await Promise.all([
    TeamYear.find({ published: true }).sort({ year: -1 }).lean(),
    TeamSettings.findById("team").lean(),
  ]);
  return JSON.parse(
    JSON.stringify({ years, settings: { ...defaultSettings, ...settings } }),
  );
}
export async function publicRoster(yearId: string) {
  await connectDB();
  const appointments = await TeamAppointment.find({ yearId, published: true })
    .sort({ order: 1, _id: 1 })
    .lean();
  const people = await TeamPerson.find({
    _id: { $in: appointments.map((a) => a.personId) },
  }).lean();
  return JSON.parse(
    JSON.stringify(
      appointments
        .map((a) => ({
          ...a,
          person: people.find((p) => String(p._id) === String(a.personId)),
        }))
        .filter((a) => a.person),
    ),
  );
}
export async function publicMember(id: string) {
  if (!idSchema.safeParse(id).success) return null;
  await connectDB();
  const appointment = (await TeamAppointment.findOne({
    _id: id,
    published: true,
  }).lean()) as any;
  if (!appointment) return null;
  const [year, person, appointments] = await Promise.all([
    TeamYear.findOne({ _id: appointment.yearId, published: true }).lean(),
    TeamPerson.findById(appointment.personId).lean(),
    TeamAppointment.find({
      personId: appointment.personId,
      published: true,
    }).lean(),
  ]);
  if (!year || !person) return null;
  const positionYears = (await TeamYear.find({
    _id: { $in: appointments.map((value) => value.yearId) },
    published: true,
  }).lean()) as any[];
  const positions = appointments
    .map((value) => {
      const positionYear = positionYears.find(
        (candidate) => String(candidate._id) === String(value.yearId),
      );
      if (!positionYear) return null;
      return {
        por: value.por || "",
        group:
          positionYear.groups?.find(
            (group: { id: string; name: string }) =>
              group.id === value.groupId,
          )?.name || "",
        year: positionYear.year,
      };
    })
    .filter(Boolean)
    .sort((a: any, b: any) => b.year - a.year);
  return JSON.parse(
    JSON.stringify({ ...appointment, year, person, positions }),
  );
}
