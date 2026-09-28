export function validateCalendars(value) {
  if (value === undefined) return undefined;
  if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).length > 200) throw new Error('Invalid activity calendars.');
  const result = {};
  for (const [key, calendar] of Object.entries(value)) {
    if (!/^\d{4}$/.test(key) || !calendar || calendar.year !== Number(key) ||
        typeof calendar.observedAt !== 'string' || !/^\d{4}-\d{2}-\d{2}T/.test(calendar.observedAt) || !Number.isFinite(Date.parse(calendar.observedAt)) ||
        !calendar.days || typeof calendar.days !== 'object' || Array.isArray(calendar.days) || Object.keys(calendar.days).length > 366) throw new Error('Invalid activity calendar.');
    const days = {};
    for (const [day, count] of Object.entries(calendar.days)) {
      const date = new Date(`${day}T00:00:00Z`);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(day) || !day.startsWith(key + '-') || !Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== day ||
          day > calendar.observedAt.slice(0, 10) || !Number.isSafeInteger(count) || count <= 0 || count > 1_000_000) throw new Error('Invalid activity calendar day.');
      days[day] = count;
    }
    result[key] = {year: calendar.year, observedAt: calendar.observedAt, days};
  }
  return result;
}
export function mergeCalendars(a = {}, b = {}) {
  const result = {...a};
  for (const [year, calendar] of Object.entries(b)) if (!result[year] || Date.parse(calendar.observedAt) >= Date.parse(result[year].observedAt)) result[year] = calendar;
  return result;
}
