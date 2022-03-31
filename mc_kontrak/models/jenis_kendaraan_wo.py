from odoo import models, fields

class JenisKendaraan(models.Model):
    _name = "mc_kontrak.jenis_kendaraan"
    _description = "Jenis Kendaraan"

    name = fields.Text(string="Jenis Kendaraan")