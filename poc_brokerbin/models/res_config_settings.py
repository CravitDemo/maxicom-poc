from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    brokerbin_link = fields.Char(related='company_id.brokerbin_link')
    brokerbin_user = fields.Char(related='company_id.brokerbin_user')
    brokerbin_pw = fields.Char(related='company_id.brokerbin_pw')

    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     get_param = self.env['ir.config_parameter'].sudo().get_param
    #     brokerbin_link = get_param('poc_brokerbin.brokerbin_link')
    #     brokerbin_user = get_param('poc_brokerbin.brokerbin_user')
    #     brokerbin_pw = get_param('poc_brokerbin.brokerbin_pw')
    #
    #     res.update(
    #         brokerbin_link=brokerbin_link,
    #         brokerbin_user=brokerbin_user,
    #         brokerbin_pw=brokerbin_pw

    #     )
    #     return res

    # def set_values(self):
    #     super(ResConfigSettings, self).set_values()
    #     self.env['ir.config_parameter'].sudo().set_param('poc_brokerbin.brokerbin_link',
    #                                                      self.brokerbin_link)
    #     self.env['ir.config_parameter'].sudo().set_param('poc_brokerbin.brokerbin_user',
    #                                                      self.brokerbin_user)
    #     self.env['ir.config_parameter'].sudo().set_param('poc_brokerbin.brokerbin_pw',
    #                                                      self.brokerbin_pw)
