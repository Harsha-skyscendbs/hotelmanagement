from odoo import models, fields,api


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

    def _compute_display_name(self):
        """
        Overridden _compute_display_name method to display rooms_code and name both.
        @param self :object pointer / recordset
        """
        # rooms_list = []
        for rooms in self:
            rooms_str = ''
            if rooms.room_code:
                rooms_str += '[' + rooms.room_code + '] '
            rooms_str += rooms.name
            rooms.display_name = rooms_str
        #     rooms_list.append((rooms.id, rooms_str))
        # return rooms_list
        # return [(record.id, "[%s] %s" % (record.room_code, record.name)) for record in self]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=10):
        """
        Overridden name_search() to search rooms via name and room_code
        @param self : object pointer /recordset
        @param name : string which is searched by user
        @param args : Domain if given on the field
        @param operator : Compare field with operator
        @param limit : Max records
        """
        print('Name---', name)
        print("Args---", args)
        print("Operator----", operator)
        print("Limit----", limit)
        if not args:
            args = []
        args += ['|', ('room_code', operator, name), ('name', operator, name)]
        rooms = self.search(args)
        return [(room.id, room.display_name) for room in rooms]

    @api.model
    def name_create(self, name):
        """
        Overridden name_create() to add room_code along with name
        @param self : object pointer /recordset
        @param name : name of the record typed in relational field
        """
        vals = {
            'name': name.upper(),
            'room_code': 'SD' + name.upper()
        }
        rooms = self.create(vals)
        print("Create rooms----", rooms)
        return rooms.id, rooms.display_name

