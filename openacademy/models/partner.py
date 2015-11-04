# -*- coding: utf-8 -*-

from openerp import models, fields

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string='Is instructor')
    session_ids = fields.One2many('openacademy.session', 'instructor_id')
    type_entite = fields.Selection((('phy', 'Physique'), ('mo', 'Morale')))
    statut_entite_id = fields.Many2one('openacademy.statutentite')
    role_mo_ids = fields.One2many('openacademy.rolepersonne', 'partner_mo_id')
    role_phy_ids = fields.One2many('openacademy.rolepersonne', 'partner_phy_id')
    
class StatutEntite(models.Model):
    _name = 'openacademy.statutentite'
    
    name = fields.Char(required=True)

class RoleEntite(models.Model):
    _name = 'openacademy.role'
    
    name = fields.Char(required=True)

class StatutRole(models.Model):
    _name = 'openacademy.statutrole'
    
    name = fields.Char(required=True)
        
class RolePersonne(models.Model):
    _name = 'openacademy.rolepersonne'
    
    partner_mo_id = fields.Many2one('res.partner', domain=[('type_entite', '=', 'mo')])
    partner_phy_id = fields.Many2one('res.partner', domain=[('type_entite', '=', 'phy')])
    role_id = fields.Many2one('openacademy.role')
    status_id = fields.Many2one('openacademy.statutrole')
    start_date = fields.Date()
    end_date = fields.Date()
    