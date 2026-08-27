function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Orders');

    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Orders');
      sheet.appendRow([
        'Order Number',
        'Date/Time',
        'Customer Name',
        'Phone',
        'Email',
        'Address',
        'Items',
        'Total',
        'Status'
      ]);
    }

    var data = JSON.parse(e.postData.contents);
    var customer = data.customer || {};
    var items = Array.isArray(data.items) ? data.items : [];

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
      data.total || 0,
      'NEW'
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(error) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
