# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv


class sale_shop(osv.osv):
    _name = 'sale.shop'
    _inherit = 'sale.shop'
    _columns = {
        'user_id': fields.many2many('res.users',
                                    'rel_user_id_res_users',
                                    'user_id',
                                    'res_user',
                                    'User'),
        }
