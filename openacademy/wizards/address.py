# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AddressSelector(models.TransientModel):
    _name = 'openacademy.address.selector'
    
    partner_id = fields.Many2one('res.partner')
    choice_id = fields.Many2one('openacademy.address.choice')
    
    @api.multi
    def validate(self):
        pass
    
class AddressChoice(models.TransientModel):
    _name = 'openacademy.address.choice'
    
    street = fields.Char()
    zip = fields.Char()
    city = fields.Char()