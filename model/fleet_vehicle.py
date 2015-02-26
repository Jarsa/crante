# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv


class fleet_vehicle(osv.osv):
    _name = 'fleet.vehicle'
    _inherit = 'fleet.vehicle'

    def _vehicle_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.model_id.brand_id.name + '/' + record.model_id.modelname + '/' + record.vin_sn + '/' + record.license_plate + '/' + record.year
        return res

    _columns = {
        'name': fields.function(_vehicle_name_get_fnc, type="char", string='Name', store=True),
        'vin_sn': fields.char('Chassis Number', required=True),
        'location': fields.char('Location', readonly=True),
        'year': fields.integer('Year', required=True),
        'purchase_price': fields.float('Purchase Price'),
        'sale_price': fields.float('Sale Price'),
        'date': fields.datetime('Date'),
                }
