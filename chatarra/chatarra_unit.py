# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare



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
                'name'              : fields.char('Placa',size=40),
                'state'             : fields.selection([
                                        ('borrador','Borrador'), 
                                        ('disponible','Disponible'), 
                                        ('asignada','Asignada'), 
                                        ('completa','Completa'), 
                                        ('enviado','Enviado a SCT'), 
                                        ('recibido','Recibido'), 
                                        ('actualizar','Actualizar'), 
                                        ('reposicion','Reposicion'), 
                                        ('enviado_agencia','Agencia'), 
                                        ('bloqueado','Bloqueado'), 
                                        ('cita','Cita'), 
                                        ('exp_enviado','Expediente Enviado'),
                                        ('chatarrizado','Chatarrizado'),
                                        ('certificado','Certificado Recibido'),
                                        ('baja','Baja'),
                                        ], 'Estado', readonly=True),
                'serie'             : fields.char('Número de serie', size=40),
                'marca'             : fields.many2one('chatarra.marca', 'Marca'),
                'modelo'            : fields.char('Modelo', size=40),
                'clase'             : fields.selection([('t2','T 2'),('t3','T 3'),('c2','C 2'),('c3','C 3')],'Clase'),
                'tipo'              : fields.many2one('chatarra.tipo','Tipo'),
                'motor'             : fields.char('Motor',size=40),
                'combustible'       : fields.selection([('diesel','Diesel'),('gasolina','Gasolina')],'Combustible'),
                'peso_vehicular'    : fields.float('Peso Vehicular'),
                'propietario_id'    : fields.many2one('res.partner','Nombre del Propietario'),
                'vat'               : fields.char('R.F.C.', size=6),
                'reg_fed'           : fields.char('Reg. Fed', size=40),
                'modalidad'         : fields.char('Modalidad', size=64),
                'no_ejes'           : fields.integer('Numero de ejes'),
                'no_llantas'        : fields.integer('Numero de llantas'),
                'cap_litros'        : fields.char('Litros', size=10),
                'cap_toneladas'     : fields.char('Toneladas', size=10),
                'cap_personas'      : fields.char('Personas', size=10),
                'alto'              : fields.float('Alto'),
                'ancho'             : fields.float('ancho'),
                'largo'             : fields.float('largo'),
                'eje_direccional'   : fields.char('Eje Direccional', size=10),
                'eje_motriz'        : fields.char('Eje Motriz', size=10),
                'eje_carga'         : fields.char('Eje Carga', size=10),
                'permiso_ruta'      : fields.char('Permiso de ruta', size=10),
                'lugar_exp'         : fields.char('Lugar de expedicion', size=10),
                'fecha_exp'         : fields.date('Fecha de expedicion'),
                'document_ids'      : fields.one2many('chatarra.documentos', 'unit_id', 'Documentos'),
                'asignacion_id'     : fields.many2one('chatarra.asignacion', 'No. de Asignacion:', readonly=True),
                'disponible_por'    : fields.many2one('res.users', 'Disponible por:', readonly=True),
                'fecha_disponible'  : fields.datetime('Fecha Disponible:', readonly=True),
                'asignada_por'      : fields.many2one('res.users', 'Asignado por:', readonly=True),
                'fecha_asignada'    : fields.datetime('Fecha Asignado:', readonly=True),
                'completa_por'      : fields.many2one('res.users', 'Doc. Completada por:', readonly=True),
                'fecha_completa'    : fields.datetime('Fecha Completada:', readonly=True),
                'enviado_por'       : fields.many2one('res.users', 'Enviado por:', readonly=True),
                'fecha_enviado'     : fields.datetime('Fecha Enviado:', readonly=True),
                'reposicion_por'    : fields.many2one('res.users', 'Reposicion por:', readonly=True),
                'fecha_reposicion'  : fields.datetime('Fecha Reposicion:', readonly=True),
                'repuesta_id'       : fields.many2one('chatarra.unit', 'Repuesta por:', readonly=True),
                'sustituye_id'      : fields.many2one('chatarra.unit', 'Sustituye a:', readonly=True),

        }

    _defaults = {
        'state': 'borrador',
    }

    _sql_constraints = [('chatarra_unit_name_unique', 'unique(name)', 'La Placa ya existe')]
    
    _constraints = [(_check_unique_insesitive, 'La Placa ya existe', ['name'])]
    
    def action_disponible(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {  'state':'disponible',
                                    'disponible_por':uid,
                                    'fecha_disponible':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def action_completa(self, cr, uid, ids, vals,context=None):
        if vals.get('document_ids'):
            count = len(vals.get('document_ids'))
            if count > 3:
                raise osv.except_osv(_('Warning!'), _('Limit to create 3 Lines'))
        self.write(cr, uid, ids, {  'state':'completa',
                                    'completa_por':uid,
                                    'fecha_completa':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

chatarra_unit()

class chatarra_unit_reposicion(osv.osv):
    _name = 'chatarra.unit.reposicion'
    _description = 'No. de Reposicion'
    _columns = {
        'name'               : fields.char('No. de Reposicion', size=64, readonly=True),
        'unidad_anterior_id' : fields.many2one('chatarra.unit','Unidad anterior:', readonly=True),
        'unidad_nueva_id'    : fields.many2one('chatarra.unit','Unidad nueva:'),
    }

    def action_reposicion(self, cr, uid, ids, vals, context=None):
        unidad_obj = self.pool.get('chatarra.unit')
        asignacion_obj = self.pool.get('chatarra.asignacion')
        reposicion = self.browse(cr, uid, ids)
        nueva = reposicion.unidad_nueva_id
        anterior = reposicion.unidad_anterior_id
        asignacion_obj.write(cr, uid, anterior.asignacion_id.id, {'unit_ids': [(4, nueva.id)]})
        unidad_obj.write(cr, uid, [nueva.id], {'sustituye_id':anterior.id, 'asignacion_id':anterior.asignacion_id.id})
        unidad_obj.write(cr, uid, [anterior.id], {'repuesta_id':nueva.id, 'state':'reposicion', 'reposicion_por':uid, 'fecha_reposicion':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    #def list_customers(self, cr, uid, ids, context):
    #sale_obj = self.pool.get('sale.order')
    #for sale in self.browse(cr, uid, ids, context):
    #    sale_ids = sale_obj.search(cr, uid, [('div_code_id','=',sale.div_code_id.id),('project_user','=',sale.project_id.id),('tower_id#','=',sale.tower_id.id)])
    #    ids_cus = []
    #    for cus in sale_obj.browse(cr, uid, sale_ids, context):
    #        if cus.partner_id.id not in ids_cus:
    #            ids_cus.append(cus.partner_id.id)
    #    self.write(cr, uid, ids, {'state_readonly':'listed','customer_ids': [(6, 0, ids_cus)]})
    #return True

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'reposicion.sequence.number')
        return super(chatarra_unit_reposicion, self).create(cr, uid, vals, context)









