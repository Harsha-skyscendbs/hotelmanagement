import datetime

from odoo import models, fields, api, Command, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class Hotel(models.Model):
    _name = 'hotel.booking'
    _description = 'Booking'
    _rec_name = 'guest_name'
    # _order='sequence'

    company_id = fields.Many2one('res.company', 'Hotel', default=lambda self: self.env.company)
    booking_id = fields.Char(string="Booking Id", required=True, help='This is used to enter booking id',
                             index=True, default=lambda self: _('New'))
    image = fields.Image('Guest Image')
    color = fields.Integer('Color')
    guest_name = fields.Char(string="Guest Name", help='It is used to enter guest name', index=True)
    guest_email = fields.Char(string="Guest Email", help="You can enter guest's email id")
    guest_age = fields.Integer(string='Guest Age', help='Enter the age of the guest')
    guest_gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender')
    # room_availability=fields.Boolean(string="Is room Available ?",help='This is need to be checked out if room not available')
    date_of_booking = fields.Date(string="Booking Date", default=fields.Date.today(),
                                  help='It is used to enter booking date')
    days_book_for = fields.Integer(string="Days book for", help='It used to specify no of days spent')
    check_in = fields.Datetime(string="Check in", help='It is used to enter check in time and date',
                               default=fields.Date.today())
    check_out = fields.Datetime(string="Check out", help='It is used to enter check out time and date',
                                compute='_cal_checkout_date')
    # guest_info=fields.Text(string="Guest Info")
    # type_of_rooms=fields.Selection(selection=[('king room','King Room'),('garden view room','Gardern View Room')],string="Types of Rooms",help='It is used select type of rooms to stay')
    # description=fields.Html(string="Description")
    sequence = fields.Integer('Sequence')
    ref = fields.Reference([('res.users', 'Users'), ('res.partner', 'Contacts')])
    active = fields.Boolean(string="Active", default=True)
    mode_of_payment = fields.Selection([('cash', 'Cash'),
                                        ('credit/debit card', 'Credit/Debit Card'),
                                        ('mobile payments', 'Mobile Payments'),
                                        ('digital wallets', 'Digital Wallets')], string='Mode of Payments')
    # password=fields.Char("Password",groups="hotel.group_hotel_staff",size=4)
    # website=fields.Char("Website")
    # guest_priority=fields.Selection([(str(ele),str(ele))for ele in range(5)],'Guest Priority')
    # sign_in =fields.Float('Sign in')
    # days_book_for=check_in-check_out

    # room_type_id = fields.Many2one('hotel.roomtype', string='Room Types')
    # rooms_ids = fields.Many2many('hotel.room', string='Room Nos', domain="[('room_types_id','=',room_type_ids)]")
    # food_category_ids = fields.Many2many('hotel.productcategories', string='Food Categories')
    # food_products_ids = fields.Many2many('hotel.products', 'book_prodt_rel', 'booking_id',
    #                                      'product_id', string='Food Order',
    #                                      domain="[('product_category_id','=',food_category_ids)]")
    facilities_ids = fields.Many2many('hotel.facilities', 'book_fac_rel', 'booking_id', 'facility_id',
                                      string='Facilities')
    is_food = fields.Boolean(string="Is food")  # ,compute="_show_tab"  ,default=False
    is_transport = fields.Boolean(string="Is transport", )  # compute="_show_tab"  default=False,

    booking_folio_ids = fields.One2many('hotel.booking.room', 'booking_id', 'Folio')
    booking_food_order_ids = fields.One2many('hotel.booking.food', 'booking_id', 'Food Order')
    booking_vehicle_facility_ids = fields.One2many('hotel.booking.vehicle', 'booking_id', 'Vehicle')

    # hotel_ids=fields.Many2one('hotel.hotel',string='Hotels')
    # per_day_cost=fields.Float(string="Per Day Cost",help='It is used to enter price for one night stay')
    # taxes=fields.Float(string="Taxes",help='Depicts levied tax in bill')
    currency_id = fields.Many2one('res.currency', 'Currency')
    total = fields.Monetary(currency_field='currency_id',
                            string="Total", help='it displays final amount',
                            digits=(16, 3), compute='_calc_total_charges', )
    guest_id_doc = fields.Binary('Guest Doc')
    file_name = fields.Char('Doc name')
    state = fields.Selection([('draft', 'Draft'),
                              ('checkin', 'Check IN'),
                              ('checkout', 'Check Out'),
                              ('done', 'Done')], default='draft')

    @api.depends('booking_folio_ids', 'booking_food_order_ids', 'booking_vehicle_facility_ids')
    def _calc_total_charges(self):
        """
        This method will calculate total charges of customer for the stay.
        -------------------------------------------------------------------
        @param:object pointer/ recordset
        """
        print('compute of total charges', self)
        # #************** filtered() ***********
        # #Takes only two postional arguments
        # active_records = self.filtered('active')
        # active_records = self.filtered(lambda r: r.guest_gender == 'female')
        # active_records = self.filtered(lambda r: r.active == True)
        # active_records = self.filtered('is_food')
        # female_records = active_records.filtered(lambda r: r.guest_gender == 'female')
        # male_records = active_records.filtered(lambda r: r.guest_gender == 'male')
        # print('Active records: ', active_records)
        # print('female records: ', female_records)
        # print('male records: ', male_records)

        # ************** mapped() *************
        # #Takes only two postional arguments
        # # active_records_name = active_records.mapped('guest_name','guest_age')
        # # above code throws error[BaseModel.filtered() takes 2 positional arguments but 3 were given]
        # active_records_name = active_records.mapped('guest_name')
        # print('Active records name', active_records_name)
        # active_records_name_age = active_records.mapped(lambda r: r.guest_name + "_" + str(r.guest_age))
        # print("Active records name and age :", active_records_name_age)

        # ************* sorted() ***************
        # # sort_by_name = active_records.sorted(key='guest_name') #---returns recordset of the active records
        # sort_by_name = active_records.sorted(key='guest_name',reverse=True).mapped('guest_name') # ----returns list of sorted name's of active records
        # print('Active records sorted by name[Reverse]: ', sort_by_name)

        # ********* Recordset operations *********
        # # 1. in
        # fr = female_records in active_records
        # print('Female records in active records ', fr)
        # for fr in female_records:
        #     print("Active records in female records (check using loop)",fr in active_records)
        # for fr in active_records:
        #     print("Female records in active records (check using loop)", fr in female_records)
        # # 2. not in
        # nfr = female_records not in active_records
        # print("female records not in active records", nfr)
        # # 3. < (subset) or <= (subset or same set)
        # print('Female records is subset of active records ',female_records < active_records )
        # print('Female records is subset of active records ',female_records <= active_records )
        # # 4. > (superset) or >= (superset or same set)
        # print('Female records is superset of active records ', female_records > active_records)
        # print('Female records is superset of active records or same set ', female_records >= active_records)
        # print('Female records is superset of female records ', female_records > female_records)
        # print('Female records is superset of female records or same set ', female_records >= female_records)
        # # 5. | (union)
        # print('Union of female records and male records ', male_records | female_records)
        # # 6. & (intersection)
        # print('Intersection of female records and active records ', female_records & active_records)
        # # 7. - (Difference)
        # print('Difference of active records and female records ', active_records - female_records)
        for booking in self:
            # print('Normal field (Booking id)', booking.booking_id)
            # print('One to many field', booking.booking_food_order_ids)
            # # print('Many to one field', booking.room_type_id)
            # print('Many to many field', booking.facilities_ids)
            # # print('Type of facilities ids', type(booking.facilities_ids))
            #      # returns class 'odoo.api.hotel.facilities'
            # print('Ensure one', booking.ensure_one())
            # print('type of Ensure one', type(booking.ensure_one()))
            #      # returns class 'odoo.api.hotel.booking'
            # print('Meta data', booking.get_metadata())
            # print('type of metadta',type(booking.get_metadata()))
            total_charges = 0.0
            # for rooms in booking.rooms_ids:
            #     total += (booking.days_book_for * rooms.rent)+(rooms.rent * booking.days_book_for * rooms.taxes / 100)
            for rooms in booking.booking_folio_ids:
                total_charges += rooms.sub_total
            for foods in booking.booking_food_order_ids:
                total_charges += foods.sub_total
            for vehicles in booking.booking_vehicle_facility_ids:
                total_charges += vehicles.charges
            booking.total = total_charges

    def print_bookings(self):
        """
        This method gets triggered when button is called. and it shows the usage of button and some special objects.
        --------------------------------------------------------------------------------------------------
        @param:object pointer/ recordset
        """
        print('Self', self)
        print('Environment [env]', self.env)
        print('ENV Args', self.env.args)
        print('Cursor', self.env.cr)
        print('User id', self.env.uid)
        print('User', self.env.user)
        print('Context', self.env.context)
        print('Company', self.env.company)
        print('Companies', self.env.companies)
        print('Language', self.env.lang)
        print('Ref', self.env.ref('hotel.view_booking_form'))
        print('Booking object', self.env['hotel.booking'])
        book_obj = self.env['hotel.booking']
        print('Booking obj', book_obj.guest_name)

    def create_rec(self):
        """ This method triggeres when button is clicked and then record will be created
        --------------------------------------------------------------------------------
        @param:object pointer/ recordset
        """
        vals_1 = {
            'guest_name': 'Liza Grizel',
            'date_of_booking': '2024-05-22',
            'days_book_for': 3,
            'guest_age': 25,
            'guest_gender': 'female',
            'booking_folio_ids': [
                (0, 0, {
                    'room_type_id': 2,
                    'rooms_id': 1
                }),
                (Command.create({
                    'room_type_id': 3,
                    'rooms_id': 2,
                }))
            ],
            'facilities_ids': [
                (4, 2),
                Command.link(3)
            ]
        }
        vals_lst = [vals_1]
        new_rec = self.create(vals_lst)
        print('New rec created..', new_rec)

    def browse_rec(self):
        """
        This is button's method used to demonstrate browse method.
        -------------------------------------------------------------------
        @param self : object pointer / recordset
        """
        booking_rec = self.browse(20)
        # booking_rec = self.browse(20).booking_id # returns booking_id of the passed id
        # booking_rec = self.browse(21).booking_id # record doesn't exist in database
        print("\n Booking record-------------", booking_rec)
        booking_dict = booking_rec.read(['booking_id', 'guest_name', 'guest_email', 'guest_age', 'currency_id',
                                         'facilities_ids', 'booking_folio_ids'], load='_classic_read')
        print("\n Booking dict --------------", booking_dict)
        print("\n Currency rec------", booking_dict[0]['currency_id'])
        print("\n Facilities ids-------", booking_dict[0]['facilities_ids'])
        print("\n Booking folio ids-------", booking_dict[0]['booking_folio_ids'])
        bookings = self.browse([1, 18])
        print("Bookings-----", bookings)
        facilities_mapped = self.env['hotel.facilities'].browse([3, 4]).mapped('name')
        print('facilities_mapped----', facilities_mapped)
        facilities = self.env['hotel.facilities'].browse([3, 4]).read(['code', 'name'])
        print('facilities_read----', facilities)

    def update_rec(self):
        """
        This is button's method used to demonstrate  write method.
        -------------------------------------------------------------------
        @param self: object pointer / recordset
        """
        vals = {
            'guest_name': 'Niyati Sharma',
            'guest_age': 25,
            'facilities_ids': [
                # (6, 8, [2, 3]),
                # (6, 0, [2, 3]),
                # (Command.set([2, 3]))
                # (5, 8, [2, 3]),
                # (5, 0, 0),
                # (Command.clear()),
                # (2,2),
                (3, 4),
                # (Command.unlink(4)),
                (4, 4)
                # (Command.link(4)),
            ],
            'booking_folio_ids': [
                # (0, 8, {'room_type_id': 2})
                (0, 0, {'room_type_id': 2}),

            ]

        }
        res = self.write(vals)
        print("Updating records---------", res)

    def copy_rec(self):
        """
        This is object type button's method used to demonstrate copy method to copy the record.
        --------------------------------------------------------------------------
        @param self: object pointer / recordset
        """
        default = {
            'guest_name': self.guest_name + '(copy)',
            'facilities_ids': self.facilities_ids
        }
        new_rec = self.copy(default=default)
        print('Created copied record------', new_rec)

    def delete_rec(self):
        """
        This is button's method used to delete record.
        --------------------------------------------------------------------------
        @param self: object pointer / recordset
        """
        del_rec = self.unlink()
        print("Deleting records-------", del_rec)

    def search_rec(self):
        """
        This is button's method used to demonstrate search method.
        --------------------------------------------------------------------------
        @param self: object pointer / recordset
        """
        all_bookings = self.search([])
        print("All bookings", all_bookings)
        male_guest = self.search([('guest_gender', '=', 'male')])
        print("Male guest---------", male_guest)
        offset_3_bookings = self.search([], offset=3)
        print("Skipping 3 records-----", offset_3_bookings)
        limit_4_bookings = self.search([], limit=4)
        print("Limit 4 bookings--------", limit_4_bookings)
        off_2_limit_4_bookings = self.search([], offset=2, limit=4)
        print("Skip 2 rec and Max 4 records -----", off_2_limit_4_bookings)
        sort_by_name = self.search([], order='guest_name')
        print("Sort by name asc------", sort_by_name)
        sort_off_lim = self.search([], offset=2, limit=4, order='guest_name desc')
        print("Sorted records in desc and skipped by 2 and max 4 rec", sort_off_lim)
        no_female_guest = self.search([], count=True)
        print("No of female guests--------", no_female_guest)

        # search_count returns integer
        total_guests = self.search_count([])
        print("Total guests------", total_guests)

        # search_read  returns list of dict
        bookings_list = self.search_read(
            fields=['guest_name', 'guest_age', 'facilities_ids', 'booking_folio_ids', 'currency_id'])
        print('Booking list------------', bookings_list)

    @api.model
    def default_get(self, fields_list):
        """
        Overridden default_get method to add additional default facilities in every bookings
        --------------------------------------------------------------
        @param self: object pointer
        @param fields_list: List of fields having default values
        """
        print("Fields list-----", fields_list)
        res = super().default_get(fields_list=fields_list)
        print("Result------", res)
        res.update({'currency_id': 1})
        # res.update({'facilities_ids': })
        # fac_ids = self.env['hotel.facilities'].browse(3).ids
        # print("facilities_ids----", fac_ids)
        # res['facilities_ids'] = [(6, 0, fac_ids)]
        res['facilities_ids'] = [(6, 0, {3})]
        print("Updated res------", res)
        return res

    @api.model
    def search(self, args, offset=None, limit=None, order=False, count=False):
        """Overridden Search method to fetch archived bookings as well
            @param self :object pointer /recordset
            @param args : Domain if given
            @param offset: To skip the no of records
            @param limit : to limit the records
            @param order: to sort the records based on the field mentioned
            @param count : True/False
        """
        args += ['|', ('active', '=', True), ('active', '=', 'False')]
        return super().search(args, offset=offset, limit=limit, order=order, count=count)

    @api.depends('check_in', 'days_book_for')
    def _cal_checkout_date(self):
        """
        This method calculates the checkout date of the customer
        --------------------------------------------------------
        @param:object pointer/ recordset
        """
        print('compute of checkout date', self)
        for booking in self:
            booking.check_out = booking.check_in + timedelta(days=booking.days_book_for)

    @api.model
    def create(self, vals):
        """
        This method auto generates the booking id for each booking's of the hotel.
        -------------------------------------------------------------------------
        @param:object pointer/ recordset
        """
        if vals.get('booking_id', 'New') == 'New':
            vals['booking_id'] = self.env['ir.sequence'].next_by_code(
                'hotel.booking') or 'New'
        res = super(Hotel, self).create(vals)
        return res

    def unlink(self):
        """
        Overridden unlink method which checks if rooms been allocated then it wont delete the record of client
        ------------------------------------------------------------------------------------------------------
        @param self:object pointer / recordset
        """
        if self.booking_folio_ids:
            raise ValidationError("You can not delete the records of client whose rooms been allocated")
        return super().unlink()

    def copy(self, default=None):
        """
        Overridden copy() method to add copy in name
        --------------------------------------------
        @param self: recordset
        @param default: Dictionary containing fields to update while duplicating
        """
        default = {
            'guest_name': self.guest_name + '- Copy'
        }

        return super().copy(default=default)

    def action_button(self):
        """
        This method triggers when action button is clicked and shows the rainbow man effect.
        ---------------------------------------------------------------------------
        @param:object pointer/ recordset
        """
        print("Button Clicked!!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Welcome to Starline Divine',
                'type': 'rainbow_man'
            }
        }

    @api.onchange('facilities_ids')
    def _onchange_facilities_ids(self):
        """
        This method displays/hide the tabs of selected facilities and even
        deletes the records of facilities which not been selected.
        --------------------------------------------------------------------------
        @param self:object pointer / recordset
        """
        food_show = False
        transportation_show = False
        for hotel_booking in self:
            for facility in hotel_booking.facilities_ids:
                if facility.name == 'Food':
                    food_show = True
                if facility.name == 'Transportation':
                    transportation_show = True
        if not self.is_food:
            # food_show = False
            for food in self.booking_food_order_ids:
                print("====food =====", food.id)
                val = {
                    'booking_food_order_ids': [(
                        Command.delete(food.id)
                    )]
                }
                res = self.write(val)
                print("Res ----", res)

        if not self.is_transport:
            for transport in self.booking_vehicle_facility_ids:
                print("Vehicle------", transport.id)
                val = {
                    'booking_vehicle_facility_ids': [(
                        Command.delete(transport.id)
                    )]
                }
                print('Deleted vehicle fac', self.write(val))
            # transportation_show = False

        self.is_food = food_show
        self.is_transport = transportation_show

    # @api.depends('facilities_ids', 'is_food', 'is_transport', 'booking_food_order_ids', 'booking_vehicle_facility_ids')
    # def _show_tab(self):
    #     """
    #     This method shows or hides the facilities tab selected in the facilities_id
    #     ------------------------------------------------------------------------
    #     @param:object pointer/ recordset
    #     """
    #     for hotel_booking in self:
    #         # food_show = False
    #         # transportation_show = False
    #         # tab.booking_food_order_ids.unlink()
    #         # tab.booking_vehicle_facility_ids.unlink()
    #
    #         food_show = False
    #         transportation_show = False
    #         for facility in hotel_booking.facilities_ids:
    #             if facility.name == 'Food':
    #                 food_show = True
    #             if facility.name == 'Transportation':
    #                 transportation_show = True
    # if not food_show:
    #     hotel_booking.booking_food_order_ids.unlink()
    #
    # if not transportation_show:
    #     hotel_booking.booking_vehicle_facility_ids.unlink()

    # hotel_booking.is_food = food_show
    # hotel_booking.is_transport = transportation_show

    # @api.depends('facilities_ids')
    # def _show_tab(self):
    #     """
    #     This method shows or hides the facilities tab selected in the facilities_id
    #     ------------------------------------------------------------------------
    #     @param:object pointer/ recordset
    #     """
    #     for tab in self:
    #         food_show = False
    #         transportation_show = False
    #         # tab.booking_food_order_ids.unlink()
    #         # tab.booking_vehicle_facility_ids.unlink()
    #
    #         # food_show = True
    #         # transportation_show = True
    #         for visible in tab.facilities_ids:
    #             print('visible--------',visible.name)
    #
    #             if visible.name == 'Food':
    #                 # for visible.name  in tab.facilities_ids.name:
    #                     food_show = True
    #                 # else:
    #                 #     tab.booking_food_order_ids.unlink()
    #
    #
    #                 # if tab.booking_vehicle_facility_ids.vehicle_id.facility_id not in tab.facilities_ids.name:
    #                 #     tab.booking_vehicle_facility_ids.unlink()
    #
    #
    #                 # if tab.env['hotel.booking'].is_transport == False:
    #                 #     tab.booking_vehicle_facility_ids.unlink()
    #
    #
    #             # if 'Transportation' not in tab.facilities_ids.name:
    #                 #     tab.booking_vehicle_facility_ids.unlink()
    #
    #                 # print('-------helllo')
    #
    #
    #             # else:
    #             #     var1 = visible.env['hotel.facilities'].search([])
    #             #     print("search ------")
    #             #     tab.booking_food_order_ids.unlink()
    #             #     print('===========1',var1)
    #                 # var2= var1.visible.unlink()
    #                 # print('=================2',var2)
    #                 # if tab.is_transport == False:
    #                 #     tab.booking_vehicle_facility_ids.unlink()
    #
    #             # if food_show == False:
    #             #     tab.booking_food_order_ids.unlink()
    #
    #                 # tab.is_transport = show
    #                 # show =True
    #                 # tab.is_food = show
    #
    #             if visible.name == 'Transportation':
    #                 # tab.is_food = show
    #                 # show = True
    #                 # tab.is_transport = show
    #                 transportation_show = True
    #                 # if tab.booking_food_order_ids.product_category_id.facility_id not in tab.facilities_ids.name:
    #                 #     tab.booking_food_order_ids.unlink()
    #                 # if tab.env['hotel.booking'].is_food == False:
    #                 #
    #                 #     tab.booking_food_order_ids.unlink()
    #                 # if 'Food' not in tab.facilities_ids.name:
    #                 #     tab.booking_food_order_ids.unlink()
    #                 # if tab.is_food == False or food_show == False and tab.is_transport == True:
    #                 #     tab.booking_food_order_ids.unlink()
    #             # if transportation_show == False:
    #             #     tab.booking_vehicle_facility_ids.unlink()
    #
    #             # if visible.name != 'Food' and visible.name == 'Transportation':
    #             #     transportation_show = True
    #             #     food_show = False
    #             #     tab.booking_food_order_ids.unlink()
    #             # if visible.name != 'Transportation' and visible.name == 'Food':
    #             #     transportation_show = False
    #             #     food_show = True
    #             #     tab.booking_vehicle_facility_ids.unlink()
    #         tab.is_food = food_show
    #         tab.is_transport = transportation_show
