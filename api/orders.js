export default async function handler(req, res) {
  try {
    const webhook = process.env.GOOGLE_SHEETS_WEBHOOK_URL;
    const adminPassword = process.env.NSP_ADMIN_PASSWORD;

    if (!webhook) {
      return res.status(503).json({
        ok: false,
        error: 'Order management is not configured yet.'
      });
    }

    if (req.method === 'GET') {
      if (!adminPassword) {
        return res.status(503).json({
          ok: false,
          error: 'Admin access is not configured yet.'
        });
      }

      if (req.headers['x-admin-password'] !== adminPassword) {
        return res.status(401).json({
          ok: false,
          error: 'Invalid admin password.'
        });
      }

      const response = await fetch(`${webhook}?action=orders`, {
        method: 'GET',
        redirect: 'follow'
      });

      if (!response.ok) {
        return res.status(502).json({
          ok: false,
          error: 'The order service could not return orders.'
        });
      }

      const data = await response.json();

      return res.status(200).json({
        ok: true,
        orders: Array.isArray(data.orders) ? data.orders : []
      });
    }

    if (req.method !== 'POST') {
      return res.status(405).json({
        ok: false,
        error: 'Method not allowed'
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
      error: 'Unable to process the order right now.'
    });
  }
}
