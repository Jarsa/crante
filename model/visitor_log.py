# -*- encoding: utf-8 -*-
from openerp import fields, models, api, _
import time
from openerp.exceptions import ValidationError
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
now = lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
server_date = DEFAULT_SERVER_DATE_FORMAT
server_datetime = DEFAULT_SERVER_DATETIME_FORMAT


class visitor_log(models.Model):
    _name = 'visitor.log'
    _description = 'Visitor Log'

    name = fields.Char(string='Log Number', readonly='True')
    state = fields.Selection([('draft', 'Draft'),
                              ('in', 'In'),
                              ('out', 'Out'),
                              ('appointment', 'Appointment')
                              ], readonly=True, default='draft')
    date = fields.Datetime(required=True, default=now)
    employee_id = fields.Many2one('hr.employee',
                                  string='Employee to visit',
                                  required=True)
    visitor_id = fields.Many2one('res.partner',
                                 string='Visitor',
                                 required=True)
    date_in = fields.Datetime(readonly=True)
    date_out = fields.Datetime(readonly=True)
    business = fields.Text(required=True)

    @api.one
    @api.constrains('visitor_id')
    def _check_in_visitor(self):
        """
        Constraint to avoid duplicate visitor inside the company
        """
        search = self.search([('state', '=', 'in')])
        visitors = [x.visitor_id.id for x in search]
        for visit in self:
            if visit.visitor_id.id in visitors:
                raise ValidationError(_('This visitor is already in'))

    @api.onchange('visitor_id')
    def _verify_in_visitor(self):
        """
        Onchange method to raise an error if the visitor is already in
        """
        search = self.search([('state', '=', 'in')])
        visitor = [x.visitor_id.id for x in search]
        for visit in self:
            if visit.visitor_id.id in visitor:
                return {
                    'warning': {
                        'title': _("Error"),
                        'message': _("This visitor is already in"),
                    }
                }

    @api.model
    def create(self, vals):
        """
        Assing a sequence number when the record is created
        """
        sequence = self.env.ref('visitor_log.sequence_visitor_log').id
        vals['name'] = self.env['ir.sequence'].next_by_id(sequence)
        visitor = super(visitor_log, self).create(vals)
        return visitor

    @api.one
    def state_in(self):
        self.write({'state': 'in',
                    'date_in': time.strftime(server_datetime)})

    @api.one
    def state_out(self):
        self.write({'state': 'out',
                    'date_out': time.strftime(server_datetime)})
