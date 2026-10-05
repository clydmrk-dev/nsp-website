function jsonResponse(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}

function normalizeEmail(email) {
  return String(email || '').trim().toLowerCase();
}

function generateVipCode() {
  var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  var code = 'NSP-';
  for (var i = 0; i < 8; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
}

function getVipSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('VIP Codes');
  if (!sheet) {
    sheet = ss.insertSheet('VIP Codes');
    sheet.appendRow(['Email', 'Code', 'Discount', 'Created At', 'Redeemed At', 'Redeemed Order']);
  }
  return sheet;
}

function createOrGetVipCode(email) {
  var normalizedEmail = normalizeEmail(email);
  if (!normalizedEmail) return { ok: false, error: 'Email is required.' };

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getVipSheet();
    var values = sheet.getDataRange().getValues();

    for (var i = 1; i < values.length; i++) {
      var rowEmail = normalizeEmail(values[i][0]);
      var code = String(values[i][1] || '').trim();
      var redeemedAt = values[i][4];
      if (rowEmail === normalizedEmail && code && !redeemedAt) {
        return { ok: true, code: code, discount: 10 };
      }
    }

    var code = generateVipCode();
    sheet.appendRow([normalizedEmail, code, 10, new Date(), '', '']);
    return { ok: true, code: code, discount: 10 };
  } finally {
    lock.releaseLock();
  }
}

function applyVipCode(email, vipCode, orderNumber) {
  var normalizedEmail = normalizeEmail(email);
  var normalizedCode = String(vipCode || '').trim().toUpperCase();
  if (!normalizedEmail || !normalizedCode) {
    return { ok: true, discount: 0, finalTotal: null };
  }

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getVipSheet();
    var values = sheet.getDataRange().getValues();

    for (var i = 1; i < values.length; i++) {
      var rowEmail = normalizeEmail(values[i][0]);
      var rowCode = String(values[i][1] || '').trim().toUpperCase();
      var redeemedAt = values[i][4];

      if (rowEmail === normalizedEmail && rowCode === normalizedCode) {
        if (redeemedAt) {
          return { ok: false, error: 'This VIP code has already been used.' };
        }

        return {
          ok: true,
          discount: 10,
          row: i + 1,
          sheet: sheet
        };
      }
    }

    return { ok: false, error: 'Invalid VIP code.' };
  } finally {
    lock.releaseLock();
  }
}

function markVipRedeemed(sheet, rowNumber, orderNumber) {
  sheet.getRange(rowNumber, 5, 1, 2).setValues([[new Date(), orderNumber || '']]);
}

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Orders');

    var data = JSON.parse(e.postData.contents);
    var action = String(data.action || '').trim();

    // VIP code generation is protected by the same server-side key used by NSP.
    if (action === 'generateVipCode') {
      var expectedKey = PropertiesService.getScriptProperties().getProperty('NSP_INTERNAL_API_KEY');
      if (expectedKey && String(data.key || '') !== expectedKey) {
        return jsonResponse({ ok: false, error: 'Unauthorized.' });
      }
      return jsonResponse(createOrGetVipCode(data.email));
    }

    // VIP redemption is handled atomically with the order request below.
    if (action === 'redeemVipCode') {
      var expectedRedeemKey = PropertiesService.getScriptProperties().getProperty('NSP_INTERNAL_API_KEY');
      if (expectedRedeemKey && String(data.key || '') !== expectedRedeemKey) {
        return jsonResponse({ ok: false, error: 'Unauthorized.' });
      }
      return jsonResponse(applyVipCode(data.email, data.vipCode, data.orderNumber));
    }

    var orderHeaders = [
      'Order Number',
      'Date/Time',
      'Customer Name',
      'Phone',
      'Email',
      'Address',
      'Items',
      'Subtotal',
      'Discount',
      'VIP Code',
      'Total',
      'Status'
    ];

    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Orders');
    }
    sheet.getRange(1, 1, 1, orderHeaders.length).setValues([orderHeaders]);

    var customer = data.customer || {};
    var items = Array.isArray(data.items) ? data.items : [];
    var subtotal = Number(data.total || 0);
    var discount = 0;
    var vipCode = String(data.vipCode || '').trim().toUpperCase();
    var vipRow = null;
    var vipSheet = null;

    if (vipCode) {
      var vipResult = applyVipCode(customer.email, vipCode, data.orderNumber);
      if (!vipResult.ok) return jsonResponse(vipResult);
      discount = Math.round(subtotal * 0.10 * 100) / 100;
      vipRow = vipResult.row;
      vipSheet = vipResult.sheet;
    }

    var finalTotal = Math.max(0, subtotal - discount);
    var itemText = items.map(function(item) {
      return item.name + ' | Size ' + item.size + ' | ₱' + item.price;
    }).join(' || ');

    sheet.appendRow([
      data.orderNumber || '',
      data.createdAt || new Date(),
      customer.name || '',
      customer.phone || '',
      customer.email || '',
      customer.address || '',
      itemText,
      subtotal,
      discount,
      vipCode,
      finalTotal,
      'NEW'
    ]);

    if (vipRow && vipSheet) {
      markVipRedeemed(vipSheet, vipRow, data.orderNumber);
    }

    return jsonResponse({ ok: true, orderNumber: data.orderNumber || '', subtotal: subtotal, discount: discount, total: finalTotal });
  } catch (error) {
    return jsonResponse({ ok: false, error: String(error) });
  }
}
