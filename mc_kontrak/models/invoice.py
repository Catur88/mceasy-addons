from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move'

    # Autofill Invoice Line
    def insert_subscription(self):
        print('insert SUBS Berhasil')
        partner_id = self.partner_id.id
        query = """UPDATE account_move_line SET
                            """
        print(query)
        terms = []
        subs_line = self.env['sale.subscription'].search([('partner_id', '=', self.partner_id.id)])
        for row in subs_line.recurring_invoice_line_ids:
            for line in subs_line.subscription_log_ids:
                values = {}
            if row.product_id.id:
                values['product_id'] = row.product_id.id
                values['name'] = row.name
                values['quantity'] = row.quantity
                values['price_unit'] = row.price_unit
                values['price_subtotal'] = row.price_subtotal
                values['subscription_id'] = line.subscription_id

            self.env.cr.execute(query)
            print(query)
        terms.append((0, 0, values))

        return self.update({'invoice_line_ids': terms})
