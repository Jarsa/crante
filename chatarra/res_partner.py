# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'agencia':fields.boolean('Agencia'),
    }

res_partner()