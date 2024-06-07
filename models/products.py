from odoo import models, fields


class Products(models.Model):
    _name = 'hotel.products'
    _description = ('this module contains the'
                    ' information of the food products according to the'
                    ' categories available')

    name = fields.Char('Food Name')
    code = fields.Char('Food code')
    # booking_id=fields.Many2one('hotel.booking','Booking Id')
    product_category_id = fields.Many2one('hotel.productcategories', 'Food Category')
    currency_id = fields.Many2one('res.currency', 'Currency')
    # quantity=fields.Integer('Quantity')
    price = fields.Monetary(currency_field='currency_id', string='Price')
    taxes = fields.Float(string='Customer Taxes')
    company_id = fields.Many2one('res.company', 'Hotel', default=lambda self: self.env.company)
