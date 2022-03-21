# -*- coding: utf-8 -*-
from odoo import http

# class LpjSales(http.Controller):
#     @http.route('/lpj_sales/lpj_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lpj_sales/lpj_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lpj_sales.listing', {
#             'root': '/lpj_sales/lpj_sales',
#             'objects': http.request.env['lpj_sales.lpj_sales'].search([]),
#         })

#     @http.route('/lpj_sales/lpj_sales/objects/<model("lpj_sales.lpj_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lpj_sales.object', {
#             'object': obj
#         })