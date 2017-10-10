# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import werkzeug
from urlparse import urljoin
from odoo import models, fields, api, http
from odoo.addons.auth_signup.models.res_partner import ResPartner


# Monkey Patching
# Overwrite the original _get_signup_url_for_action in auth_signup
# i.e. https://github.com/odoo/odoo/blob/10.0/addons/auth_signup/models
# /res_partner.py#L49-L94
@api.multi
def _get_signup_url_for_action(self, action=None, view_type=None,
                               menu_id=None, res_id=None, model=None):
    """ generate a signup url for the given partner ids and action, possibly overriding
        the url state components (menu_id, id, view_type) """

    res = dict.fromkeys(self.ids, False)
    """QTL MOD - The base url could be different among users"""
    #base_url = self.env['ir.config_parameter'].get_param('web.base.url')
    for partner in self:

        """QTL MOD - Search if the user account has the multi-website
        settings and set up the base url with correct domain
        """
        base_url = http.request.env[
            'ir.config_parameter'].get_param('web.base.url')
        domain = [
            ('partner_id', '=', partner.id),
            ('active', '=', True)
        ]
        user_ids = self.env['res.users'].search(domain)
        if user_ids and user_ids[0].website_id:
            for hostheaders in user_ids[0].website_id.hostheaders:
                base_url = "https://" + hostheaders.header

        # when required, make sure the partner has a valid signup token
        if self.env.context.get('signup_valid') and not partner.user_ids:
            partner.signup_prepare()

        route = 'login'
        # the parameters to encode for the query
        query = dict(db=self.env.cr.dbname)
        signup_type = self.env.context.get('signup_force_type_in_url',
                                           partner.signup_type or '')
        if signup_type:
            route = 'reset_password' if signup_type == 'reset' else signup_type

        if partner.signup_token and signup_type:
            query['token'] = partner.signup_token
        elif partner.user_ids:
            query['login'] = partner.user_ids[0].login
        else:
            continue  # no signup token, no user, thus no signup url!

        fragment = dict()
        base = '/web#'
        if action == '/mail/view':
            base = '/mail/view?'
        elif action:
            fragment['action'] = action
        if view_type:
            fragment['view_type'] = view_type
        if menu_id:
            fragment['menu_id'] = menu_id
        if model:
            fragment['model'] = model
        if res_id:
            fragment['res_id'] = res_id

        if fragment:
            query['redirect'] = base + werkzeug.url_encode(fragment)

        res[partner.id] = urljoin(base_url, "/web/%s?%s" % (
        route, werkzeug.url_encode(query)))
    return res

class ResPartnerHookGetUrl(models.AbstractModel):
    _name = "res.partner.hook.get.url"
    _description = "Provide hook point for _get_signup_url_for_action method"

    def _register_hook(self):
        ResPartner._get_signup_url_for_action = _get_signup_url_for_action
        return super(ResPartnerHookGetUrl, self)._register_hook()
