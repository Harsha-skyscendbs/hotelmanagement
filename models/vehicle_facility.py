from odoo import models,fields


class VehicleFacility(models.Model):
    _name = 'hotel.vehicle.facility'
    _description = 'This module is for vehicle services provided in the hotel'

    name = fields.Char('Vehicle name')
    code = fields.Char('Vehicle code')
    facility_id = fields.Many2one('hotel.facilities','Facilities', default= lambda self: self.env['hotel.facilities'].search([('name', '=', 'Transportation')]))
    currency_id = fields.Many2one('res.currency', 'Currency')
    charges = fields.Monetary(currency_field='currency_id', string='Charges')
    persons = fields.Integer('Persons')
