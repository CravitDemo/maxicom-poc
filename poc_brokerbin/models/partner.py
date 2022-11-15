from odoo import models, fields


class Partner(models.Model):
	_inherit = 'res.partner'

	vendor_rating = fields.Selection(
		[('options', 'Options'), ('good', 'Good'), ('average', 'Average'), ('poor', 'Poor')], string='Vendor Rating',
		default='average',required=True)
