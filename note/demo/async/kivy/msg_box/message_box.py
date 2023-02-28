# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# @project : new_pos_simple
# @file    : message_box.py
# @time    : 2019/8/27 11:27
# @author  : GuangLin
# @version : 0.01
# @desc    :
import gc
from kivy.clock import Clock

__all__ = [
    "MessageBoxChoose",
    "MessageBoxInfo",
    "TimeMessageBoxInfo",
    "MessageBoxIcon",
]

from kivy.uix.modalview import ModalView
from kivy import properties

from ui.kv import utils
from language import tran, t

try:
    import logging
    debug = logging.info
except ImportError:
    debug = print

ICON_PATH = ""


class MessageBoxBase(ModalView, utils.UtilMix):
    """
    消息对话框
    """

    # 光标可切换控件id
    focus_able_ids = ['btn_n_id', 'btn_y_id']
    show_msg = properties.StringProperty("")
    btn_y_text = properties.StringProperty("OK")
    btn_n_text = properties.StringProperty("Cancel")

    def __init__(self, parent, msg, btn_y="", btn_n="", callback=None, size=(500, 300), msg_len='',
                 auto_tran=False, **kwargs):
        """
        消息对话框构造
        :param parent:   父窗口
        :param msg:      显示消息内容
        :param btn_y:    `btn_y_id` 按钮文本
        :param btn_n:    `btn_n_id` 按钮文本
        :param callback: 关闭回调
        :param size:     窗口尺寸
        :param kwargs:   其他`ModalView`属性参数
        """
        utils.KvLoad.load(__file__)
        kwargs.update(size=size)
        kwargs.update(auto_dismiss=False)
        ModalView.__init__(self, **kwargs)
        msg = msg and str(msg) or t.t("unknown error")
        if msg_len == 'control':
            msg = len(msg) > 100 and msg[:100] + "..." or msg
        self.src_msg = msg

        t_msg = auto_tran and tran(msg) or msg
        self.show_msg = t_msg
        if btn_y:
            self.btn_y_text = btn_y
        if btn_n:
            self.btn_n_text = btn_n
        self._callback = callback
        self._trigger = parent

        # 保存父窗口的光标控件句柄
        if hasattr(parent, "get_focus_widget"):
            self.focus_widget = parent.get_focus_widget()
        else:
            self.focus_widget = self.find_focus_widget(parent)

        # 保存父窗口按键绑定句柄
        if hasattr(parent, "get_sub_key_bind"):
            self._key_listen_obj_bak = parent.get_sub_key_bind()
        else:
            self._key_listen_obj_bak = None

        # 绑定父窗口按键绑定MsgBox
        sub_key_bind = getattr(parent, "modal_views_key_bind", None)
        if callable(sub_key_bind):
            sub_key_bind(self)
        else:
            debug("MessageBox 入参prent无sub_key_bind")
        debug("MsgBox open:{}".format(self.src_msg))
        self.is_close = False

    def open(self):
        on_view = getattr(self._trigger, "on_modal_view", None)
        callable(on_view) and on_view(True)
        super(MessageBoxBase, self).open()

    def close(self, is_yes: bool):
        """
        关闭对话框
        :param is_yes: 选择结果
        :return: True
        """
        if self.is_close:
            return
        self.is_close = True
        debug("MsgBox close:{} -> {}".format(self.src_msg, is_yes and "Yes" or "No"))
        if callable(self._callback):
            self._callback(is_yes)
            self._callback = None

        # 恢复按键绑定
        getattr(self._trigger, "modal_views_key_unbind", lambda obj: None)(self)
        getattr(self._trigger, "sub_key_bind", lambda obj: None)(self._key_listen_obj_bak)

        # 恢复光标
        if self.focus_widget:
            self.focus_widget.focus = True

        self.dismiss()
        on_view = getattr(self._trigger, "on_modal_view", None)
        callable(on_view) and on_view(False)
        gc.collect()
        return True

    def on_enter_key(self):
        """回车键回调"""
        return
        debug("on_enter")
        wid = self.get_focus_widget_id()
        if 'y' in wid:
            return self.close(True)
        else:
            return self.close(False)

    def on_tab_key(self):
        """Tab键回调"""
        self.switch_focus()

    def on_btn_focus(self, widget, **kwargs):
        """按钮光标焦点回调"""
        debug("{} on_btn_focus:{} {}".format(self.__class__.__name__, widget, kwargs))
        if widget.focus:
            widget.color = [1, 1, 1, 1]
            widget.state = "down"
        else:
            widget.color = [33 / 255, 44 / 255, 103 / 255, 1]
            widget.state = "normal"

    def __str__(self):
        return "MessageBoxBase: 消息对话框"


