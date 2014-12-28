# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_motivo(osv.osv):
    _name = 'chatarra.motivo'
    _columns = {
        'name'      : fields.char('Motivo', size=64, required=True),
        'active'    : fields.boolean('Activo'),
    }
    _defaults = {
        'active': 'True',
    }