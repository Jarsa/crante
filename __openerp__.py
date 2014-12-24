# -*- encoding: utf-8 -*-
##################################################################################
#
#    Copyright (C) 2014 Jarsa Sistemas, S.A. de C.V. (<http://www.jarsa.com.mx>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################################################################################

{   
    'name'        : 'TMS GPS Locatel Connector',
    'version'     : '1.0',
    'category'    : 'Connector',
    'author'      : 'Jarsa Sistemas, S.A. de C.V.',
    'website'     : 'www.jarsa.com.mx',
    'depends'     : ['tms'],
    'summary'     : 'Connect GPS System with TMS Module',
    'description' : '''
                    TMS GPS Connector

 Module designed to connect TMS module to Locatel (Locatelia in Mexico) webservices.

 Features:

 * Updates vehicle position.
 * Updates travel history.
                    ''',
    'data' : ['views/tms_place_view.xml',
              'views/connector_locatel_view.xml',
              'views/fleet_vehicle_view.xml',
              'data/connector_locatel_data.xml',
              'wizard/connector_places_wizard_view.xml'],
    'application': True,
    'installable': True,
}