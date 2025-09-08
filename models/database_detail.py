""" new """
from odoo import models, fields, api


class DatabaseDetail(models.Model):
    _name = 'database.detail'
    _rec_name = 'name'

    old_db_id = fields.Integer(string='Old Database id')
    name = fields.Char(string='Database name')
    server_url = fields.Char(string='Server URL')
    password = fields.Char(string='Password')
    username = fields.Char(string='Username')