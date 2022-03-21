from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ConfigBahan(models.Model):
    _name = 'x.config.bahan'

    name = fields.Char('Nama Bahan', store=True)
    x_bahan = fields.Many2one('product.template', 'Material Type',
                              domain=[('categ_id.sts_bhn_utama.name', '=', 'Bahan Utama')])
    # x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    # x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    # x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')

    x_kategori = fields.One2many(
        'x.harga.kategori.bahan', 'x_bahan_id', string='Harga Kategori')
    x_bahan_digital = fields.Many2one(
        'x.config.bahan.digital', 'Bahan Digital')
    x_ids_type = fields.Many2many('x.product.type.precost', 'bahan_product_type_rel',
                                  'bahan_id', 'product_type_id', string="Product Type", required=True)

    # akbar tambah 19/05/21
    x_active = fields.Boolean('Active', default=True)
    x_tgl_update = fields.Date('Tgl Update Terakhir')
    # @api.depends("x_bahan")
    # def cek_name(self):
    #     if self.x_bahan:
    #         self.env.cr.execute(
    #                     "select name from product_template where id = "+ str(self.x_bahan.id))
    #         sql = self.env.cr.fetchone()
    #         self.name = sql[0]

#
# class ConfigFinishing(models.Model):
#     _name = 'x.config.finishing'
#
#     name = fields.Char('Jenis Finishing')
#     x_harga_m2 = fields.Float(string = 'Harga m2')

# class ConfigDiecut(models.Model):
#     _name = 'x.config.diecut'
#
#     name = fields.Many2one('product.template', 'PL&DC',
#                                          domain=[('categ_id.sts_bhn_utama.name', '=', 'PL&DC')])
#     x_harga_m2 = fields.Float(string = 'Harga m2')


class ConfigBahanDigital(models.Model):
    _name = 'x.config.bahan.digital'

    name = fields.Char('Nama Bahan')
    x_kategori = fields.One2many(
        'x.harga.kategori.bahan.digital', 'x_bahan_id', string='Harga Kategori')
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class ConfigTinta(models.Model):
    _name = 'x.config.tinta'
    name = fields.Char('Number of Color')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many(
        'x.harga.kategori.tinta', 'x_tinta_id', string='Harga Kategori')
    x_ids_type = fields.Many2many('x.product.type.precost', 'tinta_product_type_rel', 'tinta_id', 'product_type_id',
                                  string="Product Type", required=True)
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class ConfigMesin(models.Model):
    _name = 'x.config.mesin'

    name = fields.Char('Jenis Mesin')
    x_harga_m2 = fields.Float(string='Harga m2')

# ---------------------------------------------------------------------------------------


class ProductType(models.Model):
    _name = 'x.product.type.precost'

    # name =  fields.Selection([('stc_label', 'Sticker Label'), ('inmold', 'In-Mold Label'), ('shrink', 'Shrink Label'),
    #                           ('carton', 'Carton Packaging'), ('flexible', 'Flexible Packaging'), ('blank_shrink', 'Blank Shrink Label'),
    #                           ('blank_stc', 'Blank Sticker Label')],
    #                                         default='stc_label', string='Product Type',
    #                                         track_visibility='onchange', required=True)
    name = fields.Char(string='Product Type', compute='cek_name', store=True)
    x_categ = fields.Many2one('product.category', 'Product Category',
                              domain=[('parent_id.name', '=', 'PRD')])
    x_moq = fields.Float(string='MOQ m2')
    x_ids_proces_cost = fields.Many2many(
        'x.process.cost.precost', string="Process Cost")
    x_profit_margin = fields.One2many(
        'x.profit.margin.product.type', 'x_product_type_id', string='Profit Margin')
    x_ids_bahan = fields.Many2many('x.config.bahan', 'bahan_product_type_rel', 'product_type_id', 'bahan_id',
                                   string="Bahan")  # , required=True)
    x_ids_tinta = fields.Many2many('x.config.tinta', 'tinta_product_type_rel', 'product_type_id', 'tinta_id',
                                   string="Tinta")  # , required=True)
    x_waste = fields.One2many('x.waste.table.precost',
                              'x_product_type_id', string='Waste')
    x_tgl_update = fields.Date('Tgl Update Terakhir')

    @api.depends("x_categ")
    def cek_name(self):
        if self.x_categ:
            self.env.cr.execute(
                "select name from product_category where id = " + str(self.x_categ.id))
            sql = self.env.cr.fetchone()
            self.name = sql[0]


class ProcessCost(models.Model):
    _name = 'x.process.cost.precost'

    name = fields.Char('Process List')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many(
        'x.harga.kategori.proses', 'x_proses_id', string='Harga Kategori')
    x_tgl_update = fields.Date('Tgl Update Terakhir')

