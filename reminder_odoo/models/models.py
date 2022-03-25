
from odoo import api, fields, models


class reminder_issue(models.Model):
    _name = 'x_reminder.issue'

    name = fields.Char(string="Reminder")
    trigger_date = fields.Date(string ="Duedate Issue")
    source_doc = fields.Char(string ="Source Document")
    description = fields.Char(string="Description")
    refference = fields.Char(string="Refference")
    link_id = fields.Char(string="Link Id")
    link_id2 = fields.Char(string="Link Id2")
    day_count = fields.Char(string="Selisih Hari")
    issue_id = fields.Many2one('x_reminder.category', required=True, store=True, Index=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)


    # button di form unutk nge link ke form lain
    def button_sourcedoc_reminder(self):
        # 1. ambil data categori reminder dan loop
        # 2. cek link_id untuk set di self.env['ir.model.data'] dan returnnya
        categ_id = self.issue_id.id
        view_obj = self.env['x_reminder.category'].search([('id', '=', categ_id)])
        if view_obj:
            aselect = view_obj.link_view_line
            if aselect:
                amodel = aselect.parent_model
                aview = aselect.view_form
                ares_model = aselect.amodel_id

                view = self.env['ir.model.data'].get_object_reference(amodel, aview)
                compose_form_id = view and view[1] or False
                cek = self.env[ares_model].search([('id', '=', self.link_id)])

                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': ares_model,
                    'views': [(compose_form_id, 'form')],
                    'view_id': compose_form_id,
                    'target': 'self',
                    'res_id': cek.id,
                }

    # fetch data dr db terus di store ke tabel baru, otomatis lewat scheduller
    @api.model
    def get_reminder_issue_record(self, vals):
        # 1. delete all data from table x.reminder.issue (truncate)
        # 2. query = select * from x_reminder_category
        # 3. looping query x_reminder_category, return sql (based on line ke-n)
        # 4. looping masukkan ke x.reminder.issue

        self.env.cr.execute("TRUNCATE TABLE x_reminder_issue")
        self.env.cr.execute("ALTER SEQUENCE x_reminder_issue_id_seq RESTART WITH 1")

        line = self.env['x_reminder.issue'].search([])
        for categ in self.env['x_reminder.category'].search([]):
            self.env.cr.execute(categ.description)
            sql = self.env.cr.fetchall()

            if sql:
                for row in sql:
                    aname = categ.name
                    adue = categ.max_due
                    alate = (-1 * categ.max_late)

                    if row[4] is not None:
                        arow4 = str(int(row[4]))
                        if row[4] > 0 and row[4] <= adue:
                            aname =aname +" H-"+str(int(row[4]))
                        elif row[4] == 0:
                            aname =aname + " H"
                        elif row[4] < alate:
                            aname =aname + " > H+" + str(int(alate))
                        else:
                            aname = aname + " H+" + str(abs(int(row[4])))

                    else:
                        arow4 = None

                    line.create({
                        'name': aname,
                        'trigger_date': row[1],
                        'source_doc': row[3],
                        'description': row[6],
                        'refference': row[5],
                        'link_id': row[0],
                        'link_id2': row[2],
                        'day_count': arow4,
                        'issue_id': categ.id
                    })

                if vals == 1:
                    if categ.x_flow:
                        self.email_reminder_flow(categ.id)

    # uswa-tambah fungsi send email reminder OK 16/12/2020
    def email_reminder_flow(self, vals):
        for row in self.env['x_reminder.category'].search([('id', '=', vals)]):
            template_id = self.env['ir.model.data'].get_object_reference('reminder_odoo','email_template_for_flow')[1]

            if template_id:
                email_template_obj = self.env['mail.template'].browse(template_id)
                values = email_template_obj.generate_email(row.id, fields=None)

                values['email_to'] = 'it.system@laprintjaya.com'
                values['subject'] = 'REMINDER '+row.name

                values['res_id'] = False
                mail_mail_obj = self.env['mail.mail']
                msg_id = mail_mail_obj.create(values)
                if msg_id:
                    msg_id.send()

            return True

    # buat ngefilter reminder berdasarkan deptnya
    def dept_filter_action(self):
        current_login = self.env.uid
        user_login = self.env['res.users'].search([('id', '=', int(current_login))])
        ctx = dict(self.env.context)
        ctx.update({'group_by': ['name']})

        adomain = ""
        self.env.cr.execute("select he.department_id from hr_employee he "
                                    "join hr_department hd on hd.id = he.department_id "
                                    "join resource_resource rr on rr.id = he.resource_id "
                                    "join res_users ru on ru.id = rr.user_id "
                                    "where ru.id = '"+str(current_login)+"'")
        adept_id = self.env.cr.fetchone()
        if adept_id:
            cek_group = self.env['x_reminder.group'].search([('group_id', '=', int(adept_id[0]))])
            if cek_group:
                # cek_group.categ_line
                adomain ="[('issue_id','in'," + str(cek_group.categ_line[1:].ids) + ")]"
                adomain = "['|',('issue_id','in'," + str(cek_group.categ_line[1:].ids) + "),'&',('issue_id','=',1),('link_id2','=',"+ str(user_login.id) +")]"
            else:
                get_categ = self.env['x_reminder.category'].search([])
                if get_categ:
                    adomain = "[('issue_id','=',1),('link_id2','=',"+ str(user_login.id) +")]"


        return {
            'name': 'Reminder Issue',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'x_reminder.issue',
            'type': 'ir.actions.act_window',
            'context': ctx,
            'domain': adomain,
        }

