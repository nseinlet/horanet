# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import requests

class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string='Is instructor')
    session_ids = fields.One2many('openacademy.session', 'instructor_id')
    type_entite = fields.Selection((('phy', 'Physique'), ('mo', 'Morale')))
    statut_entite_id = fields.Many2one('openacademy.statutentite')
    role_mo_ids = fields.One2many('openacademy.rolepersonne', 'partner_mo_id')
    role_phy_ids = fields.One2many('openacademy.rolepersonne', 'partner_phy_id')
    
    @api.onchange('street', 'street2', 'city', 'zip')
    def check_with_api(self):
        if self.street and self.city and self.zip:
            params = {'q': "%s %s %s" % (self.street, self.street2, self.city),
                      'postcode': self.zip}
            url = "http://api-adresse.data.gouv.fr/search/"
            r = requests.get(url, params=params)
            if r.status_code == requests.codes.ok:
                res = r.json()
                if res[u'features']:
                    if len(res[u'features'])>1:
                        wiz_id = self.env['openacademy.address.selector'].create({'partner_id': self.id})
                        for feat in res[u'features']:
                            self.env['openacademy.address.choice'].create({
                                'street': feat['properties']['name'],
                                'city': feat['properties']['city'],
                            })
                    else:
                        elem = res[u'features'][0]
                        self.city = elem['properties']['city']
                        self.street = elem['properties']['name']
    
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
    