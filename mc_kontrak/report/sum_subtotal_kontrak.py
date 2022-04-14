from odoo import fields, models, api


class KontrakSumReport(models.AbstractModel):
    _name = 'report.mc_kontrak.report_kontrak'
    _description = 'Hitung subtotal di Kontrak'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('test from report values Kontrak')
        docs = self.env['mc_kontrak.mc_kontrak'].browse(docids[0])
        order_line = self.env['mc_kontrak.product_order_line'].search([('kontrak_id', '=', docids[0])])
        id_section = 0
        arr_items = []
        for idx, line in enumerate(order_line):
            if line.display_type == 'line_section' or line.display_type == 'line_note':
                id_section = idx
            vals = {
                'id': line.id,
                'name': line.name,
                'display_type': line.display_type,
                'price_subtotal': line.mc_payment,
            }
            arr_items.append(vals)

        subtotal_sub = 0
        subtotal_otf = 0
        for idx, val in enumerate(arr_items):
            print(val)
            if idx < id_section:
                subtotal_sub += val["price_subtotal"]
            if idx > id_section:
                subtotal_otf += val["price_subtotal"]

        print('subtotal sub : ', subtotal_sub)
        print('subtotal otf : ', subtotal_otf)

        return {
            'doc_model': 'mc_kontrak.mc_kontrak',
            'data': data,
            'docs': docs,
            'subtotal_sub': subtotal_sub,
            'subtotal_otf': subtotal_otf
        }
