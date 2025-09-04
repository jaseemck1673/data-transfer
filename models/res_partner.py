from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    old_db_id = fields.Integer(string='Old Database id')
    child_ids_list = fields.Char(string='child id list', defualt='None')
