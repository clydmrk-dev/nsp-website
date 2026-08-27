export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  try {
    const webhook = process.env.GOOGLE_SHEETS_WEBHOOK_URL;

    if (!webhook) {
      return res.status(503).json({
        ok: false,
        error: 'Order management is not configured yet.'
      });
    }

    const body = req.body || {};

    if (!body.orderNumber || !body.customer || !Array.isArray(body.items)) {
      return res.status(400).json({
        ok: false,
        error: 'Invalid order payload.'
      });
    }

    const response = await fetch(webhook, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        orderNumber: body.orderNumber,
        createdAt: new Date().toISOString(),
        customer: body.customer,
        items: body.items,
        total: body.total
      })
    });

    if (!response.ok) {
      return res.status(502).json({
        ok: false,
        error: 'The order service could not accept the order.'
      });
    }

    return res.status(200).json({
      ok: true,
      orderNumber: body.orderNumber
    });
  } catch (error) {
    console.error('NSP order sync error:', error);

    return res.status(500).json({
      ok: false,
      error: 'Unable to save the order right now.'
    });
  }
}
