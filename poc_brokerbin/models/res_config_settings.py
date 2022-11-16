from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    brokerbin_link = fields.Char(related='company_id.brokerbin_link')
    brokerbin_user = fields.Char(related='company_id.brokerbin_user')
    brokerbin_pw = fields.Char(related='company_id.brokerbin_pw')
