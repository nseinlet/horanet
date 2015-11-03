# -*- coding: utf-8 -*-

from openerp import models, fields

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string='Is instructor')
    session_ids = fields.One2many('openacademy.session', 'instructor_id')
    