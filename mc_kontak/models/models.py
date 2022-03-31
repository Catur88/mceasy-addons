# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomContact(models.Model):
    _inherit = 'res.partner'
    _description = 'Modul yang menginherit res.partner untuk menambah kolom baru'

    # Fields
    x_pic = fields.Char(string='PIC Customer', store=True)
    x_isteknisi = fields.Boolean(string='Teknisi McEasy', store=True)
    x_islocked = fields.Boolean(string='Lock Customer', store=True, default=False)

    # Relasi
    channel_ids = fields.Many2many('mail.channel', 'mail_channel_profile_partner', 'partner_id', 'channel_id',
                                   copy=False)

    x_device_wo = fields.One2many('mc_kontrak.device_wo', 'x_partner_id')

    def write(self, vals):
        print(vals)
        if 'x_isteknisi' in vals:
            if vals['x_isteknisi'] is True:
                self.env.cr.execute("""UPDATE res_partner SET function = 'Teknisi McEasy' WHERE id = %s """ % self.id)
        res = super(CustomContact, self).write(vals)
        return res
