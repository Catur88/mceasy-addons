# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
from datetime import date
from odoo.tools import datetime
from dateutil.relativedelta import relativedelta
import json



class SalesOrder(models.Model):
    _inherit = 'sale.order'

    x_po_cust = fields.Char(string='PO Customer')
    is_block = fields.Selection([('no', 'Block'), ('yes', 'Open')], string="Customer Status", readonly=True)
    x_is_pkp = fields.Boolean(related='partner_id.x_pkp', readonly=True)
    x_sales_external = fields.Many2one(related='partner_id.user_id')
    x_status_so = fields.Selection([('open', 'Open'), ('close', 'Closed')], default='open', string="Status SO")
    x_order_line = fields.One2many('sale.order.line', 'order_id')
    x_duedatekirim_sol = fields.Datetime(related='x_order_line.x_duedate_kirim', readonly=True)
    x_glob_stat_so = fields.One2many('x.global.status.so', 'name')
    x_note = fields.Text('Keterangan:',
                         default="1. Harga yang tertera diatas SUDAH termasuk Ongkos kirim.\n"
                                 "2. Harga yang tertera diatas SUDAH termasuk Cutting.\n"
                                 "3. Harga yang tertera diatas berlaku 30 hari sejak tanggal penawaran ini diberikan. Apabila tersedia promo/discount maka harus mengikuti syarat dan ketentuan yang berlaku pada saat penawaran diberikan.\n"
                                 "4. Proses Payment dibayarkan lunas (100%). Label hanya akan dicetak masal jika 50% pembayaran sudah diterima Dan akan dikirimkan jika 50% sisa pembayaran diterima.\n"
                                 "5. Terdapat kemungkinan perbedaan warna antara hasil cetak dengan design pada layar komputer. Apabila terdapat warna khusus yang diinginkan maka disarankan untuk melakukan TRIAL. Untuk proses TRIAL akan dikenakan biaya sebesar Rp. 130.000/ 1x Trial per item. Proses proofing hanya akan dilakukan jika sudah turun PO dan 50% pembayaran sudah diterima.\n"
                                 "6. Toleransi Pengiriman sebesar 10%.\n"
                                 "7. FREE ONGKIR untuk area Surabaya dan Sidoarjo. Untuk area diluar itu maka biaya pengiriman ditanggung oleh customer.\n"
                                 "8. Sprint Indonesia tidak bertanggungjawab atas ketidakoptimalan kualitas gambar printing yang diakibatkan oleh kualitas file desain dari customer. Format file yang di rekomendasikan adalah .pdf, .ai, .psd dan PNG.\n"
                                 "9. Komplain terhadap quality dapat dilakukan maksimal 14 hari kerja sejak barang diterima oleh customer dan akan ditangani sesuai kebijakan yang berlaku ( silahkan menghubungi sales untuk info lebih lanjut).\n"
                                 "10. Komplain terhadap quantity dapat dilakukan maksimal 7 hari sejak barang diterima oleh customer dan akan ditangani sesuai kebijakan yang berlaku ( silahkan menghubungi sales untuk info lebih lanjut )"
                         )
    # tambahan toggle button purchase Uswa
    purchase_request_count = fields.Integer(string="Purchase", compute='_compute_purchase_request_count')
    x_status_pr = fields.Selection([('not yet', 'Not Yet'), ('done', 'Done')],
                                   string="Status PR",
                                   default="not yet",
                                   readonly=True,
                                   store=True)

    # INHERIT FUNGSI ACTION CONFIRM PADA SALE ORDER
    @api.multi
    def action_confirm_global_so(self):
        # FUNGSI CUSTOM AKBAR
        for order in self:
            # CUSTOM FUNGSI UPDATE STATUS PRODUK
            sale_order_line = order.order_line
            terms = []

            # Looping sale order line
            for row in sale_order_line:
                if 'DELIVERY' not in str(row.product_id.categ_id.sts_bhn_utama.name).upper():
                    x_product = row.product_id
                    id_so = order.id
                    cus_id = order.partner_id.id
                    id_sol = row.id
                    qty_order = row.product_uom_qty
                    qty_kirim = row.qty_delivered
                    qty_sisa = qty_order - qty_kirim
                    qty_sisa_convert = "{:,.0f}".format(qty_sisa).replace(",", ".")
                    duedate_kirim = row.x_duedate_kirim
                    today = (datetime.now())
                    date_today = today.strftime("%Y-%m-%d")
                    date_today2 = datetime.strptime(date_today, "%Y-%m-%d").date()
                    temp = order.create_date
                    # create_date_so = temp.strftime("%Y-%m-%d")
                    date_state_before = datetime.strptime(temp, "%Y-%m-%d %H:%M:%S").date()
                    leadtime = (date_today2 - date_state_before).days
                    status_confirm = "LT " + str(leadtime) + " HARI | TGL " + str(date_today) + " | QTY " + str(
                        qty_sisa_convert)
                    product_id = row.product_id.id
                    x_repeat = False
                    self.env.cr.execute("select x_new_product from sale_order_line "
                                        "where product_id = '" + str(product_id) + "'")
                    sql = self.env.cr.fetchone()
                    if sql:
                        x_repeat = sql[0]

                    res_user = self.env['res.users'].search([('id', '=', self._uid)])
                    row.env.cr.execute(
                        "INSERT INTO x_global_status_so(x_status_repeat, create_uid,create_date,write_uid,write_date, name, x_so_line, x_qty_order, x_duedate, x_status_confirm_1, x_product, x_selisih_qty, x_status_terakhir, x_customer_id) "
                        "VALUES ('" + str(x_repeat) + "','" + str(res_user.id) + "','" + str(
                            datetime.now() - relativedelta(hours=float(7))) + "','" + str(
                            res_user.id) + "','" + str(datetime.now() - relativedelta(hours=float(7))) + "','" + str(
                            id_so) + "','" + str(
                            id_sol) + "','" + str(qty_order) + "','" + str(duedate_kirim) + "','" + str(
                            status_confirm) + "', '" + str(x_product.id) + "', 0, 'Confirm SO', '" + str(cus_id) + "');")

    # Button Unlock untuk SO yang sudah locked
    @api.multi
    def unlock_so(self):
        return self.write({'state': 'sale'})

    # INHERIT FUNGSI ACTION CONFIRM PADA SALE ORDER
    @api.multi
    def action_confirm_custom(self):
        for order in self:
            if order.is_block == 'no':
                raise UserError(_("Tidak dapat confirm SO, Customer Status Block"))
            sale_order_line = order.order_line
            for row in sale_order_line:
                if row.x_sq.id:
                    if row.x_sq.x_state_renego != '6':
                        raise UserError(_("Tidak dapat confirm SO, " + row.x_sq.name + " masih belum Approve"))
                if "NEW ITEM" in row.product_id.name.upper():
                    raise UserError(_("Tidak dapat confirm SO, ada product yg masih NEW / Belum ada master product"))

    # INHERITE FUNCTION BUTTON CONFIRM SALE ORDER
    @api.multi
    def action_confirm(self):
        self.action_confirm_custom()
        self.action_confirm_global_so()

        res = super(SalesOrder, self).action_confirm()
        return res

    # Uswa -Action klik Toggle purchase request
    @api.multi
    def action_view_purchase(self):
        action = self.env.ref('purchase_request.purchase_request_form_action').read()[0]
        action['domain'] = [('x_no_so', '=', self.id)]
        action['context'] = {}
        return action

    # Uswa -Purchase request count
    @api.multi
    def _compute_purchase_request_count(self):
        for o in self:
            purchase_request_obj = self.env['purchase.request'].search([('x_no_so', '=', o.id)])
            if purchase_request_obj:

                log_purchase_data = purchase_request_obj.sudo().read_group([('x_no_so', 'in', self.ids)],
                                                                           ['x_no_so'],
                                                                           ['x_no_so'])
                result = dict(
                    (data['x_no_so'][0], data['x_no_so_count']) for data in log_purchase_data)
                for purchase in self:
                    purchase.purchase_request_count = result.get(purchase.id, 0)

    # @api.one
    # def _compute_status_pr(self):
    #     for row in self:
    #         if row.purchase_request_count > 0:
    #             row.x_status_pr = 'done'
    #             # row.write({'x_status_pr': 'done'})


