from odoo import api, fields, models


class reminder_category(models.Model):
    _name = 'x_reminder.category'

    name = fields.Char(string="Reminder Name", required=True)
    description = fields.Text(string="Query Text", required=True)
    note = fields.Text(string="Note")
    issue_line = fields.One2many('x_reminder.issue', 'issue_id')
    max_due = fields.Integer(string="Sebelum Duedate")
    max_late = fields.Integer(string="Lewat Duedate")
    link_view_line = fields.Many2one('x_reminder_link.category', string="Link Category", required=True, Store=True,
                                     Index=True)
    x_flow = fields.Boolean(string="Reminder Flow", default=False)


class reminder_link_category(models.Model):
    _name = 'x_reminder_link.category'

    name = fields.Char(string="Link Name", required=True)
    parent_model = fields.Char(string="Parent Model", required=True)
    view_form = fields.Char(string="View Form")
    amodel_id = fields.Char(string="Model ID")
    reminder_link_id = fields.One2many('x_reminder.category', 'link_view_line')
