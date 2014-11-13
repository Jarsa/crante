# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import logging
_logger = logging.getLogger(__name__)

class chatarra_envio(osv.osv):
    _name = 'chatarra.envio'
    _columns = {
        'name'			: fields.char('No. de envio', readonly=True),
        'state'			: fields.selection([
        					('borrador','Borrador'),
        					('enviado','Enviado')
        					],'Estado', readonly=True),
        'guia'			: fields.char('Guia', required=True),
        'paqueteria_id'	: fields.many2one('res.partner','Paqueteria', required=True),
        'secretaria_id'	: fields.many2one('res.partner','Secretaria', required=True),
        'unit_ids'		: fields.many2many('chatarra.unit', 'chatarra_envio_unidad_rel', 'envio_id', 'unit_id', 'Unidades', required=True),
        'enviado_por'	: fields.many2one('res.users','Enviado por:', readonly=True),
        'fecha_enviado'	: fields.datetime('Fecha Enviado:', readonly=True),
    }

    _defaults = {
        'state': 'borrador',
    }

    def seleccionar_unidad(self, cr, uid, ids, vals, context=None):
        unit_obj = self.pool.get('chatarra.unit')
        for envio in self.browse(cr, uid, ids):
            unit_ids = False
            unit_ids = unit_obj.search(cr, uid, [('envio_id', '=', envio.id),('state', '=', 'seleccion')])
            if unit_ids:
                unit_obj.write(cr, uid, unit_ids, {'envio_id': False, 'state':'completo', 'guia': False})
            unit_ids = []
            for unidad in envio.unit_ids:
            	unit_obj.write(cr, uid, [unidad.id], {'envio_id':envio.id,'state':'seleccion','guia':envio.guia})

    def enviar_unidad(self, cr, uid, ids, vals, context=None):
    	unit_obj = self.pool.get('chatarra.unit')
    	envio = self.browse(cr, uid, ids)
    	self.write(cr, uid, ids, {'state':'enviado',
    							  'enviado_por':uid,
    							  'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
    	for unidad in envio.unit_ids:
    		unit_obj.write(cr, uid, [unidad.id], {'envio_id':envio.id,
    											  'state':'enviado',
    											  'guia':envio.guia,
    											  'enviado_por':uid,
    											  'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'envio.sequence.number')
        res = super(chatarra_envio, self).create(cr, uid, vals, context)
        self.seleccionar_unidad(cr, uid, [res], vals)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        values = vals
        super(chatarra_envio, self).write(cr, uid, ids, values, context=context)
        for envio in self.browse(cr, uid, ids):
            for unidad in envio.unit_ids:
                if unidad.state in 'reposicion':
                    self.write(cr, uid, ids, {'unit_ids': [(3, unidad.id)]})
                if envio.state in ('borrador'):
                    self.seleccionar_unidad(cr, uid, ids, vals)
        return True


chatarra_envio()