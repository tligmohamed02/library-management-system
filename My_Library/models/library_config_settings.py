

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    daily_fine_rate = fields.Integer(config_parameter='My_Library.daily_fine_rate')
    renewal_amount_monthly = fields.Integer(config_parameter='My_Library.renewal_amount_monthly')
    renewal_amount_semestry = fields.Integer(config_parameter='My_Library.renewal_amount_semestry')
    renewal_amount_yearly = fields.Integer(config_parameter='My_Library.renewal_amount_yearly')
    penalty_days_mail = fields.Integer(config_parameter='My_Library.penalty_days_mail')
