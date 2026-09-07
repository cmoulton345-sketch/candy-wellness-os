/**
 * Socrates Local Proxy — matches original wrangler config exactly
 * Model: gemini-2.5-pro on v1beta endpoint
 * Run: node server.js
 */

const http = require('http');
const https = require('https');

const GEMINI_API_KEY = 'AIzaSyAqDqdTRcAAKUNfndZPEEEjVR_0AciFz-U';
const PORT = 8787;

const SOCRATES_SYSTEM = `You are Socrates — a virtual senior associate and research engine operating at the AmLaw 100 standard. You think, anticipate, draft, and deliver output ready for a partner's desk. You are the associate who never sleeps, never bills for learning, and never misses an issue.

Rules:
- Jurisdiction first. Always confirm the operative jurisdiction.
- Flag what wasn't asked but should have been.
- Acknowledge gray areas and present the strongest counterargument.
- Never fabricate case citations. Flag uncertainty explicitly.
- End every response with a "Flags & Watch Items" section.`;

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
        try {
            const { jurisdiction, mode, message } = JSON.parse(body);

            const today = new Date().toLocaleDateString('en-CA', { year: 'numeric', month: 'long', day: 'numeric' });
            const fullPrompt = `TODAY'S DATE: ${today}\nUSER PARAMETERS:\n- Target Jurisdiction: ${jurisdiction}\n- Requested Operational Mode: ${mode}\n\nFACT PATTERN / INQUIRY:\n${message}`;

            const geminiPayload = JSON.stringify({
                system_instruction: { parts: [{ text: SOCRATES_SYSTEM }] },
                contents: [
                    { role: 'user', parts: [{ text: 'Acknowledge your operational parameters as Socrates.' }] },
                    { role: 'model', parts: [{ text: 'Parameters confirmed. I am Socrates. AmLaw 100 standard. Ready.' }] },
                    { role: 'user', parts: [{ text: fullPrompt }] }
                ],
                generationConfig: { temperature: 0.2 }
            });

            const options = {
                hostname: 'generativelanguage.googleapis.com',
                path: `/v1beta/models/gemini-2.5-pro:generateContent?key=${GEMINI_API_KEY}`,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(geminiPayload)
                }
            };

            const geminiReq = https.request(options, (geminiRes) => {
                let data = '';
                geminiRes.on('data', chunk => data += chunk);
                geminiRes.on('end', () => {
                    try {
                        const parsed = JSON.parse(data);
                        console.log('Gemini status:', geminiRes.statusCode);
                        if (geminiRes.statusCode !== 200) {
                            console.error('Gemini error:', data);
                            res.writeHead(500, { 'Content-Type': 'application/json' });
                            res.end(JSON.stringify({ response: 'Gemini API error: ' + data }));
                            return;
                        }
                        const text = parsed?.candidates?.[0]?.content?.parts?.[0]?.text ?? 'No response from Gemini.';
                        res.writeHead(200, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ response: text }));
                    } catch (e) {
                        res.writeHead(500, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ response: 'Parse error: ' + data }));
                    }
                });
            });

            geminiReq.on('error', (e) => {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ response: 'Network error: ' + e.message }));
            });

            geminiReq.write(geminiPayload);
            geminiReq.end();

        } catch (e) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ response: 'Bad request: ' + e.message }));
        }
    });
});

server.listen(PORT, () => {
    console.log(`✅ Socrates Proxy on http://localhost:${PORT}`);
    console.log(`   Model: gemini-2.5-pro (v1beta)`);
});
