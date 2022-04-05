# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import is_html_empty
from dateutil.relativedelta import relativedelta


class mc_kontrak(models.Model):
    _name = 'mc_kontrak.mc_kontrak'
    _description = 'Custom module untuk data kontrak'

    # Field
    name = fields.Char(string='No Kontrak', readonly=True, default='New')
    mc_cust = fields.Many2one('res.partner', string='Customer', domain=[("is_company", '=', True)])
    mc_pic_cust = fields.Char(string='PIC Customer')
    mc_create_date = fields.Date(string='Created Date', readonly=True, store=True, default=fields.Datetime.now())
    mc_confirm_date = fields.Date(string='Confirm Date', readonly=True, copy=False)
    mc_total = fields.Monetary(string='Total', readonly=True, compute='total_harga', store=True)
    mc_pajak = fields.Monetary(string='Total Pajak', readonly=True, store=True)
    mc_tak_pajak = fields.Monetary(string='Total Tak Pajak', readonly=True, store=True)
    mc_isopen = fields.Boolean(default=True)
    mc_sales = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    mc_admin_sales = fields.Many2one('res.users', string='Admin Sales', default=lambda self: self.env.user,
                                     readonly=True)

    x_subtotal_otf = fields.Monetary(string='Subtotal One Time Fee')
    x_subtotal_sub = fields.Monetary(string='Subtotal Subscription')
    mc_qty_kontrak = fields.Integer(default=0, store=True)

    x_kontrak_start_date = fields.Date(string="Kontrak Start Date")
    x_kontrak_end_date = fields.Date(string="Kontrak End Date")

    mc_state = fields.Selection([
        ('draft', 'Draft'),
        # ('sent', 'Quotation Sent'),
        ('done', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    so_count = fields.Integer(string='SO', compute='_count_so')

    # Relasi
    product_order_line = fields.One2many('mc_kontrak.product_order_line', 'kontrak_id', string='No Kontrak')
    histori_so_line = fields.One2many('mc_kontrak.histori_so', 'x_kontrak_id', string='Histori SO')
    currency_id = fields.Many2one('res.currency', default=12)

    @api.onchange('x_kontrak_start_date')
    def get_one_year(self):
        if self.x_kontrak_start_date:
            self.x_kontrak_end_date = self.x_kontrak_start_date + relativedelta(years=1)

    @api.onchange('mc_cust')
    def change_pic_cust(self):
        self.mc_pic_cust = self.mc_cust.x_pic

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('mc_kontrak.mc_kontrak')
        return super(mc_kontrak, self).create(vals_list)

    def write(self, vals):
        if self.product_order_line:
            print('hitung subtotal by section')
            subtotal_otf = 0
            subtotal_sub = 0
            print(subtotal_sub, subtotal_otf)

            query = """
                SELECT id FROM mc_kontrak_product_order_line
                WHERE kontrak_id = %s AND display_type = 'line_section'
            """ % self.id
            self.env.cr.execute(query)
            print(query)
            print(self.env.cr.fetchone())
            if self.env.cr.fetchone() is None:
                id_section = 0
            else:
                id_section = self.env.cr.fetchone()[0]

            if id_section != 0:
                query = """
                    SELECT SUM(mc_payment) as subtotal_sub FROM mc_kontrak_product_order_line
                    WHERE id < %s
                """ % id_section
                self.env.cr.execute(query)
                print(query)
                subtotal_sub = self.env.cr.fetchone()[0]
                if subtotal_sub is None:
                    subtotal_sub = 0

                print(subtotal_sub)

                query = """
                    SELECT SUM(mc_payment) as subtotal_otf FROM mc_kontrak_product_order_line
                    WHERE id > %s
                """ % id_section
                self.env.cr.execute(query)
                print(query)
                subtotal_otf = self.env.cr.fetchone()[0]
                if subtotal_otf is None:
                    subtotal_otf = 0

                print(subtotal_otf)

                query = """
                    UPDATE mc_kontrak_mc_kontrak SET x_subtotal_otf = %s,
                    x_subtotal_sub = %s WHERE id = %s
                """ % (subtotal_otf, subtotal_sub, self.id)
                self.env.cr.execute(query)
                print(query)

        return super(mc_kontrak, self).write(vals)

    # def action_sent(self):
    #     query = """
    #         UPDATE mc_kontrak_mc_kontrak SET mc_state = 'sent' WHERE id = %s
    #     """ % self.id
    #     self.env.cr.execute(query)
    #     print("Update kontrak state into Sent")

    # Total Harga
    @api.depends('product_order_line')
    def total_harga(self):
        total = 0.00
        pajak = 0.00
        i = 0
        for rec in self.product_order_line:
            i += 1
            print(i)
            print(rec.mc_pajak)
            total += rec.mc_payment
            pajak += rec.mc_pajak

        print('pajak', pajak)
        self.mc_total = total
        self.mc_pajak = pajak
        self.mc_tak_pajak = total - pajak

    # Hitung berapa SO di Kontrak ini
    def _count_so(self):
        query = "SELECT COUNT(0) FROM public.sale_order where kontrak_id = %s " % self.id
        print(query)
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        self.so_count = result[0]

    # Button untuk membuka related SO
    def action_view_so_button(self):
        action = self.env.ref('sale.action_quotations').read()[0]
        action['domain'] = [('kontrak_id', '=', self.id)]
        action['context'] = {}
        return action

    # Button untuk membuat SO baru dari Kontrak
    def action_create_so_button(self):
        for row in self:
            partner_id = row.mc_cust.id

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'context': {
                'default_partner_id': partner_id,
                'default_kontrak_id': self.id
            }
        }

    def action_confirm(self):
        # Action Confirm Kontrak
        query = """
            UPDATE mc_kontrak_mc_kontrak SET mc_state = 'done', mc_confirm_date = now()
            WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        print('confirm contract')

    def action_cancel(self):
        query = """
            UPDATE mc_kontrak_mc_kontrak SET mc_state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        print('cancel contract')

    @api.depends('product_order_line')
    def _hitung_qty_belum_terpasang(self):
        for row in self.product_order_line:
            query = "SELECT SUM(x_mc_qty_terpasang) FROM public.sale_order_line WHERE kontrak_id = %s AND product_id = %s" % (
                self.id, row.product_id.id)

            self.env.cr.execute(query)
            result = self.env.cr.fetchone()

            print("SUM QTY TERPASANG : ", result[0])
            row.mc_qty_belum_terpasang = row.mc_qty_kontrak - result[0]
            row.mc_qty_terpasang = result[0]


class ProductOrderLine(models.Model):
    _name = 'mc_kontrak.product_order_line'
    _description = 'Order line dari data kontrak'

    # Relasi
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string='No Kontrak', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])

    currency_id = fields.Many2one('res.currency')
    tax_id = fields.Many2one('account.tax', string='Taxes')

    # Field
    mc_qty_kontrak = fields.Integer(string='QTY Kontrak')
    mc_qty_so = fields.Integer(string='QTY SO')
    mc_qty_terpasang = fields.Integer(string='QTY Terpasang', default=0)
    mc_qty_belum_terpasang = fields.Integer(string='QTY Belum Terpasang')

    mc_harga_produk = fields.Float(string='Standard Price', related='product_template_id.list_price', store=True)
    mc_harga_diskon = fields.Monetary(string='Discounted Price')
    mc_pajak = fields.Float(string='Pajak', compute='_hitung_subtotal', store=True, readonly=True)
    mc_harga_tak_pajak = fields.Monetary(string='Harga Tak Pajak', store=True, readonly=True)

    mc_period = fields.Integer(string='Period')
    mc_period_info = fields.Selection([
        ('bulan', 'Bulan'),
        ('tahun', 'Tahun'),
        ('unit', 'Unit')
    ], string='UoM')
    mc_payment = fields.Float(string='Subtotal', readonly=True, compute='_hitung_subtotal', store=True)
    mc_total = fields.Float(string='Total', readonly=True, store=True)
    mc_isopen = fields.Boolean(default=True)
    mc_unit_price = fields.Monetary(string='Unit Price')

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    name = fields.Char(string='Description')

    @api.depends('mc_qty_kontrak', 'mc_harga_diskon', 'mc_period', 'mc_period_info', 'tax_id')
    def _hitung_subtotal(self):
        subtotal = 0
        grandtotal = 0
        pajakTotalProduk = 0
        totalTakPajak = 0

        for line in self:
            price = 0
            unitPrice = 0
            pajakTotal = pajakUnit = takPajak = 0
            if line.mc_period_info == 'tahun':
                price = line.mc_harga_diskon * line.mc_qty_kontrak * line.mc_period * 12
                unitPrice = line.mc_harga_diskon * line.mc_period * 12
                if line.tax_id:
                    if line.tax_id.amount != 0:
                        takPajak = price
                        pajakTotal = price / (line.tax_id.amount * 100)
                        pajakUnit = unitPrice / (line.tax_id.amount * 100)
            else:
                price = line.mc_harga_diskon * line.mc_qty_kontrak * line.mc_period
                unitPrice = line.mc_harga_diskon * line.mc_period
                if line.tax_id:
                    if line.tax_id.amount != 0:
                        takPajak = price
                        pajakTotal = price / (line.tax_id.amount * 100)
                        pajakUnit = unitPrice / (line.tax_id.amount * 100)

            subtotal += price
            pajakTotalProduk += pajakTotal
            totalTakPajak += takPajak
            line.update({
                'mc_payment': price + pajakTotal,
                'mc_unit_price': unitPrice + pajakUnit,
                'mc_qty_belum_terpasang': line.mc_qty_kontrak
            })

        grandtotal = subtotal
        self.mc_total = grandtotal
        self.mc_pajak = pajakTotalProduk

    @api.model
    def view_init(self, fields_list):
        print(self.display_type)
        print(fields_list)


class CustomSalesOrder(models.Model):
    _inherit = 'sale.order'
    _order = 'kontrak_id DESC'
    _description = 'Modul yang mengcustom module sale.order'

    # Relasi
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string='No Kontrak', ondelete='cascade')
    kontrak_product_line = fields.Many2one('mc_kontrak.product_order_line')
    histori_wo_line = fields.One2many('mc_kontrak.histori_wo', 'x_order_id')

    wo_count = fields.Integer(string='WO', compute='_count_wo')

    # state = fields.Selection([
    #     ('draft', 'Quotation'),
    #     ('sent', 'Terima DP'),
    #     ('sale', 'Progress'),
    #     ('done', 'Done'),
    #     ('cancel', 'Cancelled'),
    # ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    x_order_line = fields.One2many('sale.order.line', 'order_id')
    x_mc_qty_kontrak = fields.Integer(string='Quantity Kontrak')
    # x_mc_qty_terpasang = fields.Integer(string='Quantity Terpasang')
    # x_mc_harga_produk = fields.Monetary(string='Standard Price')
    x_mc_isopen = fields.Boolean(default=True, store=True)
    x_start_date = fields.Date(string='Start Date')
    x_no_po = fields.Char(string='No PO Customer')
    x_qty_terpasang = fields.Integer(default=0, store=True)

    x_subtotal_otf_so = fields.Monetary(string='Subtotal One Time Fee')
    x_subtotal_sub_so = fields.Monetary(string='Subtotal Subscription')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    x_warning = fields.Boolean(default=False)

    @api.model
    def create(self, vals_list):
        print('Akses Method Create Custom Sale Order')
        vals_list['name'] = self.env['ir.sequence'].next_by_code('sale.order.new')
        return super(CustomSalesOrder, self).create(vals_list)

    def write(self, vals):
        print('method write diakses')
        res = super(CustomSalesOrder, self).write(vals)
        print(self.kontrak_id.id)
        if ('order_line' in vals):
            arr_order_line = vals['order_line']
            print(arr_order_line)

            print('hitung subtotal SO by section')
            subtotal_otf = 0
            subtotal_sub = 0
            print(subtotal_sub, subtotal_otf)

            query = """
                SELECT id FROM sale_order_line
                WHERE order_id = %s AND display_type = 'line_section'
            """ % self.id
            self.env.cr.execute(query)
            print(query)
            hasil_fetch = self.env.cr.fetchone()
            if hasil_fetch is None:
                id_section = 0
            else:
                id_section = hasil_fetch[0]

            print(id_section)
            if id_section != 0:
                query = """
                    SELECT SUM(price_subtotal) as subtotal_sub FROM sale_order_line
                    WHERE id < %s AND order_id = %s
                """ % (id_section, self.id)
                self.env.cr.execute(query)
                print(query)
                subtotal_sub = self.env.cr.fetchone()[0]
                if subtotal_sub is None:
                    subtotal_sub = 0

                print(subtotal_sub)

                query = """
                    SELECT SUM(price_subtotal) as subtotal_otf FROM sale_order_line
                    WHERE id > %s AND order_id = %s
                """ % (id_section, self.id)
                self.env.cr.execute(query)
                print(query)
                subtotal_otf = self.env.cr.fetchone()[0]
                if subtotal_otf is None:
                    subtotal_otf = 0

                print(subtotal_otf)

                query = """
                    UPDATE sale_order SET x_subtotal_otf_so = %s,
                    x_subtotal_sub_so = %s WHERE id = %s
                """ % (subtotal_otf, subtotal_sub, self.id)
                self.env.cr.execute(query)
                print(query)

        return res

    # Auto fill Order Line
    def insert_kontrak(self):
        print('insert kontrak func')
        kontrak_id = self.kontrak_id
        partner = self.partner_id
        terms = []

        kontrak_line = self.env['mc_kontrak.mc_kontrak'].search([('id', '=', kontrak_id.id)])
        if kontrak_line:
            for row in kontrak_line.product_order_line:
                values = {}

                # Cek jika status produk open, masukkan ke SO
                if row.mc_isopen:
                    values['product_id'] = row.product_id.id
                    values['kontrak_line_id'] = row.id
                    values['x_mc_qty_kontrak'] = row.mc_qty_kontrak
                    values['kontrak_id'] = kontrak_id.id
                    values['price_unit'] = row.mc_harga_diskon
                    values['discount'] = (row.mc_harga_produk - row.mc_harga_diskon) / row.mc_harga_produk
                    values['x_mc_isopen'] = row.mc_isopen
                    values['product_uom_qty'] = row.mc_qty_kontrak - row.mc_qty_terpasang
                    values['discount'] = 0
                    values['x_mc_harga_produk'] = row.mc_harga_produk

                    terms.append((0, 0, values))

        return self.update({'order_line': terms})

    def action_cancel(self):
        print('test cancel')
        query = """
            SELECT product_uom_qty, kontrak_line_id  FROM sale_order_line sol 
            WHERE sol.order_id  = %s
        """ % self.id

        self.env.cr.execute(query)
        arrQuery = self.env.cr.dictfetchall()

        if arrQuery:
            query = """
                update mc_kontrak_mc_kontrak set mc_isopen = true where id = %s
            """ % self.kontrak_id.id
            self.env.cr.execute(query)
            for row in arrQuery:
                query = """
                    update mc_kontrak_product_order_line set
                    mc_qty_terpasang = mc_qty_belum_terpasang - %s,
                    mc_qty_belum_terpasang = mc_qty_belum_terpasang - %s
                    where id = %s 
                """ % (row['product_uom_qty'], row['product_uom_qty'], row['kontrak_line_id'])
                self.env.cr.execute(query)

        query = """
                UPDATE sale_order SET state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        query = """
            DELETE FROM mc_kontrak_histori_so WHERE x_order_id = %s
        """ % self.id
        self.env.cr.execute(query)

        res = super(CustomSalesOrder, self).action_cancel()
        return res

    def action_confirm(self):
        # Action Confirm SO
        print('action confirm from SO')
        so_line = self.x_order_line
        qty_so = 0

        query = """
            SELECT x_islocked FROM res_partner WHERE id = %s
        """ % self.partner_id.id
        print(query)
        self.env.cr.execute(query)
        is_company_locked = self.env.cr.fetchone()[0]

        if is_company_locked:
            print('Company is Locked')
            text = """Tidak dapat mengkonfirmasi SO. Status Company masih di Lock"""
            query = 'delete from display_dialog_box'
            self.env.cr.execute(query)
            value = self.env['display.dialog.box'].sudo().create({'text': text})
            return {
                'name': 'Company di Lock',
                'type': 'ir.actions.act_window',
                'res_model': 'display.dialog.box',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'res_id': value.id,
                'flags': {'form': {'action_buttons': True}}
            }
        else:
            if self.kontrak_id.id is False:
                # Buat Kontrak Baru dan Ambil IDnya
                contract_name = self.env['ir.sequence'].next_by_code('mc_kontrak.mc_kontrak')
                query = """
                    INSERT INTO mc_kontrak_mc_kontrak(mc_cust, name, mc_create_date, mc_isopen, mc_state,
                    mc_sales, mc_admin_sales, mc_confirm_date, x_kontrak_start_date, x_kontrak_end_date, mc_pic_cust) VALUES 
                    ('%s', '%s', now(), true, 'done', '%s', '%s',now(), now(), now() + interval '1 year', (SELECT x_pic
                    FROM res_partner WHERE id = %s))
                    RETURNING id
                """ % (self.partner_id.id, contract_name, self.env.user.id, self.env.user.id, self.partner_id.id)
                self.env.cr.execute(query)
                print(query)
                kontrak_id = self.env.cr.fetchone()[0]

                # Cek order_line, masukkan ke product_order_line Kontrak
                if self.x_order_line:
                    for row in self.x_order_line:
                        self.env.cr.execute("""SELECT * FROM product_template WHERE id = %s""" % row.product_id.id)
                        product_id = self.env.cr.dictfetchone()
                        query = """
                            INSERT INTO mc_kontrak_product_order_line(kontrak_id, product_id, mc_qty_kontrak, mc_qty_terpasang,
                            mc_harga_produk, mc_harga_diskon, mc_period, mc_period_info, currency_id, tax_id, mc_isopen, name)
                            VALUES ('%s','%s','%s','%s','%s','%s', '1', 'bulan', 12, 1, true, '%s') RETURNING id
                        """ % (kontrak_id, row.product_id.id, row.x_mc_qty_kontrak, int(row.product_uom_qty),
                               product_id['list_price'], row.price_unit, row.name)
                        print(query)
                        self.env.cr.execute(query)
                        result = self.env.cr.dictfetchone()
                        id_sol = result['id']

                        # Masukkan Sales Order ke histori SO
                        query = """
                            INSERT INTO mc_kontrak_histori_so(x_kontrak_id,
                            x_tgl_start, x_item, x_period, x_status_pembayaran,
                            x_note, x_qty_so) VALUES ('%s',now(),'%s','%s','%s','','%s' )
                        """ % (kontrak_id, row.product_id.id, '1 - bulan', self.state, int(row.product_uom_qty))
                        print(query)
                        self.env.cr.execute(query)

                # Update Sales Order, agar berelasi dengan Kontrak yang baru dibuat
                self.env.cr.execute("SELECT id FROM sale_order ORDER BY id DESC LIMIT 1")
                order_id = self.env.cr.fetchone()[0]
                print(order_id)

                query = """
                    UPDATE sale_order SET kontrak_id = %s WHERE id = %s
                """ % (kontrak_id, order_id)
                print(query)
                self.env.cr.execute(query)

                # Update histori SO agar nyambung Sales Order Id
                query = """
                    UPDATE mc_kontrak_histori_so SET x_order_id = %s WHERE x_kontrak_id = %s
                """ % (order_id, kontrak_id)
                self.env.cr.execute(query)

                # Update Sale Order Line set Kontrak ID
                self.env.cr.execute("""UPDATE sale_order_line SET kontrak_id = %s, kontrak_line_id = %s 
                WHERE order_id = %s""" % (kontrak_id, id_sol, order_id))
            else:
                if so_line:
                    i = 0
                    for row in so_line:
                        # if arr_order_line[i][2]['product_uom_qty']:
                        # x_qty_terpasang = arr_order_line[i][2]['product_uom_qty']
                        id_sol = 0
                        print('row :', row)
                        print('row kontrak line : ', row.kontrak_line_id.id)
                        print('row kontrak line 2 : ', row.kontrak_line_id)
                        if row.kontrak_line_id.id is False:
                            print(row.order_id.kontrak_id.mc_qty_kontrak)
                            print(int(row.order_id.kontrak_id.mc_qty_kontrak))

                            query = """
                                INSERT INTO mc_kontrak_product_order_line(kontrak_id, product_id, currency_id,
                                mc_qty_kontrak, mc_qty_terpasang, mc_harga_produk, mc_harga_diskon, mc_payment,
                                mc_total, mc_unit_price) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') RETURNING id
                            """ % (row.kontrak_id.id, row.product_id.id, row.currency_id.id,
                                   int(row.order_id.kontrak_id.mc_qty_kontrak), int(row.product_uom_qty),
                                   row.price_unit,
                                   row.price_unit, row.price_total, row.price_total, row.price_unit)
                            print(query)
                            self.env.cr.execute(query)
                            result = self.env.cr.dictfetchone()
                            id_sol = result['id']

                        query = """
                            SELECT mc_period, mc_period_info FROM mc_kontrak_product_order_line
                            WHERE kontrak_id = %s
                        """ % self.kontrak_id.id
                        print(query)
                        self.env.cr.execute(query)
                        getPeriod = self.env.cr.dictfetchone()
                        periode = str(getPeriod['mc_period']) + " " + str(getPeriod['mc_period_info'])

                        query = """
                            INSERT INTO mc_kontrak_histori_so(x_kontrak_id,
                            x_order_id, x_tgl_start, x_item, x_period, x_status_pembayaran,
                            x_note, x_qty_so) VALUES ('%s','%s',now(),'%s','%s','%s','','%s' )
                        """ % (
                            self.kontrak_id.id, row.order_id.id, row.product_id.id,
                            periode, self.state, int(row.product_uom_qty))
                        print(query)
                        self.env.cr.execute(query)

                        x_qty_terpasang = row.product_uom_qty
                        print('product_uom_qty = ', x_qty_terpasang)

                        query = "SELECT coalesce(SUM(sol.product_uom_qty), 0) FROM public.sale_order so " \
                                "JOIN public.sale_order_line sol " \
                                "ON sol.order_id = so.id " \
                                "WHERE so.state NOT IN('cancel') AND " \
                                "sol.kontrak_line_id = %s AND " \
                                "sol.id != %s" % (
                                    id_sol if row.kontrak_line_id.id is False else row.kontrak_line_id.id, row.id)
                        self.env.cr.execute(query)
                        print(query)
                        x_qty_terpasang2 = self.env.cr.fetchone()[0]
                        total_terpasang = x_qty_terpasang + x_qty_terpasang2

                        query = "UPDATE public.mc_kontrak_product_order_line SET mc_qty_terpasang = %s, " \
                                "mc_qty_belum_terpasang = (mc_qty_kontrak - %s) " \
                                "WHERE id = %s" % (
                                    total_terpasang, total_terpasang, id_sol if row.kontrak_line_id.id is False
                                    else row.kontrak_line_id.id)
                        print(query)
                        self.env.cr.execute(query)

                        query = """
                            UPDATE mc_kontrak_mc_kontrak SET mc_qty_kontrak = %s WHERE id = %s
                        """ % (row.x_mc_qty_kontrak, row.kontrak_id.id)
                        self.env.cr.execute(query)


                        if query:
                            print('oke, qty dikurangi, histori so dimasukkan')
                        i = i + 1

                    query = """
                        update mc_kontrak_mc_kontrak set
                        mc_isopen = False
                        where id = %s
                        and mc_qty_kontrak = (
                            select SUM(mkpol.mc_qty_terpasang) as mc_qty_terpasang
                            from mc_kontrak_mc_kontrak mkmk
                            join mc_kontrak_product_order_line mkpol on mkpol.kontrak_id = mkmk.id
                            where mkmk.id = %s
                        )
                    """ % (self.kontrak_id.id, self.kontrak_id.id)
                    print(query)
                    self.env.cr.execute(query)

                    query = """SELECT SUM(x_qty_so) FROM mc_kontrak_histori_so mkhs WHERE x_kontrak_id = %s""" % self.kontrak_id.id
                    print(query)
                    self.env.cr.execute(query)
                    sum_qty_so = self.env.cr.fetchone()[0]

                    query = """UPDATE mc_kontrak_product_order_line SET mc_qty_terpasang = %s 
                    WHERE kontrak_id = %s AND product_id = %s""" % (sum_qty_so, self.kontrak_id.id, row.product_id.id)
                    print(query)
                    self.env.cr.execute(query)

            query = """
                    UPDATE sale_order SET state = 'sale' WHERE id = %s
            """ % self.id
            self.env.cr.execute(query)

            res = super(CustomSalesOrder, self).action_confirm()
            return res

    # Button untuk membuat WO baru dari SO
    def action_report_wo_spk(self):
        for row in self:
            partner_id = row.kontrak_id.mc_cust.id

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mc_kontrak.work_order',
            'context': {
                'default_partner_id': partner_id,
                'default_kontrak_id': row.kontrak_id.id,
                'default_order_id': self.id
            }
        }

    # Button untuk membuka related WO
    def action_view_wo_button(self):
        action = self.env.ref('mc_kontrak.work_order_course_action').read()[0]
        action['domain'] = [('order_id', '=', self.id)]
        action['context'] = {}
        return action

    # Hitung berapa SO di Kontrak ini
    def _count_wo(self):
        self.env.cr.execute("SELECT COUNT(0) FROM public.mc_kontrak_work_order where order_id = %s " % self.id)
        result = self.env.cr.fetchone()
        self.wo_count = result[0]


class CustomSalesOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Modul yang mengcustom module sale.order.line'

    product_id = fields.Many2one('product.product')
    order_id = fields.Many2one('sale.order', required=True, Store=True, Index=True)
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak')
    kontrak_line_id = fields.Many2one('mc_kontrak.product_order_line')

    # Field
    x_mc_qty_kontrak = fields.Integer(string='QTY Kontrak', store=True)
    x_mc_qty_terpasang = fields.Integer(readonly=True, store=True)
    x_mc_harga_produk = fields.Monetary(string='Standard Price', store=True)
    x_mc_harga_diskon = fields.Monetary()
    x_mc_isopen = fields.Boolean(default=True, store=True)

    # price_subtotal = fields.Monetary(compute='_hitung_subtotal_so')

    @api.onchange('product_id')
    def _get_unit_price(self):
        if self.product_id:
            self.env.cr.execute("""SELECT product_tmpl_id FROM product_product WHERE id = %s""" % self.product_id.id)
            product_tmpl_id = self.env.cr.fetchone()[0]
            if product_tmpl_id:
                self.env.cr.execute("""SELECT list_price FROM product_template WHERE id = %s""" % product_tmpl_id)
                list_price = self.env.cr.fetchone()[0]
                self.x_mc_harga_produk = list_price

    # Total Harga
    @api.depends('x_mc_harga_produk', 'x_mc_harga_diskon', 'x_mc_qty_terpasang')
    def _hitung_subtotal_so(self):
        subtotal = 0

        for line in self:
            price = line.x_mc_harga_diskon * line.x_mc_qty_terpasang
            print('price in row ', price)
            subtotal += price
            line.update({
                'price_subtotal': price
            })


class WorkOrder(models.Model):
    _name = 'mc_kontrak.work_order'
    _inherit = 'sale.order'
    _description = 'Modul Work Order yang menginherit sale.order'

    # Field
    name = fields.Char(string='No WO', readonly=True, default='New')
    x_teknisi_1 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string="Teknisi 1", required=True)
    x_teknisi_2 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string='Teknisi 2')

    x_created_date = fields.Date(default=fields.Datetime.now(), string='Created Date')
    x_sales = fields.Many2one('res.users', string='Admin', default=lambda self: self.env.user, readonly=True)
    x_isopen = fields.Boolean(default=True, store=True)
    x_plan_start_date = fields.Datetime(store=True)
    x_plan_end_date = fields.Datetime(store=True)

    # Relasi
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak')
    order_id = fields.Many2one('sale.order', store=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', related='kontrak_id.mc_cust', store=True)
    product_id = fields.Many2one('product.product')
    work_order_line = fields.One2many('mc_kontrak.work_order_line', 'work_order_id', store=True)
    device_wo_line = fields.One2many('mc_kontrak.device_wo', 'x_work_order_id', string='Device WO', store=True,
                                     ondelete='cascade')

    # Relasi dari sale.order
    transaction_ids = fields.Many2many('payment.transaction', 'work_order_transaction_rel', 'id',
                                       'transaction_id',
                                       string='Transactions', copy=False, readonly=True)
    tag_ids = fields.Many2many('crm.tag', 'work_order_tag_rel', 'id', 'tag_id', string='Tags')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'In Progress'),
        ('sale', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', copy=False, index=True, tracking=3, default='draft')

    # Hitung jumlah subs tiap WO
    subscription_count = fields.Integer(compute='_compute_subscription_count')

    def _compute_subscription_count(self):
        """Compute the number of distinct subscriptions linked to the order."""
        for order in self:
            sub_count = len(
                self.env['mc_kontrak.work_order_line'].read_group(
                    [('work_order_id', '=', order.id), ('subscription_id', '!=', False)],
                    ['subscription_id'], ['subscription_id']))
            order.subscription_count = sub_count

    def action_open_subscriptions(self):
        action = self.env.ref('sale_subscription.sale_subscription_action').read()[0]
        action['domain'] = [('x_kontrak_id', '=', self.kontrak_id.id)]
        action['context'] = {}
        return action

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('mc_kontrak.work_order')
        return super(WorkOrder, self).create(vals_list)

    def write(self, vals):
        res = super(WorkOrder, self).write(vals)
        device_wo_line = self.device_wo_line
        if device_wo_line:
            for row in device_wo_line:
                query = """
                    UPDATE mc_kontrak_device_wo SET x_partner_id = %s
                """ % row.x_work_order_id.partner_id.id
                self.env.cr.execute(query)
        return res

    # Auto fill Order Line
    def insert_so_line(self):
        print('insert SO line func')
        kontrak_id = self.kontrak_id.id
        order_id = self.order_id.id
        terms = []
        print(order_id)
        so_line = self.env['sale.order'].search([('id', '=', order_id)])
        print(so_line)
        if so_line:
            for row in so_line.order_line:
                values = {}
                print(row.id)

                # Cek jika status produk open, masukkan ke WO Line
                values['product_id'] = row.product_id.id
                values['order_id'] = row.order_id.id
                values['product_uom_qty'] = row.product_uom_qty
                values['qty_delivered'] = row.product_uom_qty
                values['sale_order_line_id'] = row.id
                values['price_unit'] = row.price_unit

                terms.append((0, 0, values))

        return self.update({'work_order_line': terms})

    def action_cancel(self):
        print('test cancel work order')
        query = """
            SELECT qty_delivered, sale_order_line_id  FROM mc_kontrak_work_order_line wol 
            WHERE wol.work_order_id  = %s
        """ % self.id
        self.env.cr.execute(query)
        print(query)
        arrQuery = self.env.cr.dictfetchall()
        print(arrQuery)

        if arrQuery:
            query = """
                update sale_order set x_mc_isopen = true where id = %s
            """ % self.kontrak_id.id
            self.env.cr.execute(query)
            for row in arrQuery:
                query = """
                    update sale_order_line set
                    qty_delivered = qty_delivered - %s
                    where id = %s 
                """ % (row['qty_delivered'], row['sale_order_line_id'])
                print(query)
                self.env.cr.execute(query)

        query = """
            DELETE FROM mc_kontrak_histori_wo WHERE x_work_order_id = %s
        """ % self.id
        self.env.cr.execute(query)

        query = """
                UPDATE mc_kontrak_work_order SET state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        res = super(WorkOrder, self).action_cancel()
        return res

    def action_confirm(self):
        print('action confirm tes work order')
        wo_line = self.work_order_line
        if wo_line:
            i = 0
            for row in wo_line:
                qty_wo = row.qty_delivered
                print('QTY WO Terpasang = ', qty_wo)

                query = "SELECT coalesce(SUM(wol.qty_delivered), 0) FROM mc_kontrak_work_order wo " \
                        "JOIN mc_kontrak_work_order_line wol " \
                        "ON wol.work_order_id = wo.id " \
                        "WHERE wo.state NOT IN('cancel') AND " \
                        "wol.order_id = %s AND " \
                        "wol.id != %s" % (row.order_id.id, row.id)
                self.env.cr.execute(query)
                print(query)
                x_qty_terpasang2 = self.env.cr.fetchone()[0]
                total_terpasang = qty_wo + x_qty_terpasang2

                query = "UPDATE sale_order_line SET qty_delivered = %s, " \
                        "x_mc_qty_terpasang = %s " \
                        "WHERE id = %s" % (total_terpasang, total_terpasang, row.sale_order_line_id.id)
                self.env.cr.execute(query)

                query = """
                    UPDATE sale_order SET x_qty_terpasang = %s WHERE id = %s
                """ % (row.product_uom_qty, row.order_id.id)
                self.env.cr.execute(query)

                # Memasukkan Histori WO
                query = """
                    INSERT INTO mc_kontrak_histori_wo(x_qty_terpasang,x_date_created,x_work_order_id,x_order_id,
                    x_teknisi_1,x_teknisi_2,x_admin_sales) VALUES ('%s','%s','%s','%s','%s','%s','%s')
                """ % (row.qty_delivered, self.x_created_date, row.work_order_id.id, row.order_id.id,
                       self.x_teknisi_1.id,
                       self.x_teknisi_2.id if self.x_teknisi_2.id is not False else self.x_teknisi_1.id,
                       self.x_sales.id)
                self.env.cr.execute(query)

                print(query)
                print('Histori WO dimasukkan')

                i = i + 1

            query = """
                update sale_order set
                x_mc_isopen = False
                where id = %s
                and x_qty_terpasang = (
                    select SUM(sol.qty_delivered) as terpasang
                    from sale_order so
                    join sale_order_line sol on sol.order_id = so.id
                    where so.id = %s
                )
            """ % (self.order_id.id, self.order_id.id)
            print(query)
            self.env.cr.execute(query)

            query = """
                    UPDATE mc_kontrak_work_order SET state = 'done' WHERE id = %s
            """ % self.id
            self.env.cr.execute(query)

            self.env.cr.execute("""
                SELECT COUNT(id) FROM sale_subscription WHERE x_kontrak_id = %s
            """ % self.kontrak_id.id)
            count_kontrak_on_sub = self.env.cr.fetchone()[0]
            if count_kontrak_on_sub < 1:
                subs_id = self.create_subscriptions()
                query = """
                    UPDATE sale_subscription SET x_kontrak_id = %s, x_order_id = %s WHERE id = %s
                """ % (self.kontrak_id.id, self.order_id.id, subs_id[0])
                self.env.cr.execute(query)

                query = """
                    UPDATE sale_subscription_line SET x_order_id = %s WHERE analytic_account_id = %s
                """ % (self.order_id.id, subs_id[0])
                print(query)
                self.env.cr.execute(query)
            else:
                self.env.cr.execute("""
                    SELECT * FROM sale_subscription WHERE x_kontrak_id = %s
                """ % self.kontrak_id.id)
                subs_data = self.env.cr.dictfetchone()
                print(subs_data)
                self.create_line_subscriptions(subs_data, row)

            res = super(WorkOrder, self).action_confirm()
            return res

    def action_sent(self):
        query = """
            UPDATE mc_kontrak_work_order SET state = 'sent' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)
        print('Update Work Order state to Sent')

    def _siapkan_subs_data(self, template):
        """Prepare a dictionnary of values to create a subscription from a template."""
        self.ensure_one()
        date_today = fields.Date.context_today(self)
        recurring_invoice_day = date_today.day
        recurring_next_date = self.env['sale.subscription']._get_recurring_next_date(
            template.recurring_rule_type, template.recurring_interval,
            date_today, recurring_invoice_day
        )
        values = {
            'name': template.name,
            'template_id': template.id,
            'partner_id': self.partner_id.id,
            'partner_invoice_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'payment_term_id': self.payment_term_id.id,
            'date_start': fields.Date.context_today(self),
            'description': self.note if not is_html_empty(self.note) else template.description,
            'pricelist_id': self.pricelist_id.id,
            'company_id': self.company_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'recurring_next_date': recurring_next_date,
            'recurring_invoice_day': recurring_invoice_day,
            'payment_token_id': self.transaction_ids._get_last().token_id.id if template.payment_mode == 'success_payment' else False,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
        }
        default_stage = self.env['sale.subscription.stage'].search([('category', '=', 'progress')], limit=1)
        if default_stage:
            values['stage_id'] = default_stage.id
        return values

    def create_line_subscriptions(self, subs_data, wo_line):
        for order in self:
            to_create = order._bagi_sub_line()
            for template in to_create:
                values = order._siapkan_subs_data(template)
                values['recurring_invoice_line_ids'] = to_create[template]._siapkan_subs_line_data()
                to_create[template].write({'subscription_id': subs_data['id']})

                self.env['sale.subscription.log'].sudo().create({
                    'subscription_id': subs_data['id'],
                    'event_date': fields.Date.context_today(self),
                    'event_type': '0_creation',
                    'amount_signed': wo_line.price_unit * wo_line.qty_delivered,
                    'recurring_monthly': wo_line.price_unit * wo_line.qty_delivered,
                    'currency_id': 12,
                    'category': subs_data['stage_category'],
                    'user_id': order.user_id.id,
                    'team_id': order.team_id.id,
                })

                self.env['sale.subscription.line'].sudo().create({
                    'product_id': wo_line.product_id.id,
                    'analytic_account_id': subs_data['id'],
                    'company_id': wo_line.company_id.id,
                    'name': wo_line.name,
                    'quantity': wo_line.qty_delivered,
                    'uom_id': wo_line.product_id.product_tmpl_id.uom_id.id,
                    'price_unit': wo_line.price_unit,
                    'price_subtotal': wo_line.price_unit * wo_line.qty_delivered,
                    'currency_id': wo_line.currency_id.id,
                    'x_order_id': wo_line.order_id.id
                })

    def create_subscriptions(self):
        """
        Create subscriptions based on the products' subscription template.

        Create subscriptions based on the templates found on order lines' products. Note that only
        lines not already linked to a subscription are processed; one subscription is created per
        distinct subscription template found.

        :rtype: list(integer)
        :return: ids of newly create subscriptions
        """
        res = []
        for order in self:
            to_create = order._bagi_sub_line()
            # create a subscription for each template with all the necessary lines
            for template in to_create:
                values = order._siapkan_subs_data(template)
                values['recurring_invoice_line_ids'] = to_create[template]._siapkan_subs_line_data()
                subscription = self.env['sale.subscription'].sudo().create(values)
                subscription.onchange_date_start()
                res.append(subscription.id)
                to_create[template].write({'subscription_id': subscription.id})
                subscription.message_post_with_view(
                    'mail.message_origin_link', values={'self': subscription, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id, author_id=self.env.user.partner_id.id
                )
                self.env['sale.subscription.log'].sudo().create({
                    'subscription_id': subscription.id,
                    'event_date': fields.Date.context_today(self),
                    'event_type': '0_creation',
                    'amount_signed': subscription.recurring_monthly,
                    'recurring_monthly': subscription.recurring_monthly,
                    'currency_id': subscription.currency_id.id,
                    'category': subscription.stage_category,
                    'user_id': order.user_id.id,
                    'team_id': order.team_id.id,
                })
        return res

    def _bagi_sub_line(self):
        """Split the order line according to subscription templates that must be created."""
        self.ensure_one()
        res = dict()
        new_sub_lines = self.work_order_line.filtered(lambda
                                                          l: not l.subscription_id and l.product_id.subscription_template_id and l.product_id.recurring_invoice)
        templates = new_sub_lines.mapped('product_id').mapped('subscription_template_id')
        for template in templates:
            lines = self.work_order_line.filtered(
                lambda l: l.product_id.subscription_template_id == template and l.product_id.recurring_invoice)
            res[template] = lines
        return res


class WorkOrderLine(models.Model):
    _name = 'mc_kontrak.work_order_line'
    _inherit = 'sale.order.line'
    _description = 'Modul Work Order Line yang menginherit sale.order.line'

    # Relasi
    order_id = fields.Many2one('sale.order', required=True, Store=True, Index=True)
    product_id = fields.Many2one('product.product', readonly=True, store=True)
    invoice_lines = fields.Many2many('account.move.line', 'work_order_line_invoice_rel', 'order_line_id',
                                     'invoice_line_id', string='Invoice Lines', copy=False)
    work_order_id = fields.Many2one('mc_kontrak.work_order', readonly=True, store=True)
    sale_order_line_id = fields.Many2one('sale.order.line', store=True)

    # Field
    qty_delivered = fields.Integer(string='QTY Terpasang')
    x_start_date = fields.Datetime(string='Plan Start Date', store=True)
    x_end_date = fields.Datetime(string='Plan End Date', store=True)

    # x_start_date_real = fields.Date(string='Real Start Date', store=True)
    # x_end_date_real = fields.Date(string='Real End Date', store=True)

    def _siapkan_subs_line_data(self):
        """Prepare a dictionnary of values to add lines to a subscription."""
        values = list()
        for line in self:
            values.append((0, False, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.qty_delivered,
                'uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount if line.order_id.subscription_management != 'upsell' else False,
            }))
        return values

    # @api.model
    # def create(self, vals):
    #     print('Action Create dari WO Line')
    #     for row in self:
    #         self.env.cr.execute("""UPDATE mc_kontrak_work_order SET x_plan_start_date = '%s', x_plan_end_date = '%s'
    #                 WHERE id = %s """ % (vals['x_start_date'], vals['x_end_date'], row.work_order_id.id))
    #     res = super(WorkOrderLine, self).create(vals)
    #     return res

    def write(self, vals):
        print('Action Write dari WO Line')
        if 'x_start_date' in vals:
            for row in self:
                self.env.cr.execute("""UPDATE mc_kontrak_work_order SET x_plan_start_date = '%s', x_plan_end_date = '%s'
                        WHERE id = %s """ % (vals['x_start_date'], vals['x_end_date'], row.work_order_id.id))
        res = super(WorkOrderLine, self).write(vals)
        return res
