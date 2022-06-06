from odoo import models, fields, api, _


class CustomSalesSubscription(models.Model):
    _inherit = 'sale.order'
    _description = 'Modul Subscription Sale Order yang menginherit sale.order'

    def create_subscriptions(self):
        # res = super(CustomSalesSubscription, self).create_subscriptions()
        print('Create Subs From Custom Sales Subs')
        pass
        # print(res)
        # print(res[0])
        # query = """
        #     UPDATE sale_subscription SET x_kontrak_id = %s, x_order_id = %s WHERE id = %s
        # """ % (self.kontrak_id.id, self.id, res[0])
        # self.env.cr.execute(query)
        # return res

    def action_subscription_invoice(self):
        invoices = self.env['account.move'].search([('invoice_line_ids.subscription_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "out_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class McSubscription(models.Model):
    _inherit = 'sale.subscription'
    _description = 'Modul yang menginherit sale.subscription'

    x_kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string="No Kontrak", store=True, ondelete='cascade')
    x_order_id = fields.Many2one('sale.order', store=True, string="No SO", readonly=True, ondelete='cascade')
    x_status_sub = fields.Selection([
        ('opensub', 'Open Subscription'),
        ('closesub', 'Close Subscription'),
    ], string='Status', default='opensub')

    def _compute_invoice_count(self):
        can_read = self.env['account.move'].check_access_rights('read', raise_exception=False)
        if not can_read:
            self.update({'invoice_count': 0})
            return
        res = self.env['account.move.line'].read_group(
            [('subscription_id', 'in', self.ids)], ['move_id:count_distinct'], ['subscription_id'])
        invoice_count_dict = {r['subscription_id'][0]: r['move_id'] for r in res}

        query = """
                    select sol.id from sale_order_line sol
                    inner join sale_order so 
                    on sol.order_id = so.id
                    inner join sale_subscription_line ssl 
                    on ssl.x_order_id = so.id 
                    where sol.order_id = ssl.x_order_id
                """
        self.env.cr.execute(query)
        order_line_id = self.env.cr.fetchone()[0]

        query = """SELECT COUNT(invoice_line_id) FROM sale_order_line_invoice_rel WHERE order_line_id = %s """ % order_line_id
        self.env.cr.execute(query)
        count_inv = self.env.cr.fetchone()[0]
        for subscription in self:
            subscription.invoice_count = invoice_count_dict.get(subscription.id, 0) + count_inv

    # Ubah Status Subscription
    def _update_status(self):
        print('tes save')
        query = """SELECT id,recurring_next_date,current_date, DATE_PART('day', recurring_next_date::timestamp - current_date::timestamp) 
            FROM sale_subscription WHERE DATE_PART('day', recurring_next_date::timestamp - current_date::timestamp) < 0
                    """
        self.env.cr.execute(query)
        date_list = self.env.cr.dictfetchall()
        print(date_list)
        if date_list:
            query = """update sale_subscription set x_status_sub = 'closesub' where DATE_PART('day', recurring_next_date::timestamp - current_date::timestamp) < 0
            """
            self.env.cr.execute(query)



    # Button untuk membuka related Invoices
    def action_subscription_invoice(self):
        print('print tested')
        invoices = self.env['account.move'].search([('invoice_line_ids.subscription_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "out_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    # # Buat Beberapa Subs Menjadi 1 Invoice
    # def action_invoice_create(self):
    #     print('test invoice')
    #     query = """SELECT COUNT(id) FROM account_move WHERE partner_id = %s
    #     """ % (self.partner_id.id)
    #     invoice_sub = self.env.cr.fetchone()[0]
    #     self.env.cr.execute(query)
    #     if invoice_sub < 1:
    #         invoices = self.action_subscription_invoice()
    #         print(invoices)
    #         query = """UPDATE account_move_line SET subscription_id = %s WHERE id = %s
    #         """ % (self.id.id, invoices[0])
    #         self.env.cr.execute(query)
    #
    #     else:
    #         self.env.cr.execute("""
    #         SELECT * FROM account_move_line WHERE partner_id = %s
    #         """ % self.partner_id.id)
    #         inv_data = self.env.cr.dictfetchone()
    #         print(inv_data)
    #         self.action_subscription_invoice(inv_data, row)
    #
    #     res = super(McSubscription, self).action_subscription_invoice()
    #     return res
    #
    #
    # # Buat Line Invoice
    # def create_line_invoice(self, inv_data):
    #     inv_line = self.recurring_invoice_line_ids
    #     for order in self:
    #         to_create = order._bagi_inv_line()
    #         for template in to_create:
    #             values = order._siapkan_inv_data(template)
    #             values['recurring_invoice_line_ids'] = to_create[template]._siapkan_subs_line_data()
    #             to_create[template].write({'subscription_id': inv_data['id']})

    #             print('product id', inv_line.product_id.id)
    #             print('uom id', inv_line.product_id.product_tmpl_id.uom_id.id)
    #             self.env['sale.subscription.line'].sudo().create({
    #                 'product_id': inv_line.product_id.id,
    #                 'company_id': inv_line.company_id.id,
    #                 'name': inv_line.name,
    #                 'quantity': inv_line.qty_delivered,
    #                 'uom_id': inv_line.product_id.product_tmpl_id.uom_id.id,
    #                 'price_unit': inv_line.price_unit,
    #                 'price_subtotal': inv_line.price_unit * inv_line.qty_delivered,
    #                 'currency_id': inv_line.currency_id.id,
    #                 'x_order_id': inv_line.order_id.id
    #             })
    #
    #
    # def _siapkan_inv_data(self, template):
    #     """Prepare a dictionnary of values to create a subscription from a template."""
    #     self.ensure_one()
    #     date_today = fields.Date.context_today(self)
    #     recurring_invoice_day = date_today.day
    #     recurring_next_date = self.env['sale.subscription']._get_recurring_next_date(
    #         template.recurring_rule_type, template.recurring_interval,
    #         date_today, recurring_invoice_day

    #     }
    #     default_stage = self.env['sale.subscription.stage'].search([('category', '=', 'progress')], limit=1)
    #     if default_stage:
    #         values['stage_id'] = default_stage.id
    #     return values
    #
    #
    # def _bagi_inv_line(self):
    #     """Split the order line according to subscription templates that must be created."""
    #     self.ensure_one()
    #     res = dict()
    #     new_inv_lines = self.recurring_invoice_line_ids.filtered(lambda
    #                                                                  l: not l.subscription_id and l.product_id.subscription_template_id and l.product_id.recurring_invoice)
    #     templates = new_inv_lines.mapped('product_id').mapped('subscription_template_id')
    #     for template in templates:
    #         lines = self.recurring_invoice_line_ids.filtered(
    #             lambda l: l.product_id.subscription_template_id == template and l.product_id.recurring_invoice)
    #         res[template] = lines
    #     return res


class McSubscriptionLines(models.Model):
    _inherit = 'sale.subscription.line'
    _description = 'Modul yang menginherit sale.subscription.line'

    x_order_id = fields.Many2one('sale.order', store=True, string="No SO", readonly=True)


class McSubscriptionWizard(models.TransientModel):
    _inherit = 'sale.subscription.wizard'
    _description = 'Modul yang menginherit sale.subscription.wizard'

    x_kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string="No Kontrak", store=True)

    # def create_sale_order(self):
    #     res = super(McSubscriptionWizard, self).create_sale_order()
    #     print('Create SO From Subs Wizard')
    #     query = """
    #         UPDATE sale_order SET kontrak_id = %s
    #         WHERE id = %s;
    #     """ % (self.subscription_id.x_kontrak_id.id, res['res_id'])
    #     self.env.cr.execute(query)
    #
    #     query = """
    #         UPDATE sale_order_line SET kontrak_id = %s
    #         WHERE order_id = %s;
    #     """ % (self.subscription_id.x_kontrak_id.id, res['res_id'])
    #     self.env.cr.execute(query)
    #
    #     query = """
    #         SELECT * FROM sale_order_line WHERE order_id = %s
    #     """ % res['res_id']
    #     self.env.cr.execute(query)
    #     result = self.env.cr.dictfetchall()
    #     print(result)
    #     print(result[0]['id'])
    #
    #     for res in result:
    #         query = """
    #             INSERT INTO mc_kontrak_product_order_line(kontrak_id,mc_qty_kontrak,mc_harga_produk,product_id,
    #             mc_qty_terpasang,mc_harga_diskon, mc_payment, mc_total, mc_period, mc_period_info)
    #             VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','1','bulan')
    #         """ % (res['kontrak_id'], int(res['product_uom_qty']), res['price_unit'], res['product_id'],
    #                int(res['product_uom_qty']), res['price_unit'], res['price_unit'], res['price_unit'])
    #         self.env.cr.execute(query)
    #
    #         query = """
    #             UPDATE sale_order_line SET x_mc_qty_kontrak = %s
    #             WHERE order_id = %s
    #         """ % (res['product_uom_qty'], res['order_id'])
    #         self.env.cr.execute(query)
    #
    #     return res


class McSubscriptionWizardOption(models.TransientModel):
    _inherit = 'sale.subscription.wizard.option'
    _description = 'Modul yang menginherit sale.subscription.wizard.option'
