import crypto from 'crypto';

function sign(value, secret) {
  return crypto.createHmac('sha256', secret).update(value).digest('base64url');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method not allowed' });

  const password = process.env.NSP_ADMIN_PASSWORD;
  const sessionSecret = process.env.NSP_SESSION_SECRET || password;
  if (!password || !sessionSecret) return res.status(503).json({ ok: false, error: 'Admin authentication is not configured yet.' });

  const supplied = String(req.body?.password || '');
  const expected = Buffer.from(password);
  const actual = Buffer.from(supplied);
  const valid = expected.length === actual.length && crypto.timingSafeEqual(expected, actual);

  if (!valid) return res.status(401).json({ ok: false, error: 'Invalid admin password.' });

  const expires = Math.floor(Date.now() / 1000) + 8 * 60 * 60;
  const payload = `admin.${expires}`;
  const token = `${payload}.${sign(payload, sessionSecret)}`;

  res.setHeader('Set-Cookie', `nsp_admin_session=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=28800`);
  return res.status(200).json({ ok: true, expires });
}
