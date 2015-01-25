# -*- encoding: utf-8 -*-
from openerp import models, fields, api
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class chatarra_certificado_wizard(models.TransientModel):
    _name = 'chatarra.detalle'
    
    unit_id = fields.Many2one('chatarra.unit', string='Unidad', readonly=True)
    motivo_id = fields.Many2one('chatarra.motivo', string='Motivo', required=True)

    @api.one
    def action_detalle(self):
        unit_obj = self.env['chatarra.unit']
        unit = unit_obj.search([('name', '=', self.unit_id.name)])
        unit.write({'motivo_detalle': self.motivo_id.id,
                    'detalle_por': self.env.user.id,
                    'state': 'detalle',
                    'fecha_detalle': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
