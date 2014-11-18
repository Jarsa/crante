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
    "depends": ['base_vat','vat_override','sale','account_accountant'],
    "data":['chatarra_unit_view.xml',
            'chatarra_view.xml',
            'chatarra_reposicion_view.xml',
            'res_partner_view.xml',
            'chatarra_asignacion_view.xml',
            'chatarra_doc_view.xml',
            'product_template_view.xml',
            'account_invoice_view.xml',
            'ir_config_parameter.xml',
            'chatarra_envio_view.xml',
            'report/report_view.xml',
            'report/report_units_late.xml'],
    "demo_xml": [],
    "update_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}
