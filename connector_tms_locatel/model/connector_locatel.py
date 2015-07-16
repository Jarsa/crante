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

    

# vehiculo
# historico
# informes
# ver_partes
# ficheros
# gestion