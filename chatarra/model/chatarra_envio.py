# -*- encoding: utf-8 -*-
from openerp import models, fields, _, api
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import except_orm

class chatarra_envio(models.Model):
    _name = 'chatarra.envio'
    _description = 'Envios'
    
    name          = fields.Char(sting='No. de envio', readonly=True)
    state         = fields.Selection([
                            ('borrador','Borrador'),
                            ('enviado','Enviado')
                            ],'Estado', readonly=True, default='borrador')
    guia          = fields.Char(required=True)
    paqueteria_id = fields.Many2one('res.partner', string='Paqueteria', required=True)
    secretaria_id = fields.Many2one('chatarra.secretaria', sting='Secretaria', required=True)
    contacto_id   = fields.Many2one('res.partner', string='Contacto', required=True)
    unit_ids      = fields.Many2many('chatarra.unit', string='Unidades', required=True)
    enviado_por   = fields.Many2one('res.users', readonly=True)
    fecha_enviado = fields.Datetime(readonly=True)
    gestor_id     = fields.Many2one('res.partner', string='Gestor')

    @api.multi
    def _seleccionar_unidad(self, envio):
        unit_obj = self.env['chatarra.unit']
        if envio == True:
            envio = self
        units = unit_obj.search([('envio_id', '=', envio.id),('state', '=', 'seleccion')])
        if units:
            units.write({'envio_id': False,
                         'state':'completo',
                         'guia': False,
                         'paqueteria_id': False,
                         'gestor_id': False,
                         'contacto_id': False,
                         'secretaria_id': False,})
        for unit in envio.unit_ids:
            unit.write({'envio_id':envio.id,
                        'state':'seleccion',
                        'guia':envio.guia,
                        'paqueteria_id':envio.paqueteria_id.id,
                        'secretaria_id':envio.secretaria_id.id,
                        'contacto_id':envio.contacto_id.id,
                        'gestor_id':envio.gestor_id.id,})

    @api.multi
    def write(self, vals):
        envio = super(chatarra_envio, self).write(vals)
        self._seleccionar_unidad(envio)
        return envio

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_id(self.env.ref('chatarra.sequence_chatarra_envio').id)
        envio = super(chatarra_envio, self).create(vals)
        self._seleccionar_unidad(envio)
        return envio

    @api.multi
    def unlink(self):
        for envio in self:
            for unit in envio.unit_ids:
                if unit:
                    raise except_orm(_('Error'),_('No se puede borrar un envio con unidades (%s)') % unit.name)
        return super(chatarra_envio, self).unlink()

    @api.one
    def enviar_unidad(self):
        envio = self
        unit_obj = self.env['chatarra.unit']
        invoice_obj = self.env['account.invoice']
        fpos_obj = self.env['account.fiscal.position']
        prod_obj = self.env['product.product']
        product = prod_obj.search([('categoria', '=', 'envio'),('active','=', 1)], limit=1)
        product2 = prod_obj.search([('categoria', '=', 'secretaria'),('active','=', 1)], limit=1)
        prod_account = product.product_tmpl_id.property_account_expense.id
        if not prod_account:
            prod_account = product.categ_id.property_account_expense_categ.id
        if not prod_account:
            raise except_orm(_('Error'),_('There is no expense account defined for this product: "%s" (id:%d)') % (product.name, product.id,))
        prod_account = fpos_obj.map_account(prod_account)
        prod_account2 = product2.product_tmpl_id.property_account_expense.id
        if not prod_account2:
            prod_account2 = product2.categ_id.property_account_expense_categ.id
            if not prod_account2:
                raise except_orm(_('Error'),_('There is no expense account defined for this product: "%s" (id:%d)') % (product2.name, product2.id,))
        prod_account2 = fpos_obj.map_account(prod_account)
        journal_obj = self.env['account.journal']
        journal = journal_obj.search([('type', '=', 'purchase')], limit=1)
        invoice_obj.create({'partner_id':envio.paqueteria_id.id,
                            'account_id':envio.paqueteria_id.property_account_payable.id,
                            'origin':envio.name,
                            'type':'in_invoice',
                            'journal_id':journal.id,
                            'fiscal_position':envio.paqueteria_id.property_account_position.id,
                            'invoice_line':[(0,0,{'product_id':product.id,
                                                  'name':'Envio: ' + envio.name + '\nNo. de Guia: ' + envio.guia + '\nPaqueteria: ' + envio.paqueteria_id.name + '\nSecretaria: ' + envio.secretaria_id.name,
                                                  'account_id':prod_account,
                                                  'quantity':'1',
                                                  'price_unit':product.lst_price,
                                                  'invoice_line_tax_id':[(6,0,[x.id for x in product.supplier_taxes_id])],
                                                  })]
                                  })
        for unidad in envio.unit_ids:
            invoice_obj.create({'partner_id':envio.contacto_id.id,
                                'account_id':envio.contacto_id.property_account_payable.id,
                                'origin':envio.name + '/' + envio.secretaria_id.name + '/' + envio.contacto_id.name + '/' + unidad.name,
                                'type':'in_invoice',
                                'journal_id':journal.id,
                                'fiscal_position':envio.contacto_id.property_account_position.id,
                                'unit_id':unidad.id,
                                'invoice_line':[(0,0,{'product_id':product2.id,
                                                      'name':'Envio: ' + envio.name + '\nNo. de Guia: ' + envio.guia + '\nPaqueteria: ' + envio.paqueteria_id.name + '\nSecretaria: ' + envio.secretaria_id.name + '\nContacto: ' + envio.contacto_id.name,
                                                      'account_id':prod_account2,
                                                      'quantity':'1',
                                                      'price_unit':product2.lst_price,
                                                      'invoice_line_tax_id':[(6,0,[x.id for x in product2.supplier_taxes_id])],
                                                      })]
                                        })
            if envio.gestor_id:
                invoice_obj.create({'partner_id':envio.gestor_id.id,
                                    'account_id':envio.gestor_id.property_account_payable.id,
                                    'origin':envio.name + '/' + envio.secretaria_id.name + '/' + envio.gestor_id.name + '/' + unidad.name,
                                    'type':'in_invoice',
                                    'journal_id':journal.id,
                                    'fiscal_position':envio.gestor_id.property_account_position.id,
                                    'unit_id':unidad.id,
                                    'invoice_line':[(0,0,{'product_id':product2.id,
                                                          'name':'Envio: ' + envio.name + '\nNo. de Guia: ' + envio.guia + '\nPaqueteria: ' + envio.paqueteria_id.name + '\nGestor: ' + envio.gestor_id.name,
                                                          'account_id':prod_account2,
                                                          'quantity':'1',
                                                          'price_unit':product2.lst_price,
                                                          'invoice_line_tax_id':[(6,0,[x.id for x in product2.supplier_taxes_id])],
                                                          })]
                                            })
            self.write({'state':'enviado',
                        'enviado_por':self.env.user.id,
                        'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
            for unidad in envio.unit_ids:
                unidad.write({'envio_id':envio.id,
                              'state':'enviado',
                              'guia':envio.guia,
                              'enviado_por':self.env.user.id,
                              'paqueteria_id':envio.paqueteria_id.id,
                              'secretaria_id':envio.secretaria_id.id,
                              'gestor_id':envio.gestor_id.id,
                              'contacto_id':envio.contacto_id.id,
                              'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def send_envio_mail(self, cr, uid):
        envios_id = self.search(cr, uid, [])
        email_template_obj = self.pool.get('email.template')
        template = email_template_obj.search(cr, uid, [('model_id.model', '=','chatarra.envio')]) 
        for envio in envios_id:
            email_template_obj.send_mail(cr, uid, template[0], envio)
        return True