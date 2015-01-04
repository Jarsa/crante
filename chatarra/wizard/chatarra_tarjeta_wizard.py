# -*- encoding: utf-8 -*-
from openerp import models, fields, api
import time
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class chatarra_tarjeta_wizard(models.TransientModel):
    _name = 'chatarra.tarjeta'
    _rec_name = 'folio'
    
    unit_id   = fields.Many2one('chatarra.unit', string='Unidad', readonly=True)
    folio     = fields.Char(string='No. de Folio', required=True)
    fecha     = fields.Date(required=True, default=lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
    modalidad = fields.Integer(string='Folio Modalidad', required=True, size=10)

    @api.onchange('fecha')
    def onchange_date(self):
        if datetime.strptime(self.fecha, DEFAULT_SERVER_DATE_FORMAT).date() > datetime.now().date():
            return {
                        'warning': {
                            'title': "Error",
                            'message': "La fecha es futura",
                        }
                    }

    @api.one
    @api.constrains('fecha')
    def _check_date(self):
        if datetime.strptime(self.fecha, DEFAULT_SERVER_DATE_FORMAT).date() > datetime.now().date():
            return False

    @api.one
    def recibir_tarjeta(self):
        unit = self.unit_id
        unit.write({'folio_tarjeta': self.folio,
                    'fecha_tarjeta': self.fecha,
                    'folio_modalidad': self.modalidad,
                    'copia_tc': True,
                    'copia_tc_por': self.env.user.id,
                    'fecha_copia_tc': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        if unit.tarjeta_circulacion == True and unit.tarjeta_circulacion == True:
            unit.write({'state':'recibido',
                       'recibido_por': self.env.user.id,
                       'fecha_recibido':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
#         return {
#             'type': 'ir.actions.client',
#             'tag': 'chatarra_unit_enviado_sct_tree',
#             'params': {'wait': True},
# }
        return { 'type' :  'ir.actions.act_close_wizard_and_reload_view' }
        # return {
        #         'type': 'ir_actions_act_window',
        #         'tag': 'reload',
        #         }