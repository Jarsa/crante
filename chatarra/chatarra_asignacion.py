# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import logging
_logger = logging.getLogger(__name__)

class chatarra_asignacion(osv.osv):
    _name = 'chatarra.asignacion'
    _description = 'Asignacion'
    _columns = {
        'name'              : fields.char('No. de Asignacion', size=64, readonly='True'),
        'state'             : fields.selection([
                                ('borrador','Borrador'),
                                ('confirmado','Confirmado'),
                                ('enviado_sct','Enviado a SCT'),
                                ('pagado','Pagado'),
                                ('cerrado','Cerrado'),
                                ], 'Estado', readonly=True),
        'client_id'         : fields.many2one('res.partner', 'Cliente'),
        'contacto_id'       : fields.many2one('res.partner', 'Contacto'),
        'agencia_id'        : fields.many2one('res.partner','Agencia'),
        'unit_ids'		    : fields.many2many('chatarra.unit', 'chatarra_asignacion_unidad_rel', 'asignacion_id', 'unit_id', 'Unidades', required='True'),
        'confirmado_por'    : fields.many2one('res.users','Confirmado por:', readonly='True'),
        'fecha_confirmado'  : fields.datetime('Fecha Confirmado:', readonly='True'),
        'enviado_por'       : fields.many2one('res.users','Enviado por:',readonly='True'),
        'fecha_enviado'     : fields.datetime('Fecha Enviado:',readonly='True'),
        'guia'              : fields.many2one('chatarra.asignacion.guia','Numero de Guia:'),
    }

    _defaults = {
        'state': 'borrador',
    }

    def asignar_unidad(self, cr, uid, ids, vals, context=None):
        unit_obj = self.pool.get('chatarra.unit')
        for asignacion in self.browse(cr, uid, ids):
            unit_ids = False
            unit_ids = unit_obj.search(cr, uid, [('asignacion_id', '=', asignacion.id)])
            if unit_ids:
                unit_obj.write(cr, uid, unit_ids, {'asignacion_id': False, 'state':'disponible', 'asignada_por': False,'fecha_asignada': False})
            unit_ids = []
            for unidad in asignacion.unit_ids:
                if unidad.state in ('borrador'):
                    raise osv.except_osv(('Advertencia !'),
                        ('La Unidad %s esta en estado Borrador...') % (unidad.name)
                        ) 
                unit_obj.write(cr, uid, [unidad.id], {'asignacion_id':asignacion.id,'state':'asignada','asignada_por':uid,'fecha_asignada':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def enviar_unidad(self,cr, uid, ids, vals, context=None):
        unit_obj = self.pool.get('chatarra.unit')
        for asignacion in self.browse(cr, uid, ids):
            unit_ids = []
            for unidad in asignacion.unit_ids:
                if asignacion.state in 'enviado_sct':
                    unit_obj.write(cr, uid, [unidad.id], {'state':'enviado','enviado_por':uid,'fecha_enviado':asignacion.fecha_enviado})

    def write(self, cr, uid, ids, vals, context=None):
        values = vals
        super(chatarra_asignacion, self).write(cr, uid, ids, values, context=context)
        for asignacion in self.browse(cr, uid, ids):
            for unidad in asignacion.unit_ids:
                if unidad.state in 'reposicion':
                    self.write(cr, uid, ids, {'unit_ids': [(3, unidad.id)]})
            if asignacion.state in 'enviado_sct':
                self.enviar_unidad(cr, uid, ids, vals)
            if asignacion.state in ('confirmado','borrador'):
                self.asignar_unidad(cr, uid, ids, vals)
        return True

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'asignacion.sequence.number')
        res = super(chatarra_asignacion, self).create(cr, uid, vals, context)
        self.asignar_unidad(cr, uid, [res], vals)
        return res

    def action_confirmado(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {  'state':'confirmado',
                                    'confirmado_por':uid,
                                    'fecha_confirmado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return True

    def create_invoices(self, cr, uid, ids, context=None):
        invoice_obj = self.pool.get('account.invoice')
        asignacion = self.browse(cr, uid, ids)
        prod_obj = self.pool.get('product.product')
        unidad_obj = self.pool.get('chatarra.unit')
        prod_id = prod_obj.search(cr, uid, [('chatarra', '=', 1),('active','=', 1)], limit=1)
        product = prod_obj.browse(cr, uid, prod_id, context=None)
        _logger.error("producto : %r", product.description_sale)
        _logger.error("cuenta : %r", product.property_account_income.id)
        _logger.error("precio : %r", product.lst_price)
        _logger.error("impuestos : %r", product.taxes_id.id)
        if not prod_id:
            raise osv.except_osv(
                    ('Falta Configuracion !'),
                    ('No existe un producto definido como chatarra !!!'))
        for unidad in asignacion.unit_ids:
            invoice_obj.create(cr, uid, {'partner_id':asignacion.client_id.id,
                                         'contacto_id':asignacion.contacto_id.id,
                                         'agencia_id':asignacion.agencia_id.id,
                                         'asignacion_id':asignacion.id,
                                         'unit_id':unidad.id,
                                         'account_id':asignacion.client_id.property_account_receivable.id,
                                         'origin':asignacion.name,
                                         'fiscal_position':asignacion.client_id.property_account_position.id,
                                         'invoice_line':[(0,0,{'product_id':product.id,
                                                               'name':product.description_sale,
                                                               'account_id':product.property_account_income.id,
                                                               'quantity':'1',
                                                               'price_unit':product.lst_price,
                                                               'invoice_line_tax_id':[(6,0,[product.taxes_id.id])],
                                                              })]
                                        }, context=None)
            invoice_id = invoice_obj.search(cr, uid, [('unit_id','=',unidad.id)])
            invoice = invoice_obj.browse(cr, uid, invoice_id)
            unidad_obj.write(cr, uid, unidad.id, {'facturado_por':uid,
                                              'fecha_facturado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                                              'factura_id':invoice.id,
                                              })
        return True

chatarra_asignacion()

class chatarra_asignacion_guia(osv.osv):
    _name = 'chatarra.asignacion.guia'
    _description = 'No. de Guia'
    _columns = {
        'name'          : fields.char('No. de Guia', size=64, required=True),
        'asignacion_id' : fields.many2one('chatarra.asignacion','No. de Asignacion', readonly='True'),
        'paqueteria_id' : fields.many2one('res.partner','Paqueteria', required=True),
    }

    def action_enviado(self, cr, uid, ids, vals, context=None):
        asignacion_obj = self.pool.get('chatarra.asignacion')
        guia = self.browse(cr, uid, ids)
        asignacion = guia.asignacion_id.id
        for unidad in guia.asignacion_id.unit_ids:
            if unidad.state not in 'completo':
                raise osv.except_osv(('Advertencia !'),
                        ('Todas las Unidades deben estar en estado "Completo"')
                        )
            asignacion_obj.write(cr, uid, [asignacion], {'guia':guia.id, 'state':'enviado_sct', 'enviado_por':uid, 'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
            return True