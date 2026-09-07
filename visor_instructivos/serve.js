const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8085;
const VISOR_DIR = __dirname;
const ROOT_DIR = path.resolve(__dirname, '..');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  '.ppt': 'application/vnd.ms-powerpoint',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf'
};

const server = http.createServer((req, res) => {
  let parsedUrl = req.url.split('?')[0];
  let decodedPath = decodeURIComponent(parsedUrl);

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Root redirects to app
  if (decodedPath === '/' || decodedPath === '/index.html') {
    return serveFile(path.join(VISOR_DIR, 'index.html'), res);
  }

  // Try in visor_instructivos first
  let targetPath = path.join(VISOR_DIR, decodedPath);
  if (fs.existsSync(targetPath) && fs.statSync(targetPath).isFile()) {
    return serveFile(targetPath, res);
  }

  // Try in ROOT_DIR (e.g. CAPACIDAD 1, CAPACIDAD 10...)
  targetPath = path.join(ROOT_DIR, decodedPath);
  if (fs.existsSync(targetPath) && fs.statSync(targetPath).isFile()) {
    return serveFile(targetPath, res);
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('File not found: ' + decodedPath);
});

function serveFile(filePath, res) {
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';
  const stat = fs.statSync(filePath);

  res.writeHead(200, {
    'Content-Type': contentType,
    'Content-Length': stat.size,
    'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  });

  fs.createReadStream(filePath).pipe(res);
}

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Ellucian PPTX Visor Server running at http://localhost:${PORT}/`);
});
