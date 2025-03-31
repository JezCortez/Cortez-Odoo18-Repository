# models/rooms.py
from odoo import models, fields, api

class Rooms(models.Model):
    _name = 'hotel.rooms'
    _description = 'Hotel Rooms'

    name = fields.Char(string="Room No.", required=True)
    description = fields.Char(string="Room Description")