# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv

class connector_locatel(osv.osv):
    _name = 'connector.locatel'
    _columns = {
        'user'				: fields.char('User', size=64, required=True),
        'password'			: fields.char('Password', size=64, required=True),
        'ws_schema'			: fields.char('Webservices Schema URL', required=True),
        'url_vehicle'		: fields.char('URL Vehicles', size=64, required=True),
        'vehicle_namespace'	: fields.char('Vehicle Namespace', size=64, required=True),
        'url_history'		: fields.char('URL History', size=64, required=True),
        'history_namespace'	: fields.char('History Namespace', size=64, required=True),
        'url_mngmt'	  		: fields.char('URL Management', size=64, required=True),
        'mngmt_namespace'	: fields.char('Management Namespace', size=64, required=True),
        'url_reports'		: fields.char('URL Reports', size=64, required=True),
        'reports_namespace'	: fields.char('Reports Namespace', size=64, required=True),
        'url_parts'			: fields.char('URL Parts', size=64, required=True),
        'parts_namespace'	: fields.char('Parts Namespace', size=64, required=True),
    }

    # def places(self, cr, uid, ids, context=None):
    #     connector_obj = self.pool.get('connector.locatel')
    #     connector_id = connector_obj.search(cr, uid, [], limit=1)
    #     connector = connector_obj.browse(cr, uid, connector_id[0])
    #     obj = connector
    #     #obj = self.browse(cr, uid, ids)
    #     #imp = Import(obj.ws_schema)
    #     #imp.filter.add(obj.mngmt_namespace)
    #     #d = ImportDoctor(imp)
    #     #client = Client(obj.url_mngmt, doctor=d)
    #     #ListaLugaresPersonalizados = client.service.ListaLugaresPersonalizados(obj.user, obj.password)
    #     #places = ListaLugaresPersonalizados.diffgram.Lugares.Lugar
    #     #return places
    #     return obj

#         d = ImportDoctor(imp)
#         client = Client(url, doctor=d)
#         ListaLugaresPersonalizados = client.service.ListaLugaresPersonalizados(usuario, password)
#         count = 1
#         for place in ListaLugaresPersonalizados.diffgram.Lugares.Lugar:
#             print count
#             place_id = place._id
#             if places_obj.search(cr, uid, [('locatel_id', '=', place_id)]):
#                 pass
#             elif count<100:
#                 geocoder = Geocoder.reverse_geocode(float(place.latitud), float(place.longitud))
#                 if geocoder.state == 'state' or 'Baja California':
#                     pass
#                 else:
#                     state_id = state_obj.search(cr, uid, [('name','=',geocoder.state)])
#                     print state_id
#                     print geocoder.state
#                     print 'latitud: ', place.latitud
#                     print 'longitud', place.longitud
#                     places_obj.create(cr, uid, {'locatel_id':place._id,
#                                             'name':place.zona,
#                                             'latitude':place.latitud,
#                                             'longitude':place.longitud,
#                                             'state_id':state_id[0]})
#                 count = count + 1
#                 sleep(1.5)

# vehiculo
# historico
# informes
# ver_partes
# ficheros
# gestion