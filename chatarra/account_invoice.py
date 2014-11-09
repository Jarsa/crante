# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _columns = {
        'asignacion_id'	: fields.many2one('chatarra.asignacion','No. de Asignacion', readonly=True),
        'unit_id'		: fields.many2one('chatarra.unit','Unidad', readonly=True),
        'agencia_id'	: fields.many2one('res.partner','Agencia', readonly=True),
        'contacto_id'	: fields.many2one('res.partner','Contacto', readonly=True),
    }
    _sql_constraints = [
        ('unit_id_uniq', 'unique (unit_id)', 'Una de las unidades ya se facturo!'),
    ]

chatarra_invoice()