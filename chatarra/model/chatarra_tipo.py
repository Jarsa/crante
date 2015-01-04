# -*- encoding: utf-8 -*-
from openerp import fields, models

class chatarra_tipo(models.Model):
    _name = 'chatarra.tipo'
    _description = 'Tipo'
    
    name   = fields.Char(string='Tipo', required=True)
    active = fields.Boolean(string='Activo', default=True)