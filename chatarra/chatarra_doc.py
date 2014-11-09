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
                            ('foto_motor','Foto motor'),
       					            ('nueva_tc','Tarjeta de Circulacion')
       					            ], 'Tipo de Documento'),
        'unit_id'	        :fields.many2one('chatarra.unit', 'Placa', required=True),
        'imagen' 	        :fields.binary('Imagen'),
        'state'           :fields.selection([
        				            ('pendiente','Pendiente'),
        				            ('completo','Completo')
        				            ], 'Estado', readonly='True'),
        'completo_por'    :fields.many2one('res.users','Completo por:', readonly=True),
        'fecha_completo'  :fields.datetime('Fecha completo:', readonly=True),
    }
    _defaults = {
        'state': 'pendiente'
    }

    def action_completo(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {  'state':'completo',
                                    'completo_por':uid,
                                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                                  })
        return True