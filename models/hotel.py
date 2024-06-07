from odoo import fields,models

class Hotel(models.Model):
    _name='hotel.hotel'
    _description='This module contains information of hotel and its other branches'
    hotel_id=fields.Char(string='Hotel ID',required=True,help='Enter the id for the hotel')
    name=fields.Char(string='Hotel name',index=True)
    address=fields.Text(string='Address')
    phone=fields.Char('Phone no')
    email=fields.Char('Email ID')
    ratings=fields.Selection([(str(ele),str(ele))for ele in range(6)],string='Ratings')
    checkin_out=fields.Char(string='Check in and Checkout time',default='10:00 AM')
