from odoo import models, fields, api
from datetime import date

class RoomTypes(models.Model):
    _name = 'hotel.roomtypes'  # Model name
    _description = 'Room Types'

    name = fields.Char("Room Type", required=True)
    description = fields.Char("Room Type Description")
    photobed = fields.Image("Bed Photo")
    photorestroom = fields.Image("Comfort Room Photo")
    room_image = fields.Image(string="Room Image")
    bathroom_image = fields.Image(string="Bathroom Image")
    daily_charge = fields.Float(string="Daily Charge")
    extra_charge = fields.Float(string="Extra Charge")
    discount = fields.Float(string="Discount")
    total_charge = fields.Float(string="Total Charge", compute="_compute_total_charge", readonly=True)
    room_ids = fields.One2many('hotel.rooms', 'roomtype_id', string="Rooms")  # One2many relation to rooms
    room_bed_type = fields.Selection([
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed')
    ], string="Bed Type")
    room_capacity = fields.Integer(string="Room Capacity")
    room_size = fields.Float(string="Room Size (sqm)")
    room_bed_count = fields.Integer(string="Number of Beds")
    roomtypes_list = fields.Many2many('hotel.roomtypes', compute='_compute_roomtypes_list', string="All Room Types", store=False)
    
    charge_history_ids = fields.One2many('hotel.roomtype.charge.history', 'roomtype_id', string='Charge History')
    # Optional: Create a computed field to show current charge from history
    current_historical_charge = fields.Float(string='Current Historical Charge', compute='_compute_current_charge', store=True)

    @api.depends()
    def _compute_roomtypes_list(self):
        all_roomtypes = self.env['hotel.roomtypes'].search([])
        for record in self:
            record.roomtypes_list = all_roomtypes

    @api.depends('charge_history_ids', 'charge_history_ids.date_from', 
                'charge_history_ids.date_to', 'charge_history_ids.charge_amount')
    def _compute_current_charge(self):
        today = date.today()
        for record in self:
            current_charge = False
            for history in record.charge_history_ids:
                if (history.date_from <= today and 
                    (not history.date_to or history.date_to >= today)):
                    current_charge = history.charge_amount
                    break
            record.current_historical_charge = current_charge if current_charge else 0.0

    def _compute_total_charge(self):
        for record in self:
            record.total_charge = (record.daily_charge + record.extra_charge) * (1 - (record.discount or 0) / 100)
class DailyCharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'hotel roomtype daily charges list'
    charge_id = fields.Many2one('hotel.charges',string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10,2), options={'always_reload': True})
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Roomtype")

class RoomTypeChargeHistory(models.Model):
    _name = 'hotel.roomtype.charge.history'
    _description = 'Room Type Charge History'
    _order = 'date_from desc, id desc'

    roomtype_id = fields.Many2one('hotel.roomtypes', string='Room Type', required=True, ondelete='cascade')
    date_from = fields.Date(string='Valid From', required=True, default=fields.Date.today)
    date_to = fields.Date(string='Valid To')
    charge_amount = fields.Float(string='Charge Amount', required=True)
    is_current = fields.Boolean(string='Is Current', compute='_compute_is_current', store=True)

    @api.depends('date_from', 'date_to')
    def _compute_is_current(self):
        today = date.today()
        for record in self:
            record.is_current = (record.date_from <= today and (not record.date_to or record.date_to >= today))