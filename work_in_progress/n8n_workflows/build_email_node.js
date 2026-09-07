const allItems = $('Setup Lead Variables').all();
const results = [];

for (const item of allItems) {
  const L = item.json;
  const day = L.emailDay;

  const sig = `<div style="margin-top:40px;display:flex;align-items:center;border-top:1px solid #e2e8f0;padding-top:30px;"><img src="${L.photoUrl}" alt="Joe" style="width:70px;height:70px;border-radius:50%;margin-right:20px;object-fit:cover;border:2px solid #e2e8f0;"><div><p style="margin:0;font-weight:800;font-size:18px;color:#1a1a2e;">Joe Moulton</p><p style="margin:4px 0 0 0;font-size:14px;color:#64748b;font-weight:600;">Founder, FlowstateAI Automation</p><p style="margin:4px 0 0 0;font-size:13px;"><a href="${L.siteUrl}" style="color:#3b82f6;text-decoration:none;font-weight:600;">flowstateaiautomation.ai</a></p></div></div>`;

  const cta = (text, url, color = '#3b82f6') => `<div style="text-align:center;margin:40px 0;"><a href="${url}" style="background-color:${color};color:white;padding:16px 32px;text-decoration:none;border-radius:8px;font-weight:bold;font-size:16px;display:inline-block;box-shadow:0 4px 14px ${color}4d;">${text}</a></div>`;

  const wrap = (borderColor, body) => `<div style="font-family:'Helvetica Neue',Arial,sans-serif;color:#1a1a2e;max-width:600px;margin:0 auto;padding:40px 20px;line-height:1.6;background-color:#ffffff;border-top:5px solid ${borderColor};border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,0.05);"><div style="text-align:center;margin-bottom:40px;"><img src="${L.logoUrl}" alt="FlowstateAI" style="max-height:50px;"></div>${body}${sig}</div>`;

  const callout = (text, color = '#3b82f6') => `<div style="background-color:#f8fafc;padding:24px;border-left:4px solid ${color};border-radius:4px;margin:30px 0;"><p style="font-size:15px;margin:0;font-style:italic;color:#475569;">${text}</p></div>`;

  const offerBox = (headline, sub) => `<div style="text-align:center;margin:40px 0;background:linear-gradient(135deg,rgba(59,130,246,0.05),rgba(139,92,246,0.05));padding:40px 20px;border-radius:12px;border:1px solid rgba(59,130,246,0.1);"><h3 style="margin-top:0;color:#1a1a2e;font-size:18px;margin-bottom:8px;">${headline}</h3><p style="font-size:14px;color:#64748b;margin-bottom:24px;">${sub}</p><a href="${L.calendlyUrl}" style="background-color:#3b82f6;color:white;padding:16px 32px;text-decoration:none;border-radius:8px;font-weight:bold;font-size:16px;display:inline-block;box-shadow:0 4px 14px rgba(59,130,246,0.3);">Book My Free Build Session →</a></div>`;

  let subject, html;

  if (day === 0) {
    subject = `Good to meet you, ${L.firstName} — here's what I want to build for you.`;
    html = wrap('#3b82f6',
      `<h2 style="font-size:24px;font-weight:800;color:#1a1a2e;margin-bottom:24px;letter-spacing:-0.5px;">Good to meet you, ${L.firstName} — here's what I want to build for you.</h2>` +
      `<p style="font-size:16px;margin-bottom:20px;">Hi ${L.firstName},</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">I work with ${L.industry} businesses across Atlantic Canada who are great at what they do — but spending too many hours on tasks that should run automatically.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">Here's what I want to offer you — no strings attached:</p>` +
      offerBox('Your Free Build Session', 'Book 30 minutes with me. I\'ll identify the highest-impact automation for your business and build it live on the call. You walk away with it running — whether we work together or not.') +
      `<p style="font-size:16px;margin-bottom:20px;">I'll check back in a couple of days. In the meantime, if you have a specific bottleneck in mind — hit reply and tell me about it. I read every one.</p>` +
      `<p style="font-size:16px;margin-bottom:30px;">Talk soon,</p>`);

  } else if (day === 2) {
    subject = `${L.firstName}, your free build session is still open.`;
    html = wrap('#3b82f6',
      `<h2 style="font-size:24px;font-weight:800;color:#1a1a2e;margin-bottom:24px;letter-spacing:-0.5px;">${L.firstName}, your free build session is still open.</h2>` +
      `<p style="font-size:16px;margin-bottom:20px;">Hi ${L.firstName},</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">Just checking in. Life gets busy — I get it.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">The offer still stands: book 30 minutes with me and I'll build one automation into your business — live on the call, before we hang up. Yours to keep, no matter what.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">No pitch. No invoice. Just something useful you can use starting today.</p>` +
      offerBox('30 Minutes. One Working Automation.', 'I take on 3 of these calls per week. A spot is still yours.') +
      `<p style="font-size:16px;margin-bottom:20px;">If you're not sure what we'd even work on — that's exactly what the first 5 minutes of the call is for. You talk, I listen, and we find it together.</p>` +
      `<p style="font-size:16px;margin-bottom:30px;">Talk soon,</p>`);

  } else if (day === 4) {
    subject = `One idea for your ${L.industry} business, ${L.firstName}.`;
    html = wrap('#3b82f6',
      `<h2 style="font-size:24px;font-weight:800;color:#1a1a2e;margin-bottom:24px;letter-spacing:-0.5px;">One idea for your ${L.industry} business, ${L.firstName}.</h2>` +
      `<p style="font-size:16px;margin-bottom:20px;">Hi ${L.firstName},</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">I spend a lot of time thinking about what the highest-impact automation looks like for ${L.industry} businesses specifically.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">Here's the one I see come up most: <strong>an automatic follow-up that fires the moment someone submits an inquiry</strong> — before you've even seen the notification.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">It confirms you received their message, sets a personal tone, and keeps the lead warm while you finish up with your current client. Most businesses that implement this see their response-to-booking rate improve immediately — not because they responded faster, but because the lead never went cold in the first place.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">That's the kind of thing I build on the free call. Specific to you. Running before we hang up.</p>` +
      offerBox('Want me to build this for you?', '30 minutes. One automation built live. Yours to keep.') +
      `<p style="font-size:16px;margin-bottom:30px;">Talk soon,</p>`);

  } else if (day === 7) {
    subject = `${L.firstName}, I only take 3 of these calls a week.`;
    html = wrap('#3b82f6',
      `<h2 style="font-size:24px;font-weight:800;color:#1a1a2e;margin-bottom:24px;letter-spacing:-0.5px;">${L.firstName}, I only take 3 of these calls a week.</h2>` +
      `<p style="font-size:16px;margin-bottom:20px;">Hi ${L.firstName},</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">I keep it to 3 free build sessions per week — not as a sales tactic, but because I actually build the automation on the call, and doing it right takes focus.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">This week's spots are filling. I wanted to make sure you had a chance to grab one before they're gone.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">Here's what you're getting: 30 minutes, one automation built live in your business, yours to keep. No pitch until you ask for one. No invoice either way.</p>` +
      callout('"The system just... handles it." — Atlantic Canada service business owner') +
      offerBox('Grab a spot this week', '30 minutes. One automation built. Yours to keep.') +
      `<p style="font-size:16px;margin-bottom:30px;">Talk soon,</p>`);

  } else if (day === 10) {
    subject = `Last one from me, ${L.firstName}.`;
    html = wrap('#64748b',
      `<h2 style="font-size:24px;font-weight:800;color:#1a1a2e;margin-bottom:24px;letter-spacing:-0.5px;">Last one from me, ${L.firstName}.</h2>` +
      `<p style="font-size:16px;margin-bottom:20px;">Hi ${L.firstName},</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">I've sent a few emails now and I don't want to be one of those people who just keeps showing up in your inbox.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">So this is the last one — unless you want to stay in touch.</p>` +
      `<p style="font-size:16px;margin-bottom:20px;">The offer is still there. 30 minutes. One automation built live in your ${L.industry} business. Yours to keep. No cost, no pitch, no strings.</p>` +
      callout('If something has been slipping through the cracks — inquiries, follow-ups, admin that keeps piling up — and you want to see what fixing one of those things actually looks like, I\'m here.') +
      cta("Book My Free Build Session →", L.calendlyUrl) +
      `<p style="font-size:16px;margin-bottom:20px;">Either way — good luck with the business. Atlantic Canada needs more people doing real work the right way.</p>` +
      `<p style="font-size:16px;margin-bottom:30px;">Take care,</p>`);
  }

  results.push({ json: {
    html,
    subject,
    to: L.email,
    emailDay: day,
    firstName: L.firstName,
    fullName: L.fullName,
    phone: L.phone
  }});
}

return results;
