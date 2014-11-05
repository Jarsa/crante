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
        'name'		:fields.selection([
	       				('visual','Visual'),
    	   				('carta','Carta de Asignacion'),
       					('consulta','Consulta'),
       					('copia_tc','Tarjeta de Circulacion (Copia)'),
       					('factura','Factura'),
       					('fotos','Fotos'),
       					('nueva_tc','Tarjeta de Circulacion')
       					], 'Tipo de Documento'),
        'unit_id'	:fields.many2one('chatarra.unit', 'Placa', required=True),
        'imagen' 	:fields.binary('Imagen'),
        'state'		:fields.selection([
        				('borrador','borrador'),
        				('generado','Generado')
        				], 'Estado', readonly='True'),
    }
    _defaults = {
        'state': 'borrador'
    }