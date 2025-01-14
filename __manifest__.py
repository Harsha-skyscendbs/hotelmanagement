{
    'name':'Hotel Management System1',
    'description':'This module is used for booking hotel rooms',
    'author':'Harsha',
    'website':'https://www.stardivine.com',
    'version':'1.0',
    'depends':['base'],
    'data': [
             'security/hotel_security.xml',
             'security/ir.model.access.csv',
             'views/room_view.xml',
             'views/booking_view.xml',
             'views/room_type_view.xml',
             'views/hotel_view.xml',
             'views/product_categories_view.xml',
             'views/product_view.xml',
             'views/view_vehicle_facility.xml',
             'views/facilities_view.xml',
             'views/booking_tab_lines_view.xml',
            ],
    'auto_install': False,
    'installable':True,
    'application': True,
    'license':'OEEL-1',
}