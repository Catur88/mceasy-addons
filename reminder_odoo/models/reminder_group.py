from odoo import api, fields, models

class reminder_dept(models.Model):
    _name = 'x_reminder.group'

    group_id = fields.Many2one('hr.department', string='Department')
    categ_line = fields.Many2many('x_reminder.category', string='Category')
    description = fields.Char(String='Description')
    domain_categ = fields.Char(String='List ID Reminder Category')

