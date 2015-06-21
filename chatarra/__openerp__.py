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
    "author": "JARSA Sistemas, S.A. de C.V.",
    "website": "http://www.jarsa.com.mx",
    "category": "Chatarra",
    "depends": ['base_vat',                
                'account_accountant',
                'account_cancel',
                'pad'],
    "data":[
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/chatarra_view.xml',
            'views/chatarra_reposicion_view.xml',
            'views/res_partner_view.xml',
            'views/chatarra_asignacion_view.xml',
            'views/chatarra_documentos_view.xml',
            'views/product_product_view.xml',
            'views/account_invoice_view.xml',
            'views/ir_config_parameter.xml',
            'views/chatarra_envio_view.xml',
            'views/chatarra_marca_view.xml',
            'views/chatarra_tipo_view.xml',
            'views/chatarra_secretaria_view.xml',
            'views/chatarra_motivo_view.xml',
            'views/chatarra_certificado_wizard_view.xml',
            'views/chatarra_cita_wizard_view.xml',
            'views/chatarra_tarjeta_wizard_view.xml',
            'views/chatarra_detalle_wizard_view.xml',
            'views/chatarra_unit_view.xml',
            'reports/report_view.xml',
            'reports/report_units_late.xml',
            'reports/report_envio.xml',
            'data/chatarra_marca_data.xml',
            'data/chatarra_tipo_data.xml',
            'data/chatarra_motivo_data.xml',
            'data/product_data.xml',
            'data/res_partner_data.xml',
            'security/security_menu.xml',
            'static/src/js/chatarra.js',
            ],
    "demo_xml": [],
    "update_xml": [],
    "active": False,
    "installable": True,
    "certificate" : "",
}
