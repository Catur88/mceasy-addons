# -*- coding: utf-8 -*-
{
    'name': "mc_kontrak",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_subscription', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/kontrak_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence_data.xml',
        'views/sales_order_custom.xml',
        'views/sale_subscription_custom.xml',
        'views/work_order_view.xml',
        'views/churn_order_view.xml',
        'report/kontrak_report.xml',
        'report/kontrak_template.xml',
        'report/penawaran_template.xml',
        'report/wo_report.xml',
        'report/wo_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3'
}
