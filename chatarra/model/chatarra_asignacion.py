# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import except_orm

class chatarra_asignacion(models.Model):
    _name = 'chatarra.asignacion'
    _description = 'Asignacion'

    name             = fields.Char('No. de Asignacion', size=64, readonly='True')
    state            = fields.Selection([
                                        ('borrador','Borrador'),
                                        ('confirmado','Confirmado'),
                                        ('pagado','Pagado'),
                                        ('cerrado','Cerrado'),
                                        ], readonly=True, default='borrador')
    client_id        = fields.Many2one('res.partner', string='Cliente', required=True)
    contacto_id      = fields.Many2one('res.partner', string='Contacto', required=True)
    agencia_id       = fields.Many2one('res.partner', string='Agencia', required=True)
    unit_ids         = fields.Many2many('chatarra.unit', string='Unidades', required=True)
    confirmado_por   = fields.Many2one('res.users', readonly=True)
    cantidad         = fields.Integer(compute='_get_total_quantity', string='No. de Unidades', readonly=True)
    fecha_confirmado = fields.Datetime(readonly=True)

    @api.one
    @api.depends('unit_ids')
    def _get_total_quantity(self):
        if not self.unit_ids:
            self.cantidad = 0
        else:
            self.cantidad = len(self.unit_ids)

    @api.onchange('contacto_id')
    def asign_agencia(self):
        self.agencia_id = self.contacto_id.parent_id.id

    @api.multi
    def _asignar_unidad(self, asignacion):
        unit_obj = self.env['chatarra.unit']
        if asignacion == True:
            asignacion = self
        units = unit_obj.search([('asignacion_id', '=', asignacion.id),('state', '=', 'por_asignar')])
        if units:
            units.write({'asignacion_id': False,
                         'client_id': False,
                         'state':'disponible',
                         'asignada_por': False,
                         'fecha_asignada': False})
        for unit in asignacion.unit_ids:
            unit.write({'asignacion_id':asignacion.id,
                        'state':'por_asignar',
                        'client_id':asignacion.client_id.id,
                        'asignada_por':asignacion.env.user.id,
                        'fecha_asignada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.multi
    def write(self, vals):
        asignacion = super(chatarra_asignacion, self).write(vals)
        self._asignar_unidad(asignacion)
        return asignacion

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_id(self.env.ref('chatarra.sequence_chatarra_asignacion').id)
        asignacion = super(chatarra_asignacion, self).create(vals)
        self._asignar_unidad(asignacion)
        return asignacion

    @api.multi
    def unlink(self):
        for asignacion in self:
            for unit in asignacion.unit_ids:
                if unit:
                    raise except_orm(_('Error'),_('No se puede borrar una asignacion con unidades (%s)') % unit.name)
        return super(chatarra_asignacion, self).unlink()

    @api.one
    def action_confirmado(self):
        self.write({'state':'confirmado',
                    'confirmado_por':self.env.user.id,
                    'fecha_confirmado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        asignacion = self
        invoice_obj = self.env['account.invoice']
        fpos_obj = self.env['account.fiscal.position']
        prod_obj = self.env['product.product']
        unidad_obj = self.env['chatarra.unit']
        product = prod_obj.search([('categoria', '=', 'chatarra'),('active','=', 1)], limit=1)
        prod_account = product.product_tmpl_id.property_account_expense.id
        if not prod_account:
            prod_account = product.categ_id.property_account_expense_categ.id
            if not prod_account:
                raise except_orm(_('Error'),_('There is no expense account defined for this product: "%s" (id:%d)') % (product.name, product.id,))
        prod_account = fpos_obj.map_account(prod_account)
        if not product:
            raise except_orm(_('Falta configuracion'),_('No existe un producto definido como chatarra !!!'))
        for unidad in asignacion.unit_ids:
            invoice_obj.create({'partner_id':asignacion.client_id.id,
                                'contacto_id':asignacion.contacto_id.id,
                                'agencia_id':asignacion.agencia_id.id,
                                'asignacion_id':asignacion.id,
                                'unit_id':unidad.id,
                                'account_id':asignacion.client_id.property_account_receivable.id,
                                'origin':asignacion.name,
                                'fiscal_position':asignacion.client_id.property_account_position.id,
                                'invoice_line':[(0,0,{'product_id':product.id,
                                                      'name':'Marca: ' + unidad.marca_id.name + '\nSerie: ' + unidad.serie + '\nPlacas: ' + unidad.name,
                                                      'account_id':prod_account,
                                                      'quantity':'1',
                                                      'price_unit':product.lst_price,
                                                      'invoice_line_tax_id':[(6,0,[x.id for x in product.taxes_id])],
                                                      })]
                                        })
            invoice = invoice_obj.search([('unit_id','=',unidad.id),('type','=','out_invoice'),('state','=','draft')])
            unidad.write({'facturado_por':self.env.user.id,
                          'fecha_facturado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                          'factura_id':invoice.id,
                          'facturado':True,
                          'state':'asignada'
                          })