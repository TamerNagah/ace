# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_auto_generate_mail_server = fields.Boolean(string="Is Auto Generate mail server", default=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            is_auto_generate_mail_server=self.env['ir.config_parameter'].sudo().get_param('tko_mail_smtp_per_user.is_auto_generate_mail_server')
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('tko_mail_smtp_per_user.is_auto_generate_mail_server', self.is_auto_generate_mail_server)