from odoo import models, fields
from zeep import Client, Settings, helpers
from zeep.plugins import HistoryPlugin
history = HistoryPlugin()
from phpserialize import unserialize, phpobject
import logging

_logger = logging.getLogger(__name__)


class SaleBrokerbin(models.Model):
    _name = 'sale.brokerbin'
    _rec_name = 'sale_order_id'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', help='To have the option to show all BB records per SO')
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', help='To have the option to update all bb records for this order line')
    brokerbin_user = fields.Char("BrokerBin User", help="Username for the login")
    partid = fields.Char("PartID")
    country = fields.Char("Country", help="Country of the vendor")
    vendor = fields.Char("Vendor", help="Name of the vendor")
    email = fields.Char("eMail", help="Email of the vendor")
    phone = fields.Char("Phone", help="Phone of the vendor")
    quantity = fields.Char("Quantity", help="QTY of available products")
    state = fields.Char("State", help="Country of the vendor")
    currency_id = fields.Many2one('res.currency', default=lambda x: x.env.company.currency_id)
    # price = fields.Monetary("Price", currency_field="currency_id")
    price = fields.Char("Price")
    description = fields.Char("Description", help="Description from BB")
    contact = fields.Many2one('res.partner', string='Contact')
    contact_email = fields.Char(string='Email')
    contact_phone = fields.Char(string='Phone')
    # contact_email = fields.Char(related='contact.email')
    # contact_phone = fields.Char(related='contact.phone')
    payment_term = fields.Many2one('account.payment.term', related='contact.property_supplier_payment_term_id')
    rating = fields.Selection(related='contact.vendor_rating', string="Rating")


    def _cron_pull_brokenbin_data(self):
        brokerbin_link = self.env.company.brokerbin_link
        brokerbin_user = self.env.company.brokerbin_user
        brokerbin_pw = self.env.company.brokerbin_pw
        client = Client(brokerbin_link, plugins=[history])

        print("aaaaaaa", brokerbin_link)
        print("brokerbin_user........",brokerbin_user, brokerbin_pw)
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

        print('Searching for [' + partId + ']...')
        result = client.service.Search(reqPart=partId, reqOptions=xmlSearchOptions)
        unserializedResult = unserialize(bytes(result, 'utf-8'), object_hook=phpobject)
        results = unserializedResult[b'resultset'][0][b'result']
        for index in results:
            item = results[index]
            print('Result [' + str(index) + ']: ')
            vals_dict = {}
            for key in item:
                vals_dict[key.decode("utf-8")] = item[key].decode("utf-8")
                _logger.info('Data============={0}:-'.format(vals_dict.get('part')))
            print("vals_dict...........",vals_dict)
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
            }
            print("broken_bin_data..........",broken_bin_data)
            print("\n\n\n")
            self.create(broken_bin_data)










