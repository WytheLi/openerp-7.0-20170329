# -*- coding: utf-8 -*-
import logging

from openerp.osv import osv, fields

_logger = logging.getLogger(__name__)


class amos_tel(osv.osv):
    _inherit = 'amos.text'
    _description = 'amos.tel'

    _columns = {
        'tel': fields.char(u'手机号码', size=20),
    }

