from odoo import api, fields, models


class ModeuleOnlineCourse(models.Model):
    _name = 'online.course'

    name = fields.Char(string='Nama Kursus')
    description = fields.Text(string='Deskripsi')
    duration = fields.Integer(string='Durasi (jam)')
    day_course = fields.Selection(string="Hari", selection=[('senin', 'Senin'),
                                   ('selasa', 'Selasa'),
                                   ('rabu', 'Rabu'),
                                   ('kamis', 'Kamis'),
                                   ('jumat', 'Jumat')])
    teacher_id = fields.Many2one(comodel_name='teacher.course', string='Guru')

