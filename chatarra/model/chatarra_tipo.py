# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_tipo(osv.osv):
    _name = 'chatarra.tipo'
    _columns = {
                'name': fields.char('Tipo', size=40, required=True),
                'active': fields.boolean('Activo'),
        }
    _defaults = {
        'active': 'True',
    }