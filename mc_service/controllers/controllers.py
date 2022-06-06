# -*- coding: utf-8 -*-
# from odoo import http


# class McService(http.Controller):
#     @http.route('/mc_service/mc_service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mc_service/mc_service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mc_service.listing', {
#             'root': '/mc_service/mc_service',
#             'objects': http.request.env['mc_service.mc_service'].search([]),
#         })

#     @http.route('/mc_service/mc_service/objects/<model("mc_service.mc_service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mc_service.object', {
#             'object': obj
#         })
