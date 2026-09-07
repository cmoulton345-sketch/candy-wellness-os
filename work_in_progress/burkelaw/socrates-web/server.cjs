// Socrates Local Server — serves the built dist/ folder on http://localhost:3999
const http = require('http');
const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, 'dist');
const PORT = 3999;

const MIME = {
  '.html': 'text/html',
  '.js':   'application/javascript',
  '.css':  'text/css',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.png':  'image/png',
  '.woff2':'font/woff2',
  '.woff': 'font/woff',
};

http.createServer((req, res) => {
  let filePath = path.join(DIST, req.url === '/' ? '/index.html' : req.url);
  // Strip query strings
  filePath = filePath.split('?')[0];

  fs.readFile(filePath, (err, data) => {
    if (err) {
      // Fallback to index.html for SPA routing
      fs.readFile(path.join(DIST, 'index.html'), (e, d) => {
        if (e) { res.writeHead(404); res.end('Not found'); return; }
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(d);
      });
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'text/plain' });
    res.end(data);
  });
}).listen(PORT, '127.0.0.1', () => {
  console.log('');
  console.log('  ╔══════════════════════════════════════╗');
  console.log('  ║   Socrates | Virtual Legal Shadow    ║');
  console.log('  ║                                      ║');
  console.log(`  ║   http://localhost:${PORT}             ║`);
  console.log('  ║                                      ║');
  console.log('  ║   Close this window to stop server   ║');
  console.log('  ╚══════════════════════════════════════╝');
  console.log('');
});
