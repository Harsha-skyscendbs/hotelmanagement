from odoo import fields, models


class ProductCategories(models.Model):
    _name = 'hotel.productcategories'
    _description = "This module contains information of the hotel's food products categories"

    name = fields.Char('Product Category')
    code = fields.Char('Product code')
    company_id = fields.Many2one('res.company', 'Hotel', default=lambda self: self.env.company)
    facility_id = fields.Many2one('hotel.facilities','Facilities', default= lambda self: self.env['hotel.facilities'].search([('name', '=', 'Food')]))
