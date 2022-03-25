{
    'name': 'Reminder',
    'summary': """This module will record All Reminder details""",
    'version': '1.1.0',
    'description': """This module will record All Reminder details""",
    'author': 'PT Laprint Jaya',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'category': 'Reminder',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [

        'views/views.xml',
        'views/reminder_category.xml',
        'security/reminder_security.xml',
        'security/ir.model.access.csv',
        'views/reminder_group.xml',
        'views/menu.xml',
        'data/email_template_for_flow.xml'


    ],
    'demo': [],
    'depends': ['base'],
    'license': 'LGPL-3',
    'application': True,
}