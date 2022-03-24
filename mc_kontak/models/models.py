# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomContact(models.Model):
    _inherit = 'res.partner'
    _description = 'Modul yang menginherit res.partner untuk menambah kolom baru'

    # Relasi
    channel_ids = fields.Many2many('mail.channel', 'mail_channel_profile_partner', 'partner_id', 'channel_id',
                                   copy=False)

    x_device_wo = fields.One2many('mc_kontrak.device_wo', 'x_partner_id')
