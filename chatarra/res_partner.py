# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'categoria' : fields.selection([('none', 'N/A'),
        								('agencia','Agencia'),
        								('paqueteria','Paqueteria'),
        								('secretaria','Secretaria')
        								], 'Categoria'),
    }
    _defaults = {
        'categoria':'none',
    }

res_partner()