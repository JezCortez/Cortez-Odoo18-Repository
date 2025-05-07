from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    state = fields.Selection([
        ('DRAFT', 'Draft'),
        ('RESERVED', 'Reserved'),
        ('CHECKEDIN', 'Checked In'),
        ('CHECKEDOUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled')
    ], string="Status", default='DRAFT', required=True)

    @api.depends('roomname', 'guestname')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.roomname or ''}, {rec.guestname or ''}"

    def action_reserve(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid guest.')
            elif not rec.roomname:
                raise ValidationError('Please supply a valid Room Number.')
            elif not rec.datefromSched:
                raise ValidationError('Please supply a Scheduled Check In date.')
            elif not rec.datetoSched:
                raise ValidationError('Please supply a Scheduled Check Out date.')
            else:
                pkid = rec.id
                self._cr.execute("select * from public.fncheck_registrationconflict(%s)", (pkid,))
                result = self._cr.fetchall()
                result_cnt = result[0][0]
                result_msg = result[0][1]
                if result_cnt == 0:
                    rec.state = "RESERVED"
                else:
                    raise ValidationError(result_msg)

    def action_checkin(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid guest.')
            elif not rec.roomname:
                raise ValidationError('Please supply a valid Room Number.')
            elif not rec.datefromSched:
                raise ValidationError('Please supply a Scheduled Check In date.')
            elif not rec.datetoSched:
                raise ValidationError('Please supply a Scheduled Check Out date.')
            else:
                pkid = rec.id
                self._cr.execute("select * from public.fncheck_registrationconflict(%s)", (pkid,))
                result = self._cr.fetchall()
                result_cnt = result[0][0]
                result_msg = result[0][1]
                if result_cnt == 0:
                    rec.state = "CHECKEDIN"
                    rec.datefromAct = fields.Date.today()
                else:
                    raise ValidationError(result_msg)

    def action_checkout(self):
        for rec in self:
            if rec.state == "CHECKEDIN":
                rec.state = "CHECKEDOUT"
                rec.datetoAct = fields.Date.today()
            else:
                raise ValidationError("Guest is not CHECKED IN.")

    def action_cancel(self):
        for rec in self:
            if rec.state == "CHECKEDIN":
                raise ValidationError("Guest has already CHECKED IN.")
            else:
                rec.state = "CANCELLED"
