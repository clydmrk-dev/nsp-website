import crypto from 'crypto';

function sign(value, secret) {
  return crypto.createHmac('sha256', secret).update(value).digest('base64url');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method not allowed' });

  const username = process.env.NSP_ADMIN_USERNAME;
  const password = process.env.NSP_ADMIN_PASSWORD;
  const sessionSecret = process.env.NSP_SESSION_SECRET || password;
  if (!username || !password || !sessionSecret) {
    return res.status(503).json({ ok: false, error: 'Admin authentication is not configured yet.' });
  }

  const suppliedUsername = String(req.body?.username || '').trim();
  const suppliedPassword = String(req.body?.password || '');
  const expectedUsername = Buffer.from(username);
  const actualUsername = Buffer.from(suppliedUsername);
  const expectedPassword = Buffer.from(password);
  const actualPassword = Buffer.from(suppliedPassword);

  const validUsername = expectedUsername.length === actualUsername.length && crypto.timingSafeEqual(expectedUsername, actualUsername);
  const validPassword = expectedPassword.length === actualPassword.length && crypto.timingSafeEqual(expectedPassword, actualPassword);

  if (!validUsername || !validPassword) {
    return res.status(401).json({ ok: false, error: 'Invalid username or password.' });
  }

  const expires = Math.floor(Date.now() / 1000) + 8 * 60 * 60;
  const payload = `admin.${expires}`;
  const token = `${payload}.${sign(payload, sessionSecret)}`;

  res.setHeader('Set-Cookie', `nsp_admin_session=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=28800`);
  return res.status(200).json({ ok: true, expires });
}
