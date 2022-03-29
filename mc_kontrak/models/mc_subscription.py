from odoo import models, fields, api, _


class CustomSalesSubscription(models.Model):
    _inherit = 'sale.order'
    _description = 'Modul Subscription Sale Order yang menginherit sale.order'

    def create_subscriptions(self):
        # res = super(CustomSalesSubscription, self).create_subscriptions()
        print('Create Subs From Custom Sales Subs')
        # print(res)
        # print(res[0])
        # query = """
        #     UPDATE sale_subscription SET x_kontrak_id = %s, x_order_id = %s WHERE id = %s
        # """ % (self.kontrak_id.id, self.id, res[0])
        # self.env.cr.execute(query)
        # return res


class McSubscription(models.Model):
    _inherit = 'sale.subscription'
    _description = 'Modul yang menginherit sale.subscription'

    x_kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string="No Kontrak", store=True)
    x_order_id = fields.Many2one('sale.order', store=True, string="No SO", readonly=True)


class McSubscriptionLines(models.Model):
    _inherit = 'sale.subscription.line'
    _description = 'Modul yang menginherit sale.subscription.line'

    x_order_id = fields.Many2one('sale.order', store=True, string="No SO", readonly=True)


class McSubscriptionWizard(models.TransientModel):
    _inherit = 'sale.subscription.wizard'
    _description = 'Modul yang menginherit sale.subscription.wizard'

    x_kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string="No Kontrak", store=True)

    def create_sale_order(self):
        res = super(McSubscriptionWizard, self).create_sale_order()
        print('Create SO From Subs Wizard')
        query = """
            UPDATE sale_order SET kontrak_id = %s
            WHERE id = %s;
        """ % (self.subscription_id.x_kontrak_id.id, res['res_id'])
        self.env.cr.execute(query)

        query = """
            UPDATE sale_order_line SET kontrak_id = %s
            WHERE order_id = %s;
        """ % (self.subscription_id.x_kontrak_id.id, res['res_id'])
        self.env.cr.execute(query)

        query = """
            SELECT * FROM sale_order_line WHERE order_id = %s
        """ % res['res_id']
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        print(result)
        print(result[0]['id'])

        for res in result:
            query = """
                INSERT INTO mc_kontrak_product_order_line(kontrak_id,mc_qty_kontrak,mc_harga_produk,product_id,
                mc_qty_terpasang,mc_harga_diskon, mc_payment, mc_total, mc_period, mc_period_info)
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','1','bulan')
            """ % (res['kontrak_id'], int(res['product_uom_qty']), res['price_unit'], res['product_id'],
                   int(res['product_uom_qty']), res['price_unit'], res['price_unit'], res['price_unit'])
            self.env.cr.execute(query)

            query = """
                UPDATE sale_order_line SET x_mc_qty_kontrak = %s
                WHERE order_id = %s
            """ % (res['product_uom_qty'], res['order_id'])
            self.env.cr.execute(query)

        return res
