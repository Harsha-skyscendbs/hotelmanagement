from odoo import fields, models, Command


class UpdateFacilitiesWizard(models.TransientModel):
    _name = 'update.booking.facilities.wizard'
    _description = 'Update Bookings Facilities'

    bookings_id = fields.Many2one('hotel.booking', string="Booking Id")
    facility_ids = fields.Many2many('hotel.facilities', 'booking_facility_wizard_rel', 'hotel_booking_id',
                                    'hotel_facility_id', string="Facilities")

    def update_bookings_facilities(self):
        bookings_obj = self.env['hotel.booking']
        print("bookings_obj>>>>>>>>", bookings_obj)
        print("ENV context>>>>>>>", self.env.context)
        print("self context>>>>>>>", self._context)
        if self.bookings_id.ids:
            bookings = self.bookings_id
        else:
            bookings = bookings_obj.browse(self._context.get('active_ids'))
        res = bookings.write({'facilities_ids': self.facility_ids})
        print("res>>>>>>>>>", bookings)

