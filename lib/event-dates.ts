const LEGACY_IST_OFFSET_MS = 5.5 * 60 * 60 * 1000
export const EVENT_TIME_ZONE = "Asia/Kolkata"

const EVENT_DATE_FORMAT = {
  timeZone: EVENT_TIME_ZONE,
  day: "2-digit",
  month: "short",
  year: "numeric",
} as const

const EVENT_TIME_FORMAT = {
  timeZone: EVENT_TIME_ZONE,
  hour: "2-digit",
  minute: "2-digit",
  hour12: true,
} as const

export function eventDateForUse(value: Date | string, timezoneNormalized?: boolean): Date {
  const date = new Date(value)
  return timezoneNormalized ? date : new Date(date.getTime() - LEGACY_IST_OFFSET_MS)
}

/**
 * Event timestamps represent India Standard Time. Keep formatting explicit so
 * server-rendered pages (which may run in UTC) and browsers show the same time.
 */
export function formatEventDate(value: Date | string): string {
  return new Intl.DateTimeFormat("en-IN", EVENT_DATE_FORMAT).format(new Date(value))
}

export function formatEventTime(value: Date | string): string {
  return new Intl.DateTimeFormat("en-IN", EVENT_TIME_FORMAT).format(new Date(value))
}

export function formatEventDateTime(value: Date | string): { date: string; time: string } {
  return {
    date: formatEventDate(value),
    time: formatEventTime(value),
  }
}

export function eventForResponse(event: any) {
  const value = typeof event?.toObject === "function" ? event.toObject() : { ...event }
  value.date = eventDateForUse(value.date, value.timezoneNormalized)
  if (value.rsvpDeadline) {
    value.rsvpDeadline = eventDateForUse(value.rsvpDeadline, value.timezoneNormalized)
  }
  return value
}
