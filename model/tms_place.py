# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class tms_place_locatel(osv.osv):
    _inherit = 'tms.place'
    _columns = {
        'locatel_id':fields.char('Locatel ID', size=64, readonly=True),
    }