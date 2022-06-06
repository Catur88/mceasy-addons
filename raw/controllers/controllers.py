# -*- coding: utf-8 -*-
# from odoo import http


# class Raw(http.Controller):
#     @http.route('/raw/raw', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/raw/raw/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('raw.listing', {
#             'root': '/raw/raw',
#             'objects': http.request.env['raw.raw'].search([]),
#         })

#     @http.route('/raw/raw/objects/<model("raw.raw"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('raw.object', {
#             'object': obj
#         })
