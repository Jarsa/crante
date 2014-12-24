# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
from time import sleep
import geocoder

class connector_places_wizard(osv.osv):
    _name = 'connector.places.wizard'
    _description = 'Get places from Locatel'


	def get_places(self, cr, uid, ids, context=None):
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
		for place in ListaLugaresPersonalizados.diffgram.Lugares.Lugar:
			print count
			if places_obj.search(cr, uid, [('locatel_id', '=', place._id)]):
				pass
			elif '''count<100''':
				geocoder = geocoder.bing([float(place.latitud), float(place.longitud)], method = 'reverse')
				print geocoder.state
			 	# if geocoder.state == 'state' or 'Baja California':
			 	# 	pass
			 	# else:
			 	# 	state_id = state_obj.search(cr, uid, [('name','=',geocoder.state)])
			 	# 	print state_id
			 	# 	print geocoder.state
			 	# 	print 'latitud: ', place.latitud
			 	# 	print 'longitud', place.longitud
			 	# 	places_obj.create(cr, uid, {'locatel_id':place._id,
			 	#  							'name':place.zona,
			 	#  							'latitude':place.latitud,
			 	#  							'longitude':place.longitud,
			 	#  							'state_id':state_id[0]})
			 	# count = count + 1
			 	# sleep(1.5)