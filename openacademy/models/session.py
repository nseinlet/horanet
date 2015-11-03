# -*- coding: utf-8 -*-

from openerp import models, fields

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    course_id = fields.Many2one('openacademy.course', ondelete="restrict")
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), string="Duration", 
        help="Duration in days")
    seats = fields.Integer(string="# of seats")
    instructor_id = fields.Many2one('res.partner')
    attendee_ids = fields.Many2many('res.partner')