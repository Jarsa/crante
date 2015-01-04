# -*- encoding: utf-8 -*-
from openerp import models, fields, _, api
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import except_orm

class chatarra_unit_reposicion(models.Model):
    _name = 'chatarra.reposicion'
    _description = 'No. de Reposicion'
    
    name               = fields.Char(string='No. de Reposicion', readonly=True)
    unidad_anterior_id = fields.Many2one('chatarra.unit', string='Unidad anterior:', readonly=True)
    unidad_nueva_id    = fields.Many2one('chatarra.unit', string='Unidad nueva:', required=True)
    date               = fields.Date('Fecha de reposicion', readonly=True, default=lambda *a: time.strftime('%Y-%m-%d'))
    motivo_id          = fields.Many2one('chatarra.motivo', string='Motivo', required=True)

    @api.one
    def action_reposicion(self):
        invoice_obj = self.env['account.invoice']
        fpos_obj = self.env['account.fiscal.position']
        doc_obj = self.env['chatarra.documentos']
        prod_obj = self.env['product.product']
        product = prod_obj.search([('categoria', '=', 'chatarra'),('active','=', 1)], limit=1)
        prod_account = product.product_tmpl_id.property_account_expense.id
        if not prod_account:
            prod_account = product.categ_id.property_account_expense_categ.id
            if not prod_account:
                raise except_orm(_('Error'),_('There is no expense account defined for this product: "%s" (id:%d)') % (product.name, product.id,))
        prod_account = fpos_obj.map_account(prod_account)
        nueva = self.unidad_nueva_id
        anterior = self.unidad_anterior_id
        doc = doc_obj.search([('unit_id','=',anterior.id)])
        invoice_anterior = invoice_obj.search([('unit_id','=',anterior.id)])
        invoice_obj.create({'partner_id':anterior.client_id.id,
                            'contacto_id':anterior.asignacion_id.contacto_id.id,
                            'agencia_id':anterior.asignacion_id.agencia_id.id,
                            'asignacion_id':anterior.asignacion_id.id,
                            'unit_id':nueva.id,
                            'account_id':anterior.client_id.property_account_receivable.id,
                            'origin':anterior.asignacion_id.name + '/' + reposicion.name,
                            'fiscal_position':anterior.asignacion_id.client_id.property_account_position.id,
                            'invoice_line':[(0,0,{'product_id':product.id,
                                                  'name':'Marca: ' + nueva.marca.name + '\nSerie: ' + nueva.serie + '\nPlacas: ' + nueva.name,
                                                  'account_id':prod_account,
                                                  'quantity':'1',
                                                  'price_unit':product.lst_price,
                                                  'invoice_line_tax_id':[(6,0,[x.id for x in product.taxes_id])],
                                                  })]
                                    })
        invoice_nueva = invoice_obj.search([('unit_id','=',nueva.id),('type','=','out_invoice')])
        for document in doc:
            document.write({'state':'cancelado'})
        nueva.write({'sustituye_id':anterior.id,
                     'reposicion_id':self.id,
                     'state':'asignada',
                     'client_id':anterior.client_id.id,
                     'asignacion_id':anterior.asignacion_id.id,
                     'facturado':True,
                     'facturado_por':self.env.user.id,
                     'factura_id':invoice_nueva.id,
                     'fecha_facturado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        if anterior.state in ['asignada','completo','seleccion','enviado']:
            anterior.write({'repuesta_id':nueva.id,
                            'state':'reposicion',
                            'reposicion_id':self.id,
                            'reposicion_por':self.env.user.id,
                            'fact_cancelada_por':self.env.user.id,
                            'fecha_fact_cancelada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                            'fecha_reposicion':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        else:
            anterior.write({'repuesta_id':nueva.id,
                            'state':'desestimiento',
                            'reposicion_id':self.id,
                            'reposicion_por':self.env.user.id,
                            'fact_cancelada_por':self.env.user.id,
                            'fecha_fact_cancelada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                            'fecha_reposicion':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        for invoice in invoice_anterior:
            invoice.signal_workflow('invoice_cancel')
        anterior.asignacion_id.write({'unit_ids': [(4, nueva.id),(3, anterior.id)]})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_id(self.env.ref('chatarra.sequence_unit_reposicion_number').id)
        reposicion = super(chatarra_reposicion, self).create(vals)
        return reposicion