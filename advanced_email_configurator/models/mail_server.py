from odoo import models, fields,api, _
import smtplib

class MailServer(models.Model):
    _name = 'mail.server'
    _description = 'Mail Server'
    _rec_name = 'name'

    name = fields.Char(string="Provider name")
    smtp_host = fields.Char(string='SMTP Server', help="Hostname or IP of SMTP server")
    smtp_port = fields.Integer(string='SMTP Port', size=5, default=25,
                               help="SMTP Port. Usually 465 for SSL, and 25 or 587 for other cases.")
    smtp_debug = fields.Boolean(string='Debugging', help="If enabled, the full output of SMTP sessions will "
                                                         "be written to the server log at DEBUG level"
                                                         "(this is very verbose and may include confidential info!)")
    smtp_encryption = fields.Selection([('none', 'None'),
                                        ('starttls', 'TLS (STARTTLS)'),
                                        ('ssl', 'SSL/TLS')],
                                       string='Connection Security', default='none',
                                       help="Choose the connection encryption scheme:\n"
                                            "- None: SMTP sessions are done in cleartext.\n"
                                            "- TLS (STARTTLS): TLS encryption is requested at start of SMTP session (Recommended)\n"
                                            "- SSL/TLS: SMTP sessions are encrypted with SSL/TLS through a dedicated port (default: 465)")
    ir_mail_server_id = fields.Many2one('ir.mail_server',string="Ir Mail Server")
    server = fields.Char(string='Server Name', help="Hostname or IP of the mail server")
    port = fields.Integer(string="Port")
    type = fields.Selection([
        ('pop', 'POP Server'),
        ('imap', 'IMAP Server'),
        ('local', 'Local Server'),
    ], 'Server Type', index=True, default='pop')
    is_ssl = fields.Boolean('SSL/TLS',
                            help="Connections are encrypted with SSL/TLS through a dedicated port (default: IMAPS=993, POP3S=995)")
    fetchmail_id = fields.Many2one('fetchmail.server', string="Fetchmail")

    @api.onchange('smtp_encryption')
    def _onchange_encryption(self):
        result = {}
        if self.smtp_encryption == 'ssl':
            self.smtp_port = 465
            if not 'SMTP_SSL' in smtplib.__all__:
                result['warning'] = {
                    'title': _('Warning'),
                    'message': _('Your server does not seem to support SSL, you may want to try STARTTLS instead'),
                }
        else:
            self.smtp_port = 25
        return result

    @api.onchange('type', 'is_ssl')
    def onchange_server_type(self):
        self.port = 0
        if self.type == 'pop':
            self.port = self.is_ssl and 995 or 110
        elif self.type == 'imap':
            self.port = self.is_ssl and 993 or 143
        else:
            self.server = ''