# class InkCost(models.Model):
#     _name = 'x.ink.cost.precost'
#
#     name = fields.Char('Number of Color')
#     x_kategori_1 = fields.Float(string = 'Kategori I (200-999)m2')
#     x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
#     x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')


class FeatureCost(models.Model):
    _name = 'x.feature.cost.precost'

    name = fields.Char('Feature List')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many(
        'x.harga.kategori.feature', 'x_feature_id', string='Harga Kategori')
    x_kategori_digital = fields.One2many(
        'x.harga.kategori.feature.digital', 'x_feature_digital_id', string='Harga Kategori Digital')
    x_moq_digital = fields.Float(string='MOQ digital m2', default=0)
    x_deskripsi = fields.Text(string='Deskripsi')
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class OfferingCost(models.Model):
    _name = 'x.offering.cost.precost'

    name = fields.Char('Offering List')
    x_kategori_digital = fields.One2many(
        'x.harga.kategori.offering.digital', 'x_offering_id', string='Harga Kategori Digital')


class PlateCost(models.Model):
    _name = 'x.plate.cost.precost'

    name = fields.Char('Number of Plate')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many(
        'x.harga.kategori.plate', 'x_plate_id', string='Harga Kategori')
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class DiecutCost(models.Model):
    _name = 'x.diecut.cost.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Many2one('x.product.type.precost', string='Product Type')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many(
        'x.harga.kategori.diecut', 'x_diecut_id', string='Harga Kategori')
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class WasteTable(models.Model):
    _name = 'x.waste.table.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('Product Area m2')
    x_batas_atas = fields.Float(store=True, digits=(
        16, 5), string='Batas Atas m2/pcs')
    x_batas_bawah = fields.Float(store=True, digits=(
        16, 5), string='Batas Bawah m2/pcs')
    x_waste_config = fields.Char('Waste Config %')
    x_kategori_1 = fields.Float(string='Kategori I (200-999)m2')
    x_kategori_2 = fields.Float(string='Kategori II (1000-2499)m2')
    x_kategori_3 = fields.Float(string='Kategori III (>2500)m2')
    x_kategori = fields.One2many(
        'x.harga.kategori.waste', 'x_waste_id', string='Harga Kategori')
    x_product_type_id = fields.Many2one(
        'x.product.type.precost', string='Product Type')
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class ProfitMargin(models.Model):
    _name = 'x.profit.margin.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('PM List')
    x_percentage = fields.Float(string='Percentage (%)')
    x_config_product_type = fields.One2many(
        'x.profit.margin.product.type', 'x_profit_margin_id')


class HistoryPrecosting(models.Model):
    _name = 'x.history.precosting'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('SQ')
    x_id_sq = fields.Many2one('x.sales.quotation', string='No SQ')
    x_length = fields.Float(string='Length (mm)')
    x_width = fields.Float(string='Width (mm)')
    x_length_m = fields.Float(string='Length (m)')
    x_width_m = fields.Float(string='Width (m)')
    x_quantity = fields.Float(string='Quantity')
    x_area_m2_pcs = fields.Float(string='m2/pcs')
    x_area_m2_tot = fields.Float(string='m2')
    x_waste_produksi = fields.Float(string='Waste Produksi (%)')
    x_waste_config = fields.Float(string='Waste Config (%)')
    x_total_waste_m2 = fields.Float(string='Total Waste m2')
    x_category = fields.Integer(string='Category')


# class qty_roundup(models.Model):
#     _name = 'x.qty.roundup'
#     name = fields.Char(String='Qty Roundup')


class ConfigKategori(models.Model):
    _name = 'x.config.kategori.precost'

    # name = fields.Many2one('x.product.type.precost')
    name = fields.Char('Kategori')
    x_nomor = fields.Integer('Level')
    x_batas_atas = fields.Float(
        store=True, digits=(16, 2), string='Batas Atas (m2)')
    x_batas_bawah = fields.Float(
        store=True, digits=(16, 2), string='Batas Bawah (m2)')
    x_config_bahan = fields.One2many('x.harga.kategori.bahan', 'x_kategori_id')
    x_config_bahan_digital = fields.One2many(
        'x.harga.kategori.bahan.digital', 'x_kategori_id')
    x_config_tinta = fields.One2many('x.harga.kategori.tinta', 'x_kategori_id')
    x_config_proses = fields.One2many(
        'x.harga.kategori.proses', 'x_kategori_id')
    x_config_feature = fields.One2many(
        'x.harga.kategori.feature', 'x_kategori_id')
    x_config_feature_digital = fields.One2many(
        'x.harga.kategori.feature.digital', 'x_kategori_id')
    x_config_plate = fields.One2many('x.harga.kategori.plate', 'x_kategori_id')
    x_config_diecut = fields.One2many(
        'x.harga.kategori.diecut', 'x_kategori_id')
    x_config_waste = fields.One2many('x.harga.kategori.waste', 'x_kategori_id')
    x_config_offering_digital = fields.One2many(
        'x.harga.kategori.offering.digital', 'x_kategori_id')
    x_manufacturing_type = fields.Selection([('laprint', 'Laprint'), ('digital', 'Digital')],
                                            default='laprint', string='Manufacturing Type',
                                            track_visibility='always', required=True)

    # @api.depends("name")
    # def check_konversi(self):
    #     if self.name:
    #         [
    #             int(s) for s in self.name.split()
    #             if s.isdigit()
    #         ]
    #         self.x_nomor = s


