# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class chatarra_asignacion(osv.osv):
    _name = 'chatarra.asignacion'
    _description = 'Asignacion'


    def _get_newer_unit_id(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        unit_id = False
        for asignacion in self.browse(cr, uid, ids, context=context):
            for unit in asignacion.unit_ids:
                unit_id = unit.id
            res[asignacion.id] = unit_id
        return res


    _columns = {
        'name'			:fields.char('No. de Asignacion', size=64, readonly='True'),
        'client_id'		: fields.many2one('res.partner', 'Cliente'),
        'contacto_id'	: fields.many2one('res.partner', 'Contacto'),
        'agencia_id'	: fields.many2one('res.partner','Agencia'),
        'unit_id'       : fields.function(_get_newer_unit_id, method=True, relation='chatarra.unit', type="many2one", string='Unidad Actual', readonly=True, store=True, ondelete='cascade'),
        'unit_ids'		: fields.many2many('chatarra.unit', 'chatarra_asignacion_unidad_rel', 'asignacion_id', 'unit_id', 'Unidades'),
    }

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'asignacion.sequence.number')
        return super(chatarra_asignacion, self).create(cr, uid, vals, context)

chatarra_asignacion()