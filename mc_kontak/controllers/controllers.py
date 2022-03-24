# -*- coding: utf-8 -*-
# from odoo import http


# class McKontak(http.Controller):
#     @http.route('/mc_kontak/mc_kontak', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mc_kontak/mc_kontak/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mc_kontak.listing', {
#             'root': '/mc_kontak/mc_kontak',
#             'objects': http.request.env['mc_kontak.mc_kontak'].search([]),
#         })

#     @http.route('/mc_kontak/mc_kontak/objects/<model("mc_kontak.mc_kontak"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mc_kontak.object', {
#             'object': obj
#         })
