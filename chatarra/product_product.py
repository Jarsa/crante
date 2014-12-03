# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
        'categoria' : fields.selection([('no_chatarra','No Chatarra'),
        								('chatarra','Chatarra'),
        								('envio','Envio'),
        								('secretaria','Secretaria')], 'Categoria'),
    }

    def _check_category(self, cr, uid, ids, context=None):
        prod_obj = self.pool.get('product.product')
        for record in self.browse(cr, uid, ids, context=context):
            if record.categoria == 'chatarra':
                res = prod_obj.search(cr, uid, [('categoria', '=', 'chatarra')], context=None)
                if res and res[0] and res[0] != record.id:
                    return False
        return True

    _constraints = [
        (_check_category, 'Error ! No puedes tener mas de un producto definido como Chatarra', ['categoria']),
        
        ]

chatarra_product()