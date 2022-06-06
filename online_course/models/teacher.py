from odoo import api, fields, models

class ModeuleTeacherCourse(models.Model):
    _name = 'teacher.course'

    name = fields.Char(string='Nama')
    email = fields.Char(string='Email')
    no_telp = fields.Char(string='No Telp')
    address = fields.Text(string='Alamat')
    course_id = fields.Many2one(comodel_name='online.course', string='Kelas')