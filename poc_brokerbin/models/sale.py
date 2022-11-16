from odoo import models, _, api
from zeep import Client, Settings, helpers
from zeep.plugins import HistoryPlugin

history = HistoryPlugin()
from phpserialize import unserialize, phpobject


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	def get_sale_broker_bin_data(self):
		ctx = self._context.copy()
		ctx.update({'search_default_group_by_partid': 1})
		action = {
			'name': _('BrokenBin'),
			'view_mode': 'tree',
			'res_model': 'sale.brokerbin',
			'view_id': self.env.ref('poc_brokerbin.view_sale_brokerbin_tree').id,
			'type': 'ir.actions.act_window',
			'domain': [('sale_order_id', '=', self.id)],
			'context': ctx,
			'target': 'current'
		}
		return action

	def brokerbin_connect(self):
		brokerbin_link = self.env.company.brokerbin_link
		brokerbin_user = self.env.company.brokerbin_user
		brokerbin_pw = self.env.company.brokerbin_pw
		client = Client(brokerbin_link, plugins=[history])

		authToken = client.service.Authenticate(reqUsername=brokerbin_user, reqPassword=brokerbin_pw, reqOptions=[])
		partId = 'PA-FE-TX'
		searchOptions = dict()
		searchOptions["max_resultset"] = 250
		searchOptions["search_type"] = 'partkey'
		searchOptions["sort_by"] = 'price'
		searchOptions["sort_order"] = 'ASC'
		searchOptions["contact"] = True
		searchOptions["uid"] = authToken
		xmlSearchOptions = helpers.create_xml_soap_map(searchOptions)
		result = client.service.Search(reqPart=partId, reqOptions=xmlSearchOptions)
		unserializedResult = unserialize(bytes(result, 'utf-8'), object_hook=phpobject)
		results = unserializedResult[b'resultset'][0][b'result']
		return results

	def data_process_order_line(self, vals_dict, order_line):
		for line in order_line:
			if vals_dict.get('part') and vals_dict.get('part') == line.product_id.default_code:
				broken_bin_data = {
					'vendor': vals_dict.get('company'),
					'country': vals_dict.get('country'),
					'partid': vals_dict.get('part'),
					'price': vals_dict.get('price'),
					'quantity': vals_dict.get('qty'),
					'description': vals_dict.get('description'),
					'state': vals_dict.get('status'),
					'contact_phone': vals_dict.get('comp_phone'),
					'contact_email': vals_dict.get('comp_email'),
					'sale_order_id': self.id,
					'sale_order_line_id': line.id,
				}
				self.env['sale.brokerbin'].create(broken_bin_data)

	def reload_brokerbin_data(self):
		for line in self.order_line:
			brokerbin_ids = self.env['sale.brokerbin'].search([('sale_order_id', '=', self.id),
															   ('sale_order_line_id', '=', line.id)])
			if brokerbin_ids:
				brokerbin_ids.unlink()
		results = self.brokerbin_connect()
		for index in results:
			item = results[index]
			vals_dict = {}
			for key in item:
				vals_dict[key.decode("utf-8")] = item[key].decode("utf-8")
			self.data_process_order_line(vals_dict, self.order_line)
			print("\n\n\n")
		return True


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	def reload_brokerbin_data(self):
		action = {
			'name': _('BrokenBin'),
			'view_mode': 'tree',
			'res_model': 'sale.brokerbin',
			'view_id': self.env.ref('poc_brokerbin.view_sale_brokerbin_tree').id,
			'type': 'ir.actions.act_window',
			'domain': [('sale_order_line_id', '=', self.id)],
			'target': 'current'
		}
		return action

	def write(self, vals):
		res = super(SaleOrderLine, self).write(vals)
		if 'product_id' in vals:
			brokerbin_ids = self.env['sale.brokerbin'].search([('sale_order_id', '=', self.order_id.id),
															   ('sale_order_line_id', '=', self.id)])
			if brokerbin_ids:
				brokerbin_ids.unlink()
			results = self.order_id.brokerbin_connect()
			for index in results:
				item = results[index]
				vals_dict = {}
				for key in item:
					vals_dict[key.decode("utf-8")] = item[key].decode("utf-8")
				self.order_id.data_process_order_line(vals_dict, self)
		return res

	@api.model
	def create(self, vals):
		res = super(SaleOrderLine, self).create(vals)
		results = res.order_id.brokerbin_connect()
		for index in results:
			item = results[index]
			vals_dict = {}
			for key in item:
				vals_dict[key.decode("utf-8")] = item[key].decode("utf-8")
			res.order_id.data_process_order_line(vals_dict, res)

		return res
