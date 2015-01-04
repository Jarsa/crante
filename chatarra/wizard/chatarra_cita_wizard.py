# -*- encoding: utf-8 -*-
from openerp import models, fields, api
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class chatarra_cita_wizard(models.TransientModel):
    _name = 'chatarra.cita'
    
    name          = fields.Char(string='Nombre')
    fecha         = fields.Datetime(required=True)
    unidad_id     = fields.Many2one('chatarra.unit', string='Unidad', readonly=True)
    chatarrera_id = fields.Many2one('res.partner', string='Chatarrera', required=True)

    @api.one
    def action_programar_cita(self):
        unidad = self.unidad_id
        if unidad.programacion_cita == False:
            unidad.write({'state':'cita',
                          'cita_por': self.env.user.id,
                          'programacion_cita': self.fecha,
                          'chatarrera_id': self.chatarrera_id.id,
                          'fecha_cita':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        elif unidad.cita_anterior == False:
            unidad.write({'cita_reprogramada_por': self.env.user.id,
                          'cita_anterior':unidad.programacion_cita,
                          'programacion_cita': self.fecha,
                          'chatarrera_id': self.chatarrera_id.id,
                          'fecha_cita_reprogramada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        else:
            unidad.write({'cita_reprogramada2_por': self.env.user.id,
                          'cita_anterior2':unidad.cita_anterior,
                          'cita_anterior':unidad.programacion_cita,
                          'programacion_cita': self.fecha,
                          'chatarrera_id': self.chatarrera_id.id,
                          'fecha_cita_reprogramada2':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                }