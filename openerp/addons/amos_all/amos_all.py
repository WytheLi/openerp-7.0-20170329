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

    def _get_mobile(self, cr, uid, context=None):
        """通过视图上下文，初始化值"""
        print context, 'amos_all --> _get_mobile()'
        if context is None:
            context = {}
        res = context.get('search_default_user_id', 0)
        return res

    _defaults = {
        'mobile': _get_mobile,
    }

    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        print context, 'amos_all --> read'
        res = super(amos_all, self).read(cr, uid, ids, fields=fields, context=context, load=load)
        return res