class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    # product_id = fields.Many2one('product.product', readonly=True)
    order_id = fields.Many2one('sale.order', required=True, Store=True, Index=True)
    x_bentuk = fields.Many2one('x.config.bentuk', string="Bentuk")
    x_panjang = fields.Float(string="Panjang")
    x_lebar = fields.Float(string="Lebar")
    x_bahan = fields.Many2one('x.config.material', string="Bahan")
    x_finishing1 = fields.Many2one('x.config_finishing', string="Finishing 1")
    x_finishing2 = fields.Many2one('x.config_finishing', string="Finishing 2")
    x_diecut = fields.Many2one('x.config_diecut', string="Diecut")
    # x_duedate_kirim = fields.Datetime(string='Duedate kirim', required=True)
    x_duedate_kirim = fields.Datetime(string='Duedate kirim')
    x_new_product = fields.Boolean('New', default=False, store=True)
    # x_internal_categ = fields.Many2one('product.category', string="Internal Category",
    #                                    domain="[('sts_bhn_utama.name', 'in', ['product', 'Product', 'PRODUCT'])]",
    #                                    required=True)
    x_internal_categ = fields.Many2one('product.category', string="Internal Category", domain="[('sts_bhn_utama.name', 'in', "
                                                                                              "['product', 'Product', 'PRODUCT','Delivery','DELIVERY','Service','SERVICE'])]")
    # x_internal_categ = fields.Many2one('product.category', string="Internal Category",
    #                                        domain="[('sts_bhn_utama.name', 'in', ['product', 'Product', 'PRODUCT','Delivery','DELIVERY','Service','SERVICE'])]")
    is_new_item = fields.Boolean()
    # x_sq = fields.Many2one('x.sales.quotation', string="SQ", required=True)
    x_sq = fields.Many2one('x.sales.quotation', string="SQ")
    x_customer_requirement = fields.Char(string="No SQ", related="x_sq.name", store=True)
    x_flag = fields.Boolean(related='x_sq.x_flag_quo')
    x_feature = fields.Char('Feature')
    # x_feature = fields.Many2many('x.feature.cost.precost', string="Feature", required=True)
    # x_description_name = fields.Text('Description', required=True)

    # x_quantity = fields.Float(string="Quantity")
    # x_harga_satuan = fields.Float(string="Harga Satuan")
    # x_harga_total = fields.Float(string="Harga Total")

    x_quo_purchase_m2 = fields.Float(
        'Purchase Price / m2', readonly=True)
    x_quo_purchase_price_pcs = fields.Float(
        'Purchase Price / PCS', readonly=True)

    # @api.onchange('x_new_product')
    # def is_new_order(self):
    #     for row in self:
    #         if row.product_id.name in "NEW":
    #             row.x_new_product = True

    @api.model
    def create(self, vals):
        result = super(SalesOrderLine, self).create(vals)
        if str(result.product_tmpl_id.categ_id.sts_bhn_utama.name).upper() == "PRODUCT":


        # result['x_customer_requirement'] = result.x_sq.name
            result['x_flag'] = True
            result.x_panjang = result.x_sq.x_width
            result.x_lebar = result.x_sq.x_length
            result.price_unit = result.x_sq.x_harga_renego
            result.price_subtotal = result.x_sq.x_renego_total
            result.product_uom_qty = result.x_sq.x_qty
            result.product_uom = self.env['product.uom'].search([('name', 'in', ['pcs', 'PCS', 'Pcs'])]).id
            result.x_quo_purchase_m2 = result.x_sq.x_quo_purchase_m2
            result.x_quo_purchase_price_pcs = result.x_sq.x_quo_purchase_price_pcs
        return result

    @api.multi
    def write(self, vals):

        if str(self.product_tmpl_id.categ_id.sts_bhn_utama.name).upper() == "PRODUCT":
            if self.x_sq.x_flag_quo == True:
                self.x_sq.x_flag_quo = False

            if self.state != 'done':
                vals['x_flag'] = True
                vals['x_panjang'] = self.x_sq.x_width
                vals['x_lebar'] = self.x_sq.x_length
                vals['price_unit'] = self.x_sq.x_harga_renego
                vals['price_subtotal'] = self.x_sq.x_renego_total
                vals['product_uom_qty'] = self.x_sq.x_qty
                vals['product_uom'] = self.env['product.uom'].search([('name', 'in', ['pcs', 'PCS', 'Pcs'])]).id
                vals['x_quo_purchase_m2'] = self.x_sq.x_quo_purchase_m2
                vals['x_quo_purchase_price_pcs'] = self.x_sq.x_quo_purchase_price_pcs

        result = super(SalesOrderLine, self).write(vals)
        return result



    @api.multi
    def unlink(self):
        self.env['x.sales.quotation'].search([('id', '=', self.x_sq.id)]).write({'x_flag_quo': False})
        result = super(SalesOrderLine, self).unlink()
        return result

    @api.onchange('product_id')
    def _is_new_item(self):
        for row in self:
            if "NEW ITEM" in str(row.product_id.name).upper():
                row.is_new_item = True
            row.x_duedate_kirim = date.today()

    # @api.multi
    # def btn_create_product(self):
    #     # prod = self.product_id #self.x_sq.x_ids_feature
    #     prod = self.env['product.product'].search
    #     sq = self.x_sq.x_ids_feature
    #     offer = self.x_sq.x_offering_digital
    #     offer2 = self.x_sq.x_offering_digital.x_offering_cost_precost.id
    #     # for a in self:
    #     #     a.env.cr.execute(
    #     #         "INSERT INTO product_template_x_feature_cost_precost_rel"
    #     #         "(product_template_id, x_feature_cost_precost_id) "
    #     #         "VALUES ('13265','12');")
    #     # product = self.product_template.id
    #     print "ID Product", prod
    #     print "ID FItur ", sq
    #     print "ID Offer", offer2


    @api.multi
    def btn_create_product(self):
        # raise UserError(_("Tes tombol"))
        pt = self.env['product.template']

        result = pt.create({
            'name': self.name,
            'categ_id': self.x_internal_categ.id,
            'x_customer': self.order_id.partner_id.id,
            'x_length': self.x_panjang,
            'x_width': self.x_lebar,
            'x_material': self.x_bahan.id,
            'x_bentuk': self.x_bentuk.id,
            'x_diecut': self.x_diecut.id,
            'x_finishing': self.x_finishing1.id,
            'x_finishing_2': self.x_finishing2.id,
            'list_price': self.price_unit,
            'sale_ok': True,
            'purchase_ok': False,
            'type': 'product',
            'tracking': 'none',
            'route_ids': [(6, 0, [5])],
            'x_offering': self.x_sq.x_offering_digital.id,
            'x_bahan': self.x_sq.x_material_type_id2.id,
            'x_satuan' : self.x_sq.x_satuan



            # 'x_feature': self.x_sq.x_ids_feature
            #     self.env.cr.execute("select * from x_feature_cost_precost_x_sales_quotation_rel"
            #                                              "where x_feature_cost_precost_id = " + str(self.x_sq.x_ids_feature))
        })
        id_pt = result.id
        fitur = self.x_sq.x_ids_feature
        print id_pt
        print fitur
        for a in fitur:
            id = int(a)
            a.env.cr.execute(
                    "INSERT INTO product_template_x_feature_cost_precost_rel"
                    "(product_template_id, x_feature_cost_precost_id) "
                    "VALUES ('" + str(id_pt) + "','"+str(id)+"');")
            # a.env.cr.execute(
            #     "INSERT INTO product_template_x_feature_cost_precost_rel"
            #     "(product_template_id, x_feature_cost_precost_id) "
            #     "VALUES ('150','1')"
            # )
        ppid = self.env['product.product'].search([('product_tmpl_id', '=', id_pt)])
        self.product_id = ppid.id

        sq_pt = self.env['x.sales.quotation'].search([('name','=', self.x_sq.name)])
        sq_pt.write({'x_product': ppid.id })

        # self.x_sq.x_product.id = ppid.id

    # self.x_new_product = False


    @api.onchange('x_sq')
    def isi_product(self):
        for row in self:
            row.product_id = row.x_sq.x_product
            row.x_customer_requirement = row.x_sq.name
            row.x_quo_purchase_m2 = row.x_sq.x_quo_purchase_m2
            row.x_quo_purchase_price_pcs = row.x_sq.x_quo_purchase_price_pcs


            if 'NEW ITEM' in str(row.product_id.name).upper():
                # row.name = row.x_sq.item_description
                row.name = row.x_sq.item_description
            else:
                row.name = row.product_id.display_name
                # row.name = row.product_id.product_tmpl_id.name
            # row.x_description_name = row.x_sq.item_description
            id_prod_template = row.product_id.product_tmpl_id.id
            product_name = row.product_id.product_tmpl_id.name
            data_product = row.env['product.product'].search([('product_tmpl_id', '=', id_prod_template)])
            if data_product:
                row.x_bentuk = data_product['x_bentuk'].id
                row.x_panjang = data_product['x_width']
                row.x_lebar = data_product['x_length']
                row.x_bahan = data_product['x_material'].id
                row.x_finishing1 = data_product['x_finishing'].id
                row.x_finishing2 = data_product['x_finishing_2'].id
                row.x_diecut = data_product['x_diecut'].id
                row.x_internal_categ = data_product['categ_id'].id
                row.x_duedate_kirim = date.today()
                if 'NEW ITEM' in str(product_name).upper():
                    row.x_new_product = True
                    row.is_new_item = True

                # Menyamakan name config bentuk di master product dengan name config bentuk di SQ
                config_bentuk = row.env['x.config.bentuk'].search(
                    [('name', '=ilike', row.x_sq.x_bentuk_prod.name)])
                if config_bentuk:
                    row.x_bentuk = config_bentuk

                # Menyamakan name config bahan di master product dengan name config bahan di SQ
                config_bahan = row.env['x.config.material'].search(
                    [('name', '=ilike', row.x_sq.x_material_type_id2.name)])
                if config_bahan:
                    row.x_bahan = config_bahan

                # Menyamakan name config bahan di master product dengan name config bahan di SQ
                config_diecut = row.env['x.config_diecut'].search(
                    [('name', 'ilike', row.x_sq.x_offering_digital.name)])
                if config_diecut:
                    row.x_diecut = config_diecut

                # Menyamakan name config internal category di master product dengan name config product type di SQ

                config_product_type = row.env['product.category'].search(
                    [('name', '=ilike', row.x_sq.x_product_type_precost.name)])

                if config_product_type:
                    row.x_internal_categ = config_product_type
                # row.x_bentuk = data_product['x_bentuk'].id
                row.x_panjang = row.x_sq.x_width
                row.x_lebar = row.x_sq.x_length
                # row.x_bahan = data_product['x_material'].id
                # row.x_finishing1 = data_product['x_finishing'].id
                # row.x_finishing2 = data_product['x_finishing_2'].id
                # row.x_diecut = data_product['x_diecut'].id
                # row.x_internal_categ = data_product['categ_id'].id
                row.x_duedate_kirim = row.x_sq.x_req_dk

                # mengambil data feature dari sq dan diinputkan ke field feature so line
                finishing = row.x_sq.x_ids_feature
                temp = ""
                temp2 = ""
                for fin in finishing:
                    temp1 = fin.name
                    if 'NONE' not in str(temp1).upper():
                        temp = ''.join([temp, ', ', str(temp1)])
                    else:
                        temp2 = ''.join([temp, ', ', str(temp1)])
                if temp != "":
                    row.x_feature = temp[2:]
                else:
                    row.x_feature = temp2[2:]

            if 'NEW ITEM' in str(product_name).upper():
                row.x_new_product = True
                row.is_new_item = True
            else:
                row.x_new_product = False
                row.is_new_item = False


    # @api.onchange('product_id')
    # def isi_product2(self):
    #     p = int(self.product_id.product_tmpl_id)
    #     n = self.product_id.product_tmpl_id.display_name
    #     # c = self.product_id.categ_id.name
    #     self.name = self.product_id.product_tmpl_id.display_name
    #     # self.x_internal_categ = self.product_id.categ_id.name
    #     # self.x_internal_categ = self.product_id.product_tmpl_id.type
    #     print p
    #     print n
        # print c

