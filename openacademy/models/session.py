# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    course_id = fields.Many2one('openacademy.course', ondelete="restrict")
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), string="Duration", 
        help="Duration in days")
    seats = fields.Integer(string="# of seats")
    instructor_id = fields.Many2one('res.partner', domain="['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'teacher')]")
    attendee_ids = fields.Many2many('res.partner')
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(default=True)
    
    @api.depends('seats', 'attendee_ids')    
    def _taken_seats(self):
        for record in self:
            if record.seats!=0:
                record.taken_seats = 100 * len(record.attendee_ids) / record.seats
            else:
                record.taken_seats = 0
                
    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats(self):
        if self.seats<0:
            return{
                'warning': {
                    'title': 'No negative value',
                    'message': 'No negative value for the number of seats',
                }
            }
        else:
            if self.seats<len(self.attendee_ids):
                return{
                    'warning': {
                        'title': 'Too low value',
                        'message': 'Too many attendees for the number of seats',
                    }
                }