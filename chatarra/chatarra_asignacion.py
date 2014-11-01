# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

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

    def asignar_unidad(self, cr, uid, ids, vals, context=None):
        unit_obj = self.pool.get('chatarra.unit')
        for asignacion in self.browse(cr, uid, ids):
            unit_ids = False
            unit_ids = unit_obj.search(cr, uid, [('asignacion_id', '=', asignacion.id)])
            if unit_ids:
                unit_obj.write(cr, uid, unit_ids, {'asignacion_id': False, 'state':'disponible', 'asignada_por': False,'fecha_asignada': False})
            unit_ids = []
            for unidad in asignacion.unit_ids:
                if unidad.state in 'reposicion':
                    continue
                elif unidad.state in ('borrador'):
                    raise osv.except_osv(_('Warning !'),
                        _('La Unidad %s esta en estado Borrador...') % (unidad.name)
                        ) 
                unit_obj.write(cr, uid, [unidad.id], {'asignacion_id':asignacion.id,'state':'asignada','asignada_por':uid,'fecha_asignada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def write(self, cr, uid, ids, vals, context=None):
        values = vals
        super(chatarra_asignacion, self).write(cr, uid, ids, values, context=context)
        for rec in self.browse(cr, uid, ids):
            self.asignar_unidad(cr, uid, ids, vals)

        return True

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'asignacion.sequence.number')
        res = super(chatarra_asignacion, self).create(cr, uid, vals, context)
        self.asignar_unidad(cr, uid, [res], vals)
        return res



chatarra_asignacion()