# -*- coding: utf-8 -*-
{
    'name': "mc_product",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'product', 'account'],

    # always loaded
    'data': [
        'views/properties_product.xml',
        # 'security/ir.model.access.csv',
        # 'views/views_so.xml',
        # 'views/report_sale_inherit.xml',
        # 'views/report_sale_inherit2.xml',
        # 'views/view_sale_inherit.xml',
        # 'views/view_purchase_req.xml',
        # 'views/view_account_invoice_inherit.xml',
        # 'views/report_invoice.xml',
        # 'views/view_global_status.xml',
        # 'views/view_precosting.xml',
        # 'views/view_approval_gm.xml',
        # 'views/view_config_bahan.xml',
        # 'views/view_config_bahan_digital.xml',
        # 'views/view_config_bentuk.xml',
        # 'views/view_config_diecut.xml',
        # 'views/view_config_feature.xml',
        # 'views/view_config_kategori.xml',
        # 'views/view_config_mesin.xml',
        # 'views/view_config_offering.xml',
        # 'views/view_config_other.xml',
        # 'views/view_config_plate_cost.xml',
        # 'views/view_config_product_type.xml',
        # 'views/view_config_profit_margin.xml',
        # 'views/view_config_tinta.xml',
        # 'views/view_config_waste_table.xml',
        # 'views/view_process_cost.xml',
        # 'views/view_precost_price_range.xml',
        # 'views/menu.xml',
        # 'views/wizard_pricing.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}