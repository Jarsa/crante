# -*- encoding: utf-8 -*-
from openerp import models, fields

class chatarra_motivo(models.Model):
    _name = 'chatarra.motivo'
    _description = 'Motivo'
    name = fields.Char(string='Motivo', size=64, required=True)
    active = fields.Boolean(string='Activo', default=True)