export default async function handler(req, res) {
  try {
    const webhook = process.env.GOOGLE_SHEETS_WEBHOOK_URL;
    const adminPassword = process.env.NSP_ADMIN_PASSWORD;
    const internalApiKey = process.env.NSP_INTERNAL_API_KEY;

    if (!webhook) return res.status(503).json({ ok: false, error: 'Order management is not configured yet.' });
    if (!adminPassword) return res.status(503).json({ ok: false, error: 'Admin access is not configured yet.' });
    if (!internalApiKey) return res.status(503).json({ ok: false, error: 'Internal API security is not configured yet.' });

    // Customer checkout is the only public operation. Every other method requires the admin password.
    if (req.method !== 'POST' && req.headers['x-admin-password'] !== adminPassword) {
      return res.status(401).json({ ok: false, error: 'Invalid admin password.' });
    }

    if (req.method === 'GET') {
      const action = req.query?.action || 'orders';
      if (action === 'orders' && req.headers['x-admin-password'] !== adminPassword) {
        return res.status(401).json({ ok: false, error: 'Invalid admin password.' });
      }

      const url = new URL(webhook);
      url.searchParams.set('action', action);
      if (action === 'orders') url.searchParams.set('key', internalApiKey);

      const response = await fetch(url.toString(), { method: 'GET', redirect: 'follow' });
      if (!response.ok) return res.status(502).json({ ok: false, error: 'The order service could not return data.' });
      const data = await response.json();
      return res.status(200).json(data);
    }

    if (req.method === 'PATCH') {
      const body = req.body || {};

      if (body.action === 'updateInventory') {
        const product = String(body.product || '').trim();
        const sizes = body.sizes || {};
        const allowedSizes = ['S', 'M', 'L', 'XL', '2XL', '3XL'];
        if (!product) return res.status(400).json({ ok: false, error: 'Product is required.' });

        const cleanSizes = {};
        for (const size of allowedSizes) {
          const value = Number(sizes[size]);
          if (!Number.isInteger(value) || value < 0) {
            return res.status(400).json({ ok: false, error: `Invalid inventory for size ${size}.` });
          }
          cleanSizes[size] = value;
        }

        const response = await fetch(webhook, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'updateInventory', product, sizes: cleanSizes, key: internalApiKey })
        });
        if (!response.ok) return res.status(502).json({ ok: false, error: 'The inventory service could not be updated.' });
        const data = await response.json();
        if (!data.ok) return res.status(400).json({ ok: false, error: data.error || 'Inventory could not be updated.' });
        return res.status(200).json(data);
      }

      const allowed = ['NEW', 'PROCESSING', 'SHIPPED', 'COMPLETED', 'CANCELLED'];
      const status = String(body.status || '').toUpperCase();
      if (!body.orderNumber || !allowed.includes(status)) {
        return res.status(400).json({ ok: false, error: 'Invalid order status update.' });
      }

      const response = await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'updateStatus', orderNumber: body.orderNumber, status, key: internalApiKey })
      });
      if (!response.ok) return res.status(502).json({ ok: false, error: 'The order service could not update the order.' });
      const data = await response.json();
      if (!data.ok) return res.status(400).json({ ok: false, error: data.error || 'Order status could not be updated.' });
      return res.status(200).json({ ok: true, orderNumber: body.orderNumber, status });
    }

    if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method not allowed' });

    const body = req.body || {};
    if (!body.orderNumber || !body.customer || !Array.isArray(body.items)) {
      return res.status(400).json({ ok: false, error: 'Invalid order payload.' });
    }

    const response = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        orderNumber: body.orderNumber,
        createdAt: new Date().toISOString(),
        customer: body.customer,
        items: body.items,
        total: body.total
      })
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.ok === false) {
      return res.status(400).json({ ok: false, error: data.error || 'The order could not be accepted.' });
    }
    return res.status(200).json({ ok: true, orderNumber: body.orderNumber });
  } catch (error) {
    console.error('NSP order sync error:', error);
    return res.status(500).json({ ok: false, error: 'Unable to process the order right now.' });
  }
}
