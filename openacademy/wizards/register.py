# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Register(models.TransientModel):
    _name = 'openacademy.register'

    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session',
        string="Session", required=True, default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    state = fields.Selection((('1', 'step 1'), ('2', 'step2')), default='1')

    @api.multi
    def go_step1(self):
        return self.go_step('1')
        
    @api.multi
    def go_step2(self):
        return self.go_step('2')
    
    def go_step(self, state):
        self.state = state
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select attendees',
            'res_model': 'openacademy.register',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
        
    @api.multi
    def validate(self):
        for s in [s for s in self if s.attendee_ids]:
            for sess in s.session_ids:
                sess.attendee_ids |= s.attendee_ids
        return {}