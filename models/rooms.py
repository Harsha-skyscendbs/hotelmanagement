from odoo import models, fields


class Rooms(models.Model):
    _name = 'hotel.room'
    _description = 'This module contains all rooms of the particular room types'

    name = fields.Char(string='Room', index=True)
    room_code = fields.Char(string='Room Id', required=True)
    # hotel_id=fields.Many2one('hotel.hotel',string='Hotel Id')
    status = fields.Selection([('available', 'Available'),
                               ('reserved', 'Reserved'),
                               ('occupied', 'Occupied')
                               ])
    currency_id = fields.Many2one('res.currency', 'Currency')
    rent = fields.Monetary(string='Rent',currency_field='currency_id')
    no_of_persons = fields.Integer(string='Capacity of Room')
    taxes = fields.Float(string='Customer Taxes')
    room_types_id = fields.Many2one('hotel.roomtype', string='Room type')
    # bookings_id=fields.Many2one('hotel.booking','Booking')

    # class Room_lines(models.Model):
    #     _name='hotel.roomlines'
    #     _description='hotel room booking details'
    #
    #     rooms_types_id=fields.Char('hotel.roomtype',string='Room type',related='')

    # r_no = fields.Char
