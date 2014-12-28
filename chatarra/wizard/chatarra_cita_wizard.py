# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class chatarra_cita_wizard(osv.TransientModel):
    _name = 'chatarra.cita'
    _columns = {
        'name'          : fields.char('Nombre'),
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
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }