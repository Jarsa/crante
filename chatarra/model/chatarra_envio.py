# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import logging
_logger = logging.getLogger(__name__)

class chatarra_envio(osv.osv):
    _name = 'chatarra.envio'
    _columns = {
        'name'			: fields.char('No. de envio', readonly=True),
        'state'			: fields.selection([
        					('borrador','Borrador'),
        					('enviado','Enviado')
        					],'Estado', readonly=True),
        'guia'			: fields.char('Guia', required=True),
        'paqueteria_id'	: fields.many2one('res.partner','Paqueteria', required=True),
        'secretaria_id'	: fields.many2one('res.partner','Secretaria', required=True),
        'unit_ids'		: fields.many2many('chatarra.unit', 'chatarra_envio_unidad_rel', 'envio_id', 'unit_id', 'Unidades', required=True),
        'enviado_por'	: fields.many2one('res.users','Enviado por:', readonly=True),
        'fecha_enviado'	: fields.datetime('Fecha Enviado:', readonly=True),
        'gestor'        : fields.many2one('res.partner','Gestor'),
    }

    _defaults = {
        'state': 'borrador',
    }

    def seleccionar_unidad(self, cr, uid, ids, vals, context=None):
        unit_obj = self.pool.get('chatarra.unit')
        for envio in self.browse(cr, uid, ids):
            unit_ids = False
            unit_ids = unit_obj.search(cr, uid, [('envio_id', '=', envio.id),('state', '=', 'seleccion')])
            if unit_ids:
                unit_obj.write(cr, uid, unit_ids, {'envio_id': False,
                                                   'state':'completo',
                                                   'guia': False,
                                                   'paqueteria_id': False,
                                                   'secretaria_id': False,})
            unit_ids = []
            for unidad in envio.unit_ids:
            	unit_obj.write(cr, uid, [unidad.id], {'envio_id':envio.id,
                                                      'state':'seleccion',
                                                      'guia':envio.guia,
                                                      'paqueteria_id':envio.paqueteria_id.id,
                                                      'secretaria_id':envio.secretaria_id.id,})

    def enviar_unidad(self, cr, uid, ids, vals, context=None):
        envio = self.browse(cr, uid, ids)
        unit_obj = self.pool.get('chatarra.unit')
        invoice_obj = self.pool.get('account.invoice')
        fpos_obj = self.pool.get('account.fiscal.position')
        prod_obj = self.pool.get('product.product')
        prod_id = prod_obj.search(cr, uid, [('categoria', '=', 'envio'),('active','=', 1)], limit=1)
        prod2_id = prod_obj.search(cr, uid, [('categoria', '=', 'secretaria'),('active','=', 1)], limit=1)
        product = prod_obj.browse(cr, uid, prod_id, context=None)
        product2 = prod_obj.browse(cr, uid, prod2_id, context=None)
        prod_account = product.product_tmpl_id.property_account_expense.id
        if not prod_account:
            prod_account = product.categ_id.property_account_expense_categ.id
        if not prod_account:
            raise osv.except_osv(_('Error !'),
                               _('There is no expense account defined ' \
                                 'for this product: "%s" (id:%d)') % \
                                (product.name, product.id,))
        prod_account = fpos_obj.map_account(cr, uid, False, prod_account)
        prod_account2 = product2.product_tmpl_id.property_account_expense.id
        if not prod_account2:
            prod_account2 = product2.categ_id.property_account_expense_categ.id
            if not prod_account2:
                raise osv.except_osv(_('Error !'),
                                 _('There is no expense account defined ' \
                                   'for this product: "%s" (id:%d)') % \
                                   (product2.name, produc2t.id,))
        prod_account = fpos_obj.map_account(cr, uid, False, prod_account)
        journal_obj = self.pool.get('account.journal')
        journal_id = journal_obj.search(cr, uid, [('type', '=', 'purchase')], limit=1)
        journal = journal_obj.browse(cr, uid, journal_id, context=None)
        invoice_obj.create(cr, uid, {'partner_id':envio.paqueteria_id.id,
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
                                  }, context=None)
        for unidad in envio.unit_ids:
            invoice_obj.create(cr, uid, {'partner_id':envio.secretaria_id.id,
                                   'account_id':envio.secretaria_id.property_account_payable.id,
                                   'origin':envio.name + '/' + envio.secretaria_id.name + '/' + unidad.name,
                                   'type':'in_invoice',
                                   'journal_id':journal.id,
                                   'fiscal_position':envio.secretaria_id.property_account_position.id,
                                   'unit_id':unidad.id,
                                   'invoice_line':[(0,0,{'product_id':product2.id,
                                                         'name':'Envio: ' + envio.name + '\nNo. de Guia: ' + envio.guia + '\nPaqueteria: ' + envio.paqueteria_id.name + '\Secretaria: ' + envio.secretaria_id.name,
                                                         'account_id':prod_account2,
                                                         'quantity':'1',
                                                         'price_unit':product2.lst_price,
                                                         'invoice_line_tax_id':[(6,0,[x.id for x in product2.supplier_taxes_id])],
                                                        })]
                                  }, context=None)
            if envio.gestor:
                invoice_obj.create(cr, uid, {'partner_id':envio.gestor.id,
                                   'account_id':envio.gestor.property_account_payable.id,
                                   'origin':envio.name + '/' + envio.gestor.name + '/' + unidad.name,
                                   'type':'in_invoice',
                                   'journal_id':journal.id,
                                   'fiscal_position':envio.gestor.property_account_position.id,
                                   'unit_id':unidad.id,
                                   'invoice_line':[(0,0,{'product_id':product2.id,
                                                         'name':'Envio: ' + envio.name + '\nNo. de Guia: ' + envio.guia + '\nPaqueteria: ' + envio.paqueteria_id.name + '\Gestor: ' + envio.gestor.name,
                                                         'account_id':prod_account2,
                                                         'quantity':'1',
                                                         'price_unit':product2.lst_price,
                                                         'invoice_line_tax_id':[(6,0,[x.id for x in product2.supplier_taxes_id])],
                                                        })]
                                  }, context=None)
            self.write(cr, uid, ids, {'state':'enviado',
    							  'enviado_por':uid,
    							  'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
            for unidad in envio.unit_ids:
                unit_obj.write(cr, uid, [unidad.id], {'envio_id':envio.id,
    											  'state':'enviado',
    											  'guia':envio.guia,
    											  'enviado_por':uid,
                                                  'paqueteria_id':envio.paqueteria_id.id,
                                                  'secretaria_id':envio.secretaria_id.id,
    											  'fecha_enviado':time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})

    def create(self, cr, uid, vals, context={}):
        if (not 'name' in vals) or (vals['name'] == False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'envio.sequence.number')
        res = super(chatarra_envio, self).create(cr, uid, vals, context)
        self.seleccionar_unidad(cr, uid, [res], vals)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        values = vals
        super(chatarra_envio, self).write(cr, uid, ids, values, context=context)
        for envio in self.browse(cr, uid, ids):
            for unidad in envio.unit_ids:
                if unidad.state in 'reposicion':
                    self.write(cr, uid, ids, {'unit_ids': [(3, unidad.id)]})
                if envio.state in ('borrador'):
                    self.seleccionar_unidad(cr, uid, ids, vals)
        return True
chatarra_envio()