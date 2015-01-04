# -*- encoding: utf-8 -*-
from openerp import models, fields

class chatarra_marca(models.Model):
    _name = 'chatarra.marca'
    _description = 'Marca'
    name = fields.Char(string='Marca', size=40, required=True)
    active = fields.Boolean(sting='Activo', default=True)