class MessageBoxChoose(MessageBoxBase):
    """
    选择性消息对话框
    For example:

    def handler(choose, a):
        print("MessageBoxChoose:{}, {}".format(choose, a))

    MessageBoxChoose(self, "确认整单取消？", callback=handler, btn_y='确定', btn_n='取消')
    """
    def __init__(self, *args, **kwargs):
        super(MessageBoxChoose, self).__init__(*args, **kwargs)
        self.open()


class MessageBoxInfo(MessageBoxBase):
    """
    提示性消息对话框
    For example:

    def handler(choose, a):
        print("MessageBoxChoose:{}, {}".format(choose, a))

    MessageBoxInfo(self, "下载完成", callback=handler, btn_y='确定')

    """
    key_handler = dict(enter="on_enter_key")

    def __init__(self, *args, **kwargs):
        super(MessageBoxInfo, self).__init__(*args, **kwargs)
        self.ids.button_layout.width = 150
        self.ids.button_layout.remove_widget(self.ids.btn_n_id)
        self.open()


class MessageBoxIcon(ModalView, utils.UtilMix):
    # 光标可切换控件id
    focus_able_ids = ['btn_n_id', 'btn_y_id']

    hint_img = properties.StringProperty("")
    show_title = properties.StringProperty("")
    btn_y_text = properties.StringProperty("")
    btn_n_text = properties.StringProperty("")
    cnt_event = False

    def __init__(self, parent, title, icon, btn_y="", btn_n="", callback_yes=None, callback_no=None,
                 countdown_y=False, countdown_y_cnt=0, **kwargs):
        utils.KvLoad.load(__file__)
        kwargs.update(auto_dismiss=False)
        ModalView.__init__(self, **kwargs)

        # btn_y, btn_n 二者必须有一个，因为还没有加入自动关闭
        self.btn_y_text, self.btn_n_text = btn_y, btn_n
        self.countdown_y, self.countdown_y_cnt, self.icon = countdown_y, countdown_y_cnt, icon

        # 必传项title, 提示信息
        self.show_title = t.t(title)
        # 必传项icon, 布尔类型（图片增加后可以扩展此类型）
        self.hint_img = utils.icon_kv("success_icon.png") if icon else utils.icon_kv("print_fail.png")

        if btn_y:
            self.btn_y_text = btn_y
            self.ids.btn_y_id.opacity = 1
            self.ids.btn_y_id.size_hint = 1, 1
            self.ids.btn_n_id.size_hint = 0, 1
            self.ids.btn_n_id.width = 0
            self.ids.btn_y_id.width = 150
        else:
            self.ids.button_layout.width = 150
            self.ids.btn_y_id.opacity = 0

        if btn_n:
            self.btn_n_text = btn_n
            self.ids.btn_n_id.opacity = 1
            self.ids.btn_n_id.size_hint = 1, 1
            self.ids.btn_y_id.size_hint = 0, 1
            self.ids.btn_y_id.width = 0
            self.ids.btn_n_id.width = 150
        else:
            self.ids.button_layout.width = 150
            self.ids.btn_n_id.opacity = 0

        if self.ids.btn_y_id.opacity == 1 and self.ids.btn_n_id.opacity == 1:
            self.ids.button_layout.width = 300
            self.ids.btn_y_id.size_hint = .5, 1
            self.ids.btn_n_id.size_hint = .5, 1

        # 特殊处理确定按钮的展示
        if self.countdown_y and self.countdown_y_cnt:
            self.btn_y_origin_text = self.btn_y_text
            self.btn_y_text = self.get_btn_y_text()
            if not self.cnt_event:
                self.cnt_event = Clock.create_trigger(self.update_btn_y_text, timeout=1, interval=True)
                self.cnt_event()
        else:
            self.btn_y_text = t.t(btn_y)

        self._callback_yes = callback_yes
        self._callback_no = callback_no
        self._trigger = parent

        # 通用处理，保存父窗口的光标控件句柄
        if hasattr(parent, "get_focus_widget"):
            self.focus_widget = parent.get_focus_widget()
        else:
            self.focus_widget = self.find_focus_widget(parent)

        # 通用处理，保存父窗口按键绑定句柄
        if hasattr(parent, "get_sub_key_bind"):
            self._key_listen_obj_bak = parent.get_sub_key_bind()
        else:
            self._key_listen_obj_bak = None

        # 通用处理，绑定父窗口按键绑定MsgBox
        sub_key_bind = getattr(parent, "modal_views_key_bind", None)
        if callable(sub_key_bind):
            sub_key_bind(self)
        else:
            debug("MessageBox 入参prent无sub_key_bind")
        self.is_close = False
        self.open()

    def on_dismiss(self):
        self.is_close = True

    def update_message_box(self, title, icon, btn_y="", btn_n="", callback_yes=None, callback_no=None,
                           countdown_y=False, countdown_y_cnt=0, **kwargs):
        self.show_title = t.t(title)
        # btn_y, btn_n 二者必须有一个，因为还没有加入自动关闭
        self.btn_y_text, self.btn_n_text = btn_y, btn_n
        self.countdown_y, self.countdown_y_cnt, self.icon = countdown_y, countdown_y_cnt, icon

        # 必传项title, 提示信息
        self.show_title = t.t(title)
        # 必传项icon, 布尔类型（图片增加后可以扩展此类型）
        self.hint_img = utils.icon_kv("success_icon.png") if icon else utils.icon_kv("print_fail.png")

        if btn_y:
            self.btn_y_text = btn_y
            self.ids.btn_y_id.opacity = 1
            self.ids.btn_y_id.size_hint = 1, 1
            self.ids.btn_n_id.size_hint = 0, 1
            self.ids.btn_n_id.width = 0
            self.ids.btn_y_id.width = 150
        else:
            self.ids.button_layout.width = 150
            self.ids.btn_y_id.opacity = 0

        if btn_n:
            self.btn_n_text = btn_n
            self.ids.btn_n_id.opacity = 1
            self.ids.btn_n_id.size_hint = 1, 1
            self.ids.btn_y_id.size_hint = 0, 1
            self.ids.btn_y_id.width = 0
            self.ids.btn_n_id.width = 150
        else:
            self.ids.button_layout.width = 150
            self.ids.btn_n_id.opacity = 0

        if self.ids.btn_y_id.opacity == 1 and self.ids.btn_n_id.opacity == 1:
            self.ids.button_layout.width = 300
            self.ids.btn_y_id.size_hint = .5, 1
            self.ids.btn_n_id.size_hint = .5, 1

        # 特殊处理确定按钮的展示
        if self.countdown_y and self.countdown_y_cnt:
            self.btn_y_origin_text = self.btn_y_text
            self.btn_y_text = self.get_btn_y_text()
            self.cnt_event = Clock.create_trigger(self.update_btn_y_text, timeout=1, interval=True)
            self.cnt_event()
        else:
            self.btn_y_text = t.t(btn_y)

        self._callback_yes = callback_yes
        self._callback_no = callback_no

        if self.is_close:
            self.open()
            self.is_close = False

    def get_btn_y_text(self):
        self.btn_y_text = ""
        return "{} ({}{})".format(t.t(self.btn_y_origin_text), self.countdown_y_cnt, t.t("Seconds"))

    def update_btn_y_text(self, *args):
        if self.is_close:
            return False

        self.countdown_y_cnt -= 1
        self.btn_y_text = self.get_btn_y_text()

        if self.countdown_y_cnt == 0:
            callable(self._callback_yes) and self.press_yes()

    def open(self):
        on_view = getattr(self._trigger, "on_modal_view", None)
        callable(on_view) and on_view(True)
        super(MessageBoxIcon, self).open()
        debug("MessageBoxIcon open {}".format(self.show_title.replace("\n", " ")))

    def press_yes(self, *args):
        if self.is_close:
            return
        self.is_close = True

        debug("MsgBox close:{} -> {}".format(self.show_title, "Yes"))
        if callable(self._callback_yes):
            self._callback_yes()
            self._callback_yes = None

        # 通用处理，恢复按键绑定
        getattr(self._trigger, "modal_views_key_unbind", lambda obj: None)(self)  # a
        getattr(self._trigger, "sub_key_bind", lambda obj: None)(self._key_listen_obj_bak)  # a

        # 通用处理，恢复光标
        if self.focus_widget:
            self.focus_widget.focus = True

        self.cnt_event and self.cnt_event.cancel()
        self.dismiss()
        on_view = getattr(self._trigger, "on_modal_view", None)
        callable(on_view) and on_view(False)
        gc.collect()
        return True

    def on_enter_key(self):
        """回车键回调"""
        return

    def on_tab_key(self):
        """Tab键回调"""
        self.switch_focus()

    def on_btn_focus(self, widget, **kwargs):
        """按钮光标焦点回调"""
        debug("{} on_btn_focus:{} {}".format(self.__class__.__name__, widget, kwargs))
        if widget.focus:
            widget.color = [1, 1, 1, 1]
            widget.state = "down"
        else:
            widget.color = [33 / 255, 44 / 255, 103 / 255, 1]
            widget.state = "normal"

    def press_no(self, *args):
        if self.is_close:
            return
        self.is_close = True
        debug("MsgBox close: -> No")
        if callable(self._callback_no):
            self._callback_no()
            self._callback_no = None

        # 恢复按键绑定
        getattr(self._trigger, "modal_views_key_unbind", lambda obj: None)(self)

        self.cnt_event and self.cnt_event.cancel()
        self.dismiss()
        gc.collect()
        return True


