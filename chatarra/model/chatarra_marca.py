# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_marca(osv.osv):
    _name = 'chatarra.marca'
    _columns = {
                'name': fields.char('Marca', size=40, required=True),
                'active': fields.boolean('Activo'),
        }
    _defaults = {
        'active': 'True',
    }