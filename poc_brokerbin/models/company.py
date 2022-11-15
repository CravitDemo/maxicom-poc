# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    brokerbin_link = fields.Char("BrokerBin Link", help="Link to the BB webservices")
    brokerbin_user = fields.Char("BrokerBin User", help="Username for the login")
    brokerbin_pw = fields.Char("BrokerBin Password", help="Password for the login")
