# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class chatarra_certificado_wizard(osv.TransientModel):
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
                                              'state': 'certificado',
                                              'fecha_certificado': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }