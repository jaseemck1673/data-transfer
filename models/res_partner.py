""" new """
from odoo import models, fields, api
import json
from odoo import Command

class ResPartner(models.Model):
    _inherit = 'res.partner'

    old_db_id = fields.Integer(string='Old Database id')
    old_db_name = fields.Char(string='Database Name', readonly=True)
    child_ids_list = fields.Char(string='child id list', defualt='None')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._link_child_ids()
        return records

    def _link_child_ids(self):
        """ method for linking child ids """
        res_partner = self.search([])
        db_list = list(set(res_partner.mapped('old_db_name')))
        for db in db_list:
            rec_child_ids = res_partner.filtered(lambda data: data.child_ids_list and data.old_db_name == db)
            print(rec_child_ids)
            old_db_list = res_partner.filtered(lambda data: data.old_db_id and \
                                                            data.old_db_name == db).mapped('old_db_id')
            for rec in rec_child_ids:
                for id in old_db_list:
                    if id in json.loads(rec.child_ids_list):
                        record_id = res_partner.filtered(lambda rec: rec.old_db_id == id and rec.old_db_name == db).id
                        rec.write({
                            'child_ids': [Command.link(record_id)]
                        })
            print('function called')
