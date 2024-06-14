from odoo import fields, models, api


class BookingRoom(models.Model):
    _name = 'hotel.booking.room'
    _description = 'This model contains information of the rooms folio'
    _rec_name = 'rooms_id'

    booking_id = fields.Many2one('hotel.booking', 'booking id')
    room_type_id = fields.Many2one('hotel.roomtype', string='Room Types')
    rooms_id = fields.Many2one('hotel.room', string=' Room Nos.', domain="[('room_types_id','=',room_type_id)]")
    currency_id = fields.Many2one('res.currency',related='rooms_id.currency_id')
    rent = fields.Monetary(string='Rent', related='rooms_id.rent',currency_field='currency_id')
    no_of_persons = fields.Integer(string='Capacity of Room', related='rooms_id.no_of_persons')
    taxes = fields.Float(string='Customer Taxes', related='rooms_id.taxes')
    sub_total = fields.Monetary(string='Sub Total', compute='_calc_room_charges',currency_field='currency_id')

    @api.depends('booking_id', 'rent', 'taxes')
    def _calc_room_charges(self):
        """
        This method calculates the room charges of the stay
        ---------------------------------------------------
        @param:object pointer/ recordset
        """
        for records in self:
            if records.rent and records.taxes:
                records.sub_total = (records.rent * records.booking_id.days_book_for +
                                     (records.rent * records.booking_id.days_book_for * records.taxes / 100))
            else:
                records.sub_total = 0.0


class BookingFoodOrder(models.Model):
    _name = 'hotel.booking.food'
    _description = 'Food order details'

    booking_id = fields.Many2one('hotel.booking', 'booking id')
    food_category_id = fields.Many2one('hotel.productcategories', string='Food Categories')
    # facility_id = fields.Many2one('hotel.facilities', 'Facilities', related='food_category_id.facility_id', readonly=True)
    food_products_id = fields.Many2one('hotel.products', string='Food Name',
                                       domain="[('product_category_id','=',food_category_id)]")
    quantity = fields.Integer('Quantity')
    currency_id = fields.Many2one('res.currency',related='food_products_id.currency_id')
    price = fields.Monetary(currency_field='currency_id', string='Price', related='food_products_id.price')
    taxes = fields.Float(string='Customer Taxes', related='food_products_id.taxes')
    sub_total = fields.Monetary(currency_field='currency_id', string='Sub Total', compute='_calc_food_charges')

    @api.depends('price', 'taxes', 'quantity')
    def _calc_food_charges(self):
        """
        This method calculates the food charges of the customer
        ---------------------------------------------------
        @param:object pointer/ recordset
        """
        for records in self:
            if records.quantity and records.taxes and records.price:
                records.sub_total = (records.price * records.quantity +
                                     (records.price * records.quantity * records.taxes / 100))
            else:
                records.sub_total = 0.0


class BookingVehicle(models.Model):
    _name = 'hotel.booking.vehicle'
    _description = 'Vehicle facility details'

    booking_id = fields.Many2one('hotel.booking', 'booking id')
    vehicle_id = fields.Many2one('hotel.vehicle.facility', 'Vehicle')
    # facility_id = fields.Many2one('hotel.facilities', 'Facilities', related='vehicle_id.facility_id',
    #                               readonly=True)
    currency_id = fields.Many2one('res.currency', 'Currency', related='vehicle_id.currency_id')
    charges = fields.Monetary(currency_field='currency_id', string='Charges', related='vehicle_id.charges')
    persons = fields.Integer('Persons', related='vehicle_id.persons')


