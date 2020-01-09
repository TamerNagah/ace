from odoo import models, fields, api, http, _


class KsOffice365MailChannel(models.Model):
    _inherit = "res.users"

    def ks_generate_token(self):
        ks_mail_installed = self.env['ir.module.module']\
                                .sudo().search([('name', '=', 'ks_office365_mails'),
                                                ('state', '=', 'installed')])
        if ks_mail_installed:
            self.ks_create_outgoing_mail_server()
        return super(KsOffice365MailChannel, self).ks_generate_token()

    def ks_create_outgoing_mail_server(self):
        """ This Function Creates the Outgoing Mail server
            For Particular User. """
        ks_obj = self.env['ir.mail_server']
        ks_is_exists = ks_obj.search([('smtp_user', '=', self.partner_id.email)], limit=1)
        if not ks_is_exists:
            ks_data = {
                'name': "#Outlook Outgoing Mail Server for %s" %self.login,
                'smtp_host': 'smtp.office365.com',
                'smtp_port': 587,
                'smtp_user': self.partner_id.email,
                'smtp_encryption': 'starttls',
                'sequence': 20,
                'smtp_pass': 'password',
            }
            # Create the Outgoing Server
            try:
                ks_id = self.env['ir.mail_server'].create(ks_data)
            except Exception as err:
                pass

    def ks_clear_token(self):
        # Deleting The Outlook Outgoing server
        ks_mail_installed = self.env['ir.module.module'].sudo()\
                                .search([('name', '=', 'ks_office365_mails'),
                                        ('state', '=', 'installed')])
        if ks_mail_installed:
            ks_is_exists = self.env['ir.mail_server'].sudo().search([('smtp_user', '=', self.partner_id.email),
                                                              ('name', 'ilike', '#Outlook')])
            if ks_is_exists:
                ks_is_exists.unlink()

        return super(KsOffice365MailChannel, self).ks_clear_token()