class ConfigHargaBahan(models.Model):
    _name = 'x.harga.kategori.bahan'

    # name = fields.Float(string = 'Name', related='x_harga', store=True)
    x_bahan_id = fields.Many2one('x.config.bahan', string='Nama Bahan')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigHargaBahanDigital(models.Model):
    _name = 'x.harga.kategori.bahan.digital'

    # name = fields.Float(string = 'Name', related='x_harga', store=True)
    x_bahan_id = fields.Many2one(
        'x.config.bahan.digital', string='Nama Bahan Digital')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga Jual(Rp)')
    x_harga_beli = fields.Float(string='Harga Beli (Rp)')


class ConfigHargaTinta(models.Model):
    _name = 'x.harga.kategori.tinta'

    # name = fields.Many2one('x.product.type.precost')
    x_tinta_id = fields.Many2one('x.config.tinta', string='Nama Tinta')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigHargaProses(models.Model):
    _name = 'x.harga.kategori.proses'

    # name = fields.Many2one('x.product.type.precost')
    x_proses_id = fields.Many2one(
        'x.process.cost.precost', string='Nama Proses')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigHargaFeature(models.Model):
    _name = 'x.harga.kategori.feature'

    # @api.model
    # def _default_feature_id(self):
    #     if self._context.get('active_model') == 'x.feature.cost.precost':
    #         return self._context.get('active_id')
    #     else:
    #         id = self._context.get('parent_id')
    #         return id
    #     return False

    x_feature_id = fields.Many2one(
        'x.feature.cost.precost', string='Nama Feature')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigHargaFeatureDigital(models.Model):
    _name = 'x.harga.kategori.feature.digital'

    # @api.model
    # def _default_feature_id(self):
    #     if self._context.get('active_model') == 'x.feature.cost.precost':
    #         return self._context.get('active_id')
    #     else:
    #         id = self._context.get('parent_id')
    #         return id
    #     return False

    x_feature_digital_id = fields.Many2one(
        'x.feature.cost.precost', string='Nama Feature')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga Jual (Rp)')
    x_harga_beli = fields.Float(string='Harga Beli (Rp)')


class ConfigHargaOfferingDigital(models.Model):
    _name = 'x.harga.kategori.offering.digital'

    x_offering_id = fields.Many2one(
        'x.offering.cost.precost', string='Offering')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga Jual (Rp)')
    x_harga_beli = fields.Float(string='Harga Beli (Rp)')


class ConfigHargaPlate(models.Model):
    _name = 'x.harga.kategori.plate'

    # name = fields.Many2one('x.product.type.precost')
    x_plate_id = fields.Many2one('x.plate.cost.precost', string='Nama Plate')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigHargaDiecut(models.Model):
    _name = 'x.harga.kategori.diecut'

    # name = fields.Many2one('x.product.type.precost')
    x_diecut_id = fields.Many2one(
        'x.diecut.cost.precost', string='Nama Diecut')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigHargaWaste(models.Model):
    _name = 'x.harga.kategori.waste'

    # name = fields.Many2one('x.product.type.precost')
    x_waste_id = fields.Many2one('x.waste.table.precost', string='Nama Waste')
    x_kategori_id = fields.Many2one(
        'x.config.kategori.precost', string='Kategori')
    x_harga = fields.Float(string='Harga (Rp)')


class ConfigProfitMargin(models.Model):
    _name = 'x.profit.margin.product.type'

    # name = fields.Many2one('x.product.type.precost')
    x_product_type_id = fields.Many2one(
        'x.product.type.precost', string='Product Type')
    x_profit_margin_id = fields.Many2one(
        'x.profit.margin.precost', string='Profit Margin')
    x_percentage = fields.Float(string='Percentage (%)')


class OtherPrecost(models.Model):
    _name = 'x.other.precost'

    name = fields.Char('Name')
    x_percentage = fields.Float(string='Percentage (%)')
    x_tgl_update = fields.Date('Tgl Update Terakhir')


class ConfigBentuk(models.Model):
    _name = 'x.config.bentuk2'

    name = fields.Char('Name')