class TimeMessageBoxInfo(MessageBoxBase):
    """
    定时消息对话框
    For example:

    def handler(choose, a):
        print("MessageBoxChoose:{}, {}".format(choose, a))

    MessageBoxInfo(self, "下载完成", callback=handler, btn_y='确定')

    """
    key_handler = dict(enter="on_enter_key")

    def __init__(self, *args, **kwargs):
        super(TimeMessageBoxInfo, self).__init__(*args, **kwargs)
        self.ids.button_layout.width = 150
        self.ids.button_layout.remove_widget(self.ids.btn_n_id)
        Clock.schedule_once(self.time_to_enable, 3)
        self.ids['btn_y_id'].disabled = True
        self.open()

    def time_to_enable(self, *args):
        self.ids['btn_y_id'].disabled = False


class NoButtonMessageBoxInfo(MessageBoxBase):
    """
    提示性消息对话框
    For example:

    def handler(choose, a):
        print("MessageBoxChoose:{}, {}".format(choose, a))

    MessageBoxInfo(self, "下载完成", callback=handler, btn_y='确定')

    """
    key_handler = dict(enter="on_enter_key")

    def __init__(self, *args, **kwargs):
        super(NoButtonMessageBoxInfo, self).__init__(*args, **kwargs)
        # self.ids.button_layout.width = 150
        self.ids.float_layout.remove_widget(self.ids.button_layout)
        self.ids.lab_prom.pos_hint = {'center_x': .5, 'center_y': .5}
        self.ids.lab_prom.line_height = 1.5
        # self.ids.button_layout.remove_widget(self.ids.btn_n_id)
        # self.ids.button_layout.remove_widget(self.ids.btn_y_id)
        self.open()


class TimeCloseMessageBoxInfo(NoButtonMessageBoxInfo):
    """
    定时消息对话框自动关闭
    For example:

    def handler(choose, a):
        print("MessageBoxChoose:{}, {}".format(choose, a))

    MessageBoxInfo(self, "下载完成", callback=handler, btn_y='确定')

    """
    key_handler = dict(enter="on_enter_key")

    def __init__(self, *args, **kwargs):
        super(TimeCloseMessageBoxInfo, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.time_to_close, 2)

    def time_to_close(self, *args):
        self.close(True)


class MessageBoxInfoData(MessageBoxBase):
    """
    提示性消息对话框
    For example:

    def handler(choose, a):
        print("MessageBoxChoose:{}, {}".format(choose, a))

    MessageBoxInfoData(self, "下载完成", callback=handler, btn_y='确定')

    """
    key_handler = dict(enter="on_enter_key")

    def __init__(self, *args, **kwargs):
        super(MessageBoxInfoData, self).__init__(*args, **kwargs)
        self.ids.button_layout.width = 150
        self.ids.button_layout.remove_widget(self.ids.btn_n_id)
        self.ids.lab_prom.halign = 'left'
        self.ids.lab_prom.valign = 'middle'
        self.open()
