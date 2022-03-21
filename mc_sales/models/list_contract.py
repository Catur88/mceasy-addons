
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
from datetime import date
from odoo.tools import datetime
from dateutil.relativedelta import relativedelta

class ListContractCustomer(models.Model):
    _name = "x.list.contract"


    x_so = fields.Char(string="SO")
    x_product = fields.Many2one('product.product' , string="Product")
    x_period = fields.Char(string="Period")
    x_date_start = fields.Date(string="Start Date")
    x_date_end = fields.Date(string="End Date")

