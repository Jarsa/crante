# -*- encoding: utf-8 -*-
from openerp import models, fields, _, api
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import except_orm

class chatarra_unit(models.Model):
    _name = 'chatarra.unit'
    _description = 'Unidad'

    name                     = fields.Char(string='Placa', size=10, required=True)
    state                    = fields.Selection([
                                                ('borrador','Borrador'),
                                                ('disponible','Disponible'),
                                                ('por_asignar','Seleccionado para Asignacion'),
                                                ('asignada','Asignada'),
                                                ('completo','Expediente Completo'),
                                                ('seleccion','Seleccionado para Envio'),
                                                ('enviado','Enviado a SCT'),
                                                ('recibido','Recibido'),
                                                ('consulta','Consulta'),
                                                ('reposicion','Reposicion'),
                                                ('bloqueado','Bloqueado'),
                                                ('cita','Cita'),
                                                ('exp_enviado','Expediente Enviado'),
                                                ('chatarrizado','Chatarrizado'),
                                                ('certificado','Certificado Recibido'),
                                                ('baja','Baja'),
                                                ('cancelado','Cancelado'),
                                                ('desestimiento','Desestimiento'),
                                                ], readonly=True, default='borrador')
    client_id                = fields.Many2one('res.partner', string='Cliente', readonly=True)
    supplier_id              = fields.Many2one('res.partner', string='Proveedor', required=True)
    serie                    = fields.Char(string='Numero de serie', size=40, required=True)
    marca_id                 = fields.Many2one('chatarra.marca', string='Marca', required=True)
    modelo                   = fields.Char(required=True)
    color_placa              = fields.Char(string='Color de la Placa', required=True)
    tipo_placa               = fields.Selection([('carga','CARGA'),
                                                ('pasaje','PASAJE'),
                                                ('turismo','TURISMO'),
                                                ], string='Tipo de Placa', required=True)
    clase                    = fields.Selection([('t2','T 2'),
                                                ('t3','T 3'),
                                                ('c2','C 2'),
                                                ('c3','C 3'),
                                                ], string='Clase', required=True)
    tipo_id                  = fields.Many2one('chatarra.tipo', string='Tipo', required=True)
    motor                    = fields.Char(required=True)
    combustible              = fields.Selection([('diesel','Diesel'),
                                                ('gasolina','Gasolina')
                                                ], required=True)
    peso_vehicular           = fields.Float(required=True)
    rfc                      = fields.Char(string='R.F.C.', size=13, required=True)
    modalidad                = fields.Char(required=True)
    no_ejes                  = fields.Integer(string='Numero de ejes', required=True)
    no_llantas               = fields.Integer(string='Numero de llantas', required=True)
    cap_litros               = fields.Char(string='Litros', size=10, required=True)
    cap_toneladas            = fields.Char(string='Toneladas', size=10, required=True)
    cap_personas             = fields.Char(string='Personas', size=10, required=True)
    alto                     = fields.Float(required=True)
    ancho                    = fields.Float(required=True)
    largo                    = fields.Float(required=True)
    eje_direccional          = fields.Char(required=True)
    eje_motriz               = fields.Char(required=True)
    eje_carga                = fields.Char(required=True)
    permiso_ruta             = fields.Char(string='Permiso de ruta', required=True)
    lugar_exp                = fields.Char(string='Lugar de expedicion', required=True)
    fecha_exp                = fields.Date(string='Fecha de expedicion', required=True)
    document_ids             = fields.One2many('chatarra.documentos', 'unit_id', string='Documentos', readonly=True)
    asignacion_id            = fields.Many2one('chatarra.asignacion', string='No. de Asignacion', readonly=True)
    desasignado_por          = fields.Many2one('res.users', string='Desasignado por', readonly=True)
    fecha_desasignado        = fields.Datetime(string='Fecha Desasignado', readonly=True)
    asignacion2_id           = fields.Many2one('chatarra.asignacion', string='Asignacion anterior', readonly=True)
    desasignado2_por         = fields.Many2one('res.users', string='Desasignado 2 por', readonly=True)
    fecha_desasignado2       = fields.Datetime(string='Fecha Desasignado 2', readonly=True)
    asignacion3_id           = fields.Many2one('chatarra.asignacion', string='Asignacion anterior 2', readonly=True)
    disponible_por           = fields.Many2one('res.users', string='Disponible por', readonly=True)
    fecha_disponible         = fields.Datetime(string='Fecha Disponible', readonly=True)
    asignada_por             = fields.Many2one('res.users', string='Asignado por', readonly=True)
    fecha_asignada           = fields.Datetime(string='Fecha Asignado', readonly=True)
    completo_por             = fields.Many2one('res.users', string='Expediente Completo por', readonly=True)
    fecha_completo           = fields.Datetime(string='Fecha Expediente Completo', readonly=True)
    enviado_por              = fields.Many2one('res.users', string='Enviado por', readonly=True)
    fecha_enviado            = fields.Datetime(string='Fecha Enviado', readonly=True)
    consulta_por             = fields.Many2one('res.users', string='Consulta por', readonly=True)
    fecha_consulta           = fields.Datetime(string='Fecha Consulta', readonly=True)
    tc_por                   = fields.Many2one('res.users', string='TC por', readonly=True)
    fecha_tc                 = fields.Datetime(string='Fecha TC', readonly=True)
    copia_tc_por             = fields.Many2one('res.users', string='Copia TC por', readonly=True)
    fecha_copia_tc           = fields.Datetime(string='Fecha Copia TC', readonly=True)
    recibido_por             = fields.Many2one('res.users', string='Recibido por', readonly=True)
    fecha_recibido           = fields.Datetime(string='Fecha Recibido', readonly=True)
    bloqueado_por            = fields.Many2one('res.users', string='Bloqueado por', readonly=True)
    fecha_bloqueado          = fields.Datetime(string='Fecha Bloqueado', readonly=True)
    cita_por                 = fields.Many2one('res.users', string='Cita por', readonly=True)
    fecha_cita               = fields.Datetime(string='Fecha Cita', readonly=True)
    cita_reprogramada_por    = fields.Many2one('res.users', string='Cita Reprogramada por', readonly=True)
    fecha_cita_reprogramada  = fields.Datetime(string='Fecha Cita Reprogramada', readonly=True)
    cita_reprogramada2_por   = fields.Many2one('res.users', string='Cita Reprogramada 2 por', readonly=True)
    fecha_cita_reprogramada2 = fields.Datetime(string='Fecha Cita Reprogramada 2', readonly=True)
    exp_enviado_por          = fields.Many2one('res.users', string='Exp. Enviado por', readonly=True)
    fecha_exp_enviado        = fields.Datetime(string='Fecha Exp. Enviado', readonly=True)
    chatarrizado_por         = fields.Many2one('res.users', string='Chatarrizado por', readonly=True)
    fecha_chatarrizado       = fields.Datetime(string='Fecha Chatarrizado', readonly=True)
    certificado_por          = fields.Many2one('res.users', string='Certificado por', readonly=True)
    fecha_certificado        = fields.Datetime(string='Fecha Certificado', readonly=True)
    baja_por                 = fields.Many2one('res.users', string='Baja por', readonly=True)
    fecha_baja               = fields.Datetime(string='Fecha Baja', readonly=True)
    cancelado_por            = fields.Many2one('res.users', string='Cancelada por', readonly=True)
    fecha_cancelado          = fields.Datetime(string='Fecha Cancelada', readonly=True)
    desestimiento_por        = fields.Many2one('res.users', string='Desestimiento por', readonly=True)
    fecha_desestimiento      = fields.Datetime(string='Fecha Desestimiento', readonly=True)
    reposicion_por           = fields.Many2one('res.users', string='Reposicion por', readonly=True)
    fecha_reposicion         = fields.Datetime(string='Fecha Reposicion', readonly=True)
    facturado_por            = fields.Many2one('res.users', string='Facturado por', readonly=True)
    fecha_facturado          = fields.Datetime(string='Fecha Facturado', readonly=True)
    fact_cancelada_por       = fields.Many2one('res.users', string='Fact. Cancelada por', readonly=True)
    fecha_fact_cancelada     = fields.Datetime(string='Fecha Cancelada', readonly=True)
    repuesta_id              = fields.Many2one('chatarra.unit', string='Repuesta por', readonly=True)
    sustituye_id             = fields.Many2one('chatarra.unit', string='Sustituye a', readonly=True)
    reposicion_id            = fields.Many2one('chatarra.reposicion', string='No. de Reposicion', readonly=True)
    factura_id               = fields.Many2one('account.invoice', string='No. de Factura', readonly=True)
    facturado                = fields.Boolean(string='Facturado', readonly=True)
    envio_id                 = fields.Many2one('chatarra.envio', string='No. Envio', readonly=True)
    guia                     = fields.Char(readonly=True)
    copia_tc                 = fields.Boolean(string='Copia TC', readonly=True)
    consulta                 = fields.Boolean(string='Consulta', readonly=True)
    tarjeta_circulacion      = fields.Boolean(string='Tarjeta de Circulacion', readonly=True)
    folio_modalidad          = fields.Integer(string='Folio Modalidad', readonly=True, size=10)
    folio_tarjeta            = fields.Char(string='No. de Folio TC', readonly=True)
    fecha_tarjeta            = fields.Date(string='Fecha de Tarjeta de Circulacion', readonly=True)
    chatarrera_id            = fields.Many2one('res.partner', string='Chatarrera', readonly=True)
    paqueteria_id            = fields.Many2one('res.partner', string='Paqueteria', readonly=True)
    contacto_id              = fields.Many2one('res.partner', string='Contacto', readonly=True)
    secretaria_id            = fields.Many2one('chatarra.secretaria', string='Secretaria', readonly=True)
    gestor_id                = fields.Many2one('res.partner', string='Gestor', readonly=True)
    programacion_cita        = fields.Datetime(string='Fecha de Cita', readonly=True)
    cita_anterior            = fields.Datetime(string='Fecha de Cita Anterior', readonly=True)
    cita_anterior2           = fields.Datetime(string='Fecha de Cita Anterior 2', readonly=True)
    certificado              = fields.Char(readonly=True)
    certificado_fecha        = fields.Date(string='Fecha del Certificado', readonly=True)
    factura_proveedor_id     = fields.Many2one('account.invoice', string='Factura de Proveedor', readonly=True)
    tramite                  = fields.Char(required=True)
    observacion              = fields.Text()
    fecha_sustitucion        = fields.Char(string='Fecha de sustitucion')
    propietario_anterior     = fields.Char(string='Razon Social', required=True,)
    calle                    = fields.Char(required=True)
    numero                   = fields.Char(required=True)
    colonia                  = fields.Char(required=True)
    codigo_postal            = fields.Char(required=True)
    ciudad                   = fields.Char(required=True)
    importe                  = fields.Float(required=True)
    fecha_registro           = fields.Datetime(string='Fecha de registro', required=True, default=lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
   
    _sql_constraints = [('chatarra_unit_name_unique', 'unique(name)', 'La Placa ya existe'),
                        ('chatarra_unit_serie_unique', 'unique(serie)', 'La Serie ya existe')]

    @api.one
    @api.constrains('name','serie')
    def _check_unique_insesitive(self):
        units = [unit.name.lower() for unit in self.search([]) if unit.id not in self.ids]
        for unit in self:
            if unit.name and unit.name.lower() in units:
                raise except_orm('La placa ya existe')

    @api.one
    def action_disponible(self):
        invoice_obj = self.env['account.invoice']
        fpos_obj = self.env['account.fiscal.position']
        prod_obj = self.env['product.product']
        product = prod_obj.search([('categoria', '=', 'chatarra'),('active','=', 1)], limit=1)
        prod_account = product.product_tmpl_id.property_account_expense.id
        if not prod_account:
          prod_account = product.categ_id.property_account_expense_categ.id
          if not prod_account:
            raise except_orm(_('Error'),_('There is no expense account defined for this product: "%s" (id:%d)') % (product.name, product.id,))
        prod_account = fpos_obj.map_account(prod_account)
        journal_obj = self.env['account.journal']
        journal = journal_obj.search([('type', '=', 'purchase')], limit=1)
        unidad = self
        invoice_obj.create({'partner_id':unidad.supplier_id.id,
                            'account_id':unidad.supplier_id.property_account_payable.id,
                            'origin':unidad.name,
                            'unit_id':unidad.id,
                            'type':'in_invoice',
                            'journal_id':journal.id,
                            'fiscal_position':unidad.supplier_id.property_account_position.id,
                            'invoice_line':[(0,0,{'product_id':product.id,
                                                  'name':'Marca: ' + unidad.marca_id.name + '\nSerie: ' + unidad.serie + '\nPlacas: ' + unidad.name,
                                                  'account_id':prod_account,
                                                  'quantity':'1',
                                                  'price_unit':unidad.importe,
                                                  'invoice_line_tax_id':[(6,0,[x.id for x in product.supplier_taxes_id])],
                                                })]
                            })
        invoice = invoice_obj.search([('unit_id','=',unidad.id),('type','=','in_invoice')])
        self.write({'state':'disponible',
                    'disponible_por':self.env.user.id,
                    'fecha_disponible':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'factura_proveedor_id':invoice.id,
                    'document_ids': [(0, 0, {'name':'visual', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'carta', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'consulta', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'copia_tc', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'factura_origen', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'factura_venta', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'factura_compra', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'foto_frente', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'foto_chasis', 'unit_id':unidad.id}),
                                     (0, 0, {'name':'foto_motor', 'unit_id':unidad.id}),
                                     ]})

    @api.one
    def action_recibir_consulta(self):
        self.write({'consulta': True,
                    'consulta_por': self.env.user.id,
                    'fecha_consulta':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        if self.tarjeta_circulacion == True and self.copia_tc == True:
            self.write({'state':'recibido',
                        'recibido_por': self.env.user.id,
                        'fecha_recibido':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.one
    def action_recibir_tarjeta(self):
        unidad = self
        self.write({'tarjeta_circulacion': True,
                    'tc_por': self.env.user.id,
                    'fecha_tc':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        if unidad.consulta == True and unidad.copia_tc == True:
            self.write({'state':'recibido',
                        'recibido_por': self.env.user.id,
                        'fecha_recibido':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.one
    def action_bloqueado(self):
        self.write({'state':'bloqueado',
                    'bloqueado_por': self.env.user.id,
                    'fecha_bloqueado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.one
    def action_exp_enviado(self):
        self.write({'state':'exp_enviado',
                    'exp_enviado_por': self.env.user.id,
                    'fecha_exp_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.one
    def action_chatarrizado(self):
        self.write({'state':'chatarrizado',
                    'chatarrizado_por': self.env.user.id,
                    'fecha_chatarrizado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.one
    def action_baja(self):
        self.write({'state':'baja',
                    'baja_por': self.env.user.id,
                    'fecha_baja':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.one
    def action_cancelado(self):
        unidad = self
        asignacion_obj = self.env['chatarra.asignacion']
        asignacion = asignacion_obj.search([('unit_ids','=',unidad.id)])
        self.write({'state':'cancelado',
                    'cancelado_por': self.env.user.id,
                    'fecha_cancelado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        asignacion.write({'unit_ids': [(3, unidad.id)]})

    @api.one
    def action_desasignar(self):
        unidad = self
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.search([('unit_id','=',unidad.id),('type','=','out_invoice')])
        asignacion_obj = self.env['chatarra.asignacion']
        asignacion = asignacion_obj.search([('unit_ids','=',unidad.id)])
        asignacion.write({'unit_ids': [(3, unidad.id)]})
        if unidad.asignacion2_id == False:
            self.write({'state':'disponible',
                        'asignacion_id':False,
                        'asignacion2_id':unidad.asignacion_id.id,
                        'desasignado_por':self.env.user.id,
                        'fecha_desasignado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        else:
            self.write({'state':'disponible',
                        'asignacion_id':False,
                        'asignacion2_id':unidad.asignacion_id.id,
                        'asignacion3_id':unidad.asignacion2_id.id,
                        'desasignado2_por':self.env.user.id,
                        'fecha_desasignado2':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        invoice.signal_workflow('invoice_cancel')

    @api.one
    def action_completo_unidad(self):
        unidad = self
        for documento in unidad.document_ids:
            if documento.state == 'pendiente':
                raise except_orm(_('Error'),_('El documento "%s" sigue pendiente') % documento.name.upper())
            else:
                self.write({'state':'completo',
                            'completo_por':self.env.user.id,
                            'fecha_completo':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    @api.onchange('name')
    def _verify_name(self):
        units = [unit.name.lower() for unit in self.search([])]
        for unit in self:
            if unit.name and unit.name.lower() in units:
                return {
                    'warning': {
                        'title': "Error",
                        'message': "La placa ya existe",
                    }
                }

    @api.onchange('serie')
    def _verify_serie(self):
        units = [unit.serie.lower() for unit in self.search([])]
        for unit in self:
            if unit.serie and unit.serie.lower() in units:
                return {
                    'warning': {
                        'title': "Error",
                        'message': "La serie ya existe",
                    }
                }