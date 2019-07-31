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
        'email': fields.char(u'邮箱'),
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

    def _get_sequence(self, cr, uid, ids, context=None):
        """初始化序列值"""
        new_id = self.pool.get('ir.sequence').get(cr, uid, 'amos.text')
        return new_id

    _defaults = {
        'state': lambda *a: 'draft',
        # 'name': '/',
        'name': _get_sequence,
    }

    def create(self, cr, uid, vals, context=None):
        """
        点击保存按钮，会触发该方法。
        此处点击保存按钮，自动生成默认值
        :param cr:
        :param uid:
        :param vals: 保存着model的字段
        :param context:
        :return: 新的记录id
        """

        if context is context:
            context = {}
        if vals.get('name', '/') == '/':
            # 从连接池中获取序列对象，
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'amos.text') or '/'
            ctx = dict(context or {}, mail_create_nolog=True)
            new_id = super(amos_text, self).create(cr, uid, vals, context=ctx)
            return new_id
        else:
            return super(amos_text, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """
        编辑保存时触发此方法。
        这里编辑保存获取修改的字段值，以及获取原始表单未修改的字段
        :param cr:
        :param uid:
        :param ids:
        :param vals: 接受的是view中被改动字段的值
        :param context:
        :return:
        """
        # vals中获取改动的字段
        print vals, "amos_text --> write()"
        # 获取未改动的值
        obj = self.browse(cr, uid, ids[0])  # 获取当前操作表单对象
        print obj, '更改对象'
        print obj.user_id.name, obj.date_start, obj.date_start
        res = super(amos_text, self).write(cr, uid, ids, vals, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        """判断表单状态，当为草稿时删除执行删除方法删除记录"""
        obj = self.browse(cr, uid, ids, context)    # 获取当前操作表单对象 值为列表型
        if obj[0].state != 'draft':
            raise osv.except_osv(u'提醒', u'只能删除草稿')
        return super(amos_text, self).unlink(cr, uid, ids, context=context)
    
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        """
        查看对象时触发
        :param cr:
        :param uid:
        :param ids:
        :param fields: 对象的字段列表
        :param context: 上下文数据
        :param load:
        :return:
        """
        res = super(amos_text, self).read(cr, uid, ids, fields=fields, context=context, load=load)
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        obj = self.browse(cr, uid, id, context=context)
        default["name"] = "%s(副本)" % obj.name
        return super(amos_text, self).copy(cr, uid, id, default=default, context=context)

    def onchange_user_id(self, cr, uid, ids, user_id, context=None):
        res = {}
        if user_id:
            obj = self.pool.get('res.users').browse(cr, uid, user_id, context=context)
            print obj, "obj"
            res['email'] = obj.email
        return {'value': res}

    # 定义按钮事件处理函数
    def btn_review(self, cr, uid, ids, context=None):
        state = 'review'
        message = '提交草稿，等待审核！'
        self.write(cr, uid, ids, {'state': state}, context=context)
        # self.message_post(cr, uid, ids, body=_(message), context=context)
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
        # self.message_post(cr, uid, ids, body=_(message), context=context)
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

    def install_amos_text(self, cr, uid, ids, context=None):
        print context, 'amos.text --> install_amos_text()'
        # 可以实现如sql写入的业务代码
        return True


class amos_text_line(osv.osv):
    _name = 'amos.text.line'
    _description = 'amos.text.line'

    _columns = {
        'product_id': fields.many2one('product.product', u'费用名称', domain=[('sale_ok', '=', True)]),
        'date_order': fields.datetime(u'实到日期', select=True, copy=False),
        'price_unit': fields.float(u'培训费用',),
        'is_buy': fields.boolean(u'是否购买教程',),
        'amos_text_id': fields.many2one('amos.text', u'培训'),
        'ref': fields.selection([('1', u'网络'),
                                 ('2', u'电话营销')],
                                u'会员来源',),
    }

    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        res = {}
        if product_id:
            obj = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            res['price_unit'] = obj.list_price
        return {'value': res}


class amos_tag(osv.osv):
    _name = 'amos.tag'
    _description = 'amos.tag'

    _columns = {
        'name': fields.char(u'编号'),
    }




