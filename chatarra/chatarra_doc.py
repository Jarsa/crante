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


#class chatarra_visual(osv.osv):
#    _name = 'chatarra.visual'
#    _description = 'Visual'
#    _columns = {
#        'name'				:fields.char('Nombre', size=40),
#        'imagen'			:fields.boolean('Imagen'),
#        'visual_o2m_unidad' :fields.char('Visual'),
#        'unit_id'			:fields.many2one('chatarra.unit','Unidad', required=True),
#        'state'				:fields.selection([
#        	('borrador','Borrador'),
#        	('recibido','Recibido'),
#        	], 'Estado', readonly=True)
#    }
#    _defaults = {
#        'state': 'borrador'
#        'name': lambda *a: None,
#    }
#    chatarra_visual()
#
#class chatarra_carta(osv.osv):
#    _name = 'chatarra.carta'
#    _description = 'Carta de Asignacion'
#    _columns = {
#        'name'				:fields.char('Nombre', size=40),
#        'imagen'			:fields.boolean('Imagen'),
#        'carta_o2m_unidad' :fields.char('Carta de Asignacion'),
#        'unit_id'			:fields.many2one('chatarra.unit','Unidad', required=True),
#        'state'				:fields.selection([
#        	('borrador','Borrador'),
#        	('pedido_agencia','Pedido a Agencia'),
#        	('recibir_copia','Copia recibida'),
#        	('recibir_original','Original recibida')
#        	], 'Estado', readonly=True)
#    }
#    _defaults = {
#        'state': 'borrador'
#        'name': lambda *a: None,
#    }
#    chatarra_carta()
#
#class chatarra_consulta(osv.osv):
#    _name = 'chatarra.consulta'
#    _description = 'Visual'
#    _columns = {
#        'name'				:fields.char('Nombre', size=40),
#        'imagen'			:fields.boolean('Imagen'),
#        'consulta_o2m_unidad' :fields.char('Consulta'),
#        'unit_id'			:fields.many2one('chatarra.unit','Unidad', required=True),
#        'state'				:fields.selection([
#        	('borrador','borrador'),
#        	('generado','Generado'),
#        	], 'Estado', readonly=True)
#    }
#    _defaults = {
#        'state': 'borrador'
#        'name': lambda *a: None,
#    }
#    chatarra_consulta()
#
#class chatarra_tarjeta(osv.osv):
#    _name = 'chatarra.tarjeta'
#    _description = 'Tarjeta de Circulacion'
#    _columns = {
#        'name'				:fields.char('Nombre', size=40),
#        'imagen'			:fields.boolean('Imagen'),
#        'consulta_o2m_tarjeta' :fields.char('Consulta'),
#        'unit_id'			:fields.many2one('chatarra.unit','Unidad', required=True),
#        'state'				:fields.selection([
#        	('borrador','borrador'),
#        	('generado','Generado'),
#        	], 'Estado', readonly=True)
#    }
#    _defaults = {
#        'state': 'borrador'
#        'name': lambda *a: None,
#    }
#    chatarra_tarjeta()
#
# class chatarra_tarjeta(osv.osv):
#    _name = 'chatarra.tarjeta'
#    _description = 'Tarjeta de Circulacion'
#    _columns = {
#        'name'				:fields.char('Nombre', size=40),
#        'imagen'			:fields.boolean('Imagen'),
#        'consulta_o2m_tarjeta' :fields.char('Consulta'),
#        'unit_id'			:fields.many2one('chatarra.unit','Unidad', required=True),
#        'state'				:fields.selection([
#        	('borrador','borrador'),
#        	('generado','Generado'),
#        	], 'Estado', readonly=True)
#    }
#    _defaults = {
#        'state': 'borrador'
#        'name': lambda *a: None,
#    }
#    chatarra_tarjeta()#