# -*- coding: utf-8 -*-
# from odoo import http


# class OnlineCourse(http.Controller):
#     @http.route('/online_course/online_course', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/online_course/online_course/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('online_course.listing', {
#             'root': '/online_course/online_course',
#             'objects': http.request.env['online_course.online_course'].search([]),
#         })

#     @http.route('/online_course/online_course/objects/<model("online_course.online_course"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('online_course.object', {
#             'object': obj
#         })
