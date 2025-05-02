# models/rooms.py
from odoo import models, fields, api

class Rooms(models.Model):
    _name = 'hotel.rooms'
    _description = 'Hotel Rooms'

    name = fields.Char(string="Room No.", required=True)
    description = fields.Char(string="Room Description")
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type", required=True)
    roomtype_name = fields.Char(string="Room Type Name", related='roomtype_id.name', store=True, readonly=True)