# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class chatarra_documentos(models.Model):
    _name = 'chatarra.documentos'
    _description = 'Documentos'

    name = fields.Selection([('visual','Visual'),
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
    unit_id = fields.Many2one('chatarra.unit', string='Placa', required=True)
    imagen = fields.Binary()
    state = fields.Selection([('pendiente','Pendiente'),
                             ('completo','Completo'),
                             ('no_requerido','No Requerido'),
                             ('cancelado','Cancelado'),
                             ('revision_1', 'Revision 1'),
                             ('revision_2', 'Revision 2'),
                             ], 'Estado', readonly='True', default='pendiente')
    completo_por = fields.Many2one('res.users', string='Completo por', readonly=True)
    fecha_completo = fields.Datetime(string='Fecha completo', readonly=True)
    revision_1_por = fields.Many2one('res.users', string='Revision 1 por', readonly=True)
    fecha_revision_1 = fields.Datetime(string='Fecha Revision 1', readonly=True)
    revision_2_por = fields.Many2one('res.users', string='Revision 2 por', readonly=True)
    fecha_revision_2 = fields.Datetime(string='Fecha Revision 2', readonly=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente', readonly=True)
    completo = fields.Boolean(readonly=True)
    revision_1 = fields.Boolean(readonly=True)
    revision_2 = fields.Boolean(readonly=True)

    @api.one
    def action_completo(self):
        self.write({'state':'completo',
                    'completo_por': self.env.user.id,
                    'fecha_completo': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'completo': True,
                    })

    @api.one
    def action_revision_1(self):
        print "DEBERIA ESTAR FUNCIONANDO"
        self.write({'state':'revision_1',
                    'revision_1_por': self.env.user.id,
                    'fecha_revision_1': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'revision_1': True,
                    })

    @api.one
    def action_revision_2(self):
        self.write({'state':'revision_2',
                    'revision_2_por':self.env.user.id,
                    'fecha_revision_2':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'revision_2': True,
                    })

    @api.one
    def action_no_requerido(self):
        self.write({'state':'no_requerido',
                    'completo_por':self.env.user.id,
                    'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'completo': True,
                    'revision_1': True,
                    'revision_2': True,
                    })

    @api.multi
    def write(self, vals):
        unidad = self.unit_id
        super(chatarra_documentos, self).write(vals)
        for document in unidad.document_ids:
            if document.state in ('pendiente'):
                return False
        unidad.write({'expediente_completo': True,
                      'completo_por': self.env.user.id,
                      'fecha_completo': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
