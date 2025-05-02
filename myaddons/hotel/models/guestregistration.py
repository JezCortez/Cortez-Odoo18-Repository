from odoo import models, fields, api

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'hotel guest registration list'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")

    # Related fields from hotel.rooms
    roomname = fields.Char("Room No.", related='room_id.name')
    roomtname = fields.Char("Room Type", related='room_id.roomtype_id.name')

    # Related field from hotel.guests (computed field 'name')
    guestname = fields.Char("Guest Name", related='guest_id.name')

    datecreated = fields.Date("Date Created", default=lambda self: fields.Date.today())
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")

    # Computed field: concatenation of room name and guest name
    name = fields.Char("Guest Registration", compute='_compute_name', store=False)

    @api.depends('roomname', 'guestname')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.roomname or ''}, {rec.guestname or ''}"
