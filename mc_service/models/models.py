# -*- coding: utf-8 -*-

from odoo import models, fields, api


class McService(models.Model):
    _name = 'mc_service.mc_service'


class WorkOrder(models.Model):
    _inherit = 'mc_kontrak.work_order'


class WorkOrderLine(models.Model):
    _inherit = 'mc_kontrak.work_order_line'
