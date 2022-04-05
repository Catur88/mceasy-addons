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
        for line in order_line:
            if line.display_type == 'line_section':
                id_section = line.id
            vals = {
                'id': line.id,
                'name': line.name,
                'display_type': line.display_type,
                'price_subtotal': line.price_subtotal,
            }
            arr_items.append(vals)

        subtotal_sub = 0
        subtotal_otf = 0
        for val in arr_items:
            if val["id"] < id_section:
                subtotal_sub += val["price_subtotal"]
            if val["id"] > id_section:
                subtotal_otf += val["price_subtotal"]

        # print('subtotal sub : ', subtotal_sub)
        # print('subtotal otf : ', subtotal_otf)

        return {
            'doc_model': 'sale.order',
            'data': data,
            'docs': docs,
            'subtotal_sub': subtotal_sub,
            'subtotal_otf': subtotal_otf
        }
