from odoo import models, fields, api


class ChurnOrder(models.Model):
    _name = 'mc_kontrak.churn_order'
    _description = 'Churn Order'

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', store=True)
    name = fields.Char(string='No Churn', readonly=True, default='New')
    x_teknisi_1 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string="Teknisi 1", required=True)
    x_teknisi_2 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string='Teknisi 2')

    x_created_date = fields.Date(default=fields.Datetime.now(), string='Created Date')
    x_sales = fields.Many2one('res.users', string='Admin', default=lambda self: self.env.user, readonly=True)
    x_isopen = fields.Boolean(default=True, store=True)
    x_plan_start_date = fields.Datetime(store=True)
    x_plan_end_date = fields.Datetime(store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'In Progress'),
        ('sale', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', copy=False, index=True, tracking=3, default='draft')

    x_device_churn_line = fields.One2many('mc_kontrak.churn_order_line', 'x_churn_order')

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('mc_kontrak.churn_order')
        return super(ChurnOrder, self).create(vals_list)

    def action_confirm(self):
        print('confirm')
        count_hapus = 0
        kontrak_id = 0
        for row in self.x_device_churn_line:
            # Hapus dari Device Terpasang
            kontrak_id = row.x_imei.x_work_order_id.kontrak_id.id
            work_order_id = row.x_imei.x_work_order_id.id

            query = """
                UPDATE mc_kontrak_device_wo SET x_isdeleted = True WHERE id = %s
            """ % row.x_imei.id
            print(query)
            self.env.cr.execute(query)
            count_hapus += 1

        # Get product Id dari Churn Order Line
        query = """
                SELECT product_id FROM mc_kontrak_work_order_line WHERE kontrak_id = %s AND work_order_id = %s
            """ % (kontrak_id, work_order_id)
        self.env.cr.execute(query)
        product_id = self.env.cr.fetchone()[0]

        # Masukkan ke Histori
        query = """
            INSERT INTO mc_kontrak_histori_so(x_kontrak_id, x_churn_id, x_item, x_tgl_start, x_qty_so, x_tipe) VALUES
            ('%s', '%s', '%s', '%s', '%s', 'churn')
        """ % (kontrak_id, self.id, product_id, self.x_plan_start_date, count_hapus * -1)
        self.env.cr.execute(query)

        query = """
            UPDATE mc_kontrak_mc_kontrak SET mc_qty_kontrak = mc_qty_kontrak - %s WHERE id = %s
        """ % (count_hapus, kontrak_id)
        self.env.cr.execute(query)

        query = """
            UPDATE mc_kontrak_product_order_line SET mc_qty_kontrak = mc_qty_kontrak - %s WHERE kontrak_id = %s 
            AND product_id = %s
        """ % (count_hapus, kontrak_id, product_id)
        self.env.cr.execute(query)

        query = """
            UPDATE mc_kontrak_churn_order SET state = 'done' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)
        print('Update Work Order state to Done')

    def action_cancel(self):
        query = """
            UPDATE mc_kontrak_churn_order SET state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)
        print('Update Work Order state to Cancel')

    def action_sent(self):
        query = """
            UPDATE mc_kontrak_churn_order SET state = 'sent' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)
        print('Update Work Order state to Sent')


class ChurnOrderLine(models.Model):
    _name = 'mc_kontrak.churn_order_line'
    _description = 'Churn Order Line'

    x_jenis_kendaraan = fields.Many2one('mc_kontrak.jenis_kendaraan', string="Jenis Kendaraan",
                                        store=True, related='x_imei.x_jenis_kendaraan')
    x_nopol = fields.Char(string='Nopol', store=True, related='x_imei.x_nopol')
    x_tahun = fields.Char(string='Tahun', store=True, related='x_imei.x_simcard')
    x_simcard = fields.Char(string='No Simcard', store=True, related='x_imei.x_simcard')
    x_tgl_start_lepas = fields.Datetime(string="Tgl Start Lepas")
    x_tgl_end_lepas = fields.Datetime(string="Tgl End Lepas")

    # Relasi
    x_partner_id = fields.Many2one('res.partner', store=True)
    x_churn_order = fields.Many2one('mc_kontrak.churn_order', store=True)
    x_imei = fields.Many2one('mc_kontrak.device_wo', string='IMEI', ondelete='cascade',
                             domain=[('x_isdeleted', '!=', True)])
