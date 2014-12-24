# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
from pygeocoder import Geocoder
from time import sleep

class connector_places_wizard(osv.osv):
    _name = 'connector.places'
    _description = 'Sync places'
    _columns = {
			'name':fields.char('Get Places', size=64, readonly=True),
			    }

    def get_places(self,cr,uid,ids,vals):
		places_obj = self.pool.get('tms.place')
		state_obj = self.pool.get('res.country.state')
		#state = state_obj.browse(cr, uid, state_id, context=None)
		#print state_id
		url = 'http://ws.locatel.es/servicios/gestion/gestion.asmx?WSDL'
		usuario = 'mersa10'
		password = 'mersa10'
		imp = Import('http://www.w3.org/2001/XMLSchema')
		imp.filter.add('http://locatel.es/')
		d = ImportDoctor(imp)
		client = Client(url, doctor=d)
		ListaLugaresPersonalizados = client.service.ListaLugaresPersonalizados(usuario, password)
		count = 1
		for place in ListaLugaresPersonalizados.diffgram.Lugares.Lugar:
			print count
			place_id = place._id
			if places_obj.search(cr, uid, [('locatel_id', '=', place_id)]):
				pass
			elif count<100:
				geocoder = Geocoder.reverse_geocode(float(place.latitud), float(place.longitud))
			 	if geocoder.state == 'state' or 'Baja California':
			 		pass
			 	else:
			 		state_id = state_obj.search(cr, uid, [('name','=',geocoder.state)])
			 		print state_id
			 		print geocoder.state
			 		print 'latitud: ', place.latitud
			 		print 'longitud', place.longitud
			 		places_obj.create(cr, uid, {'locatel_id':place._id,
			 	 							'name':place.zona,
			 	 							'latitude':place.latitud,
			 	 							'longitude':place.longitud,
			 	 							'state_id':state_id[0]})
			 	count = count + 1
			 	sleep(1.5)