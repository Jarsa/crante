# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from tools.translate import _
import time
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
server_date = DEFAULT_SERVER_DATE_FORMAT
server_datetime = DEFAULT_SERVER_DATETIME_FORMAT


class visitor_log(osv.osv):
    _name = 'visitor.log'

    def _get_day(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids):
            date = record.date
            day = time.strptime(date, '%Y-%m-%d')
            res[record.id] = day.tm_mday
            return res

    _description = 'Visitor Log'
    _columns = {
                'name': fields.char('Log Number', readonly='True'),
                'state': fields.selection([('draft', 'Draft'),
                                           ('in', 'In'),
                                           ('out', 'Out'),
                                           ('appointment', 'Appointment')
                                           ], 'State', readonly=True),
                'date': fields.date('Date',required=True),
                'employee_id': fields.many2one('hr.employee',
                                               'Employee to visit',
                                               required=True),
                'visitor_id': fields.many2one('res.partner',
                                              'Visitor',
                                              required=True),
                'date_in': fields.datetime('Date in', readonly=True),
                'date_out': fields.datetime('Date out', readonly=True),
                'business': fields.text('Business', required=True),
                'shop_id' : fields.many2one('sale.shop', 'Company'),
                'day': fields.function(_get_day,
                                       type='char',
                                       store=True,
                                       string='Day'),
                }

    _defaults = {
        'state': 'draft',
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # def _check_in_visitor(self, cr, uid, ids):
    #     """
    #         Constraint to avoid duplicate visitor inside the company
    #     """
    #     visitor_obj = self.pool.get('visitor.log')
    #     search = self.search(cr, uid, [('state', '=', 'in')])
    #     print search
    #     records = visitor_obj.browse(cr, uid, search)
    #     visitor = [x.visitor_id.id for x in records]
    #     for visit in self.browse(cr, uid, ids):
    #         if visit.visitor_id.id in visitor:
    #             return False
    #         else:
    #             return True
    
    # _constraints = [
    #     (_check_in_visitor, _('Error: This visitor is already in'), ['visitor_id']),
    # ]

    # def onchange_in_visitor(self, cr, uid, ids, visitor_id):
    #     """
    #         Onchange method to raise an error if the visitor is already in
    #     """
    #     visitor_obj = self.pool.get('visitor.log')
    #     search = self.search(cr, uid, [('state', '=', 'in')])
    #     records = visitor_obj.browse(cr, uid, search)
    #     visitor = [x.visitor_id.id for x in records]
    #     for visit in self.browse(cr, uid, ids):
    #         if visit.visitor_id.id in visitor:
    #             raise osv.except_osv(_('Error'), _('This visitor is already in'))
    #     return True

    def create(self, cr, uid, vals, context={}):
        """
        Assing a sequence number when the record is created
        """
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'visitor.log.sequence.number')
        return super(visitor_log, self).create(cr, uid, vals, context)

    def state_in(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'in',
                                  'date_in': time.strftime(server_datetime)
                                  })

    def state_out(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'out',
                                  'date_out': time.strftime(server_datetime)
                                  })
