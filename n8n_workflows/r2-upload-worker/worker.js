// MIME type detection by file extension
function getMimeType(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  const types = {
    mp4: 'video/mp4',
    mov: 'video/quicktime',
    webm: 'video/webm',
    png: 'image/png',
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    gif: 'image/gif',
    webp: 'image/webp',
  };
  return types[ext] || 'application/octet-stream';
}

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const filename = url.pathname.replace(/^\//, '');

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // ── GET: fetch file from R2 (for testing + serving) ──
    if (request.method === 'GET') {
      if (!filename) {
        return new Response(JSON.stringify({ error: 'Specify a filename in the path.' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
        });
      }
      const object = await env.SOCIAL_IMAGES.get(filename);
      if (!object) {
        return new Response(JSON.stringify({ error: 'File not found.' }), {
          status: 404,
          headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
        });
      }
      return new Response(object.body, {
        status: 200,
        headers: {
          'Content-Type': getMimeType(filename),
          'Cache-Control': 'public, max-age=3600',
          ...CORS_HEADERS,
        },
      });
    }

    // ── PUT: upload file to R2 ──
    if (request.method === 'PUT') {
      const targetFilename = filename || `upload-${Date.now()}.bin`;
      const fileData = await request.arrayBuffer();

      if (!fileData || fileData.byteLength === 0) {
        return new Response(JSON.stringify({ error: 'Empty body.' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
        });
      }

      // Auto-detect MIME type from filename extension; fall back to Content-Type header
      const contentType =
        getMimeType(targetFilename) !== 'application/octet-stream'
          ? getMimeType(targetFilename)
          : (request.headers.get('Content-Type') || 'application/octet-stream');

      await env.SOCIAL_IMAGES.put(targetFilename, fileData, {
        httpMetadata: { contentType },
      });

      return new Response(JSON.stringify({
        success: true,
        filename: targetFilename,
        contentType,
        bytes: fileData.byteLength,
        publicUrl: `https://pub-049f9709a41044818786fa0bec5938c3.r2.dev/${targetFilename}`,
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
      });
    }

    return new Response(JSON.stringify({ error: 'Method not allowed. Use GET or PUT.' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
    });
  },
};
