# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import geocoder

class connector_places_wizard(osv.osv_memory):
    _name = 'connector.places.wizard'
    _description = 'Get places from Locatel'

    def get_places(self, cr, uid, ids, *args):
        places_obj = self.pool.get('tms.place')
        state_obj = self.pool.get('res.country.state')
        connector_obj = self.pool.get('connector.locatel')
        connector_id = connector_obj.search(cr, uid, [], limit=1)
        connector = connector_obj.browse(cr, uid, connector_id[0])
        imp = Import(connector.ws_schema)
        imp.filter.add(connector.mngmt_namespace)
        d = ImportDoctor(imp)
        client = Client(connector.url_mngmt, doctor=d)
        ListaLugaresPersonalizados = client.service.ListaLugaresPersonalizados(connector.user, connector.password)
        places = ListaLugaresPersonalizados.diffgram.Lugares.Lugar
        count = 1
        states_bing = {'AGS':'AGU',
                       'BCN':'BCN',
                       'BCS':'BCS',
                       'CAM':'CAM',
                       'CHIS':'CHP',
                       'CHIH':'CHH',
                       'COAH':'COA',
                       'COL':'COL',
                       'DF':'DIF',
                       'DGO':'DUR',
                       'EMEX':'MEX',
                       'GTO':'GUA',
                       'GRO':'GRO',
                       'HGO':'HID',
                       'JAL':'JAL',
                       'MICH':'MIC',
                       'MOR':'MOR',
                       'NAY':'NAY',
                       'NL':'NLE',
                       'OAX':'OAX',
                       'PUE':'PUE',
                       'QRO':'QUE',
                       'QR':'ROO',
                       'SLP':'SLP',
                       'SIN':'SIN',
                       'SON':'SON',
                       'TAB':'TAB',
                       'TAMPS':'TAM',
                       'TLAX':'TLA',
                       'VER':'VER',
                       'YUC':'YUC',
                       'ZAC':'ZAC',}
        states_google = {'AGS':'AGU',
                         'BC':'BCN',
                         'BCS':'BCS',
                         'CAMP':'CAM',
                         'CHIS':'CHP',
                         'CHIH':'CHH',
                         'COAH':'COA',
                         'COL':'COL',
                         'D.F.':'DIF',
                         'DGO':'DUR',
                         'MEX':'MEX',
                         'GTO':'GUA',
                         'GRO':'GRO',
                         'HGO':'HID',
                         'JAL':'JAL',
                         'MICH':'MIC',
                         'MOR':'MOR',
                         'NAY':'NAY',
                         'NL':'NLE',
                         'OAX':'OAX',
                         'PUE':'PUE',
                         'QRO':'QUE',
                         'QROO':'ROO',
                         'SLP':'SLP',
                         'SIN':'SIN',
                         'SON':'SON',
                         'TAB':'TAB',
                         'TAMPS':'TAM',
                         'TLAX':'TLA',
                         'Vereda':'VER',
                         'YUC':'YUC',
                         'ZAC':'ZAC',}
        for place in ListaLugaresPersonalizados.diffgram.Lugares.Lugar:
            print count
            if places_obj.search(cr, uid, [('locatel_id', '=', place._id)]):
                pass
            else:
                bing = geocoder.bing([float(place.latitud),float(place.longitud)], method='reverse')
                if bing.state in states_bing:
                    state_id = state_obj.search(cr, uid, [('code','=',states_bing[bing.state])])
                    places_obj.create(cr, uid, {'locatel_id':place._id,
                                                'name':place.zona,
                                                'latitude':place.latitud,
                                                'longitude':place.longitud,
                                                'state_id':state_id[0]})
                    if states_bing[bing.state]:
                        print 'Bing', states_bing[bing.state]
                elif bing.state not in states_bing:
                    google = geocoder.google([float(place.latitud),float(place.longitud)], method='reverse')
                    state_id = state_obj.search(cr, uid, [('code','=',states_google[google.state])])
                    places_obj.create(cr, uid, {'locatel_id':place._id,
                                                'name':place.zona,
                                                'latitude':place.latitud,
                                                'longitude':place.longitud,
                                                'state_id':state_id[0]})
                    print 'Google', states_google[google.state]
            count += 1
        return True