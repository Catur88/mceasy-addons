# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api


class CustomContact(models.Model):
    _inherit = 'res.partner'
    _description = 'Modul yang menginherit res.partner untuk menambah kolom baru'

    # Fields
    x_pic = fields.Char(string='PIC Customer', store=True)
    x_isteknisi = fields.Boolean(string='Teknisi McEasy', store=True)
    x_islocked = fields.Boolean(string='Lock Customer', store=True, default=False)
    x_domain = fields.Char(string="Domain", store=True)

    # Relasi
    channel_ids = fields.Many2many('mail.channel', 'mail_channel_profile_partner', 'partner_id', 'channel_id',
                                   copy=False)

    x_device_wo = fields.One2many('mc_kontrak.device_wo', 'x_partner_id', domain=[('x_isdeleted', '=', False)])

    @api.model
    def create(self, vals_list):
        print(vals_list)
        if 'x_isteknisi' in vals_list:
            if vals_list['x_isteknisi'] is True:
                vals_list['function'] = 'Teknisi McEasy'

        if 'name' in vals_list and vals_list['x_domain'] is False:
            comp_name = vals_list['name'].split(' ')
            domain_name = ''
            print(comp_name)
            for nama in comp_name:
                nama = nama.lower()
                domain_name += nama[0:3]

            print('domain_name : ', domain_name)
            query = "SELECT x_domain FROM res_partner WHERE x_domain LIKE '" + domain_name + "%' ORDER BY id DESC LIMIT 1"
            self.env.cr.execute(query)
            domain_in_db = self.env.cr.fetchone()

            if domain_in_db is not None:
                no_urut = re.findall(r'%s(\d+)' % domain_name, domain_in_db[0])[0]
                fix_domain_name = domain_name + str(int(no_urut) + 1).zfill(len(no_urut))
            else:
                fix_domain_name = domain_name + '001'

            vals_list['x_domain'] = fix_domain_name

        res = super(CustomContact, self).create(vals_list)
        return res

    def write(self, vals):
        if 'x_isteknisi' in vals:
            if vals['x_isteknisi'] is True:
                self.env.cr.execute("""UPDATE res_partner SET function = 'Teknisi McEasy' WHERE id = %s """ % self.id)
        res = super(CustomContact, self).write(vals)
        return res
