export default async function handler(req, res) {
  try {
    if (req.method !== 'GET') {
      return res.status(405).json({ ok: false, error: 'Method not allowed' });
    }

    const webhook = process.env.GOOGLE_SHEETS_WEBHOOK_URL;
    if (!webhook) {
      return res.status(503).json({ ok: false, error: 'Inventory service is not configured yet.' });
    }

    const response = await fetch(`${webhook}?action=inventory`, {
      method: 'GET',
      redirect: 'follow',
      cache: 'no-store'
    });

    if (!response.ok) {
      return res.status(502).json({ ok: false, error: 'The inventory service could not return data.' });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('NSP inventory sync error:', error);
    return res.status(500).json({ ok: false, error: 'Unable to load inventory right now.' });
  }
}
