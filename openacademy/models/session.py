# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api
from openerp.exceptions import ValidationError

PRIORITY_LIST = (('0', 'Low'), ('1', 'Normal'), ('2', 'High'), ('3', 'Nuclear'))
STATES_LIST = (('draft', 'Draft'),
               ('confirmed', 'Confirmed'),
               ('done', 'Done'))

class Session(models.Model):
    _name = 'openacademy.session'
    _inherit = 'mail.thread'
    _order = "priority, name"
    
    name = fields.Char(required=True)
    state = fields.Selection(STATES_LIST, track_visibility="onchange")
    course_id = fields.Many2one('openacademy.course', ondelete="restrict", track_visibility="onchange")
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), string="Duration", 
        help="Duration in days")
    end_date = fields.Date(store=True, compute='_compute_end_date', inverse='_computeinverse_end_date')
    seats = fields.Integer(string="# of seats", track_visibility="onchange")
    instructor_id = fields.Many2one('res.partner', domain="['|', ('instructor', '=', True), ('category_id.name', 'ilike', 'teacher')]", track_visibility="onchange")
    attendee_ids = fields.Many2many('res.partner')
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    active = fields.Boolean(default=True)
    country_id = fields.Many2one('res.country', string="Country", related="course_id.responsible_id.partner_id.country_id")
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')
    color = fields.Integer()
    priority = fields.Selection(PRIORITY_LIST , default='1') 
    
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

    @api.constrains('attendee_ids', 'instructor_id')
    def _check_instructor(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id.id in rec.attendee_ids.ids:
                raise ValidationError("Instructor cannot be an attendee of his own session.")
            
    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.duration:
                rec.end_date = fields.Date.to_string(fields.Date.from_string(rec.start_date+" 00:00:00") + timedelta(days=rec.duration, seconds=-1))
            
    def _computeinverse_end_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration = (fields.Date.from_string(rec.end_date+" 23:59:00") - fields.Date.from_string(rec.start_date+" 00:00:00")).days + 1
                
    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24
        
    @api.multi
    def action_draft(self):
        self.state = "draft"
            
    @api.multi
    def action_confirm(self):
        self.state = "confirmed"

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})
        