# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

class tms_place_locatel(osv.osv):
    _inherit = 'fleet.vehicle'
    
    def get_vehicle_gps(self, cr, uid, ids, *args):
        vehicle_obj = self.pool.get('fleet.vehicle')
        connector_obj = self.pool.get('connector.locatel')
        connector_id = connector_obj.search(cr, uid, [], limit=1)
        connector = connector_obj.browse(cr, uid, connector_id[0])
        imp = Import(connector.ws_schema)
        imp.filter.add(connector.vehicle_namespace)
        d = ImportDoctor(imp)
        client = Client(connector.url_vehicle, doctor=d)
        ListaVehiculos = client.service.ListaVehiculos(connector.user, connector.password)
        vehicles = ListaVehiculos.diffgram.Flota.coches
        for vehicle in vehicles:
            vehicle_id = vehicle_obj.search(cr, uid, [('gps_id', '=', vehicle.vehiculo_id)])
            if hasattr(vehicle, 'ult_zona3') and vehicle_id != []:
                vehicle_obj.write(cr, uid, vehicle_id, {'longitude':vehicle.ult_longitud,
                                                        'latitude':vehicle.ult_latitud,
                                                        'location':vehicle.ult_zona3,})
            else:
                vehicle_obj.write(cr, uid, vehicle_id, {'longitude':vehicle.ult_longitud,
                                                        'latitude':vehicle.ult_latitud,
                                                        'location':'-',})