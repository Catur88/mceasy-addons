from odoo import api, fields, models

class ModuleParticipantCourse(models.Model):
    _name = 'participant.course'

    name = fields.Char(string='Nama')
    age = fields.Integer(string='Umur (tahun)')
    email = fields.Char(string='Email')
    address = fields.Text(string='Alamat')

    course_line_ids = fields.One2many(
        comodel_name='online.course.line',
        inverse_name='line_ids',
        string='Kelas yang Diambil',
    )


class ModuleOnlineCourseLine(models.Model):
    _name = 'online.course.line'

    line_ids = fields.Many2one(string='Line Kursus', comodel_name="participant.course")

    course_name = fields.Many2one(comodel_name='online.course', string='Nama Kelas')
    course_description = fields.Text(string='Deskripsi', related='course_name.description')
    course_duration = fields.Integer(string='Durasi (jam)', related='course_name.duration')
