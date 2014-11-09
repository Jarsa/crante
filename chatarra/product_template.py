# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_product(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'
    _columns = {
        'chatarra' : fields.boolean('Chatarra'),
    }
    _sql_constraints = [
        ('chatarra_uniq', 'unique (chatarra)', 'Solo puedes tener un solo producto como chatarra!'),
    ]

chatarra_product()