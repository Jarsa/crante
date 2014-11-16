# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import logging
_logger = logging.getLogger(__name__)

class chatarra_unit(osv.osv):
    _name = 'chatarra.unit'

    def _check_unique_insesitive(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 , [], context=context)
        lst = [x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context) if x.name and x.id not in ids]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.name and self_obj.name.lower() in  lst:
                return False
            return True

    def onchange_vat(self, cr, uid, ids, propietario_id, context=None):
        vat = False
        if propietario_id:
            vat = self.pool.get('res.partner').browse(cr, uid, propietario_id, context=context).vat
        return {'value': {'vat': vat}}
    
    _columns = {  
                'name'                    : fields.char('Placa',size=40),
                'state'                   : fields.selection([
                                              ('borrador','Borrador'),
                                              ('disponible','Disponible'),
                                              ('asignada','Asignada'),
                                              ('elaboracion','Elaboracion de Expediente'),
                                              ('completo','Expediente Completo'),
                                              ('seleccion','Seleccionado para Envio'),
                                              ('enviado','Enviado a SCT'),
                                              ('recibido','Recibido'),
                                              ('consulta','Consulta'),
                                              ('reposicion','Reposicion'),
                                              ('enviado_agencia','Agencia'),
                                              ('bloqueado','Bloqueado'),
                                              ('cita','Cita'),
                                              ('exp_enviado','Expediente Enviado'),
                                              ('chatarrizado','Chatarrizado'),
                                              ('certificado','Certificado Recibido'),
                                              ('baja','Baja'),
                                              ('cancelado','Cancelado'),
                                              ('desestimiento','Desestimiento'),
                                              ], 'Estado', readonly=True),
                'client_id'               : fields.many2one('res.partner', 'Cliente', readonly=True),
                'serie'                   : fields.char('Número de serie', size=40),
                'marca'                   : fields.many2one('chatarra.marca', 'Marca'),
                'modelo'                  : fields.char('Modelo', size=40),
                'color_placa'             : fields.char('Color de la Placa'),
                'tipo_placa'              : fields.selection([('carga','CARGA'),
                                                              ('pasaje','PASAJE'),
                                                              ('turismo','TURISMO')
                                                              ],'Tipo de Placa'),
                'clase'                   : fields.selection([('t2','T 2'),('t3','T 3'),('c2','C 2'),('c3','C 3')],'Clase'),
                'tipo'                    : fields.many2one('chatarra.tipo','Tipo'),
                'motor'                   : fields.char('Motor',size=40),
                'combustible'             : fields.selection([('diesel','Diesel'),('gasolina','Gasolina')],'Combustible'),
                'peso_vehicular'          : fields.float('Peso Vehicular'),
                'propietario_id'          : fields.many2one('res.partner','Nombre del Propietario'),
                'vat'                     : fields.char('R.F.C.', size=20),
                'reg_fed'                 : fields.char('Reg. Fed', size=40),
                'modalidad'               : fields.char('Modalidad', size=64),
                'no_ejes'                 : fields.integer('Numero de ejes'),
                'no_llantas'              : fields.integer('Numero de llantas'),
                'cap_litros'              : fields.char('Litros', size=10),
                'cap_toneladas'           : fields.char('Toneladas', size=10),
                'cap_personas'            : fields.char('Personas', size=10),
                'alto'                    : fields.float('Alto'),
                'ancho'                   : fields.float('ancho'),
                'largo'                   : fields.float('largo'),
                'eje_direccional'         : fields.char('Eje Direccional', size=10),
                'eje_motriz'              : fields.char('Eje Motriz', size=10),
                'eje_carga'               : fields.char('Eje Carga', size=10),
                'permiso_ruta'            : fields.char('Permiso de ruta', size=10),
                'lugar_exp'               : fields.char('Lugar de expedicion', size=10),
                'fecha_exp'               : fields.date('Fecha de expedicion'),
                'document_ids'            : fields.one2many('chatarra.documentos', 'unit_id', 'Documentos', readonly=True),
                'asignacion_id'           : fields.many2one('chatarra.asignacion', 'No. de Asignacion:', readonly=True),
                'disponible_por'          : fields.many2one('res.users', 'Disponible por:', readonly=True),
                'fecha_disponible'        : fields.datetime('Fecha Disponible:', readonly=True),
                'asignada_por'            : fields.many2one('res.users', 'Asignado por:', readonly=True),
                'fecha_asignada'          : fields.datetime('Fecha Asignado:', readonly=True),
                'completo_por'            : fields.many2one('res.users', 'Expediente Completo por:', readonly=True),
                'fecha_completo'          : fields.datetime('Fecha Expediente Completo:', readonly=True),
                'enviado_por'             : fields.many2one('res.users', 'Enviado por:', readonly=True),
                'fecha_enviado'           : fields.datetime('Fecha Enviado:', readonly=True),
                'recibido_por'            : fields.many2one('res.users', 'Recibido por:', readonly=True),
                'fecha_recibido'          : fields.datetime('Fecha Recibido:', readonly=True),
                'consulta_por'            : fields.many2one('res.users', 'Consulta por:', readonly=True),
                'fecha_consulta'          : fields.datetime('Fecha Consulta:', readonly=True),
                'enviado_agencia_por'     : fields.many2one('res.users', 'Enviado Agencia por:', readonly=True),
                'fecha_enviado_agencia'   : fields.datetime('Fecha Enviado Agencia:', readonly=True),
                'bloqueado_por'           : fields.many2one('res.users', 'Bloqueado por:', readonly=True),
                'fecha_bloqueado'         : fields.datetime('Fecha Bloqueado:', readonly=True),
                'cita_por'                : fields.many2one('res.users', 'Cita por:', readonly=True),
                'fecha_cita'              : fields.datetime('Fecha Cita:', readonly=True),
                'cita_reprogramada_por'   : fields.many2one('res.users', 'Cita Reprogramada por:', readonly=True),
                'fecha_cita_reprogramada' : fields.datetime('Fecha Cita Reprogramada:', readonly=True),
                'exp_enviado_por'         : fields.many2one('res.users', 'Exp. Enviado por:', readonly=True),
                'fecha_exp_enviado'       : fields.datetime('Fecha Exp. Enviado:', readonly=True),
                'chatarrizado_por'        : fields.many2one('res.users', 'Chatarrizado por:', readonly=True),
                'fecha_chatarrizado'      : fields.datetime('Fecha Chatarrizado:', readonly=True),
                'certificado_por'         : fields.many2one('res.users', 'Certificado por:', readonly=True),
                'fecha_certificado'       : fields.datetime('Fecha Certificado:', readonly=True),
                'baja_por'                : fields.many2one('res.users', 'Baja por:', readonly=True),
                'fecha_baja'              : fields.datetime('Fecha Baja:', readonly=True),
                'cancelado_por'           : fields.many2one('res.users', 'Cancelada por:', readonly=True),
                'fecha_cancelado'         : fields.datetime('Fecha Cancelada:', readonly=True),
                'desestimiento_por'       : fields.many2one('res.users', 'Desestimiento por:', readonly=True),
                'fecha_desestimiento'     : fields.datetime('Fecha Desestimiento:', readonly=True),
                'reposicion_por'          : fields.many2one('res.users', 'Reposicion por:', readonly=True),
                'fecha_reposicion'        : fields.datetime('Fecha Reposicion:', readonly=True),
                'facturado_por'           : fields.many2one('res.users', 'Facturado por:', readonly=True),
                'fecha_facturado'         : fields.datetime('Fecha Facturado:', readonly=True),
                'fact_cancelada_por'      : fields.many2one('res.users', 'Fact. Cancelada por:', readonly=True),
                'fecha_fact_cancelada'    : fields.datetime('Fecha Cancelada:'),
                'repuesta_id'             : fields.many2one('chatarra.unit', 'Repuesta por:', readonly=True),
                'sustituye_id'            : fields.many2one('chatarra.unit', 'Sustituye a:', readonly=True),
                'reposicion_id'           : fields.many2one('chatarra.reposicion', 'No. de Reposicion:', readonly=True),
                'factura_id'              : fields.many2one('account.invoice', 'No. de Factura:'),
                'facturado'               : fields.boolean('Facturado:', readonly=True),
                'envio_id'                : fields.many2one('chatarra.envio','No. Envio:', readonly=True),
                'guia'                    : fields.char('Guia:', readonly=True),
                'copia_tc'				  : fields.boolean('Copia TC', readonly=True),
                'consulta'				  : fields.boolean('Consulta', readonly=True),
                'tarjeta_circulacion'	  : fields.boolean('Tarjeta de Criculacion', readonly=True),
                'folio_modalidad'		  : fields.integer('Folio Modalidad', readonly=True, size=10),
                'folio_tarjeta'			  : fields.char('No. de Folio TC', readonly=True),
                'fecha_tarjeta'			  : fields.date('Fecha de Tarjeta de Circulacion', readonly=True),
                'chatarrera_id'           : fields.many2one('res.partner','Chatarrera', readonly=True),
                'programacion_cita'       : fields.datetime('Fecha de Cita', readonly=True),
                'cita_anterior'           : fields.datetime('Fecha de Cita Anterior', readonly=True),
        }

    _defaults = {
        'state': 'borrador',
    }

    _sql_constraints = [('chatarra_unit_name_unique', 'unique(name)', 'La Placa ya existe')]
    
    _constraints = [(_check_unique_insesitive, 'La Placa ya existe', ['name'])]

    def action_disponible(self, cr, uid, ids, context=None):
        unidad = self.browse(cr, uid, ids)
        self.write(cr, uid, ids, {  'state':'disponible',
                                    'disponible_por':uid,
                                    'fecha_disponible':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                    'document_ids': [(0, 0, {'name':'visual', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'carta', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'consulta', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'copia_tc', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'factura_origen', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'factura_venta', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'factura_compra', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'foto_frente', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'foto_chasis', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'foto_motor', 'unit_id':unidad.id})
                                                     ]})
        return True

    def action_completo(self, cr, uid, ids, vals,context=None):
        unidad = self.browse(cr, uid, ids)
        for documento in unidad.document_ids:
            if documento.state in ('pendiente'):
                raise osv.except_osv(('Advertencia !'),
                       ('El documento %s esta en estado Pendiente...') % (documento.name)
                       )
        self.write(cr, uid, ids, {'state':'completo',
                                      'completo_por':uid,
                                      'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def action_recibir_consulta(self, cr, uid, ids, vals,context=None):
        unidad = self.browse(cr, uid, ids)
        self.write(cr, uid, ids, {'consulta': True})
        if unidad.tarjeta_circulacion == True and unidad.copia_tc == True:
        	self.write(cr, uid, ids, {'state':'recibido',
                                  'recibido_por': uid,
                                  'fecha_recibido':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_recibir_tarjeta(self, cr, uid, ids, vals,context=None):
    	unidad = self.browse(cr, uid, ids)
        self.write(cr, uid, ids, {'tarjeta_circulacion': True})
        if unidad.consulta == True and unidad.copia_tc == True:
        	self.write(cr, uid, ids, {'state':'recibido',
                                  'recibido_por': uid,
                                  'fecha_recibido':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_bloqueado(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'bloqueado',
                                  'bloqueado_por': uid,
                                  'fecha_bloqueado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_cita(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'cita',
                                  'cita_por': uid,
                                  'fecha_cita':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_exp_enviado(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'exp_enviado',
                                  'exp_enviado_por': uid,
                                  'fecha_exp_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_chatarrizado(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'chatarrizado',
                                  'chatarrizado_por': uid,
                                  'fecha_chatarrizado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_certificado(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'certificado',
                                  'certificado_por': uid,
                                  'fecha_certificado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_baja(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'baja',
                                  'baja_por': uid,
                                  'fecha_baja':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_cancelado(self, cr, uid, ids, vals,context=None):
        self.write(cr, uid, ids, {'state':'cancelado',
                                  'cancelado_por': uid,
                                  'fecha_cancelado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

chatarra_unit()