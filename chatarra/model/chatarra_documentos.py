# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class chatarra_documentos(models.Model):
    _name = 'chatarra.documentos'
    _description = 'Documentos'

    name           = fields.Selection([
                                    ('visual','Visual'),
                                    ('carta','Carta de Asignacion'),
                                    ('consulta','Consulta'),
                                    ('copia_tc','Tarjeta de Circulacion Prop. Anterior'),
                                    ('factura_origen','Factura de origen'),
                                    ('factura_venta','Factura de venta'),
                                    ('factura_compra','Factura de compra'),
                                    ('foto_frente','Foto frente'),
                                    ('foto_chasis','Foto chasis'),
                                    ('foto_motor','Foto motor')
                                    ], string='Tipo de Documento', required=True)
    unit_id        =fields.Many2one('chatarra.unit', string='Placa', required=True)
    imagen         =fields.Binary()
    state          =fields.Selection([
                                    ('pendiente','Pendiente'),
                                    ('completo','Completo'),
                                    ('no_requerido','No Requerido'),
                                    ('cancelado','Cancelado'),
                                    ], 'Estado', readonly='True', default='pendiente')
    completo_por   = fields.Many2one('res.users', string='Completo por', readonly=True)
    fecha_completo = fields.Datetime(string='Fecha completo:', readonly=True)

    @api.one
    def action_completo(self):
        self.write({'state':'completo',
                    'completo_por':self.env.user.id,
                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    })

    @api.one
    def action_no_requerido(self):
        self.write({'state':'no_requerido',
                    'completo_por':self.env.user.id,
                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    })