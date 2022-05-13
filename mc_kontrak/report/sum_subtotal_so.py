from odoo import fields, models, api


class CustomSaleOrderSumReport(models.AbstractModel):
    _name = 'report.mc_kontrak.report_penawaran'
    _description = 'Hitung subtotal di Custom Quotation'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('test from report values SO')
        docs = self.env['sale.order'].browse(docids[0])
        order_line = self.env['sale.order.line'].search([('order_id', '=', docids[0])])
        id_section = 0
        arr_items = []
        for idx, line in enumerate(order_line):
            if line.display_type == 'line_section' or line.display_type == 'line_note':
                id_section = idx
            vals = {
                'id': line.id,
                'name': line.name,
                'display_type': line.display_type,
                'price_subtotal': line.price_subtotal,
                'currency_id': line.currency_id,
            }
            arr_items.append(vals)

        subtotal_sub = 0
        subtotal_otf = 0
        currency_id = 0
        for idx, val in enumerate(arr_items):
            print(val)
            currency_id = val["currency_id"]
            if idx < id_section:
                subtotal_sub += val["price_subtotal"]
            if idx > id_section:
                subtotal_otf += val["price_subtotal"]

        print('subtotal sub : ', subtotal_sub)
        print('subtotal otf : ', subtotal_otf)

        return {
            'doc_model': 'sale.order',
            'data': data,
            'docs': docs,
            'subtotal_sub': subtotal_sub,
            'subtotal_otf': subtotal_otf,
            'x_currency_id': currency_id,
        }
