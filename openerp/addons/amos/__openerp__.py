# -*- coding: utf-8 -*-


{
	'name': u'text',
	'summary': 'PosBox',
	'version': '1.0',
    'description': u"""模块描述
    """,
	'category': 'li',
	'sequence': 0,
    'author': 'li',
    'website': 'http://www.openerp.com',
    'depends': ['base', 'mail', 'product'],
    'data': [
        'amos_text_view.xml',
        'amos_text_workflow.xml',
        'data.xml',
        'amos_sequence.xml',
        'amos_groups.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        # xx.xml
    ],
    'demo': [

    ],
    'test': [
        # test.yml
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}