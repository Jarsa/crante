# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import logging
_logger = logging.getLogger(__name__)


class chatarra_marca(osv.osv):
    _name = 'chatarra.marca'
    _columns = {
                'name': fields.char('Marca',size=40),
                'active': fields.boolean('Activo'),
        }
    _defaults = {
        'active': 'True',
    }
    
chatarra_marca()

class chatarra_tipo(osv.osv):
    _name = 'chatarra.tipo'
    _columns = {
                'name': fields.char('Tipo',size=40),
                'active': fields.boolean('Activo'),
        }
    _defaults = {
        'active': 'True',
    }
chatarra_tipo()

class chatarra_motivo(osv.osv):
    _name = 'chatarra.motivo'
    _columns = {
        'name'      : fields.char('Motivo', size=64, required=True),
        'active'    : fields.boolean('Activo'),
    }
    _defaults = {
        'active' : 'True',
    }
chatarra_motivo()

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
                'name'                 : fields.char('Placa',size=40),
                'state'                : fields.selection([
                                           ('borrador','Borrador'),
                                           ('disponible','Disponible'),
                                           ('asignada','Asignada'),
                                           ('elaboracion','Elaboracion de Expediente'),
                                           ('completo','Expediente Completo'),
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
                'serie'                : fields.char('Número de serie', size=40),
                'marca'                : fields.many2one('chatarra.marca', 'Marca'),
                'modelo'               : fields.char('Modelo', size=40),
                'color_placa'          : fields.char('Color de la Placa'),
                'tipo_placa'           : fields.selection([('carga','CARGA'),
                                                           ('pasaje','PASAJE'),
                                                           ('turismo','TURISMO')
                                                           ],'Tipo de Placa'),
                'clase'                : fields.selection([('t2','T 2'),('t3','T 3'),('c2','C 2'),('c3','C 3')],'Clase'),
                'tipo'                 : fields.many2one('chatarra.tipo','Tipo'),
                'motor'                : fields.char('Motor',size=40),
                'combustible'          : fields.selection([('diesel','Diesel'),('gasolina','Gasolina')],'Combustible'),
                'peso_vehicular'       : fields.float('Peso Vehicular'),
                'propietario_id'       : fields.many2one('res.partner','Nombre del Propietario'),
                'vat'                  : fields.char('R.F.C.', size=20),
                'reg_fed'              : fields.char('Reg. Fed', size=40),
                'modalidad'            : fields.char('Modalidad', size=64),
                'no_ejes'              : fields.integer('Numero de ejes'),
                'no_llantas'           : fields.integer('Numero de llantas'),
                'cap_litros'           : fields.char('Litros', size=10),
                'cap_toneladas'        : fields.char('Toneladas', size=10),
                'cap_personas'         : fields.char('Personas', size=10),
                'alto'                 : fields.float('Alto'),
                'ancho'                : fields.float('ancho'),
                'largo'                : fields.float('largo'),
                'eje_direccional'      : fields.char('Eje Direccional', size=10),
                'eje_motriz'           : fields.char('Eje Motriz', size=10),
                'eje_carga'            : fields.char('Eje Carga', size=10),
                'permiso_ruta'         : fields.char('Permiso de ruta', size=10),
                'lugar_exp'            : fields.char('Lugar de expedicion', size=10),
                'fecha_exp'            : fields.date('Fecha de expedicion'),
                'document_ids'         : fields.one2many('chatarra.documentos', 'unit_id', 'Documentos'),
                'asignacion_id'        : fields.many2one('chatarra.asignacion', 'No. de Asignacion:', readonly=True),
                'disponible_por'       : fields.many2one('res.users', 'Disponible por:', readonly=True),
                'fecha_disponible'     : fields.datetime('Fecha Disponible:', readonly=True),
                'asignada_por'         : fields.many2one('res.users', 'Asignado por:', readonly=True),
                'fecha_asignada'       : fields.datetime('Fecha Asignado:', readonly=True),
                'completo_por'         : fields.many2one('res.users', 'Expediente Completo por:', readonly=True),
                'fecha_completo'       : fields.datetime('Fecha Expediente Completo:', readonly=True),
                'enviado_por'          : fields.many2one('res.users', 'Enviado por:', readonly=True),
                'fecha_enviado'        : fields.datetime('Fecha Enviado:', readonly=True),
                'reposicion_por'       : fields.many2one('res.users', 'Reposicion por:', readonly=True),
                'fecha_reposicion'     : fields.datetime('Fecha Reposicion:', readonly=True),
                'facturado_por'        : fields.many2one('res.users', 'Facturado por:', readonly=True),
                'fecha_facturado'      : fields.datetime('Fecha Facturado:', readonly=True),
                'fact_cancelada_por'   : fields.many2one('res.users', 'Fact. Cancelada por:', readonly=True),
                'fecha_fact_cancelada' : fields.datetime('Fecha Cancelada:'),
                'repuesta_id'          : fields.many2one('chatarra.unit', 'Repuesta por:', readonly=True),
                'sustituye_id'         : fields.many2one('chatarra.unit', 'Sustituye a:', readonly=True),
                'reposicion_id'        : fields.many2one('chatarra.unit.reposicion', 'No. de Reposicion', readonly=True),
                'factura_id'           : fields.many2one('account.invoice', 'No. de Factura'),
                'facturado'            : fields.boolean('Facturado:', readonly=True),

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
                                                     (0, 0, {'name':'foto_motor', 'unit_id':unidad.id}),
                                                     (0, 0, {'name':'nueva_tc', 'unit_id':unidad.id})
                                                     ]})
        return True

    def action_completo(self, cr, uid, ids, vals,context=None):
        unidad = self.browse(cr, uid, ids)
        doc_obj = self.pool.get('chatarra.documentos')
        doc_visual = doc_obj.search(cr, uid, [('name','=','visual'),('unit_id','=',unidad.id)], count=True)
        if doc_visual == 0:
            raise osv.except_osv(('Advertencia!'), ('Falta Visual'))
        if doc_visual > 1:
            raise osv.except_osv(('Advertencia!'), ('Solo puede existir un Visual'))
        self.write(cr, uid, ids, {  'state':'completo',
                                    'completo_por':uid,
                                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

chatarra_unit()

class chatarra_unit_reposicion(osv.osv):
    _name = 'chatarra.unit.reposicion'
    _description = 'No. de Reposicion'
    _columns = {
        'name'               : fields.char('No. de Reposicion', size=64, readonly=True),
        'unidad_anterior_id' : fields.many2one('chatarra.unit','Unidad anterior:', readonly=True),
        'unidad_nueva_id'    : fields.many2one('chatarra.unit','Unidad nueva:', required=True),
        'date'               : fields.date('Fecha de reposicion', readonly=True),
        'motivo'             : fields.many2one('chatarra.motivo', 'Motivo', required=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def action_reposicion(self, cr, uid, ids, vals, context=None):
        unidad_obj = self.pool.get('chatarra.unit')
        invoice_obj = self.pool.get('account.invoice')
        asignacion_obj = self.pool.get('chatarra.asignacion')
        prod_obj = self.pool.get('product.product')
        prod_id = prod_obj.search(cr, uid, [('chatarra', '=', 1),('active','=', 1)], limit=1)
        product = prod_obj.browse(cr, uid, prod_id, context=None)
        reposicion = self.browse(cr, uid, ids)
        nueva = reposicion.unidad_nueva_id
        anterior = reposicion.unidad_anterior_id
        invoice_anterior_id = invoice_obj.search(cr, uid, [('unit_id','=',anterior.id)])
        invoice_anterior = invoice_obj.browse(cr, uid, invoice_anterior_id, context=None)
        _logger.error("##################### asignacion : %r", anterior.asignacion_id.id)
        invoice_obj.create(cr, uid, {'partner_id':anterior.asignacion_id.client_id.id,
                                     'contacto_id':anterior.asignacion_id.contacto_id.id,
                                     'agencia_id':anterior.asignacion_id.agencia_id.id,
                                     'asignacion_id':anterior.asignacion_id.id,
                                     'unit_id':nueva.id,
                                     'account_id':anterior.asignacion_id.client_id.property_account_receivable.id,
                                     'origin':(anterior.asignacion_id.name, reposicion.name),
                                     'fiscal_position':anterior.asignacion_id.client_id.property_account_position.id,
                                     'invoice_line':[(0,0,{'product_id':product.id,
                                                           'name':product.description_sale,
                                                           'account_id':product.property_account_income.id,
                                                           'quantity':'1',
                                                           'price_unit':product.lst_price,
                                                           'invoice_line_tax_id':[(6,0,[product.taxes_id.id])],
                                                          })]
                                    }, context=None)
        invoice_nueva_id = invoice_obj.search(cr, uid, [('unit_id','=',nueva.id)])
        invoice_nueva = invoice_obj.browse(cr, uid, invoice_nueva_id, context=None)
        unidad_obj.write(cr, uid, [nueva.id], {'sustituye_id':anterior.id,
                                               'reposicion_id':reposicion.id,
                                               'asignacion_id':anterior.asignacion_id.id,
                                               'facturado':True,
                                               'facturado_por':uid,
                                               'factura_id':invoice_nueva.id,
                                               'fecha_facturado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        unidad_obj.write(cr, uid, [anterior.id], {'repuesta_id':nueva.id,
                                                  'state':'reposicion',
                                                  'reposicion_id':reposicion.id,
                                                  'reposicion_por':uid,
                                                  'fact_cancelada_por':uid,
                                                  'fecha_fact_cancelada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                                  'fecha_reposicion':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        invoice_obj.write(cr, uid, [invoice_anterior.id], {'state':'cancel'})
        asignacion_obj.write(cr, uid, anterior.asignacion_id.id, {'unit_ids': [(4, nueva.id),(3, anterior.id)]})
        return True

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'reposicion.sequence.number')
        return super(chatarra_unit_reposicion, self).create(cr, uid, vals, context)









