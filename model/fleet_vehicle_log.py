# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from tools.translate import _
import time
import datetime
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT,
                           DEFAULT_SERVER_DATETIME_FORMAT)
server_date = DEFAULT_SERVER_DATE_FORMAT
server_datetime = DEFAULT_SERVER_DATETIME_FORMAT


class vehicle_log(osv.osv):
    _name = 'vehicle.log'

    def _get_day(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids):
            date = record.date
            day = time.strptime(date, '%Y-%m-%d %H:%M:%S')
            res[record.id] = day.tm_mday
            return res

    def _get_year(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids):
            date = record.date
            day = time.strptime(date, '%Y-%m-%d %H:%M:%S')
            res[record.id] = day.tm_year
            return res

    def _get_week(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids):
            date = record.date
            day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            res[record.id] = _('Week ') + str(day.isocalendar()[1])
            return res

    _description = 'Vehicle Log'
    _columns = {
        'name': fields.char('Log Number', readonly='True'),
        'state': fields.selection([('draft', 'Draft'),
                                   ('in', 'In'),
                                   ('out', 'Out'),
                                   ], 'State', readonly=True),
        'sale_state': fields.selection([('reserved', 'Reserved'),
                                        ('sold', 'Sold'),
                                        ('avialable', 'Avialable'),
                                        ], 'Sale State', readonly=True),
        'date': fields.datetime('Date', required=True),
        'approved_by': fields.many2one('hr.employee',
                                       'Approved by',
                                       required=True),
        'vehicle_id': fields.many2one('fleet.vehicle',
                                      'Vehicle',
                                      required=True),
        'date_in': fields.datetime('Date in', readonly=True),
        'date_out': fields.datetime('Date out', readonly=True),
        'business': fields.text('Business', required=True),
        'shop_id': fields.many2one('sale.shop', 'Company', required=True),
        'day': fields.function(_get_day,
                               type='char',
                               store=True,
                               string='Day'),
        'year': fields.function(_get_year,
                                type='char',
                                store=True,
                                string='Year'),
        'week': fields.function(_get_week,
                                type='char',
                                store=True,
                                string='Week'),
        }

    _defaults = {
        'state': 'draft',
        'date': time.strftime(server_datetime)
    }

    def create(self, cr, uid, vals, context={}):
        """
        Assing a sequence number when the record is created
        """
        sequence = 'vehicle.log.sequence.number'
        if ('name' not in vals) or (vals['name'] is False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, sequence)
        return super(vehicle_log, self).create(cr, uid, vals, context)

    def vehicle_in(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'in',
                                  'date_in': time.strftime(server_datetime)
                                  })

    def vehicle_out(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'out',
                                  'date_out': time.strftime(server_datetime)
                                  })
