export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') {
      return res.status(405).json({ ok: false, error: 'Method not allowed.' });
    }

    const webhook = process.env.GOOGLE_SHEETS_WEBHOOK_URL;
    const internalApiKey = process.env.NSP_INTERNAL_API_KEY;
    if (!webhook || !internalApiKey) {
      return res.status(503).json({ ok: false, error: 'VIP service is not configured yet.' });
    }

    const body = req.body || {};
    const action = String(body.action || 'generateVipCode');
    const email = String(body.email || '').trim().toLowerCase();
    if (!email) {
      return res.status(400).json({ ok: false, error: 'Email is required.' });
    }

    if (action !== 'generateVipCode') {
      return res.status(400).json({ ok: false, error: 'Invalid VIP action.' });
    }

    const response = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'generateVipCode', email, key: internalApiKey })
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.ok === false) {
      return res.status(400).json({ ok: false, error: data.error || 'Unable to generate a VIP code.' });
    }

    return res.status(200).json({
      ok: true,
      code: data.code,
      discount: Number(data.discount || 10)
    });
  } catch (error) {
    console.error('NSP VIP code error:', error);
    return res.status(500).json({ ok: false, error: 'Unable to generate a VIP code right now.' });
  }
}
