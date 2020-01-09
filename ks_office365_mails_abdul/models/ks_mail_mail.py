from odoo import models, fields, api, _


class KsOffice365MailMail(models.Model):
    """ This class will override the mail.mail model. """

    _inherit = "mail.mail"

    @api.model
    def create(self, values):
        """Overriding the Create Function of Original Mail.mail"""
        # These code are to get the outlook mail server id
        if 'mail_message_id' in values:
            ks_username = self.env['mail.message'].search([('id', '=', values['mail_message_id'])],
                                                          limit=1).author_id.email
            ks_mail_server_id = self.env['ir.mail_server'].search([('smtp_user', '=', ks_username)],
                                                                  limit=1).id
            if ks_mail_server_id:
                values['mail_server_id'] = ks_mail_server_id
        return super(KsOffice365MailMail, self).create(values)
