# -*- coding: utf-8 -*-
import logging

from openerp.osv import osv, fields

_logger = logging.getLogger(__name__)


class amos_text(osv.osv):
    _name = 'amos.text'
    _description = 'amos.text'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _log_access = True      # 缺省值: True, 是否自动在对应的数据表中增加create_uid, create_date, write_uid, write_date四个字段

    def _amount(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        print ids
        print uid

        for prm in self.browse(cr, uid, ids, context=context):
            print prm
            print prm.order_line
            total = 0.0
            for line in prm.order_line:
                total += line.price_unit
            res[prm.id] = total
        return res

    states_draft = {'draft': [('readonly', False)]}
    states_draft_and_review = {'draft': [('readonly', False)], 'review': [('readonly', False)]}

    _columns = {
        'name': fields.char(u'编号', states=states_draft, readonly=True),
        'user_id': fields.many2one('res.users', u'主持人', states=states_draft, readonly=True),
        'duration': fields.float(u'时长', states=states_draft, readonly=True),
        'date_start': fields.datetime(u'开始日期', select=True, copy=False, states=states_draft, readonly=True),
        'date_end': fields.datetime(u'结束日期', select=True, copy=False, states=states_draft, readonly=True),
        'number': fields.integer(u'应参加人数', states=states_draft, readonly=True),
        'note': fields.text(u'培训内容', states=states_draft, readonly=True),
        'street': fields.char(u'培训地址', states=states_draft, readonly=True),
        'price_subtotal': fields.function(_amount, string=u'合计', digits=(16,2), store=True),    # store=True 从数据库渲染
        'state': fields.selection([('draft', u'草稿'),
                                   ('review', u'等待审核'),
                                   ('done', u'已完成'),
                                   ('sent', u'发送邮件'),
                                   ('cancel', u'取消')],
                                  u'状态', states=states_draft, readonly=True),
        'order_line': fields.one2many('amos.text.line', 'amos_text_id', u'明细', states=states_draft, readonly=True),
        'tag_ids': fields.many2many('amos.tag', 'amos_text_amos_tag_rel', 'text_id', 'tag_id', u'分类', states=states_draft, readonly=True),
    }

    _defaults = {
        'state': lambda *a: 'draft',
    }

    # 定义按钮事件处理函数
    def btn_review(self, cr, uid, ids, context=None):
        state = 'review'
        message = '提交草稿，等待审核！'
        self.write(cr, uid, ids, {'state': state}, context=context)
        self.message_post(cr, uid, ids, body=_(message), context=context)
        return True

    def btn_cancel(self, cr, uid, ids, context=None):
        state = 'cancel'
        message = '单据已取消！'
        self.btn_action(cr, uid, ids, state, message, context=context)
        return True

    def btn_done(self, cr, uid, ids, context={}):
        state = 'done'
        message = '单据已完成！'
        self.btn_action(cr, uid, ids, state, message, context=context)
        return True

    def btn_draft(self, cr, uid, ids, context={}):
        state = 'draft'
        message = '单据重置为草稿！'
        self.btn_action(cr, uid, ids, state, message, context=context)
        return True

    def btn_action(self, cr, uid, ids, state, message, context={}):
        """按键触发事件"""

        self.write(cr, uid, ids, {'state': state}, context=context)
        # 推送消息
        self.message_post(cr, uid, ids, body=_(message), context=context)
        print ids
        o = self.browse(cr, uid, ids[0], context)

        if hasattr(self, 'message_subscribe'):
            self.message_subscribe(cr, uid, ids, [o.user_id.partner_id.id], context=context)
        return True

    # 定义工作流事件处理函数
    def amos_review(self, cr, uid, ids, context=None):
        state = 'review'
        message = '提交草稿，等待审核！'
        self.write(cr, uid, ids, {'state': state}, context=context)
        # self.message_post(cr, uid, ids, body=_(message), context=context)
        return True

    def amos_cancel(self, cr, uid, ids, context=None):
        state = 'cancel'
        message = '单据已取消！'
        self.wkf_action(cr, uid, ids, state, message, context=context)
        return True

    def amos_done(self, cr, uid, ids, context={}):
        state = 'done'
        message = '单据已完成！'
        self.wkf_action(cr, uid, ids, state, message, context=context)
        return True

    def amos_draft(self, cr, uid, ids, context={}):
        state = 'draft'
        message = '单据重置为草稿！'
        self.wkf_action(cr, uid, ids, state, message, context=context)
        return True

    def wkf_action(self, cr, uid, ids, state, message, context={}):
        """按键触发事件"""

        self.write(cr, uid, ids, {'state': state}, context=context)
        # 推送消息
        # self.message_post(cr, uid, ids, body=_(message), context=context)

        # if hasattr(self, 'message_subscribe'):
        #     self.message_subscribe(cr, uid, ids, [4], context=context)
        return True


class amos_text_line(osv.osv):
    _name = 'amos.text.line'
    _description = 'amos.text.line'

    _columns = {
        'date_order': fields.datetime(u'实到日期', select=True, copy=False),
        'price_unit': fields.float(u'培训费用',),
        'is_buy': fields.boolean(u'是否购买教程',),
        'amos_text_id': fields.many2one('amos.text', u'培训'),
        'ref': fields.selection([('1', u'网络'),
                                 ('2', u'电话营销')],
                                u'会员来源',),
    }


class amos_tag(osv.osv):
    _name = 'amos.tag'
    _description = 'amos.tag'

    _columns = {
        'name': fields.char(u'编号'),
    }




