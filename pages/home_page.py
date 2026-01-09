"""
首页模块
包含主界面的UI和逻辑
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from datetime import datetime
from utils.config import get_text, is_android, CHINESE_FONT
from widgets.ui_utils import create_label, create_text_input, create_button
from data_manager import DataManager


class HomePage(BoxLayout):
    """首页页面"""
    
    def __init__(self, data_manager, on_view_history, on_edit_history, show_popup_callback, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.data_manager = data_manager
        self.on_view_history = on_view_history
        self.on_edit_history = on_edit_history
        self.show_popup = show_popup_callback
        
        # 设置浅蓝色背景
        with self.canvas.before:
            Color(0.85, 0.92, 1.0, 1)  # 浅蓝色 (RGB: 217, 235, 255)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        self.bind(pos=update_rect, size=update_rect)
        
        # 根据平台调整布局参数
        android = is_android()
        if android:
            padding_val = 25
            spacing_val = 20
            title_font_size = 42
            normal_font_size = 30
            label_height = 65
            input_height = 95
            button_height = 95
        else:
            padding_val = 30
            spacing_val = 20
            title_font_size = 36
            normal_font_size = 24
            label_height = 50
            input_height = 70
            button_height = 70
        
        # 主布局
        main_layout = BoxLayout(
            orientation='vertical',
            padding=padding_val,
            spacing=spacing_val,
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # 创建ScrollView以支持滚动
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
        
        # 标题（深蓝色加粗）
        title = create_label(
            get_text('app_title'),
            size_hint_y=None,
            height=label_height * 2,
            font_size=title_font_size,
            bold=True,
            color=(0.2, 0.3, 0.6, 1)  # 深蓝色文字
        )
        main_layout.add_widget(title)
        
        # 日期显示
        self.date_label = create_label(
            f'{get_text("date")}: {datetime.now().strftime("%Y-%m-%d")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.3, 0.3, 0.3, 1)  # 深灰色文字
        )
        main_layout.add_widget(self.date_label)
        
        # 当天分数输入区域
        score_input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=input_height,
            spacing=spacing_val
        )
        score_label = create_label(
            f'{get_text("today_score")}:',
            size_hint_x=0.3,
            font_size=normal_font_size,
            color=(0.3, 0.3, 0.3, 1)
        )
        score_input_layout.add_widget(score_label)
        
        self.score_input = create_text_input(
            multiline=False,
            input_filter='int',
            hint_text=get_text('input_score'),
            size_hint_x=0.4,
            font_size=normal_font_size,
            background_color=(1, 1, 1, 1),  # 白色背景
            foreground_color=(0.2, 0.2, 0.2, 1)  # 深灰色文字
        )
        score_input_layout.add_widget(self.score_input)
        
        self.save_button = create_button(
            get_text('save'),
            size_hint_x=0.3,
            font_size=normal_font_size + 2,
            on_press=self.save_score,
            background_color=(0.615686, 0.964706, 0.615686, 1),  # 浅绿色背景
            color=(1, 1, 1, 1),  # 白色文字
            bold=True  # 加粗
        )
        score_input_layout.add_widget(self.save_button)
        main_layout.add_widget(score_input_layout)
        
        # 分数描述输入
        desc_input_height = int(input_height * 1.8)
        desc_input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=desc_input_height,
            spacing=spacing_val
        )
        desc_label = create_label(
            f'{get_text("score_desc")}:',
            size_hint_x=0.3,
            font_size=normal_font_size,
            color=(0.3, 0.3, 0.3, 1)
        )
        desc_input_layout.add_widget(desc_label)
        
        self.desc_input = create_text_input(
            multiline=False,
            hint_text=get_text('input_desc'),
            size_hint_x=0.7,
            font_size=normal_font_size,
            background_color=(1, 1, 1, 1),  # 白色背景
            foreground_color=(0.2, 0.2, 0.2, 1),  # 深灰色文字
            padding_y=[normal_font_size * 0.5, normal_font_size * 0.5]
        )
        desc_input_layout.add_widget(self.desc_input)
        main_layout.add_widget(desc_input_layout)
        
        # 分隔线
        separator = create_label('─' * 20, size_hint_y=None, height=15)
        main_layout.add_widget(separator)
        
        # 当天分数显示
        self.today_score_label = create_label(
            f'{get_text("today_score_label")}: {get_text("not_recorded")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.today_score_label)
        
        # 当天描述显示
        self.today_desc_label = create_label(
            f'{get_text("today_desc_label")}: {get_text("none")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.3, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.today_desc_label)
        
        # 总分显示
        self.total_score_label = create_label(
            f'{get_text("total_score")}: 0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.total_score_label)
        
        # 平均分显示
        self.avg_score_label = create_label(
            f'{get_text("avg_score")}: 0.0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.avg_score_label)
        
        # 按钮布局（查看历史记录和修改历史记录）
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=button_height,
            spacing=spacing_val
        )
        
        # 查看历史记录按钮
        history_button = create_button(
            get_text('view_history'),
            size_hint_x=0.5,
            font_size=normal_font_size + 2,
            on_press=lambda x: on_view_history(),
            background_color=(1.0, 0.92, 0.80, 1),  # 浅橙色背景
            color=(1, 1, 1, 1),  # 白色文字
            bold=True  # 加粗
        )
        button_layout.add_widget(history_button)
        
        # 修改历史记录按钮
        edit_button = create_button(
            get_text('edit_history'),
            size_hint_x=0.5,
            font_size=normal_font_size + 2,
            on_press=lambda x: on_edit_history(),
            background_color=(1.0, 0.92, 0.80, 1),  # 浅橙色背景
            color=(1, 1, 1, 1),  # 白色文字
            bold=True  # 加粗
        )
        button_layout.add_widget(edit_button)
        
        main_layout.add_widget(button_layout)
        
        # 更新显示
        self.update_display()
        
        # 定时更新日期（每天更新）
        Clock.schedule_interval(self.update_date, 60)  # 每分钟检查一次
    
    def update_date(self, dt):
        """更新日期显示"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_label.text = f'{get_text("date")}: {current_date}'
        self.update_display()
    
    def save_score(self, instance):
        """保存分数"""
        try:
            score_text = self.score_input.text.strip()
            desc_text = self.desc_input.text.strip()
            
            if not score_text:
                self.show_popup(get_text('tip'), get_text('enter_score'))
                return
            
            score = int(score_text)
            if score < 0 or score > 100:
                self.show_popup(get_text('tip'), get_text('score_range'))
                return
            
            # 保存数据
            today = datetime.now().strftime("%Y-%m-%d")
            self.data_manager.save_score(today, score, desc_text)
            
            # 清空输入框
            self.score_input.text = ''
            self.desc_input.text = ''
            
            # 更新显示
            self.update_display()
            
            self.show_popup(get_text('success'), get_text('score_saved'))
        except ValueError:
            self.show_popup(get_text('error'), get_text('invalid_number'))
        except Exception as e:
            self.show_popup(get_text('error'), f'{get_text("save_failed")}: {str(e)}')
    
    def update_display(self):
        """更新所有显示"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 获取今天的数据
        today_data = self.data_manager.get_score(today)
        if today_data:
            score_value = today_data["score"]
            self.today_score_label.text = f'{get_text("today_score_label")}: {score_value}'
            desc_value = today_data.get("desc", get_text("none"))
            self.today_desc_label.text = f'{get_text("today_desc_label")}: {desc_value}'
        else:
            self.today_score_label.text = f'{get_text("today_score_label")}: {get_text("not_recorded")}'
            self.today_desc_label.text = f'{get_text("today_desc_label")}: {get_text("none")}'
        
        # 计算总分和平均分
        all_scores = self.data_manager.get_all_scores()
        total = sum(data['score'] for data in all_scores.values())
        count = len(all_scores)
        avg = total / count if count > 0 else 0
        
        self.total_score_label.text = f'{get_text("total_score")}: {total}'
        self.avg_score_label.text = f'{get_text("avg_score")}: {avg:.2f}'

