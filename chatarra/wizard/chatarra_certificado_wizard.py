# -*- encoding: utf-8 -*-
from openerp import models, fields, api
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class chatarra_certificado_selfard(models.TransientModel):
    _name = 'chatarra.certificado'
    
    unit_id     = fields.Many2one('chatarra.unit',string='Unidad', readonly=True)
    certificado = fields.Char(string='No. de Certificado', required=True)
    fecha       = fields.Datetime(readonly=True)

    @api.one
    def recibir_certificado(self):
        unit = self.unit_id
        unit.write({'certificado': self.certificado,
                    'certificado_fecha': self.fecha,
                    'certificado_por': self.env.user.id,
                    'state': 'certificado',
                    'fecha_certificado': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }