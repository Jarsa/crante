# -*- encoding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import except_orm

class chatarra_product(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'
    
    categoria = fields.Selection([('no_chatarra','No Chatarra'),
                                  ('chatarra','Chatarra'),
                                  ('envio','Envio'),
                                  ('secretaria','Secretaria')], required=True, default='no_chatarra')

    @api.one
    @api.constrains('categoria')
    def _check_category(self):
        if self.categoria == 'chatarra':
            productos = self.search([('categoria', '=', 'chatarra'),('active', '=',True)])
            for producto in productos:
                if producto.id != self.id:
                    raise except_orm(_("Error !"),_("No puedes tener mas de un producto definido como Chatarra"))
        if self.categoria == 'envio':
            productos = self.search([('categoria', '=', 'envio'),('active', '=',True)])
            for producto in productos:
                if producto.id != self.id:
                    raise except_orm(_("Error !"),_("No puedes tener mas de un producto definido como Envio"))
        if self.categoria == 'secretaria':
            productos = self.search([('categoria', '=', 'secretaria'),('active', '=',True)])
            for producto in productos:
                if producto.id != self.id:
                    raise except_orm(_("Error !"),_("No puedes tener mas de un producto definido como Secretaria"))
        return True