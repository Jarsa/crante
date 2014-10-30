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
                'modelo': fields.char('Modelo', size=40),
                'clase': fields.selection([('t2','T 2'),('t3','T 3'),('c2','C 2'),('c3','C 3')],'Clase'),
                'tipo': fields.many2one('chatarra.tipo','Tipo'),
                'motor': fields.char('Motor',size=40),
                'combustible': fields.selection([('diesel','Diesel'),('gasolina','Gasolina')],'Combustible'),
                'peso_vehicular': fields.float('Peso Vehicular'),
                'propietario_id': fields.many2one('res.partner','Nombre del Propietario'),
                'vat': fields.char('R.F.C.', size=6),
                'reg_fed': fields.char('Reg. Fed', size=40),
                'modalidad': fields.char('Modalidad', size=64),
                'no_ejes': fields.integer('Numero de ejes'),
                'no_llantas': fields.integer('Numero de llantas'),
                'cap_litros': fields.char('Litros', size=10),
                'cap_toneladas': fields.char('Toneladas', size=10),
                'cap_personas': fields.char('Personas', size=10),
                'alto': fields.float('Alto'),
                'ancho': fields.float('ancho'),
                'largo': fields.float('largo'),
                'eje_direccional': fields.char('Eje Direccional', size=10),
                'eje_motriz': fields.char('Eje Motriz', size=10),
                'eje_carga': fields.char('Eje Carga', size=10),
                'permiso_ruta': fields.char('Permiso de ruta', size=10),
                'lugar_exp': fields.char('Lugar de expedicion', size=10),
                'fecha_exp': fields.date('Fecha de expedicion'),

        }

    _sql_constraints = [('chatarra_unit_name_unique', 'unique(name)', 'La Placa ya existe')]
    
    _constraints = [(_check_unique_insesitive, 'La Placa ya existe', ['name'])]
    

chatarra_unit()