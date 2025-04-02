# models/guests.py
from odoo import models, fields, api
from datetime import date

class Guests(models.Model):
    _name = 'hotel.guests'
    _description = 'Hotel Guests'

    lastname = fields.Char(string="Lastname", required=True)
    firstname = fields.Char(string="Firstname", required=True)
    middlename = fields.Char(string="Middlename")
    address_streetno = fields.Char(string="Address/ Street & No.")
    address_area = fields.Char(string="Address / Area, Unit & Bldg, Brgy")
    address_city = fields.Char(string="Address / City/Town")
    address_province = fields.Char(string="Address / Province/State")
    zipcode = fields.Char(string="ZIP Code")
    contactno = fields.Char(string="Contact No.")
    email = fields.Char(string="Email")
    gender = fields.Selection([('FEMALE', 'Female'), ('MALE', 'Male')], string="Gender")
    birthdate = fields.Date(string="BirthDate")
    photo = fields.Image(string="Guest Photo")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)  # Add computed age field

    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = date.today()
                record.age = today.year - record.birthdate.year - (
                    (today.month, today.day) < (record.birthdate.month, record.birthdate.day)
                )
            else:
                record.age = 0
