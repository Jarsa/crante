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
        'active': 'True',
    }
chatarra_motivo()

class chatarra_tarjeta_wizard(osv.osv):
    _name = 'chatarra.tarjeta'
    
    def onchange_date(self, cr, uid, ids, fecha, context=None):
        if datetime.strptime(fecha, DEFAULT_SERVER_DATE_FORMAT).date() > datetime.now().date():
            raise osv.except_osv(('Advertencia!'), ('La fecha es futura'))
            return { 'value': { 'fecha': False } }
        return fecha
        

    def _check_date(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if datetime.strptime(obj.fecha, DEFAULT_SERVER_DATE_FORMAT).date() > datetime.now().date():
            return False
        return True

    _columns = {
        'unit_id'   : fields.many2one('chatarra.unit','Unidad', readonly=True),
        'folio'     : fields.char('No. de Folio', required=True),
        'fecha'     : fields.date('Fecha', required=True),
        'modalidad' : fields.integer('Folio Modalidad', required=True, size=10),

    }

    _constraints = [(_check_date, '¡La fecha es futura!',['fecha'])]

    _defaults = {
        'fecha': lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
    }

    def recibir_tarjeta(self,cr,uid,ids,context=None):
        unidad_obj = self.pool.get('chatarra.unit')
        wiz = self.browse(cr,uid,ids)
        unit = wiz.unit_id
        unidad_obj.write(cr, uid, [unit.id], {'folio_tarjeta': wiz.folio,
                                              'fecha_tarjeta': wiz.fecha,
                                              'folio_modalidad': wiz.modalidad,
                                              'copia_tc': True,
                                              'copia_tc_por': uid,
                                              'fecha_copia_tc': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        if unit.tarjeta_circulacion == True and unit.tarjeta_circulacion == True:
            unidad_obj.write(cr, uid, [unit.id], {'state':'recibido',
                                  'recibido_por': uid,
                                  'fecha_recibido':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

chatarra_tarjeta_wizard()

class chatarra_cita(osv.osv):
    _name = 'chatarra.cita'
    _columns = {
        'fecha'         : fields.datetime('Fecha', required=True),
        'unidad_id'     : fields.many2one('chatarra.unit', 'Unidad', readonly=True),
        'chatarrera_id' : fields.many2one('res.partner', 'Chatarrera', required=True),
    }

    def action_programar_cita(self, cr, uid, ids, vals, context=None):
        unidad_obj = self.pool.get('chatarra.unit')
        cita = self.browse(cr, uid, ids)
        unidad = cita.unidad_id
        if unidad.programacion_cita == False:
            unidad_obj.write(cr, uid, [unidad.id], {'state':'cita',
                                                'cita_por': uid,
                                                'programacion_cita': cita.fecha,
                                                'chatarrera_id': cita.chatarrera_id.id,
                                                'fecha_cita':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        elif unidad.cita_anterior == False:
            unidad_obj.write(cr, uid, [unidad.id], {'cita_reprogramada_por': uid,
                                                    'cita_anterior':unidad.programacion_cita,
                                                    'programacion_cita': cita.fecha,
                                                    'chatarrera_id': cita.chatarrera_id.id,
                                                    'fecha_cita_reprogramada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        else:
            unidad_obj.write(cr, uid, [unidad.id], {'cita_reprogramada2_por': uid,
                                                    'cita_anterior2':unidad.cita_anterior,
                                                    'cita_anterior':unidad.programacion_cita,
                                                    'programacion_cita': cita.fecha,
                                                    'chatarrera_id': cita.chatarrera_id.id,
                                                    'fecha_cita_reprogramada2':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

chatarra_cita()

class chatarra_certificado_wizard(osv.osv):
    _name = 'chatarra.certificado'
    _columns = {
        'unit_id'       : fields.many2one('chatarra.unit','Unidad', readonly=True),
        'certificado'   : fields.char('No. de Certificado', required=True),
        'fecha'         : fields.date('Fecha', readonly=True),

    }

    def recibir_certificado(self,cr,uid,ids,context=None):
        unidad_obj = self.pool.get('chatarra.unit')
        wiz = self.browse(cr,uid,ids)
        unit = wiz.unit_id
        unidad_obj.write(cr, uid, [unit.id], {'certificado': wiz.certificado,
                                              'certificado_fecha': wiz.fecha,
                                              'certificado_por': uid,
                                              'fecha_certificado': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
chatarra_certificado_wizard()