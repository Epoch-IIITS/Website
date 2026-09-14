export const MEDIA_CLEANUP_GRACE_MS = 24 * 60 * 60 * 1000;

export function describeMediaCleanupGracePeriod(
  milliseconds = MEDIA_CLEANUP_GRACE_MS,
) {
  const hours = milliseconds / (60 * 60 * 1000);
  return `${hours} ${hours === 1 ? "hour" : "hours"}`;
}

export const MEDIA_REFERENCE_LOCATIONS = [
  ["blogs", "featuredImage"],
  ["blogs", "content"],
  ["projects", "image"],
  ["events", "image"],
  ["galleries", "images.url"],
  // Mongoose pluralizes the TeamPerson model name to `teampeople`.
  ["teampeople", "photo"],
  ["teamrequests", "photo"],
  ["users", "image"],
];

export async function readMediaReferenceValues(db) {
  const groups = await Promise.all(
    MEDIA_REFERENCE_LOCATIONS.map(([collection, field]) =>
      db
        .collection(collection)
        .distinct(field, { [field]: { $type: "string", $ne: "" } }),
    ),
  );
  return groups.flat();
}

export function selectOrphanCandidates(assets, referenced, now = Date.now()) {
  const cutoff = now - MEDIA_CLEANUP_GRACE_MS;
  return assets.filter(
    (asset) =>
      new Date(asset.created_at).getTime() < cutoff &&
      !referenced.publicIds.has(asset.public_id) &&
      !referenced.urls.has(asset.secure_url),
  );
}
