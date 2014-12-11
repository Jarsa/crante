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
    "name": "Chatarra",
    "version": "1.0",
    "description": 
    """
        Module designed for specific needs
    """,
    "author": "JARSA Sistemas, S.A. de C.V.",
    "website": "http://www.jarsa.com.mx",
    "category": "Chatarra",
    "depends": ['base_vat',
                'vat_override',
                'account_accountant',
                'account_cancel'],
    "data":['views/chatarra_unit_view.xml',
            'views/chatarra_view.xml',
            'views/chatarra_reposicion_view.xml',
            'views/res_partner_view.xml',
            'views/chatarra_asignacion_view.xml',
            'views/chatarra_doc_view.xml',
            'views/product_product_view.xml',
            'views/account_invoice_view.xml',
            'views/ir_config_parameter.xml',
            'views/chatarra_envio_view.xml',
            'reports/report_view.xml',
            'reports/report_units_late.xml',
            'data/chatarra_marca_data.xml',
            'data/chatarra_tipo_data.xml',],
    'js': ['static/src/js/chatarra.js'],
    "demo_xml": [],
    "update_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}
