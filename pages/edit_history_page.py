"""
编辑历史记录页面模块
包含编辑历史记录的功能
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import calendar
from datetime import datetime
from utils.config import get_text, is_android, CHINESE_FONT
from widgets.ui_utils import create_label, create_text_input, create_button, create_popup
from data_manager import DataManager


class EditHistoryPage:
    """编辑历史记录页面管理类"""
    
    def __init__(self, data_manager, show_popup_callback, update_display_callback, refresh_history_callback):
        self.data_manager = data_manager
        self.show_popup = show_popup_callback
        self.update_display_callback = update_display_callback
        self.refresh_history_callback = refresh_history_callback
        self.edit_popup = None
        self.year_spinner = None
        self.month_spinner = None
        self.day_spinner = None
        self.edit_score_input = None
        self.edit_desc_input = None
    
    def show_edit_record(self, date_str=None):
        """显示编辑指定日期的记录界面"""
        android = is_android()
        
        # 如果提供了日期字符串，解析它；否则使用当前日期
        if date_str:
            try:
                date_parts = date_str.split('-')
                if len(date_parts) != 3:
                    self.show_popup(get_text('error'), get_text('invalid_date'))
                    return
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
            except (ValueError, IndexError):
                self.show_popup(get_text('error'), get_text('invalid_date'))
                return
        else:
            # 使用当前日期
            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day
        
        # 创建修改历史记录界面
        padding_val = 8 if android else 10
        spacing_val = 5 if android else 10
        top_padding = 0 if android else padding_val
        edit_layout = BoxLayout(
            orientation='vertical',
            padding=[padding_val, top_padding, padding_val, padding_val],
            spacing=spacing_val
        )
        
        # 设置浅黄色背景
        with edit_layout.canvas.before:
            Color(1.0, 0.98, 0.90, 1)  # 浅黄色 (RGB: 255, 250, 230)
            edit_layout.rect = Rectangle(size=edit_layout.size, pos=edit_layout.pos)
        
        def update_edit_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        edit_layout.bind(pos=update_edit_rect, size=update_edit_rect)
        
        # 标题
        title_label = create_label(
            get_text('edit_title'),
            size_hint_y=None,
            height=48 if android else 45,
            font_size=30 if android else 24,
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        edit_layout.add_widget(title_label)
        
        # 日期选择区域 - 年、月、日三级选择器
        date_select_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=spacing_val)
        
        # 日期标签
        date_label = create_label(
            f'{get_text("select_date")}:',
            size_hint_y=None,
            height=38 if android else 35,
            font_size=20 if android else 16,
            color=(0.2, 0.2, 0.2, 1)
        )
        date_select_layout.add_widget(date_label)
        
        # 年、月、日选择器布局
        date_picker_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=55 if android else 50,
            spacing=spacing_val
        )
        
        # 年份选择器
        year_values = [str(i) for i in range(year - 10, year + 11)]
        year_label = create_label(
            f'{get_text("year")}:',
            size_hint_x=0.15,
            font_size=20 if android else 16,
            color=(0.2, 0.2, 0.2, 1)
        )
        date_picker_layout.add_widget(year_label)
        
        self.year_spinner = Spinner(
            text=str(year),
            values=year_values,
            size_hint_x=0.28,
            font_size=20 if android else 16
        )
        if CHINESE_FONT:
            self.year_spinner.font_name = CHINESE_FONT
        self.year_spinner.bind(text=self.update_day_spinner)
        date_picker_layout.add_widget(self.year_spinner)
        
        # 月份选择器
        month_values = [str(i) for i in range(1, 13)]
        month_label = create_label(
            f'{get_text("month")}:',
            size_hint_x=0.15,
            font_size=20 if android else 16,
            color=(0.2, 0.2, 0.2, 1)
        )
        date_picker_layout.add_widget(month_label)
        
        self.month_spinner = Spinner(
            text=str(month),
            values=month_values,
            size_hint_x=0.28,
            font_size=20 if android else 16
        )
        if CHINESE_FONT:
            self.month_spinner.font_name = CHINESE_FONT
        self.month_spinner.bind(text=self.update_day_spinner)
        date_picker_layout.add_widget(self.month_spinner)
        
        # 日期选择器
        day_label = create_label(
            f'{get_text("day")}:',
            size_hint_x=0.15,
            font_size=20 if android else 16,
            color=(0.2, 0.2, 0.2, 1)
        )
        date_picker_layout.add_widget(day_label)
        
        days = self.get_days_in_month(year, month)
        day_values = [str(i) for i in range(1, days + 1)]
        self.day_spinner = Spinner(
            text=str(min(day, days)),
            values=day_values,
            size_hint_x=0.28,
            font_size=20 if android else 16
        )
        if CHINESE_FONT:
            self.day_spinner.font_name = CHINESE_FONT
        self.day_spinner.bind(text=self.on_date_components_selected)
        date_picker_layout.add_widget(self.day_spinner)
        
        date_select_layout.add_widget(date_picker_layout)
        edit_layout.add_widget(date_select_layout)
        
        # 分数输入区域
        score_edit_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=55 if android else 50,
            spacing=spacing_val
        )
        score_edit_label = create_label(
            f'{get_text("score")}:',
            size_hint_x=0.3,
            font_size=20 if android else 16,
            color=(0.2, 0.2, 0.2, 1)
        )
        score_edit_layout.add_widget(score_edit_label)
        
        self.edit_score_input = create_text_input(
            multiline=False,
            input_filter='int',
            hint_text=get_text('input_score'),
            size_hint_x=0.7,
            font_size=20 if android else 16
        )
        score_edit_layout.add_widget(self.edit_score_input)
        edit_layout.add_widget(score_edit_layout)
        
        # 描述输入区域（2行高度）
        desc_edit_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=70 if android else 60,
            spacing=spacing_val
        )
        desc_edit_label = create_label(
            f'{get_text("desc")}:',
            size_hint_x=0.3,
            font_size=20 if android else 16,
            color=(0.2, 0.2, 0.2, 1)
        )
        desc_edit_layout.add_widget(desc_edit_label)
        
        self.edit_desc_input = create_text_input(
            multiline=True,  # 允许多行输入
            hint_text=get_text('input_desc'),
            size_hint_x=0.7,
            font_size=20 if android else 16,
            padding_y=[8, 8]
        )
        desc_edit_layout.add_widget(self.edit_desc_input)
        edit_layout.add_widget(desc_edit_layout)
        
        # 按钮区域
        button_edit_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=75 if android else 60,
            spacing=spacing_val
        )
        
        # 保存修改按钮
        save_edit_button = create_button(
            get_text('save_edit'),
            size_hint_x=0.5,
            font_size=20 if android else 16,
            on_press=self.save_edit
        )
        button_edit_layout.add_widget(save_edit_button)
        
        # 关闭按钮
        close_edit_button = create_button(
            get_text('close'),
            size_hint_x=0.5,
            font_size=20 if android else 16,
            on_press=lambda x: self.edit_popup.dismiss()
        )
        button_edit_layout.add_widget(close_edit_button)
        
        edit_layout.add_widget(button_edit_layout)
        
        # 创建弹窗
        self.edit_popup = create_popup(
            get_text('edit_title'),
            edit_layout,
            size_hint=(0.95 if android else 0.7, 0.7 if android else 0.45),
            title_size=18 if android else 20
        )
        
        # 加载该日期的数据
        Clock.schedule_once(lambda dt: self.on_date_components_selected(), 0.1)
        
        self.edit_popup.open()
    
    def get_days_in_month(self, year, month):
        """获取指定年月的天数"""
        return calendar.monthrange(int(year), int(month))[1]
    
    def update_day_spinner(self, *args):
        """当年或月改变时，更新日期选择器的天数"""
        if self.year_spinner and self.month_spinner and self.day_spinner:
            year = self.year_spinner.text
            month = self.month_spinner.text
            if year and month:
                days = self.get_days_in_month(year, month)
                day_values = [str(i) for i in range(1, days + 1)]
                current_day = self.day_spinner.text
                self.day_spinner.values = day_values
                # 如果当前选择的日期超出范围，选择最后一天
                if current_day and int(current_day) > days:
                    self.day_spinner.text = str(days)
                elif not current_day or current_day not in day_values:
                    self.day_spinner.text = day_values[0] if day_values else '1'
                # 触发日期选择事件
                self.on_date_components_selected()
    
    def on_date_components_selected(self, *args):
        """当年、月、日都选择后，加载该日期的数据"""
        if self.year_spinner and self.month_spinner and self.day_spinner:
            year = self.year_spinner.text
            month = self.month_spinner.text
            day = self.day_spinner.text
            if year and month and day:
                # 格式化日期为 YYYY-MM-DD
                try:
                    date_str = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                    score_data = self.data_manager.get_score(date_str)
                    if score_data:
                        # 如果有记录，加载数据
                        self.edit_score_input.text = str(score_data.get('score', ''))
                        self.edit_desc_input.text = score_data.get('desc', '')
                    else:
                        # 如果没有记录，清空输入框
                        self.edit_score_input.text = ''
                        self.edit_desc_input.text = ''
                except ValueError:
                    pass
    
    def save_edit(self, instance):
        """保存修改的历史记录"""
        try:
            # 从年、月、日选择器获取日期
            year = self.year_spinner.text
            month = self.month_spinner.text
            day = self.day_spinner.text
            
            if not year or not month or not day:
                self.show_popup(get_text('error'), get_text('select_complete_date'))
                return
            
            # 格式化日期为 YYYY-MM-DD
            try:
                selected_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                self.show_popup(get_text('error'), get_text('invalid_date'))
                return
            
            score_text = self.edit_score_input.text.strip()
            desc_text = self.edit_desc_input.text.strip()
            
            if not score_text:
                self.show_popup(get_text('tip'), get_text('enter_score'))
                return
            
            score = int(score_text)
            if score < 0 or score > 100:
                self.show_popup(get_text('tip'), get_text('score_range'))
                return
            
            # 保存或更新数据（save_score会自动创建或更新）
            self.data_manager.save_score(selected_date, score, desc_text)
            
            # 更新显示
            self.update_display_callback()
            self.edit_popup.dismiss()
            
            # 如果历史记录弹窗还打开，刷新内容
            if self.refresh_history_callback:
                self.refresh_history_callback()
            
            # 检查是新建还是更新
            all_scores = self.data_manager.get_all_scores()
            if selected_date in all_scores:
                self.show_popup(get_text('success'), f'{selected_date}{get_text("record_updated")}')
            else:
                self.show_popup(get_text('success'), f'{selected_date}{get_text("record_created")}')
        except ValueError:
            self.show_popup(get_text('error'), get_text('invalid_number'))
        except Exception as e:
            self.show_popup(get_text('error'), f'{get_text("save_failed")}: {str(e)}')

