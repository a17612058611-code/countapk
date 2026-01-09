"""
历史记录页面模块
包含历史记录查看和删除功能
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from utils.config import get_text, is_android, CHINESE_FONT
from widgets.ui_utils import create_label, create_button, create_popup
from data_manager import DataManager


class HistoryPage:
    """历史记录页面管理类"""
    
    def __init__(self, data_manager, show_popup_callback, show_edit_callback, update_display_callback):
        self.data_manager = data_manager
        self.show_popup = show_popup_callback
        self.show_edit_callback = show_edit_callback
        self.update_display_callback = update_display_callback
        self.history_popup = None
    
    def show_history(self):
        """显示历史记录"""
        android = is_android()
        all_scores = self.data_manager.get_all_scores()
        
        if not all_scores:
            self.show_popup(get_text('history_title'), get_text('no_history'))
            return
        
        # 创建历史记录内容
        padding_val = 8 if android else 10
        spacing_val = 8 if android else 10
        history_layout = BoxLayout(orientation='vertical', padding=padding_val, spacing=spacing_val)
        
        # 设置很浅的紫色背景
        with history_layout.canvas.before:
            Color(0.96, 0.93, 0.99, 1)  # 很浅的紫色 (RGB: 245, 237, 252)
            history_layout.rect = Rectangle(size=history_layout.size, pos=history_layout.pos)
        
        def update_history_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        history_layout.bind(pos=update_history_rect, size=update_history_rect)
        
        # 标题
        title_label = create_label(
            get_text('history_title'),
            size_hint_y=None,
            height=55 if android else 45,
            font_size=32 if android else 24,
            bold=True,
            color=(0.2, 0.2, 0.2, 1)  # 黑色文字
        )
        history_layout.add_widget(title_label)
        
        # 创建滚动视图
        scroll = ScrollView(size_hint=(1, 1))
        scroll_content = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_y=None,
            padding=[0, 10, 0, 0]
        )
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        # 按日期排序（最新的在前）
        sorted_dates = sorted(all_scores.keys(), reverse=True)
        
        for date in sorted_dates:
            score_data = all_scores[date]
            score = score_data.get('score', 0)
            desc = score_data.get('desc', get_text('none'))
            
            # 创建单条记录布局
            record_height = 165 if android else 150
            record_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=record_height,
                padding=8
            )
            
            # 信息区域
            info_layout = BoxLayout(orientation='vertical', size_hint_y=None)
            label_height = 38 if android else 30
            
            date_label = create_label(
                f'{get_text("date")}: {date}',
                size_hint_y=None,
                height=label_height,
                font_size=24 if android else 18,
                color=(0.2, 0.2, 0.2, 1)
            )
            info_layout.add_widget(date_label)
            
            score_label = create_label(
                f'{get_text("score")}: {score}',
                size_hint_y=None,
                height=label_height,
                font_size=22 if android else 16,
                color=(0.2, 0.2, 0.2, 1)
            )
            info_layout.add_widget(score_label)
            
            desc_label = create_label(
                f'{get_text("desc")}: {desc}',
                size_hint_y=None,
                height=label_height,
                font_size=22 if android else 16,
                color=(0.2, 0.2, 0.2, 1)
            )
            info_layout.add_widget(desc_label)
            record_layout.add_widget(info_layout)
            
            # 按钮区域
            button_height = 70 if android else 55
            button_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=button_height,
                spacing=8
            )
            
            # 编辑按钮
            edit_btn = create_button(
                get_text('edit'),
                size_hint_x=0.5,
                font_size=22 if android else 18,
                background_color=(0.4, 0.7, 1.0, 1),  # 浅蓝色
                color=(1, 1, 1, 1),  # 白色文字
                bold=True  # 加粗
            )
            edit_btn.bind(on_press=lambda x, d=date: self.edit_record_from_history(d))
            button_layout.add_widget(edit_btn)
            
            # 删除按钮
            delete_btn = create_button(
                get_text('delete'),
                size_hint_x=0.5,
                font_size=22 if android else 18,
                background_color=(1.0, 0.5, 0.5, 1),  # 浅红色
                color=(1, 1, 1, 1),  # 白色文字
                bold=True  # 加粗
            )
            delete_btn.bind(on_press=lambda x, d=date: self.delete_record_from_history(d))
            button_layout.add_widget(delete_btn)
            
            record_layout.add_widget(button_layout)
            
            # 添加分隔线
            separator = create_label(
                '─' * 20,
                size_hint_y=None,
                height=4,
                font_size=8,
                color=(0.2, 0.2, 0.2, 1)
            )
            scroll_content.add_widget(record_layout)
            scroll_content.add_widget(separator)
        
        scroll.add_widget(scroll_content)
        history_layout.add_widget(scroll)
        
        # 关闭按钮
        close_button = create_button(
            get_text('close'),
            size_hint_y=None,
            height=70 if android else 55,
            font_size=24 if android else 18,
            bold=True
        )
        close_button.bind(on_press=lambda x: self.history_popup.dismiss())
        history_layout.add_widget(close_button)
        
        # 创建弹窗
        self.history_popup = create_popup(
            get_text('history_title'),
            history_layout,
            size_hint=(0.95 if android else 0.8, 0.9 if android else 0.8),
            title_size=22 if android else 20
        )
        self.history_popup.open()
    
    def delete_record_from_history(self, date):
        """从历史记录中删除一条记录"""
        android = is_android()
        from kivy.uix.boxlayout import BoxLayout as BL
        
        # 显示确认对话框
        confirm_layout = BL(orientation='vertical', padding=10, spacing=10)
        
        confirm_label = create_label(
            get_text('delete_confirm'),
            size_hint_y=1,
            font_size=20 if android else 16
        )
        confirm_layout.add_widget(confirm_label)
        
        button_layout = BL(
            orientation='horizontal',
            size_hint_y=None,
            height=55 if android else 40,
            spacing=10
        )
        
        # 确认按钮
        yes_button = create_button(
            get_text('confirm'),
            size_hint_x=0.5,
            font_size=20 if android else 16
        )
        button_layout.add_widget(yes_button)
        
        # 取消按钮
        no_button = create_button(
            get_text('close'),
            size_hint_x=0.5,
            font_size=20 if android else 16
        )
        button_layout.add_widget(no_button)
        
        confirm_layout.add_widget(button_layout)
        
        confirm_popup = create_popup(
            get_text('tip'),
            confirm_layout,
            size_hint=(0.7 if android else 0.5, 0.3 if android else 0.25),
            title_size=16 if android else 18
        )
        
        def confirm_delete(instance):
            try:
                if self.data_manager.delete_score(date):
                    # 删除成功
                    confirm_popup.dismiss()
                    self.history_popup.dismiss()
                    self.update_display_callback()  # 更新主界面显示
                    self.show_popup(get_text('success'), get_text('record_deleted'))
                    # 重新打开历史记录
                    Clock.schedule_once(lambda dt: self.show_history(), 0.1)
                else:
                    confirm_popup.dismiss()
                    self.show_popup(get_text('error'), get_text('delete_failed'))
            except Exception as e:
                confirm_popup.dismiss()
                self.show_popup(get_text('error'), f'{get_text("delete_failed")}: {str(e)}')
        
        def cancel_delete(instance):
            confirm_popup.dismiss()
        
        yes_button.bind(on_press=confirm_delete)
        no_button.bind(on_press=cancel_delete)
        confirm_popup.open()
    
    def edit_record_from_history(self, date):
        """从历史记录中编辑一条记录"""
        # 打开编辑界面，并设置日期
        self.show_edit_callback(date)

