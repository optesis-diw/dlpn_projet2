#-*- coding: utf-8 -*-
from odoo import models, fields, api

class so_custom_confirm_date(models.Model):
    _inherit = 'sale.order'
    
    date_order_immutable = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', True)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders")
    
    def action_confirm(self):
        res = super(so_custom_confirm_date, self).action_confirm()
        for order in self:
            order.write({
            'date_order': order.date_order_immutable
            })
        return res