from odoo import models, fields, api, _


class DeviceWO(models.Model):
    _name = 'mc_kontrak.device_wo'
    _description = 'Modul yang berisi pemasangan dari WO dan berelasi ke Contact'

    x_jenis_kendaraan = fields.Many2one('mc_kontrak.jenis_kendaraan', string="Jenis Kendaraan")
    x_nopol = fields.Char(string='Nopol')
    x_tahun = fields.Char(string='Tahun')
    x_imei = fields.Char(string='IMEI')
    x_simcard = fields.Char(string='No Simcard')
    x_tgl_start_pasang = fields.Datetime(string="Tgl Start Pasang")
    x_tgl_end_pasang = fields.Datetime(string="Tgl End Pasang")
    x_isdeleted = fields.Boolean(default=False, store=True)

    # Relasi
    x_work_order_id = fields.Many2one('mc_kontrak.work_order', ondelete='cascade')
    x_partner_id = fields.Many2one('res.partner')
    x_churn_oder_line_id = fields.One2many('mc_kontrak.churn_order_line', 'x_imei', ondelete='cascade')

    def name_get(self):
        result = []
        for rec in self:
            imei = rec.x_imei
            result.append((rec.id, imei))

        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += [('x_imei', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

