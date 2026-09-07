import http.server
import json
import urllib.request
import urllib.error
from datetime import datetime

PORT = 8787
GEMINI_API_KEY = 'AIzaSyAqDqdTRcAAKUNfndZPEEEjVR_0AciFz-U'

SOCRATES_SYSTEM = """You are Socrates — a virtual senior associate and research engine operating at the AmLaw 100 standard. You think, anticipate, draft, and deliver output ready for a partner's desk. You are the associate who never sleeps, never bills for learning, and never misses an issue.

Rules:
- Jurisdiction first. Always confirm the operative jurisdiction.
- Flag what wasn't asked but should have been.
- Acknowledge gray areas and present the strongest counterargument.
- Never fabricate case citations. Flag uncertainty explicitly.
- End every response with a "Flags & Watch Items" section."""

class SocratesProxyHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            jurisdiction = req_data.get('jurisdiction', '')
            mode = req_data.get('mode', '')
            message = req_data.get('message', '')

            today = datetime.now().strftime('%B %d, %Y')
            full_prompt = f"TODAY'S DATE: {today}\nUSER PARAMETERS:\n- Target Jurisdiction: {jurisdiction}\n- Requested Operational Mode: {mode}\n\nFACT PATTERN / INQUIRY:\n{message}"

            gemini_payload = {
                "system_instruction": { "parts": [{ "text": SOCRATES_SYSTEM }] },
                "contents": [
                    { "role": "user", "parts": [{ "text": "Acknowledge your operational parameters as Socrates." }] },
                    { "role": "model", "parts": [{ "text": "Parameters confirmed. I am Socrates. AmLaw 100 standard. Ready." }] },
                    { "role": "user", "parts": [{ "text": full_prompt }] }
                ],
                "generationConfig": { "temperature": 0.2 }
            }

            req_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
            req_body = json.dumps(gemini_payload).encode('utf-8')

            req = urllib.request.Request(
                req_url,
                data=req_body,
                headers={'Content-Type': 'application/json'}
            )

            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read().decode('utf-8')
                    parsed_res = json.loads(res_body)
                    
                    # Extract the response text
                    candidates = parsed_res.get('candidates', [])
                    if candidates:
                        parts = candidates[0].get('content', {}).get('parts', [])
                        if parts:
                            text = parts[0].get('text', 'No response from Gemini.')
                        else:
                            text = 'No response from Gemini.'
                    else:
                        text = 'No response from Gemini.'

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'response': text}).encode('utf-8'))
                    print("Gemini status: 200")

            except urllib.error.HTTPError as e:
                err_content = e.read().decode('utf-8')
                print(f"Gemini API error status: {e.code}, content: {err_content}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'response': f'Gemini API error: {err_content}'}).encode('utf-8'))

            except Exception as e:
                print(f"Network / parsing error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'response': f'Server error: {str(e)}'}).encode('utf-8'))

        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': f'Bad request: {str(e)}'}).encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, SocratesProxyHandler)
    print(f"✅ Socrates Proxy (Python) on http://localhost:{PORT}")
    print("   Model: gemini-2.5-pro (v1beta)")
    httpd.serve_forever()
