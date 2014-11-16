# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class chatarra_documentos(osv.osv):
    _name = 'chatarra.documentos'
    _description = 'documentos'
    _columns = {
        'name'		        :fields.selection([
	       				            ('visual','Visual'),
    	   				            ('carta','Carta de Asignacion'),
       					            ('consulta','Consulta'),
       					            ('copia_tc','Tarjeta de Circulacion Prop. Anterior'),
       					            ('factura_origen','Factura de origen'),
                            ('factura_venta','Factura de venta'),
                            ('factura_compra','Factura de compra'),
       					            ('foto_frente','Foto frente'),
                            ('foto_chasis','Foto chasis'),
                            ('foto_motor','Foto motor')
       					            ], 'Tipo de Documento'),
        'unit_id'	        :fields.many2one('chatarra.unit', 'Placa', required=True),
        'imagen' 	        :fields.binary('Imagen'),
        'state'           :fields.selection([
        				            ('pendiente','Pendiente'),
        				            ('completo','Completo'),
                            ('no_requerido','No Requerido')
        				            ], 'Estado', readonly='True'),
        'completo_por'    :fields.many2one('res.users','Completo por:', readonly=True),
        'fecha_completo'  :fields.datetime('Fecha completo:', readonly=True),
    }
    _defaults = {
        'state': 'pendiente'
    }

    #def action_completo_unidad(self, cr, uid, ids, vals,context=None):
    #    unidad = self.browse(cr, uid, ids)
    #    for documento in unidad.document_ids:
    #        if documento.state in ('pendiente'):
    #            return False
    #            #raise osv.except_osv(('Advertencia !'),
    #            #       ('El documento %s esta en estado Pendiente...') % (documento.name)
    #            #       )
    #    self.write(cr, uid, ids, {'state':'completo',
    #                                  'completo_por':uid,
    #                                  'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def write(self, cr, uid, ids, vals, context=None):
        values = vals
        documento = self.browse(cr, uid, ids)
        unidad_obj = self.pool.get('chatarra.unit')
        unidad = documento.unit_id
        super(chatarra_documentos, self).write(cr, uid, ids, values, context=context)
        for document in unidad.document_ids:
            if document.state in ('pendiente'):
                return False
                #raise osv.except_osv(('Advertencia !'),
                #       ('El documento %s esta en estado Pendiente...') % (documento.name)
                #       )
        unidad_obj.write(cr, uid, [unidad.id], {'state':'completo',
                                                'completo_por':uid,
                                                'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        #if unidad.state in 'asignada':
        #    self.action_completo_unidad(cr, uid, ids, vals)
        return True

    def action_completo(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {  'state':'completo',
                                    'completo_por':uid,
                                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                                  })
    def action_no_requerido(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {  'state':'no_requerido',
                                    'completo_por':uid,
                                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                                  })
        return True