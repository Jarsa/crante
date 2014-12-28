# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class chatarra_tarjeta_wizard(osv.TransientModel):
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
        return { 'type' :  'ir.actions.act_close_wizard_and_reload_view' }
        # return {
        #         'type': 'ir.actions.client',
        #         'tag': 'reload',
        #         }