class GlobalStatusSO(models.Model):
    _name = 'x.global.status.so'

    # name = fields.Char('Name')
    name = fields.Many2one('sale.order', string='SO', ondelete='cascade', readonly=True)
    x_so_line = fields.Many2one('sale.order.line', string='SO Item', ondelete='cascade', readonly=True)
    x_qty_order = fields.Float(string='Qty Order', readonly=True)
    x_duedate = fields.Datetime(string='Duedate', readonly=True)
    x_status_confirm_1 = fields.Char(string='State SO Confirm', readonly=True)
    x_status_unlock_2 = fields.Char(string='State Unlock Item', readonly=True)
    x_status_planned_3 = fields.Char(string='State OK Planned', readonly=True)
    x_status_material_4 = fields.Char(string='State Material Ready', readonly=True)
    x_status_cetak_5 = fields.Char(string='State OK Cetak', readonly=True)
    x_status_cetak_5_2 = fields.Char(string='State OK Cetak 2', compute='split_string', readonly=True)
    x_status_finishing_6 = fields.Char(string='State OK Finishing', readonly=True)
    x_status_finishing_6_2 = fields.Char(string='State OK Finishing 2', compute='split_string', readonly=True)
    x_status_packing_7 = fields.Char(string='State OK Packing', readonly=True)
    x_status_packing_7_2 = fields.Char(string='State OK Packing 2', compute='split_string', readonly=True)
    x_status_partial_8 = fields.Char(string='State SJK Partial', readonly=True)
    x_status_full_9 = fields.Char(string='State SJK Full', readonly=True)
    x_status_pengiriman_10 = fields.Char(string='State SJK Pengiriman', readonly=True)
    # x_ok = fields.Many2one('mrp.production', string='Nomor OK', ondelete='cascade', readonly=True)
    x_ok = fields.Char(string='Nomor OK', ondelete='cascade', readonly=True)
    x_product = fields.Many2one('product.product', string='Product Name', readonly=True)
    x_status_duedate = fields.Integer('Status Duedate', compute='split_string', readonly=True)
    x_status_duedate_done = fields.Char('Status Duedate Done', compute='status_duedate_done', readonly=True)
    x_total_leadtime = fields.Integer('Total Leadtime', compute='status_duedate_done', readonly=True)
    x_status_duedate_done_save = fields.Char('Status Duedate Done', readonly=True)
    x_total_leadtime_save = fields.Integer('Total Leadtime', readonly=True)
    x_selisih_qty = fields.Float('Selisiih Qty', readonly=True)
    x_customer_id = fields.Many2one('res.partner', string='Customer', related='name.partner_id', store=True)
    x_sjk = fields.Many2one('stock.picking', string='Nomor SJK', ondelete='cascade', readonly=True)
    x_status_terakhir = fields.Char(string='Status Terakhir', ondelete='cascade', readonly=True)
    x_status_repeat = fields.Boolean(string='Status Repeat', ondelete='cascade', readonly=True)


    @api.one
    def split_string(self):
        if self.x_status_cetak_5:
                    self.x_status_cetak_5_2 = self.x_status_cetak_5[0:5]
        if self.x_status_finishing_6:
                    self.x_status_finishing_6_2 = self.x_status_finishing_6[0:5]
        if self.x_status_packing_7:
                    self.x_status_packing_7_2 = self.x_status_packing_7[0:5]
        duedate = datetime.strptime(self.x_duedate, "%Y-%m-%d %H:%M:%S")
        selisih_duedate = (duedate - datetime.now()).days
        self.x_status_duedate = selisih_duedate

    @api.one
    def status_duedate_done(self):
        for row in self:
            if row.x_status_pengiriman_10:
                duedate = datetime.strptime(row.x_duedate, "%Y-%m-%d %H:%M:%S").date()
                state_tgl_done_pengiriman = row.x_status_pengiriman_10
                list_tgl_done_pengiriman = state_tgl_done_pengiriman.split(" | ")
                temp = list_tgl_done_pengiriman[1].split()
                tgl_done_pengiriman = datetime.strptime(str(temp[1]), "%Y-%m-%d").date()
                leadtime = (duedate - tgl_done_pengiriman).days
                temp_2 = str(row.name.confirmation_date)
                # x_confirm_so = temp_2.strftime("%Y-%m-%d")
                date_confirm_so = datetime.strptime(temp_2, "%Y-%m-%d %H:%M:%S").date()
                total_leadtime = (tgl_done_pengiriman - date_confirm_so).days
                row.x_total_leadtime = total_leadtime
                if leadtime >= 0:
                    row.x_status_duedate_done = 'DONE ON TIME'
                else:
                    row.x_status_duedate_done = 'DONE LATE'
            else:
                row.x_total_leadtime = None



    @api.model
    def open_url(self):
        requests.get("http://182.253.112.110:5758/odoo_api/")
        # requests.get("http://localhost/odoo_api")


    @api.model
    def update_global_status(self, vals):
        for row in vals:
            id_po = row['x_source_po']
            id_prod = row['x_prod_code']
            status_terakhir = row['x_status_terakhir']
            if status_terakhir == 'Confirm SO':
                status_terakhir = status_terakhir + ' LPJ'

            po_line = self.env['purchase.order.line'].search([('order_id.name', '=', id_po), ('product_id.default_code', '=', id_prod)])
            if po_line:
                for line_obj in po_line:
                    globalso_obj = self.env['x.global.status.so'].search([('x_product', '=', line_obj.product_id.id), ('name', '=', line_obj.x_no_so.id), ('x_status_terakhir', '!=', 'SJK Done')])
                    if globalso_obj:
                        globalso_obj.write({'x_status_terakhir': status_terakhir})
                        globalso_obj.write({'x_qty_order': row['x_qty_order']})
                        globalso_obj.write({'x_status_unlock_2': row['x_status_unlock_2']})
                        globalso_obj.write({'x_status_planned_3': row['x_status_planned_3']})
                        globalso_obj.write({'x_status_material_4': row['x_status_material_4']})
                        globalso_obj.write({'x_status_cetak_5': row['x_status_cetak_5']})
                        globalso_obj.write({'x_status_finishing_6': row['x_status_finishing_6']})
                        globalso_obj.write({'x_status_packing_7': row['x_status_packing_7']})
                        globalso_obj.write({'x_status_partial_8': row['x_status_partial_8']})
                        globalso_obj.write({'x_status_full_9': row['x_status_full_9']})
                        globalso_obj.write({'x_status_pengiriman_10': row['x_status_pengiriman_10']})

                    # else:
                    #     line_obj.env.cr.execute("INSERT INTO x_global_status_so( x_status_repeat, create_uid, create_date, write_uid, write_date, name, x_so_line,"
                    #                             "x_qty_order, x_duedate, x_status_confirm_1, x_product, x_selisih_qty, x_status_terakhir,x_customer_id, x_source_po, "
                    #                             "x_prod_code,x_status_unlock_2, x_status_planned_3, x_status_material_4, x_status_cetak_5,x_status_finishing_6, "
                    #                             "x_status_packing_7, x_status_partial_8, x_status_full_9,x_status_pengiriman_10 ),"
                    #                             "SELECT x_status_repeat, create_uid, create_date, write_uid, write_date, name, x_so_line,"
                    #                             "'" +str(row['x_qty_order']+ "', x_duedate, x_status_confirm_1, x_product, x_selisih_qty, "
                    #                             "x_status_terakhir, x_customer_id, x_source_po, x_prod_code,'" +str(row['x_status_unlock_2'])+ "','" +str(row['x_status_planned_3'])+
                    #                             "','" +str(row['x_status_material_4'])+ "','" +str(row['x_status_cetak_5'])+ "','" +str(row['x_status_finishing_6'])+ "','"
                    #                             +str(row['x_status_packing_7'])+ "','" +str(row['x_status_partial_8'])+ "','" + str(row['x_status_full_9'])+ "','"
                    #                             +str(row['x_status_pengiriman_10'])+ "' FROM x_global_status_so WHERE x_product ='" +str(line_obj.product_id.id))+ "', and name ='"
                    #                             +str(line_obj.x_no_so.id)+ "'limit  1'")

        return True