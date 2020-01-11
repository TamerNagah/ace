# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
from odoo.exceptions import except_orm, UserError
from odoo.tools import ustr, pycompat

_logger = logging.getLogger(__name__)


class ResUser(models.Model):
    _inherit = 'res.users'

    def _default_required_field(self):
        res_config = self.env['res.config.settings'].sudo().get_values()
        if res_config.get('is_auto_generate_mail_server'):
            return True
        else:
            return False

    smtp_server_id = fields.One2many('ir.mail_server', 'user_id',
                                     'Email Server')
    mail_server_id = fields.Many2one('ir.mail_server', string='User')
    incoming_server_id = fields.Many2one('fetchmail.server', string='Incoming User')
    provider_id = fields.Many2one('mail.server', string="Provider")
    is_required_field = fields.Boolean(string='Is Required', compute='_compute_required_field', default=_default_required_field)

    @api.multi
    def _compute_required_field(self):
        for record in self:
            res_config = self.env['res.config.settings'].sudo().get_values()
            if res_config.get('is_auto_generate_mail_server'):
                record.is_required_field = True
            else:
                record.is_required_field = False

    @api.multi
    def test_connection(self):
        if not self.password_preference:
            raise UserError(_('Please Enter Password'))
        if not self.provider_id:
            raise UserError(_('Please Enter Provider'))
        self.set_mail_server()
        self._cr.commit()
        current_user = self.env['ir.mail_server'].search([('user_id','=',self.id)])
        self.mail_server_id = current_user.id
        mailserver = self.provider_id
        host_server = mailserver.smtp_host
        port_server = mailserver.smtp_port
        encryption_server = mailserver.smtp_encryption
        current_incoming_user = self.env['fetchmail.server'].search([('user_id', '=', self.id)])
        for server in current_user:
            smtp = False
            try:
                smtp = self.env['ir.mail_server'].connect(user=self.email,password=self.password_preference,host=host_server, encryption=encryption_server, port=port_server)
                # simulate sending an email from current user's address - without sending it!
                email_from, email_to = self.env.user.email, 'noreply@odoo.com'
                if not email_from:
                    raise UserError(_('Please configure an email on the current user to simulate '
                                      'sending an email message via this outgoing server'))
                # Testing the MAIL FROM step should detect sender filter problems
                (code, repl) = smtp.mail(email_from)
                if code != 250:
                    raise UserError(_('The server refused the sender address (%(email_from)s) '
                                      'with error %(repl)s') % locals())
                # Testing the RCPT TO step should detect most relaying problems
                (code, repl) = smtp.rcpt(email_to)
                if code not in (250, 251):
                    raise UserError(_('The server refused the test recipient (%(email_to)s) '
                                      'with error %(repl)s') % locals())
                # Beginning the DATA step should detect some deferred rejections
                # Can't use self.data() as it would actually send the mail!
                smtp.putcmd("data")
                (code, repl) = smtp.getreply()
                if code != 354:
                    raise UserError(_('The server refused the test connection '
                                      'with error %(repl)s') % locals())
            except UserError as e:
                print ("00")
                # let UserErrors (messages) bubble up
                raise e
            except Exception as e:
                raise UserError(_("Connection Test Failed! Here is what we got instead:\n %s") % ustr(e))
            finally:
                try:
                    smtp = self.env['ir.mail_server'].connect(user=self.email,password=self.password_preference,host=host_server, encryption=encryption_server, port=port_server)
                    # simulate sending an email from current user's address - without sending it!
                    email_from, email_to = self.env.user.email, 'noreply@odoo.com'
                    if not email_from:
                        raise UserError(_('Please configure an email on the current user to simulate '
                                          'sending an email message via this outgoing server'))
                    # Testing the MAIL FROM step should detect sender filter problems
                    (code, repl) = smtp.mail(email_from)
                    if code != 250:
                        raise UserError(_('The server refused the sender address (%(email_from)s) '
                                          'with error %(repl)s') % locals())
                    # Testing the RCPT TO step should detect most relaying problems
                    (code, repl) = smtp.rcpt(email_to)
                    if code not in (250, 251):
                        raise UserError(_('The server refused the test recipient (%(email_to)s) '
                                          'with error %(repl)s') % locals())
                    # Beginning the DATA step should detect some deferred rejections
                    # Can't use self.data() as it would actually send the mail!
                    smtp.putcmd("data")
                    (code, repl) = smtp.getreply()
                    if code != 354:
                        raise UserError(_('The server refused the test connection '
                                          'with error %(repl)s') % locals())
                except UserError as e:
                    print ("00")
                    # let UserErrors (messages) bubble up
                    raise e
                except Exception as e:
                    raise UserError(_("Connection Test Failed! Here is what we got instead:\n %s") % ustr(e))
                finally:
                    try:
                        if smtp:
                            smtp.close()
                    except Exception:
                        # ignored, just a consequence of the previous exception
                        pass
            if current_incoming_user:
                current_incoming_user.sudo().user = self.email
                current_incoming_user.sudo().password = self.password_preference
                current_incoming_user.sudo().button_confirm_login()
            self._cr.commit()
            raise UserError(_("Connection Test Succeeded! Everything seems properly set up!"))
        raise UserError(_("Please add mail service provider!"))

    @api.multi
    def set_mail_server(self):
        current_user = self.env['ir.mail_server'].search([('user_id', '=', self.id)])
        if current_user:
            self.mail_server_id = current_user.id

            dict = {
                'smtp_user': self.email,
                'smtp_pass': self.password_preference,
                'name': self.env.user.name,
                'user_id': self.id,
                'mail_server_id':self.provider_id.id
            }
            self.mail_server_id.sudo().write(dict)
        else:
            dict = {
                'smtp_user': self.email,
                'smtp_pass': self.password_preference,
                'name': self.env.user.name,
                'user_id': self.id,
                'mail_server_id': self.provider_id.id
            }
            self.env['ir.mail_server'].sudo().with_context(default_smtp_encryption=self.provider_id.smtp_encryption, default_smtp_port=self.provider_id.smtp_port).create(dict)

        current_incoming_user = self.env['fetchmail.server'].search([('user_id', '=', self.id)])
        if current_incoming_user:
            self.incoming_server_id = current_incoming_user.id

            incomingdict = {
                'user': self.email,
                'password': self.password_preference,
                'name': self.name,
                'user_id': self.id,
                'mail_server_id': self.provider_id.id
            }
            self.incoming_server_id.sudo().write(incomingdict)
        else:
            incomingdict = {
                'user': self.email,
                'password': self.password_preference,
                'name': self.name,
                'user_id': self.id,
                'mail_server_id': self.provider_id.id
            }
            self.env['fetchmail.server'].sudo().with_context(default_type=self.provider_id.type).create(incomingdict)
        return True

    @api.model
    def create(self, vals):
        res = super(ResUser, self).create(vals)

        res_config = self.env['res.config.settings'].sudo().get_values()
        if res_config.get('is_auto_generate_mail_server'):
            outgoingdict = {
                'smtp_user': res.email,
                'smtp_pass': res.password_preference,
                'name': res.name,
                'user_id': res.id,
                'mail_server_id': self.provider_id.id
            }
            self.env['ir.mail_server'].create(outgoingdict)

            incomingdict = {
                'user': res.email,
                'password': res.password_preference,
                'name': res.name,
                'user_id': res.id,
                'mail_server_id': self.provider_id.id
            }
            self.env['fetchmail.server'].create(incomingdict)
        return res

    @api.multi
    def write(self, vals):
        if self._context.get('preference_user') and not self._context.get('is_write_preference'):
            return super(ResUser, self).sudo().with_context(is_write_preference=1).write(vals)
        else:
            return super(ResUser, self).write(vals)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    password_preference = fields.Char(string='Password', help="Optional password for SMTP authentication")