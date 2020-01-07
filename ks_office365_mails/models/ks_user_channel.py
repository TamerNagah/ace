from odoo import models, fields, api, http, _
import requests
from datetime import datetime
import json
from odoo.http import request
from odoo.exceptions import ValidationError


class Office365MailChannel(models.Model):
    _inherit = "res.users"

    ks_office365_channel_inbox = fields.Many2one('mail.channel',
                                                 string="Office365 Inbox")
    ks_office365_channel_sentitems = fields.Many2one('mail.channel',
                                                     string="Office365 Sentitems")
    ks_office365_channel_archive = fields.Many2one('mail.channel',
                                                   string="Office365 Archive")

    def ks_generate_token(self):
        ks_mail_installed = self.env['ir.module.module']\
                                .sudo().search([('name', '=', 'ks_office365_mails'),
                                                ('state', '=', 'installed')])
        if ks_mail_installed:
            self.ks_create_private_mail_channel()
        return super(Office365MailChannel, self).ks_generate_token()

    def ks_create_private_mail_channel(self):
        """ A Private Mail channel for This User"""
        ks_initial_folder = ['Office365 Inbox',
                             'Office365 Sent Items',
                             'Office365 Archive']
        for folder in ks_initial_folder:
            ks_is_exist = False
            if folder == 'Office365 Inbox' and self.ks_office365_channel_inbox:
                ks_is_exist = True
            if folder == 'Office365 Sent Items' and self.ks_office365_channel_sentitems:
                ks_is_exist = True
            if folder == 'Office365 Archive' and self.ks_office365_channel_archive:
                ks_is_exist = True

            if not ks_is_exist:
                channel_obj = self.env['mail.channel']
                ks_data = {
                    'name': folder,
                    'channel_type': 'channel',
                    'public': 'private',
                }
                ks_channel_res = channel_obj.create(ks_data)
                if ks_channel_res:
                    channel_partner_obj = self.env['mail.channel.partner']
                    ks_partner_data = {
                        'partner_id': self.partner_id.id,
                        'channel_id': ks_channel_res.id,
                    }
                    ks_partner_res = channel_partner_obj.create(ks_partner_data)
                    ks_channel_res.update({
                        'channel_last_seen_partner_ids': [(4, ks_partner_res.id)]
                    })
                    if folder == 'Office365 Inbox':
                        self.ks_office365_channel_inbox = ks_channel_res.id
                    if folder == 'Office365 Sent Items':
                        self.ks_office365_channel_sentitems = ks_channel_res.id
                    if folder == 'Office365 Archive':
                        self.ks_office365_channel_archive = ks_channel_res.id
