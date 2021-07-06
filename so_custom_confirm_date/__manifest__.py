# -*- coding: utf-8 -*-
{
    'name': "Optesis Sale Order Custom Validation Date",

    'summary': """
        La date saisie dans le sale.order doit etre considérée comme de confirmation et date prévue du stock.picking associé au sale order""",

    'description': """
        
    """,

    'author': "Optesis SA, by Robilife",
    'website': "http://www.optesis.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_inherit_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
