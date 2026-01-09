"""
公共UI工具函数模块
提供共享的UI创建函数，如Label、Popup等
"""
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from utils.config import CHINESE_FONT, is_android, get_text


def create_label(text, **kwargs):
    """创建带中文字体的Label"""
    label = Label(text=text, **kwargs)
    if CHINESE_FONT:
        label.font_name = CHINESE_FONT
    return label


def create_text_input(**kwargs):
    """创建带中文字体的TextInput"""
    from kivy.uix.textinput import TextInput
    text_input = TextInput(**kwargs)
    if CHINESE_FONT:
        text_input.font_name = CHINESE_FONT
    return text_input


def create_button(text, **kwargs):
    """创建带中文字体的Button"""
    button = Button(text=text, **kwargs)
    if CHINESE_FONT:
        button.font_name = CHINESE_FONT
    return button


def create_popup(title, content_layout, size_hint=None, title_size=None):
    """创建带中文字体的Popup"""
    if size_hint is None:
        size_hint = (0.8 if is_android() else 0.6, 0.35 if is_android() else 0.3)
    if title_size is None:
        title_size = 16 if is_android() else 18
        
    popup = Popup(
        title=title,
        content=content_layout,
        size_hint=size_hint,
        title_size=title_size
    )
    
    if CHINESE_FONT:
        try:
            popup.title_font_name = CHINESE_FONT
        except:
            pass
    
    return popup


def show_message_popup(title, message):
    """显示消息弹窗"""
    content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
    
    content_label = create_label(
        message,
        size_hint_y=1,
        font_size=20 if is_android() else 16
    )
    content_layout.add_widget(content_label)
    
    close_button = create_button(
        get_text('close'),
        size_hint_y=None,
        height=55 if is_android() else 45,
        font_size=20 if is_android() else 16
    )
    close_button.bind(on_press=lambda x: popup.dismiss())
    content_layout.add_widget(close_button)
    
    popup = create_popup(title, content_layout)
    popup.open()
    
    return popup

