from odoo import http
from odoo.http import request
import os
from string import punctuation


class WebsiteShopBrands(http.Controller):
    # Fixme-  Find a way to save customization settings in attachment

    @http.route([
        '/write/updated/scss',
    ], type='http', auth="public", website=True)
    def KsWriteUpdatedScss(self, **kw):
        if kw.get('color',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_scss_path = "/static/src/css/ks_updated_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_scss_path, 'w+')
            f.write(kw['color']+'\n'+kw['theme_textcolor'])
            f.close()
            self.createQwebIfNotAvialable('ks_theme_kinetik.ks_updated_color_' + str(request.website.id),
                                          'ks_updated_color_' + str(request.website.id))
            self.active_current_website_css("/ks_updated_color_")

        elif kw.get('theme_text_color',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_scss_path = "/static/src/css/ks_updated_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_scss_path, 'w+')
            f.write(kw['theme_color']+'\n'+kw['theme_text_color'])
            f.close()
            self.createQwebIfNotAvialable('ks_theme_kinetik.ks_updated_color_' + str(request.website.id),
                                          'ks_updated_color_' + str(request.website.id))
            self.active_current_website_css("/ks_updated_color_")
        elif kw.get('reset_themetcolor',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_scss_path = "/static/src/css/ks_updated_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_scss_path, 'w+')
            f.write(kw['reset_themecolor']+'\n'+kw['reset_themetcolor'])
            f.close()
            self.createQwebIfNotAvialable('ks_theme_kinetik.ks_updated_color_' + str(request.website.id),
                                          'ks_updated_color_' + str(request.website.id))
            self.active_current_website_css("/ks_updated_color_")
        return None

    @http.route([
        '/write/updated/buttonscss',
    ], type='http', auth="public", website=True)
    def KsWriteUpdatedButtonScss(self, **kw):
        if kw.get('textcolor',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = "/static/src/css/ks_updated_button_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_button_scss_path, 'w+')
            f.write(kw['textcolor']+'\n'+kw['text_bgcolor']+'\n'+kw['text_radius']+'\n'+kw['text_border'])
            f.close()
            self.createQwebIfNotAvialableButton('ks_theme_kinetik.ks_updated_button_color_'+str(request.website.id),'ks_updated_button_color_'+str(request.website.id))
            self.active_current_website_buttoncss("/ks_updated_button_color_")
        elif kw.get('bgcolor',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = "/static/src/css/ks_updated_button_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_button_scss_path, 'w+')
            f.write(kw['bg_textcolor']+'\n'+kw['bgcolor']+'\n'+kw['bg_radius']+'\n'+kw['bg_boder_color'])
            f.close()
            self.createQwebIfNotAvialableButton('ks_theme_kinetik.ks_updated_button_color_' + str(request.website.id),
                                          'ks_updated_button_color_' + str(request.website.id))
            self.active_current_website_buttoncss("/ks_updated_button_color_")
        elif kw.get('button_radius',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = "/static/src/css/ks_updated_button_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_button_scss_path, 'w+')
            f.write(kw['tcolor'] + '\n' + kw['bcolor']+'\n'+kw['button_radius']+'\n'+kw['btn_bcolor'])
            f.close()
            self.createQwebIfNotAvialableButton('ks_theme_kinetik.ks_updated_button_color_' + str(request.website.id),
                                          'ks_updated_button_color_' + str(request.website.id))
            self.active_current_website_buttoncss("/ks_updated_button_color_")

        elif kw.get('resettxtcolor',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = "/static/src/css/ks_updated_button_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_button_scss_path, 'w+')
            f.write(kw['resettxtcolor'] + '\n' + kw['reset_bgcolor']+'\n'+kw['reset_radius']+'\n'+kw['resetborder'])
            f.close()
            self.createQwebIfNotAvialableButton('ks_theme_kinetik.ks_updated_button_color_' + str(request.website.id),
                                          'ks_updated_button_color_' + str(request.website.id))
            self.active_current_website_buttoncss("/ks_updated_button_color_")
        elif kw.get('border_color',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = "/static/src/css/ks_updated_button_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_button_scss_path, 'w+')
            f.write(kw['bordertexcolor']+'\n'+kw['borderbgcolor']+'\n'+kw['border_radius']+'\n'+kw['border_color'])
            f.close()
            self.createQwebIfNotAvialableButton('ks_theme_kinetik.ks_updated_button_color_' + str(request.website.id),
                                          'ks_updated_button_color_' + str(request.website.id))
            self.active_current_website_buttoncss("/ks_updated_button_color_")
        return None

    @http.route([
        '/write/updated/hoverscss',
    ], type='http', auth="public", website=True)
    def KsWriteUpdatedhoverScss(self, **kw):
        if kw.get('hovertextcolor', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = "/static/src/css/ks_updated_hover_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_hover_scss_path, 'w+')
            f.write(kw['hovertextcolor'] + '\n' + kw['hover_bgcolor']+'\n'+kw['hover_border'])
            f.close()
            self.createQwebIfNotAvialableHover('ks_theme_kinetik.ks_updated_hover_color_' + str(request.website.id),
                                                'ks_updated_hover_color_' + str(request.website.id))
            self.active_current_website_hovercss("/ks_updated_hover_color_")
        elif kw.get('hover_backgroundcolor', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = "/static/src/css/ks_updated_hover_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_hover_scss_path, 'w+')
            f.write(kw['hovertcolor'] + '\n' + kw['hover_backgroundcolor']+'\n'+kw['hover_b_color'])
            f.close()
            self.createQwebIfNotAvialableHover('ks_theme_kinetik.ks_updated_hover_color_' + str(request.website.id),
                                                'ks_updated_hover_color_' + str(request.website.id))
            self.active_current_website_hovercss("/ks_updated_hover_color_")
        elif kw.get('resethovertextcolor', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = "/static/src/css/ks_updated_hover_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_hover_scss_path, 'w+')
            f.write(kw['resethovertextcolor'] + '\n' + kw['resethover_bgcolor']+'\n'+kw['resethover_border'])
            f.close()
            self.createQwebIfNotAvialableHover('ks_theme_kinetik.ks_updated_hover_color_' + str(request.website.id),
                                                'ks_updated_hover_color_' + str(request.website.id))
            self.active_current_website_hovercss("/ks_updated_hover_color_")

        elif kw.get('hoverbordercolor', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = "/static/src/css/ks_updated_hover_color_" + str(request.website.id) + ".scss";
            f = open(module_path + ks_hover_scss_path, 'w+')
            f.write(kw['hovertext2color'] + '\n' + kw['hover_bg2color']+'\n'+kw['hoverbordercolor'])
            f.close()
            self.createQwebIfNotAvialableHover('ks_theme_kinetik.ks_updated_hover_color_' + str(request.website.id),
                                                'ks_updated_hover_color_' + str(request.website.id))
            self.active_current_website_hovercss("/ks_updated_hover_color_")

        return None

    def active_current_website_css(self, key):
        all_css_templates = request.env['ir.ui.view'].search([('key', 'like', 'ks_theme_kinetik.ks_updated_color_'), ('active', '=', True)])
        currnt_website_id = request.website.id
        for template in all_css_templates:
            if template.active:
                template.write({
                    'active': False
                })

        current_css_tempalte = all_css_templates.search([('key', '=', 'ks_theme_kinetik.ks_updated_color_' + str(currnt_website_id)),
                                                             ('active', '=', False),('website_id', '=', currnt_website_id)])


        if current_css_tempalte:
            current_css_tempalte.sudo().write({
                'active': True,
            })
        else:
            res = all_css_templates.search(
                [('key', '=', 'ks_theme_kinetik.ks_updated_color'),
                 ('active', 'in', True) or ('active', 'in', False)])
            if res:
                res.write(
                    {'active': True, })

    def active_current_website_buttoncss(self, key):
        all_css_templates = request.env['ir.ui.view'].search(
            [('key', 'like', 'ks_theme_kinetik.ks_updated_button_color_'), ('active', '=', True)])
        currnt_website_id = request.website.id
        for template in all_css_templates:
            if template.active:
                template.write({
                    'active': False
                })

        current_css_tempalte = all_css_templates.search(
            [('key', '=', 'ks_theme_kinetik.ks_updated_button_color_' + str(currnt_website_id)),
             ('active', '=', False), ('website_id', '=', currnt_website_id)])

        if current_css_tempalte:
            current_css_tempalte.sudo().write({
                'active': True,
            })
        else:
            res = all_css_templates.search(
                [('key', '=', 'ks_theme_kinetik.ks_updated_button_color'),
                 ('active', 'in', True) or ('active', 'in', False)])
            if res:
                res.write(
                    {'active': True, })



    def active_current_website_hovercss(self, key):
        all_css_templates = request.env['ir.ui.view'].search(
            [('key', 'like', 'ks_theme_kinetik.ks_updated_hover_color_'), ('active', '=', True)])
        currnt_website_id = request.website.id
        for template in all_css_templates:
            if template.active:
                template.write({
                    'active': False
                })

        current_css_tempalte = all_css_templates.search(
            [('key', '=', 'ks_theme_kinetik.ks_updated_hover_color_' + str(currnt_website_id)),
             ('active', '=', False), ('website_id', '=', currnt_website_id)])

        if current_css_tempalte:
            current_css_tempalte.sudo().write({
                'active': True,
            })
        else:
            res = all_css_templates.search(
                [('key', '=', 'ks_theme_kinetik.ks_updated_hover_color'),
                 ('active', 'in', True) or ('active', 'in', False)])
            if res:
                res.write(
                    {'active': True, })

    # @Key -- to check if the file is already created
    # @file_name -- to create new file with the exsistin website id
    def createQwebIfNotAvialable(self, key, file_name):
        qweb = request.env['ir.ui.view'].search([('key', '=', key)])
        if qweb:
            return
        else:
            assets = request.env['ir.ui.view'].search([('key', '=', 'web.assets_frontend')], limit=1)
            view_arch = u'<data>' \
                        u'  <xpath expr="." position="inside">' \
                        u'      <link rel="stylesheet"type="text/scss"href="/ks_theme_kinetik/static/src/css/%s.scss"/>' \
                        u'  </xpath>' \
                        u'</data>' % (file_name)

            res = request.env['ir.ui.view'].create({
                'name': key,
                'key': key,
                'priority': 1,
                'active': False,
                'website_id': request.website.id,
                'type': 'qweb',
                'arch_db': view_arch,
                'inherit_id': assets.id,
            })

        return res
    def createQwebIfNotAvialableButton(self, key, file_name):
        qweb = request.env['ir.ui.view'].search([('key', '=', key)])
        if qweb:
            return
        else:
            assets = request.env['ir.ui.view'].search([('key', '=', 'web.assets_frontend')], limit=1)
            view_arch = u'<data>' \
                        u'  <xpath expr="." position="inside">' \
                        u'      <link rel="stylesheet"type="text/scss"href="/ks_theme_kinetik/static/src/css/%s.scss"/>' \
                        u'  </xpath>' \
                        u'</data>' % (file_name)

            res = request.env['ir.ui.view'].create({
                'name': key,
                'key': key,
                'priority': 12,
                'active': False,
                'website_id': request.website.id,
                'type': 'qweb',
                'arch_db': view_arch,
                'inherit_id': assets.id,
            })

        return res


    def createQwebIfNotAvialableHover(self, key, file_name):
        qweb = request.env['ir.ui.view'].search([('key', '=', key)])
        if qweb:
            return
        else:
            assets = request.env['ir.ui.view'].search([('key', '=', 'web.assets_frontend')], limit=1)
            view_arch = u'<data>' \
                        u'  <xpath expr="." position="inside">' \
                        u'      <link rel="stylesheet"type="text/scss"href="/ks_theme_kinetik/static/src/css/%s.scss"/>' \
                        u'  </xpath>' \
                        u'</data>' % (file_name)

            res = request.env['ir.ui.view'].create({
                'name': key,
                'key': key,
                'priority': 18,
                'active': False,
                'website_id': request.website.id,
                'type': 'qweb',
                'arch_db': view_arch,
                'inherit_id': assets.id,
            })

        return res


    @http.route([
        '/get/updated/scss',
    ], type='http', auth="public", website=True)
    def KsGetUpdatedScss(self, **kw):
        if kw.get('scss_path',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_scss_path = module_path + "/static/src/css/ks_updated_color_" + str(request.website.id) + ".scss";
            exists = os.path.isfile(ks_scss_path)
            if exists:
                f = open(ks_scss_path, 'r')
                theme_color = f.read()
                # f.close()
                return theme_color.split('\n')[0].split(":")[1][:8]
            return "#FAB446"
        elif kw.get('text_scss_path',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_scss_path = module_path + "/static/src/css/ks_updated_color_" + str(request.website.id) + ".scss";
            exists = os.path.isfile(ks_scss_path)
            if exists:
                f = open(ks_scss_path, 'r')
                theme_color = f.read()
                # f.close()
                return theme_color.split('\n')[1].split(":")[1][:8]
            return "#FAB446"

    @http.route([
        '/get/updated/buttonscss',
    ], type='http', auth="public", website=True)
    def KsGetUpdatedbuttonScss(self, **kw):
        if kw.get('bg_scss_path',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = module_path + "/static/src/css/ks_updated_button_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_button_scss_path)
            if exists:
                f = open(ks_button_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[1].split(':')[1][:8]
            return "#FAB446"
        elif kw.get('text_scss_path',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = module_path + "/static/src/css/ks_updated_button_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_button_scss_path)
            if exists:
                f = open(ks_button_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[0].split(':')[1][:8]
            return "#FAB446"
        elif kw.get('radius_scss_path',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = module_path + "/static/src/css/ks_updated_button_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_button_scss_path)
            if exists:
                f = open(ks_button_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[2].split(':')[1].split('p')[0]
            return "0"
        elif kw.get('border_scss_path',False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_button_scss_path = module_path + "/static/src/css/ks_updated_button_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_button_scss_path)
            if exists:
                f = open(ks_button_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[3].split(':')[1][:8]
            return "#FAB446"

    @http.route([
        '/get/updated/hoverscss',
    ], type='http', auth="public", website=True)
    def KsGetUpdatedhoverScss(self, **kw):
        if kw.get('hover_bg_scss_path', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = module_path + "/static/src/css/ks_updated_hover_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_hover_scss_path)
            if exists:
                f = open(ks_hover_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[1].split(':')[1][:8]
            return "#FAB446"
        elif kw.get('hover_text_scss_path', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = module_path + "/static/src/css/ks_updated_hover_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_hover_scss_path)
            if exists:
                f = open(ks_hover_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[0].split(':')[1][:8]
            return "#FAB446"
        elif kw.get('hover_border_scss_path', False):
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            ks_hover_scss_path = module_path + "/static/src/css/ks_updated_hover_color_" + str(
                request.website.id) + ".scss";
            exists = os.path.isfile(ks_hover_scss_path)
            if exists:
                f = open(ks_hover_scss_path, 'r')
                data = f.read()
                # f.close()
                return data.split('\n')[2].split(':')[1][:8]
            return "#FAB446"


    #controller for dynamic font url option
    @http.route(['/some_url'], type='json', auth="public", website=True)
    def dynamic_font(self, **kwargs):
        try:
            url = kwargs['url']

            font_family=url.split('=')[1].split(('&'))[0]
            if ':' in font_family:
                font_family=url.split('=')[1].split(('&'))[0].split(':')[0]
            count = max([int(i.key.split('_')[-1]) for i in request.env['ir.ui.view'].search([('key', 'like', 'ks_theme_kinetik.custom_font_layout_%'), ('active', 'in', [1, ''])])])
            count += 1
            for i in list(punctuation):
                if i in font_family:
                    font_family = font_family.replace(i, ' ')
            module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
            path = module_path + '/static/src/scss/fonts/default.scss'
            f = open(path, 'r+')
            data = f.read()
            url = "'" + url + "'"
            data = data.replace('URLREPLACE', url)
            data = data.replace('FONTREPLCER', font_family)
            path1 = module_path + '/static/src/scss/fonts/font_' + str(count) + '.scss'
            g = open(path1, 'w+')
            g.write(data)
            g.close()
            self.createQwebIfNotAvialableForFont('ks_theme_kinetik.custom_font_layout_' + str(count),  'font_' + str(count), font_family)

        except Exception as e:
            pass




    def createQwebIfNotAvialableForFont(self, key, file_name, font_family):
        qweb = request.env['ir.ui.view'].search([('key', '=', key)])
        if qweb:
            return
        else:
            assets = request.env['ir.ui.view'].search([('key', '=', 'web.assets_frontend')], limit=1)
            view_arch = u'<data>' \
                        u'  <xpath expr="." position="inside">' \
                        u'      <link rel="stylesheet"type="text/scss"href="/ks_theme_kinetik/static/src/scss/fonts/%s.scss"/>' \
                        u'  </xpath>' \
                        u'</data>' % (file_name)

            res = request.env['ir.ui.view'].create({
                'name': font_family,
                'key': key,
                'priority': 16,
                'active': False,
                'website_id': request.website.id,
                'type': 'qweb',
                'arch_db': view_arch,
                'inherit_id': assets.id,
                'state': False,
            })

        return res
    # handling event for deleting font
    @http.route(['/site'], type='json', auth="public", website=True)
    def delete_font(self, **kwargs):
        view_id=kwargs['view_id']
        number=request.env['ir.ui.view'].browse(kwargs['view_id']).key.split('_')[-1]
        module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
        path = module_path + '/static/src/scss/fonts/font_'+number+ '.scss'
        if os.path.isfile(path):
            os.remove(path)
        if request.env['ir.ui.view'].browse(view_id):
            request.env['ir.ui.view'].browse(view_id).unlink()
        return

    @http.route(['/reset'], type='json', auth="public", website=True)
    def reset(self):
        module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
        path=module_path+'/static/src/css/ks_updated_button_color.scss'
        f=open(path,'r+')
        data=f.read()
        path1 = module_path + '/static/src/css/ks_updated_hover_color.scss'
        f1 = open(path1, 'r+')
        data1 = f1.read()
        values = {
            'bgcolor': data.split('\n')[1],
            'txtcolor': data.split('\n')[0],
            'radius': data.split('\n')[2],
            'border': data.split('\n')[3],
            'hoverbgcolor':data1.split('\n')[1],
            'hovertxtcolor':data1.split('\n')[0],
            'hoverbordercolor':data1.split('\n')[2]
        }
        return values

    @http.route(['/reset/themecolor'], type='json', auth="public", website=True)
    def reset_themecolor(self):
        module_path = '/'.join((os.path.realpath(__file__)).split('/')[:-2])
        path = module_path + '/static/src/css/ks_updated_color.scss'
        f = open(path, 'r+')
        data = f.read()
        value = {
            'themecolor': data.split('\n')[0],
            'themetxtcolor': data.split('\n')[1],
        }
        return value


