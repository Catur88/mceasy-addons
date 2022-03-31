from odoo import fields
from odoo.osv import osv


class DisplayDialogBox(osv.osv_memory):
    _name = "display.dialog.box"

    text = fields.Text(readonly=True, string='Keterangan')


DisplayDialogBox()
