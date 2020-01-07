from odoo import models, fields, api, http, _
import requests
from datetime import datetime
import json
from odoo.http import request
from odoo.exceptions import ValidationError


class KsJob(models.Model):
    _name = "ks.office.job"
    _order = "id desc"

    ks_records = fields.Integer(string="Records Processed", default=0)
    ks_status = fields.Selection([('in_process', 'In Process'), ('completed', 'Completed'), ('error', 'Error')],
                                 string="Status")
    ks_error_text = fields.Text("Error Message")
    ks_job = fields.Selection([('calendar_import', 'Office to Odoo'), ('calendar_export', 'Odoo to Office'),
                               ('contact_import', 'Office to Odoo'), ('contact_export', 'Odoo to Office'),
                               ('mail_import', 'Office to Odoo'), ('mail_export', 'Odoo to Office'),
                               ('task_import', 'Office to Odoo'), ('task_export', 'Odoo to Office')], string="Operation")
    ks_module = fields.Selection([('calendar', 'Calendar'), ('contact', 'Contact'), ('mail', 'Mail'), ('task', 'Task')],
                                 string="Module")

    def ks_complete_any_job(self):
        for job in self:
            job.write({'ks_status': 'completed'})


class Office365(models.Model):
    _inherit = "res.users"

    ks_code = fields.Char("Code")
    ks_scope = fields.Char("Scope")
    ks_auth_token = fields.Char("Authorization Token", store=True)
    ks_auth_refresh_token = fields.Char("Refresh Token", store=True)

    def ks_is_job_completed(self, ks_job, ks_module):
        ks_previous_job = self.env["ks.office.job"].search([('ks_records', '>=', 0), ('ks_status', '=', 'error'),
                                                            ('ks_module', '=', ks_module),
                                                            ('create_uid', '=', self.env.user.id)])
        is_ks_process_running = self.env["ks.office.job"].search(
            [('ks_records', '>=', 0), ('ks_status', '=', 'in_process'),
             ('ks_job', '=', ks_job), ('create_uid', '=', self.id)])

        if is_ks_process_running:
            return False
        elif ks_previous_job and ks_previous_job[0].ks_job == ks_job:
            return ks_previous_job[0]
        else:
            return self.env["ks.office.job"].create({'ks_status': 'in_process',
                                                     'ks_module': ks_module,
                                                     'ks_job': ks_job})

    def ks_get_installed_modules(self):
        ks_calendar_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_calendar'), ('state', '=', 'installed')])
        ks_contact_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_contacts'), ('state', '=', 'installed')])
        ks_task_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_tasks'), ('state', '=', 'installed')])
        ks_mail_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_mails'), ('state', '=', 'installed')])

        return {
            "calendar": ks_calendar_installed or False,
            "contact": ks_contact_installed or False,
            "task": ks_task_installed or False,
            "mail": ks_mail_installed or False,
        }

    """ Cron function for automatic syncing"""
    def run_import_contact_cron(self):
        for user in self.env['res.users'].search([]):
            if 'Internal User' in user.groups_id.mapped('name'):
                if not user.ks_auth_token:
                    user.ks_create_log("contact", user.name, "", 0, datetime.now(), "office_to_odoo",
                                       "authentication", "failed",
                                       "Generate Authentication Token. '%s\' has not generated token yet." % user.name)
                    continue
                user.ks_get_contacts()

    def ks_run_import_task_cron_functions(self):
        for user in self.env['res.users'].search([]):
            if 'Internal User' in user.groups_id.mapped('name'):
                if not user.ks_auth_token:
                    user.ks_create_log("task", user.name, "", 0, datetime.now(), "office_to_odoo",
                                       "authentication", "failed",
                                       "Generate Authentication Token. '%s\' has not generated token yet." % user.name)
                    continue
                user.ks_get_tasks()

    def run_export_contact_cron(self):
        for user in self.env['res.users'].search([]):
            if 'Internal User' in user.groups_id.mapped('name'):
                if not user.ks_auth_token:
                    user.ks_create_log("contact", user.name, "", 0, datetime.now(), "odoo_to_office",
                                       "authentication", "failed",
                                       "Generate Authentication Token. '%s\' has not generated token yet." % user.name)
                    continue
                user.ks_post_contacts()

    def ks_run_export_task_cron_functions(self):
        for user in self.env['res.users'].search([]):
            if 'Internal User' in user.groups_id.mapped('name'):
                if not user.ks_auth_token:
                    user.ks_create_log("task", user.name, "", 0, datetime.now(), "odoo_to_office",
                                       "authentication", "failed",
                                       "Generate Authentication Token. '%s\' has not generated token yet." % user.name)
                    continue
                user.ks_post_tasks()

    # Function Responsible for Syncing Mail From Office 365 To Odoo
    def ks_run_import_mails_cron_functions(self):
        for user in self.env['res.users'].search([]):
            if 'Internal User' in user.groups_id.mapped('name'):
                if not user.ks_auth_token:
                    user.ks_create_log("task", user.name, "", 0, datetime.now(), "odoo_to_office",
                                       "authentication", "failed",
                                       "Generate Authentication Token. '%s\' has not generated token yet." % user.name)
                    continue
                user.ks_get_mails()

    # Function Responsible for Syncing Mail From Odoo to Office 365
    def ks_run_export_mails_cron_functions(self):
        for user in self.env['res.users'].search([]):
            if 'Internal User' in user.groups_id.mapped('name'):
                if not user.ks_auth_token:
                    user.ks_create_log("task", user.name, "", 0, datetime.now(), "odoo_to_office",
                                       "authentication", "failed",
                                       "Generate Authentication Token. '%s\' has not generated token yet." % user.name)
                    continue
                user.ks_post_mails()

    def open_current_user(self):
        return {
            'name': 'User form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.users',
            'view_id': self.env.ref('ks_office365_base.ks_office365_main_form').id,
            'res_id': self.env.user.id,
            'context': {
                'default_form_view_ref': 'ks_office365_base.ks_office365_view_users_form'
            }
        }

    def get_authentication_code(self):
        ks_admin = self.env['ks_office365.settings'].sudo().search([])
        ks_client_id = ks_admin.ks_client_id
        ks_client_secret = ks_admin.ks_client_secret
        ks_redirect_url = ks_admin.ks_redirect_url
        ks_computed_scope = self.get_scope()

        if type(ks_computed_scope) is dict:
            return ks_computed_scope

        ks_scope = "offline_access " + ks_computed_scope
        self.sudo().ks_scope = ks_scope

        if not ks_client_id or not ks_client_secret or not ks_redirect_url:
            self.ks_create_log("authentication", "Authentication", "", 0, datetime.today(), "authentication",
                               "authentication", "failed",
                               "Client ID not entered!")
            return self.ks_show_error_message(_("Client ID, Client Secret and Redirect URI are required!"))

        data = (ks_client_id, "code", ks_redirect_url, ks_scope, "query", "ks_success")
        url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=%s" \
              "&response_type=%s&redirect_uri=%s&scope=%s&response_mode=%s&state=%s" % data

        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': url
        }

    def ks_generate_token(self):
        ks_current_datatime = datetime.today()
        api_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        ks_auth_user = self.env["ks_office365.settings"].sudo().search([], limit=1)
        ks_client_id = ks_auth_user.ks_client_id
        ks_client_secret = ks_auth_user.ks_client_secret
        ks_redirect_url = ks_auth_user.ks_redirect_url
        ks_scope = self.ks_scope
        ks_code = self.ks_code

        if not ks_auth_user or not ks_code:
            self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                               "authentication", "failed", "Access Denied! \nUser is not authenticated.")
            return self.ks_show_error_message("Access Denied! \nUser is not authenticated.")

        ks_data = {
            "client_id": ks_client_id,
            "client_secret": ks_client_secret,
            "redirect_uri": ks_redirect_url,
            "code": ks_code,
            "scope": ks_scope,
            "grant_type": "authorization_code",
        }
        try:
            response = requests.post(api_endpoint, data=ks_data)
        except Exception as ex:
            return self.ks_show_error_message("Internet connected failed!")
        json_data = json.loads(response.text)
        if "access_token" in json_data:
            access_token = json_data['access_token']
            refresh_token = json_data['refresh_token']
            token_type = json_data['token_type']
            self.ks_auth_token = token_type + " " + access_token
            self.ks_auth_refresh_token = refresh_token
            self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                               "authentication", "success", "Token generated successful!")
        else:
            self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                               "authentication", "failed", json_data['error_description'])
            return self.ks_show_error_message("Authentication failed!\n Check log to know more")

    """ Login with MIcrosoft Account """
    def ks_login_office_user(self, ks_setting, ks_code):
        ks_client_id = ks_setting.ks_client_id
        ks_client_secret = ks_setting.ks_client_secret
        ks_redirect_url = ks_setting.ks_redirect_url
        ks_scope = "User.Read"
        ks_data = {
            "client_id": ks_client_id,
            "client_secret": ks_client_secret,
            "redirect_uri": ks_redirect_url,
            "code": ks_code,
            "scope": ks_scope,
            "grant_type": "authorization_code",
        }
        try:
            response = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=ks_data)
        except Exception as ex:
            return self.ks_show_error_message("Internet connected failed!")
        json_data = json.loads(response.text)
        if "access_token" in json_data:
            access_token = json_data['access_token']
            refresh_token = json_data['refresh_token']
            token_type = json_data['token_type']
            ks_auth_token = token_type + " " + access_token
            ks_head = {
                "Authorization": ks_auth_token,
                "Host": "graph.microsoft.com"
            }
            ks_response = requests.get("https://graph.microsoft.com/v1.0/me/", headers=ks_head)
            ks_json = json.loads(ks_response.text)
            if 'error' not in ks_json:
                _name = ks_json['displayName']
                _email = ks_json['userPrincipalName']

                user = request.env['res.users'].sudo().search([('login', '=', _email)])
                if not user:
                    user = request.env['res.users'].sudo().create({'name': _name, 'login': _email, 'email': _email})

                group_ids = self.env['res.groups']\
                    .search([('name', 'in', ['Office365 Users', 'Contact Creation', 'Technical Features'])]).ids
                group_ids.append(self.env.ref('base.group_user').id)
                user.groups_id = [(4, gid) for gid in group_ids]
                return user
            else:
                raise ValidationError(_("Error Logging In \nReason: %s" % ks_json['error_description']))
        else:
            raise ValidationError(_("Error Logging In \nReason: %s" % json_data['error_description']))

    """ Defines scope for token generation """
    def get_scope(self):
        ks_current_datatime = datetime.today()

        ks_scope = ""
        ks_calendar_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_calendar'), ('state', '=', 'installed')])
        ks_contact_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_contacts'), ('state', '=', 'installed')])
        ks_task_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_tasks'), ('state', '=', 'installed')])
        ks_mail_installed = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'ks_office365_mails'), ('state', '=', 'installed')])

        if ks_calendar_installed:
            if self.ks_import_office_calendar and not self.ks_export_office_calendar:
                ks_scope = "Calendars.Read"
            elif self.ks_export_office_calendar:
                ks_scope = "Calendars.ReadWrite"
            else:
                self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                   "authentication", "failed", "Calendar scope not specified.")
                return self.ks_show_error_message("Scope of the Calendar is not defined.")

        if ks_contact_installed:
            if ks_scope == "":
                if self.ks_import_office365_contact and not self.ks_export_office365_contact:
                    ks_scope = "Contacts.Read"
                elif self.ks_export_office365_contact:
                    ks_scope = "Contacts.ReadWrite"
                else:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication",
                                       "failed", "Contact scope not specified.")
                    return self.ks_show_error_message("Scope of the Contacts is not defined.")
            else:
                if self.ks_import_office365_contact and not self.ks_export_office365_contact:
                    ks_scope += " Contacts.Read"
                elif self.ks_export_office365_contact:
                    ks_scope += " Contacts.ReadWrite"
                else:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication",
                                       "failed", "Contact scope not specified.")
                    return self.ks_show_error_message("Scope of the Contacts is not defined.")

        if ks_task_installed:
            if ks_scope == "":
                if self.ks_task_import and not self.ks_task_export:
                    ks_scope = "Tasks.Read"
                elif self.ks_task_export:
                    ks_scope = "Tasks.ReadWrite"
                else:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication",
                                       "failed", "Tasks scope not specified.")
                    return self.ks_show_error_message("Scope of the Tasks is not defined.")
            else:
                if self.ks_task_import and not self.ks_task_export:
                    ks_scope += " Tasks.Read"
                elif self.ks_task_export:
                    ks_scope += " Tasks.ReadWrite"
                else:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication",
                                       "failed", "Tasks scope not specified.")
                    return self.ks_show_error_message("Scope of the Tasks is not defined.")

        if ks_mail_installed:
            if ks_scope == "":
                if self.ks_import_office365_mail and not self.ks_export_office365_mail:
                    ks_scope = "Mail.Read"
                elif self.ks_export_office365_mail:
                    ks_scope = "Mail.ReadWrite"
                else:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication",
                                       "failed", "Mail scope not specified.")
                    return self.ks_show_error_message("Scope of the Mail is not defined.")
            else:
                if self.ks_import_office365_mail and not self.ks_export_office365_mail:
                    ks_scope += " Mail.Read"
                elif self.ks_export_office365_mail:
                    ks_scope += " Mail.ReadWrite"
                else:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication",
                                       "failed", "Mail scope not specified.")
                    return self.ks_show_error_message("Scope of the Mail is not defined.")

        if not ks_scope:
            raise ValidationError(_("You have to install at least one of the modules to generate token"))

        return ks_scope

    """ Refresh authentication Token """
    def refresh_token(self):
        ks_current_datatime = datetime.today()
        api_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

        ks_auth_user = self.env["ks_office365.settings"].sudo().search([], limit=1)
        ks_client_id = ks_auth_user.ks_client_id
        ks_client_secret = ks_auth_user.ks_client_secret
        ks_redirect_url = ks_auth_user.ks_redirect_url
        ks_scope = self.ks_scope

        if not ks_auth_user:
            self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                               "authentication", "failed", "Access Denied!\n User is not authenticated.")
            return self.ks_show_error_message("Access Denied!\n User is not authenticated.")

        ks_data = {
            "client_id": ks_client_id,
            "client_secret": ks_client_secret,
            "redirect_uri": ks_redirect_url,
            "refresh_token": self.ks_auth_refresh_token,
            "scope": ks_scope,
            "grant_type": "refresh_token",
        }

        try:
            response = requests.post(api_endpoint, data=ks_data)
        except Exception as ex:
            return self.ks_show_error_message("Internet connected failed!")
        json_data = json.loads(response.text)
        if "access_token" in json_data:
            access_token = json_data['access_token']
            refresh_token = json_data['refresh_token']
            token_type = json_data['token_type']
            self.sudo().ks_auth_token = token_type + " " + access_token
            self.sudo().ks_auth_refresh_token = refresh_token
            self.sudo().ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                      "authentication", "success", "Token refreshed successful!")
        else:
            if response.status_code == 401:
                self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                   "authentication", "failed", "Invalid value of Client Secret!")
                return self.ks_show_error_message("Invalid value of Client Secret!")
            else:
                if "error_codes" in json_data:
                    self.ks_create_log("authentication", "Authentication", "", 0, ks_current_datatime, "authentication",
                                       "authentication", "failed", json_data['error_description'])
                    return self.ks_show_error_message("Authentication failed!\n Check log to know more")

    def ks_has_sync_error(self):
        return {
            'type': 'ir.actions.client',
            'params': {
                'task': 'notify',
                'message': 'Sync Completed!\n Some events could not be synced. \nPlease check log for more information.',
            },
            'tag': 'ks_base_message'
        }

    """ Redirect to logs """
    def ks_no_sync_error(self):
        return {
            'name': 'Office365 logs',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'ks_office365.logs',
            'view_id': False,
            'context': self.env.context,
        }

    """ Display error message """
    def ks_show_error_message(self, message):
        return {
            'type': 'ir.actions.client',
            'params': {
                'task': 'warn',
                'message': message,
            },
            'tag': 'ks_base_message'
        }

    """ Create log for every record """
    def ks_create_log(self, ks_module_type, ks_rec_name, ks_office_id, ks_odoo_id, ks_date, ks_operation,
                      ks_operation_type, ks_status, ks_message):
        ks_vals = {
            "ks_record_name": ks_rec_name,
            "ks_user": self.id,
            "ks_module_type": ks_module_type,
            "ks_office_id": ks_office_id,
            "ks_odoo_id": ks_odoo_id,
            "ks_date": ks_date,
            "ks_operation": ks_operation,
            "ks_operation_type": ks_operation_type,
            "ks_status": ks_status,
            "ks_message": ks_message,
        }
        self.env["ks_office365.logs"].sudo().create(ks_vals)
