# -*- coding: utf-8 -*-

from openerp import models, fields, api
from session import PRIORITY_LIST 

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users')
    session_ids = fields.One2many('openacademy.session', 'course_id')
    nbr_sessions = fields.Integer('N° of skills', compute='_get_nbr_sessions')
    prc_sessions = fields.Integer('Percentage of skills', compute='_get_prc_sessions')
    sessions_graph = fields.Char(_compute='_get_skills_daily')
    
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]
    
    @api.one
    def _get_skills_daily(self):
        a = unicode([
            { "tooltip" : "Old", "value": 5},
            { "tooltip" : "New", "value": 7},
            { "tooltip" : "New 2", "value": 7},
            { "tooltip" : "New 3", "value": 7},
        ]).replace("'","\"")
        self.sessions_graph = a
        
    @api.one
    @api.depends('session_ids')
    def _get_nbr_sessions(self):
        self.nbr_sessions = self.env['openacademy.session'].sudo().search_count([('course_id', '=', self.id)])
            
    @api.one
    @api.depends('session_ids')
    def _get_prc_sessions(self):
        nbr = self.env['openacademy.session'].sudo().search_count([])
        if not nbr:
            self.prc_sessions = 0.0
        else:
            self.prc_sessions = 100.0 * self.env['openacademy.session'].sudo().search_count([('course_id', '=', self.id)]) / nbr
            
    @api.one
    def _get_skills_daily(self):
        a = unicode([
            { "tooltip" : "Old", "value": 5},
            { "tooltip" : "New", "value": 7},
            { "tooltip" : "New 2", "value": 7},
            { "tooltip" : "New 3", "value": 7},
        ]).replace("'","\"")
        self.skills_daily = a
        
    @api.multi
    def sessions_list(self):
        return {
            'name': 'Sessions',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'openacademy.session',
            'type': 'ir.actions.act_window',
            'domain': [['id', 'in', self.session_ids.ids]],
        }
        
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
    
        
    
            