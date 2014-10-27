# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools

class chatarra_marca(osv.osv):
    _name = 'chatarra.marca'
    _columns = {
                'name': fields.char('Marca',size=40),
                'active': fields.boolean('Activo'),
        }
    _defaults = {
        'active': 'True',
    }
    
chatarra_marca()

class chatarra_tipo(osv.osv):
    _name = 'chatarra.tipo'
    _columns = {
                'name': fields.char('Tipo',size=40),
                'active': fields.boolean('Activo'),
        }
    _defaults = {
        'active': 'True',
    }
chatarra_tipo()

class chatarra_unit(osv.osv):
    _name = 'chatarra.unit'

    def _check_unique_insesitive(self, cr, uid, ids, context=None):
        sr_ids = self.search(cr, 1 , [], context=context)
        lst = [x.name.lower() for x in self.browse(cr, uid, sr_ids, context=context) if x.name and x.id not in ids]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.name and self_obj.name.lower() in  lst:
                return False
            return True

    def onchange_vat(self, cr, uid, ids, propietario_id, context=None):
        vat = False
        if propietario_id:
            vat = self.pool.get('res.partner').browse(cr, uid, propietario_id, context=context).vat
        return {'value': {'vat': vat}}
    
    _columns = {
                'name': fields.char('Placa',size=40),
                'serie': fields.char('Número de serie', size=40),
                'marca': fields.many2one('chatarra.marca', 'Marca'),
                'clase': fields.selection([('t2','T 2'),('t3','T 3'),('c2','C 2'),('c3','C 3')],'Clase'),
                'tipo': fields.many2one('chatarra.tipo','Tipo'),
                'motor': fields.char('Motor',size=40),
                'combustible': fields.selection([('diesel','Diesel'),('gasolina','Gasolina')],'Combustible'),
                'toneladas': fields.integer('Toneladas'),
                'peso_vehicular': fields.float('Peso Vehicular'),
                'largo_vehiculo': fields.float('Largo Vehiculo'),
                'propietario_id': fields.many2one('res.partner','Nombre del Propietario'),
                'vat': fields.char('R.F.C.'),
        }

    _sql_constraints = [('chatarra_unit_name_unique', 'unique(name)', 'La Placa ya existe')]
    
    _constraints = [(_check_unique_insesitive, 'La Placa ya existe', ['name'])]

chatarra_unit()