""" data transfer wizard"""
from email.policy import default

from odoo import models, fields
import xmlrpc.client as xmlrpclib
import json
from odoo import Command


class DataTransferWizard(models.TransientModel):
    """ Wizard for data transfer"""
    _name = 'data.transfer.wizard'
    _description = 'Wizard for data fetching'

    password = fields.Char(string='Password')
    username = fields.Char(string='Username')
    server_url = fields.Char(string='Server URL', default='http://localhost:8017')
    db_name = fields.Char(string='Database name')

    def data_fetch(self):
        """ Function for fetch and transfer datas"""
        res_partner_to_create = []
        # -----------------------------------------------------------------
        model_url_1 = self.server_url
        url_common_1 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(model_url_1))
        db_1 = 'odoo17.1'
        username_1 = 'admin'
        pwd_1 = 'admin'
        uid_1 = url_common_1.authenticate(db_1, username_1, pwd_1, {})
        if uid_1:
            print("Authentication success")
        else:
            print("Authentication failed")
        url_model_1 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(model_url_1))
        res_partner_from = url_model_1.execute_kw(db_1, uid_1, pwd_1, 'res.partner', 'search_read', [[]], {
        })
        # ---------------------------------------------------------
        model_url_2 = 'http://localhost:8018'
        url_common_2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(model_url_2))
        db_2 = 'odoo18'
        username_2 = 'admin1'
        pwd_2 = 'admin1'
        uid_2 = url_common_2.authenticate(db_2, username_2, pwd_2, {})
        if uid_2:
            print("Authentication success")
        else:
            print("Authentication failed")
        url_model_2 = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(model_url_2))
        res_partner_to = url_model_2.execute_kw(db_2, uid_2, pwd_2, 'res.partner', 'search_read', [[]])
        res_partner_to_names = [rec.get('name', None) for rec in res_partner_to if rec]
        length = len(res_partner_from)
        for index in range(length):
            if res_partner_from and res_partner_from[index]['name'] not in res_partner_to_names:
                res_partner_to_create.append(res_partner_from[index])
        create_data = self.data_create(res_partner_to_create)

        if create_data:
            data_added = url_model_2.execute_kw(db_2, uid_2, pwd_2, 'res.partner', 'create', [create_data])
            self.link_child_ids()

    def data_create(self, datas):
        """ Method for fetched value adding into dictionary"""
        create_data = []
        for value in datas:
            create_data.append({'old_db_id': value['id'],
                                'name': value['name'], 'image_1920': value['image_1920'],
                                'image_1024': value['image_1024'], 'image_512': value['image_512'],
                                'image_256': value['image_256'],
                                'image_128': value['image_128'], 'avatar_1920': value['avatar_1920'],
                                'avatar_1024': value['avatar_1024'],
                                'avatar_512': value['avatar_512'], 'avatar_256': value['avatar_256'],
                                'avatar_128': value['avatar_128'],
                                'complete_name': value['complete_name'],
                                'title': value['title'],
                                'parent_name': value['parent_name'],
                                'child_ids_list': str(value['child_ids']),
                                'ref': value['ref'], 'lang': value['lang'],
                                'active_lang_count': value['active_lang_count'], 'tz': value['tz'],
                                'tz_offset': value['tz_offset'],
                                'vat': value['vat'],
                                'company_registry': value['company_registry'],
                                'website': value['website'], 'comment': value['comment'],
                                'active': value['active'],
                                'employee': value['employee'],
                                'function': value['function'], 'type': value['type'], 'street': value['street'],
                                'street2': value['street2'],
                                'zip': value['zip'], 'city': value['city'], 'state_id': value['state_id'][0],
                                'country_id': value['country_id'][0], 'country_code': value['country_code'],
                                'partner_latitude': value['partner_latitude'],
                                'partner_longitude': value['partner_longitude'], 'email': value['email'],
                                'email_formatted': value['email_formatted'], 'phone': value['phone'],
                                'mobile': value['mobile'],
                                'is_company': value['is_company'], 'is_public': value['is_public'],
                                'company_type': value['company_type'],
                                'color': value['color'],
                                'partner_share': value['partner_share'], 'contact_address': value['contact_address'],
                                'commercial_company_name': value['commercial_company_name'],
                                'company_name': value['company_name'], 'barcode': value['barcode'],
                                'display_name': value['display_name'],
                                # 'create_uid': value['create_uid'], 'create_date': value['create_date'],
                                # 'write_uid': value['write_uid'][0],
                                'write_date': value['write_date'], 'im_status': value['im_status'],
                                # 'channel_ids': value['channel_ids'],
                                'contact_address_inline': value['contact_address_inline'],
                                'signup_type': value['signup_type'],
                                'additional_info': value['additional_info'],
                                'phone_sanitized': value['phone_sanitized'],
                                'phone_sanitized_blacklisted': value['phone_sanitized_blacklisted'],
                                'phone_blacklisted': value['phone_blacklisted'],
                                'mobile_blacklisted': value['mobile_blacklisted'],
                                'phone_mobile_search': value['phone_mobile_search']})
        return create_data

    def link_child_ids(self):
        """ method for linking child ids"""
        res_partner = self.env['res.partner'].search([])
        rec_child_ids = res_partner.filtered(lambda data: data.child_ids_list)
        old_db_list = res_partner.mapped('old_db_id')
        for rec in rec_child_ids:
            for id in old_db_list:
                if id in json.loads(rec.child_ids_list):
                    record_id = res_partner.filtered(lambda rec: rec.old_db_id == id).id
                    rec.write({
                        'child_ids': [Command.link(record_id)]
                    })
