
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
from datetime import date
from odoo.tools import datetime
from dateutil.relativedelta import relativedelta

class SalesOrderLine(models.Model):

    _inherit = "sale.order.line"
    _name = "sale.order.line"

    x_sales_type = fields.Selection([('otf', 'One Time Fee'), ('monthly', 'Monthly'), ('yearly', 'Yearly')],
                                    string="Sales Type", default='otf')


    @api.onchange("product_id")
    def addproperty(self):
        for row in self:
            data_product = row.env['product.product'].search([('product_tmpl_id', '=', row.product_id.product_tmpl_id.id)])
            if data_product:
                row.x_sales_type = data_product['x_sales_type']

