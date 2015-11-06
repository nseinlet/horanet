# -*- coding: utf-8 -*-
from openerp import models, fields

class sessionanalysis(models.Model):
    _name = "openacademy.session.analysis"
    _description = "Course and session analysis"
    _order='name'
    _auto = False

    name = fields.Char(string="Title")
    responsible_id = fields.Many2one('res.users', string="responsible")
    start_date = fields.Date("Begin date")
    duration = fields.Integer("Duration")
    seats = fields.Integer("seats")
    country_id = fields.Many2one('res.country')
    
    def init(self, cr):
        #tools.sql.drop_view_if_exists(cr, 'academy_session_analysis')
        cr.execute('''CREATE OR REPLACE VIEW openacademy_session_analysis AS (
            select sess.id, sess.duration, sess.start_date, sess.seats, 
            course.name, course.responsible_id, prtn.country_id
            from openacademy_session as sess
            left join openacademy_course as course on course.id=sess.course_id
            left join res_partner as prtn on prtn.id=course.responsible_id)''')
        