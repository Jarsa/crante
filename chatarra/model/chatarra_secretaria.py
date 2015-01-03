# -*- encoding: utf-8 -*-
from openerp import models, fields

class chatarra_secretaria(models.Model):
    _name = 'chatarra.secretaria'
    _description = 'Secretaria'
    name = fields.Char(string='Secretaria', size=40, required=True)
    active = fields.Boolean(sting='Activo', default=True)