from odoo import fields,models

class room_type(models.Model):
    _name='hotel.roomtype'
    _description='this model is for rooms type'
    name=fields.Char('name')
    code=fields.Char('code')
    no_of_rooms=fields.Integer('Total Rooms')
    # rooms=fields.One2many('hotel.room','room_types_id',string='Rooms')
    # rooms=fields.Many2one('hotel.room',string='Rooms')