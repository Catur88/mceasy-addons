# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
from datetime import date
from odoo.tools import datetime
from dateutil.relativedelta import relativedelta
import json


class PropertiesProduct(models.Model):
    _inherit = "product.template"

    x_sales_type = fields.Selection([('otf', 'One Time Fee'), ('monthly', 'Monthly'), ('yearly', 'Yearly')],
                                    string="Sales Type", default='otf')
