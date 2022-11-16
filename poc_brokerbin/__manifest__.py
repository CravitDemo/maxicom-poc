##############################################################################
#
#    Author: Cravit.
#    Copyright 2017 B-informed B.V.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
	"name": "BrokerBin",
	"summary": "BrokerBin",
	"description": """
	This module design for an integration with a 3rd party called BrokerBin (BB) (https://brokerbin.com/ ). 
	This 3rd party is used by the customer to reflect prices and stock of suppliers during the sales process.
    """,
	"website": "https://www.cravit.nl",
	'version': "15.0.1.0.0",
	"author": "Cravit",
	"license": "OPL-1",
	'category': 'sale',
	"depends": [
		'sale', 'product'
	],
	"qweb": [],
	'data': [
		'security/ir.model.access.csv',
		'data/brokerbin_cron.xml',
		'views/company_view.xml',
		'views/res_config_settings_view.xml',
		'views/broker_bin_view.xml',
		'views/partner_inherit_view.xml',
		'views/sale_form_view.xml',
	]
}
