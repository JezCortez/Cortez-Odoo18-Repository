from odoo import models, fields, api

class charges(models.Model):
    _name = 'hotel.charges'
    _description = 'hotel charges master list'

    name = fields.Char("Charge Name")
    description = fields.Char("Charge Description")