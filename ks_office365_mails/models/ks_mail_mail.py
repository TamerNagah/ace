from odoo import models, fields, api, _


class Office365MailMail(models.Model):
    """ This class will override the mail.mail model
        And set the auto delete flag to False.
        This is done to save the mails for Syncing Purpose."""

    _inherit = "mail.mail"

    def create(self, values):
        """Overriding the Create Function of Original Mail.mail"""
        values['auto_delete'] = False
        res = super(Office365MailMail, self).create(values)
        return res

    def write(self, vals):
        vals['auto_delete'] = False
        res = super(Office365MailMail, self).write(vals)
        return res
