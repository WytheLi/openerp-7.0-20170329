# -*- coding: utf-8 -*-
import logging

from openerp.osv import osv, fields

_logger = logging.getLogger(__name__)


class amos_all(osv.osv):

    _name = 'amos.all'
    _inherits = {'amos.text': 'text_id'}
    _description = u'全继承演示'

    _columns = {
        'mobile': fields.char(u'手机号', size=64),
        'text_id': fields.many2one('amos.text', u'原对象'),
    }


