# -*- encoding: utf-8 -*-
from openerp import models, fields

class chatarra_invoice(models.Model):
    _inherit = 'account.invoice'
    asignacion_id = fields.Many2one('chatarra.asignacion', string='No. de Asignacion', readonly=True)
    unit_id = fields.Many2one('chatarra.unit', string='Unidad', readonly=True)
    agencia_id = fields.Many2one('res.partner',string='Agencia', readonly=True)
    contacto_id	= fields.Many2one('res.partner',string='Contacto', readonly=True)