# -*- encoding: utf-8 -*-
from osv import fields, osv
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

class gps_url(osv.osv):
    _name = 'gps.url'
    _description = 'URL'
    _columns = {
        'name'		: fields.char('URL', size=64, required=True),
        'active'	: fields.boolean('Active')
    }
gps_url()

class gps_vehiculo(osv.osv):
    _name = 'gps.vehiculo'
    _description = 'Description'
    _columns = {
        'vehiculo_id'		: fields.char('Vehicle'),
        'matricula_coche' 	: fields.char('License Plate'),
        'modelo_coche'		: fields.char('Model'),
        'conductor'			: fields.char('Driver'),
    }

    def ListaVehiculos(self, cr, uid, ids):



gps_vehiculo()
vehiculo
historico
informes
ver_partes
ficheros
gestion


Importante: Ver alertas
ListaLugaresPersonalizados



from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

url = 'http://ws.locatel.es/servicios/vehiculos/vehiculos.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema')
imp.filter.add('http://locatel.es/')
d = ImportDoctor(imp)
client = Client(url, doctor=d)

usuario = 'mersa10'
password = 'mersa10'

ListaVehiculos = client.service.ListaVehiculos(usuario, password)

for vehiculo in ListaVehiculos.diffgram.Flota.coches:
	print 'vehiculo_id: ' + vehiculo.vehiculo_id + '\nLatitud: ' + vehiculo.ult_latitud + '\nLongitud: ' + vehiculo.ult_longitud
	
LeeVehiculo = client.service.LeeVehiculo(usuario, password, vehiculo_id)
FechasVehiculos = client.service.FechasVehiculos(usuario, password)

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import datetime
url = 'http://ws.locatel.es/servicios/historicos/historico.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema')
imp.filter.add('http://ws.locatel.es/')
doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

usuario = 'odoomersa'
password = 'RWnR8XZ2'
vehiculo = '35788'
inicio = datetime.datetime(2014, 11, 20, 00, 00, 00)
fin = datetime.datetime(2014, 11, 20, 23, 59, 59)
real = '2'

VerHistorico = client.service.VerHistorico(usuario, password, vehiculo, inicio, fin)
for vehiculo in VerHistorico.diffgram.historico.Table:
    print vehiculo.latitud

VerHistoricoOrigen = client.service.VerHistoricoOrigen(usuario, password, vehiculo, inicio, fin, real)

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
url = 'http://ws.locatel.es/servicios/gestion/gestion.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema')
imp.filter.add('http://locatel.es/')
d = ImportDoctor(imp)
client = Client(url, doctor=d)

usuario = 'odoomersa'
password = 'RWnR8XZ2'

ListaLugaresPersonalizados = client.service.ListaLugaresPersonalizados(usuario, password)

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import datetime
url = 'http://ws.locatel.es/servicios/informes/informes.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema')
imp.filter.add('http://www.locatel.es/servicios/informes')
doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

usuario = 'odoomersa'
password = 'RWnR8XZ2'
vehiculo = '35788'
inicio = datetime.datetime(2014, 11, 20, 00, 00, 00)
fin = datetime.datetime(2014, 11, 20, 23, 59, 59)

InformeRecorridos = client.service.InformeRecorridos(usuario, password, vehiculo, inicio, fin)

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import
import datetime
url = 'http://ws.locatel.es/servicios/partesvisita/Partes.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema')
imp.filter.add('http://ws.locatel.es/Partesvisita/Partes')
doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

usuario = 'odoomersa'
password = 'RWnR8XZ2'
vehiculo = '35788'
inicio = datetime.datetime(2014, 11, 20, 00, 00, 00)
fin = datetime.datetime(2014, 11, 20, 23, 59, 59)

VerPartes = client.service.InformeRecorridos(usuario, password, vehiculo, inicio, fin)