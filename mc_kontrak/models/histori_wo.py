from odoo import models, fields, api


class HistoriWO(models.Model):
    _name = 'mc_kontrak.histori_wo'
    _description = 'Modul yang menampung histori pemasangan WO agar tampil ke SO'

    # Fields
    x_qty_terpasang = fields.Integer(string="QTY Terpasang")
    x_date_created = fields.Date(string="Date Created")

    # Relation
    x_work_order_id = fields.Many2one('mc_kontrak.work_order')
    x_order_id = fields.Many2one('sale.order')
    x_teknisi_1 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string="Teknisi 1")
    x_teknisi_2 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string='Teknisi 2')
    x_admin_sales = fields.Many2one('res.users', string='Admin Sales', default=lambda self: self.env.user)
