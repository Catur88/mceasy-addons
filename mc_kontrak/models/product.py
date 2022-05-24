from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    harga_diskon = fields.Float(string='Discounted Price')