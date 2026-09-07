// ─── State-Machine Nurture Logic ───
// Schedule: Day 0, 2, 4, 7, 10
// Sheet columns: nurture_started (ISO date), last_email_day (0/2/4/7/10/done)

const SCHEDULE = [0, 2, 4, 7, 10];
const allRows = $input.all();
const results = [];
const seenEmails = new Set();

for (const item of allRows) {
  const _originalEmail = (item.json['email'] || '').trim(); // preserve original casing for sheet row matching
  const email = _originalEmail.toLowerCase();               // lowercase for dedup logic only
  if (!email || !email.includes('@')) continue;
  if (seenEmails.has(email)) continue;
  seenEmails.add(email);

  const nurtureStarted = (item.json['nurture_started'] || '').trim();
  const lastDay = String(item.json['last_email_day'] ?? '').trim();

  // ── NEW LEAD: no nurture_started yet ──
  if (!nurtureStarted) {
    results.push({
      json: {
        ...item.json,
        email,
        _originalEmail,
        _action: 'send',
        _emailDay: 0,
        _isNewLead: true,
        _nurtureStartedValue: new Date().toISOString()
      }
    });
    continue;
  }

  // ── COMPLETED: skip leads that finished the sequence ──
  if (lastDay === 'done') continue;

  // ── IN-PROGRESS: calculate what day they're on ──
  const startDate = new Date(nurtureStarted);
  const now = new Date();
  const elapsedDays = Math.floor((now - startDate) / (1000 * 60 * 60 * 24));
  const lastDayNum = parseInt(lastDay) || 0;
  const nextDay = SCHEDULE.find(d => d > lastDayNum && elapsedDays >= d);

  if (nextDay !== undefined) {
    results.push({
      json: {
        ...item.json,
        email,
        _originalEmail,
        _action: 'send',
        _emailDay: nextDay,
        _isNewLead: false,
        _nurtureStartedValue: nurtureStarted
      }
    });
  }
}

if (results.length === 0) return [];
return results;
