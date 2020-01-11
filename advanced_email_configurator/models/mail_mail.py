# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    user_id = fields.Many2one('res.users', string='Owner')
    mail_server_id = fields.Many2one('mail.server', string="Outgoing Provider")
    smtp_host = fields.Char(string='SMTP Server', related='mail_server_id.smtp_host', help="Hostname or IP of SMTP server")
    smtp_port = fields.Integer(string='SMTP Port', related='mail_server_id.smtp_port', size=5, default=25,
                               help="SMTP Port. Usually 465 for SSL, and 25 or 587 for other cases.")
    smtp_debug = fields.Boolean(string='Debugging', related='mail_server_id.smtp_debug', help="If enabled, the full output of SMTP sessions will "
                                                         "be written to the server log at DEBUG level"
                                                         "(this is very verbose and may include confidential info!)")
    smtp_encryption = fields.Selection([('none', 'None'),
                                        ('starttls', 'TLS (STARTTLS)'),
                                        ('ssl', 'SSL/TLS')],
                                       string='Connection Security', default='none',
                                       related='mail_server_id.smtp_encryption',
                                       help="Choose the connection encryption scheme:\n"
                                            "- None: SMTP sessions are done in cleartext.\n"
                                            "- TLS (STARTTLS): TLS encryption is requested at start of SMTP session (Recommended)\n"
                                            "- SSL/TLS: SMTP sessions are encrypted with SSL/TLS through a dedicated port (default: 465)")

    _sql_constraints = [
        ('smtp_user_uniq', 'unique(user_id)',
         'That user already has a SMTP server.')
    ]

    @api.model
    def send_email(self, message, mail_server_id=None,
                   smtp_server=None, smtp_port=None, smtp_user=None,
                   smtp_password=None, smtp_encryption=None,
                   smtp_debug=False,smtp_session=None):



        from_rfc2822 = extract_rfc2822_addresses(message['From'])
        server_id = self.env['ir.mail_server'].search([
            ('smtp_user', 'in', from_rfc2822)])
        if server_id and server_id[0]:
            if 'Return-Path' in message:
                message.replace_header('Return-Path', from_rfc2822)
        return super(IrMailServer, self).send_email(message, mail_server_id,
                                                   smtp_server, smtp_port,
                                                   smtp_user, smtp_password,
                                                   smtp_encryption,
                                                   smtp_debug,smtp_session)


class MailMail(models.Model):
    _inherit = 'mail.mail'

    def send(self, auto_commit=False, raise_exception=False):

        for email in self.env['mail.mail'].browse(self.ids):
            from_rfc2822 = extract_rfc2822_addresses(email.email_from)
            server_id = self.env['ir.mail_server'].search([
                ('smtp_user', 'in', from_rfc2822)])
            server_id = server_id and server_id[0] or False
            if server_id:
                self.write(
                    {'mail_server_id': server_id[0].id,
                     'reply_to': email.email_from})
            else:
                server_id = self.env['ir.mail_server'].search([], order="sequence", limit=1)
                server_id = server_id.id or False
                server_obj = self.env['ir.mail_server'].browse(server_id)
                if server_id:
                    self.write(
                               {'mail_server_id': server_id,
                                'email_from': server_obj.smtp_user,
                                'reply_to': server_obj.smtp_user})
        return super(MailMail, self).send(auto_commit=auto_commit,
                                          raise_exception=raise_exception)
