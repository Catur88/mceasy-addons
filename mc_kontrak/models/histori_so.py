# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HistoriSO(models.Model):
    _name = 'mc_kontrak.histori_so'
    _description = 'Modul berisi data SO yang akan berelasi dengan kontrak'

    _sql_constraints = [
        ('no_so_unique', 'unique(x_order_id)', 'Tidak boleh duplikasi')
    ]

    x_kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak')
    x_order_id = fields.Many2one('sale.order', ondelete='cascade')
    x_churn_id = fields.Many2one('mc_kontrak.churn_order', ondelete='cascade')

    x_tgl_start = fields.Date(string='Tgl Start')
    x_tgl_end = fields.Date(string='Tgl End')
    x_item = fields.Many2one('product.product', string='Item')
    x_period = fields.Char(string='Period')
    x_status_pembayaran = fields.Char(string='Status Pembayaran')
    x_note = fields.Text(string='Note')
    x_qty_terpasang = fields.Integer(string='QTY Terpasang')
    x_qty_so = fields.Integer(string='QTY SO')
    x_tipe = fields.Char(string='Tipe')
