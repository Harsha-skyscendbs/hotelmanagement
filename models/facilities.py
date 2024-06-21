from odoo import fields,models


class Facilities(models.Model):
    _name = 'hotel.facilities'
    _description = 'This module contains information of the facilities available in the hotel'

    code = fields.Char('code')
    name = fields.Char('Facility')
    color = fields.Integer('Color')

# class BookingFacilities(models.Model):
#     _name = 'hotel.booking.facilities'
#     _description = 'This module contains info of customers facilities chosen'
#     _rec_name = 'facilities_id'
#
#     facilities_id=fields.Many2one('hotel.facilities')
#     booking_id = fields.Many2one('hotel.booking', 'booking id')

