from datetime import datetime
import werkzeug
import logging
import werkzeug.utils
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RedirectCode(http.Controller):

    @http.route("/office365/callback", auth="public")
    def fetch_code(self, **kwargs):
        ks_user = request.env['res.users'].sudo().search([('id', '=', request.env.user.id)])
        if "error" in kwargs:
            _logger.error('Login with Microsoft Failed \nReason: %s' % kwargs["error"])

        ks_setting = request.env['ks_office365.settings'].sudo().search([], limit=1)
        if 'state' in kwargs and kwargs['state'] == 'office_login':
            ks_setting.write({'ks_office_login': True})

        if 'code' in kwargs:
            ks_code = kwargs.get('code')
            if not ks_setting.ks_office_login:
                ks_user.write({'ks_code': ks_code})
                ks_user.ks_generate_token()
                return request.render("ks_office365_base.ks_authentication_redirect_success_page", {})

            else:
                user = ks_user.ks_login_office_user(ks_setting, ks_code)
                if not user:
                    return werkzeug.utils.redirect("/")
                request.session.rotate = True
                request.session.uid = user.id
                request.session.login = user.login
                request.session.session_token = user.id and user._compute_session_token(request.session.sid)
                request.uid = user.id
                request.disable_db = False
                ks_setting.write({'ks_office_login': False})
                _logger.info('\'%s\' successfully logged in with Microsoft' % user.name)
                return werkzeug.utils.redirect("/")
        else:
            return request.render("ks_office365_base.ks_authentication_redirect_fail_page", {})

