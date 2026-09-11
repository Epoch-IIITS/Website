const LEGACY_IST_OFFSET_MS = 5.5 * 60 * 60 * 1000

export function eventDateForUse(value: Date | string, timezoneNormalized?: boolean): Date {
  const date = new Date(value)
  return timezoneNormalized ? date : new Date(date.getTime() - LEGACY_IST_OFFSET_MS)
}

export function eventForResponse(event: any) {
  const value = typeof event?.toObject === "function" ? event.toObject() : { ...event }
  value.date = eventDateForUse(value.date, value.timezoneNormalized)
  if (value.rsvpDeadline) {
    value.rsvpDeadline = eventDateForUse(value.rsvpDeadline, value.timezoneNormalized)
  }
  return value
}
