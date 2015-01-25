# -*- encoding: utf-8 -*-
from openerp import fields, models

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    categoria = fields.Selection([
                    ('none', 'N/A'),
                    ('agencia','Agencia'),
                    ('paqueteria','Paqueteria'),
                    ('secretaria','Secretaria'),
                    ('chatarrera','Chatarrera'),
                    ('gestor','Gestor'),
                    ('proveedor_visual','Proveedor Visual')
                ], default='none')
    agencia = fields.Boolean()
    secretaria = fields.Boolean()
    paqueteria = fields.Boolean()
    chatarrera = fields.Boolean()
    gestor = fields.Boolean()
    proveedor_visual = fields.Boolean()