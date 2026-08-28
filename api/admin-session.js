import crypto from 'crypto';

function sign(value, secret) {
  return crypto.createHmac('sha256', secret).update(value).digest('base64url');
}

function validSession(req) {
  const secret = process.env.NSP_SESSION_SECRET || process.env.NSP_ADMIN_PASSWORD;
  const cookie = String(req.headers.cookie || '').match(/(?:^|;\s*)nsp_admin_session=([^;]+)/)?.[1];
  if (!secret || !cookie) return false;

  const parts = cookie.split('.');
  if (parts.length !== 3 || parts[0] !== 'admin') return false;
  const payload = `${parts[0]}.${parts[1]}`;
  const signature = parts[2];
  const expected = sign(payload, secret);
  if (signature.length !== expected.length) return false;
  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) return false;
  return Number(parts[1]) > Math.floor(Date.now() / 1000);
}

export { validSession };

export default async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).json({ ok: false, error: 'Method not allowed' });
  return res.status(200).json({ ok: validSession(req) });
}
