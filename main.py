from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.text import LabelBase
from datetime import datetime
import json
import os
import platform
from data_manager import DataManager

# 配置中文字体
def get_chinese_font():
    """获取系统支持中文的字体文件路径"""
    system = platform.system()
    if system == 'Darwin':  # macOS
        # macOS 系统字体文件路径（按优先级排序）
        font_paths = [
            '/System/Library/Fonts/STHeiti Medium.ttc',  # 黑体-简
            '/System/Library/Fonts/STHeiti Light.ttc',   # 黑体-简（细体）
            '/System/Library/Fonts/PingFang.ttc',         # 苹方（如果存在）
        ]
        # 检查字体文件是否存在
        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path
    elif system == 'Windows':
        # Windows 系统字体路径
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
            'C:/Windows/Fonts/simhei.ttf',    # 黑体
            'C:/Windows/Fonts/simsun.ttc',    # 宋体
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path
    # Linux/Android 或其他系统，返回None使用默认字体
    return None

# 获取中文字体路径
CHINESE_FONT = get_chinese_font()

# 如果找到字体文件，注册字体
if CHINESE_FONT:
    try:
        LabelBase.register(name='ChineseFont', fn_regular=CHINESE_FONT)
        CHINESE_FONT = 'ChineseFont'  # 使用注册的名称
    except Exception as e:
        print(f"警告: 字体注册失败: {e}")
        CHINESE_FONT = None
else:
    CHINESE_FONT = None


class ScoreApp(App):
    def build(self):
        self.data_manager = DataManager()
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 辅助函数：创建带中文字体的Label
        def create_label(text, **kwargs):
            label = Label(text=text, **kwargs)
            if CHINESE_FONT:
                label.font_name = CHINESE_FONT
            return label
        
        # 标题
        title = create_label(
            '每日分数记录',
            size_hint_y=None,
            height=60,
            font_size=24,
            bold=True
        )
        main_layout.add_widget(title)
        
        # 日期显示
        self.date_label = create_label(
            f'日期: {datetime.now().strftime("%Y-%m-%d")}',
            size_hint_y=None,
            height=40,
            font_size=18
        )
        main_layout.add_widget(self.date_label)
        
        # 当天分数输入区域
        score_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        score_label = create_label('今天分数:', size_hint_x=0.3, font_size=16)
        score_input_layout.add_widget(score_label)
        self.score_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text='输入分数(0-100)',
            size_hint_x=0.4
        )
        if CHINESE_FONT:
            self.score_input.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.score_input)
        self.save_button = Button(text='保存', size_hint_x=0.3, on_press=self.save_score)
        if CHINESE_FONT:
            self.save_button.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.save_button)
        main_layout.add_widget(score_input_layout)
        
        # 分数描述输入
        desc_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        desc_label = create_label('分数描述:', size_hint_x=0.3, font_size=16)
        desc_input_layout.add_widget(desc_label)
        self.desc_input = TextInput(
            multiline=False,
            hint_text='输入描述',
            size_hint_x=0.7
        )
        if CHINESE_FONT:
            self.desc_input.font_name = CHINESE_FONT
        desc_input_layout.add_widget(self.desc_input)
        main_layout.add_widget(desc_input_layout)
        
        # 分隔线
        separator = create_label('─' * 30, size_hint_y=None, height=20)
        main_layout.add_widget(separator)
        
        # 当天分数显示
        self.today_score_label = create_label(
            '今天分数: 未记录',
            size_hint_y=None,
            height=40,
            font_size=18
        )
        main_layout.add_widget(self.today_score_label)
        
        # 当天描述显示
        self.today_desc_label = create_label(
            '今天描述: 无',
            size_hint_y=None,
            height=40,
            font_size=16
        )
        main_layout.add_widget(self.today_desc_label)
        
        # 总分显示
        self.total_score_label = create_label(
            '总分: 0',
            size_hint_y=None,
            height=40,
            font_size=18
        )
        main_layout.add_widget(self.total_score_label)
        
        # 平均分显示
        self.avg_score_label = create_label(
            '平均分: 0.0',
            size_hint_y=None,
            height=40,
            font_size=18
        )
        main_layout.add_widget(self.avg_score_label)
        
        # 查看历史记录按钮
        history_button = Button(
            text='查看历史记录',
            size_hint_y=None,
            height=50,
            on_press=self.show_history
        )
        if CHINESE_FONT:
            history_button.font_name = CHINESE_FONT
        main_layout.add_widget(history_button)
        
        # 更新显示
        self.update_display()
        
        # 定时更新日期（每天更新）
        Clock.schedule_interval(self.update_date, 60)  # 每分钟检查一次
        
        return main_layout
    
    def update_date(self, dt):
        """更新日期显示"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_label.text = f'日期: {current_date}'
        self.update_display()
    
    def save_score(self, instance):
        """保存分数"""
        try:
            score_text = self.score_input.text.strip()
            desc_text = self.desc_input.text.strip()
            
            if not score_text:
                self.show_popup('提示', '请输入分数')
                return
            
            score = int(score_text)
            if score < 0 or score > 100:
                self.show_popup('提示', '分数范围应在0-100之间')
                return
            
            # 保存数据
            today = datetime.now().strftime("%Y-%m-%d")
            self.data_manager.save_score(today, score, desc_text)
            
            # 清空输入框
            self.score_input.text = ''
            self.desc_input.text = ''
            
            # 更新显示
            self.update_display()
            
            self.show_popup('成功', '分数已保存')
        except ValueError:
            self.show_popup('错误', '请输入有效的数字')
        except Exception as e:
            self.show_popup('错误', f'保存失败: {str(e)}')
    
    def update_display(self):
        """更新所有显示"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 获取今天的数据
        today_data = self.data_manager.get_score(today)
        if today_data:
            self.today_score_label.text = f'今天分数: {today_data["score"]}'
            self.today_desc_label.text = f'今天描述: {today_data.get("desc", "无")}'
        else:
            self.today_score_label.text = '今天分数: 未记录'
            self.today_desc_label.text = '今天描述: 无'
        
        # 计算总分和平均分
        all_scores = self.data_manager.get_all_scores()
        total = sum(data['score'] for data in all_scores.values())
        count = len(all_scores)
        avg = total / count if count > 0 else 0
        
        self.total_score_label.text = f'总分: {total}'
        self.avg_score_label.text = f'平均分: {avg:.2f}'
    
    def show_popup(self, title, message):
        """显示弹窗"""
        content_label = Label(text=message)
        if CHINESE_FONT:
            content_label.font_name = CHINESE_FONT
        popup = Popup(
            title=title,
            content=content_label,
            size_hint=(0.6, 0.3),
            title_size=18
        )
        # Popup的title_font属性在某些版本可能不支持，使用title_font_name
        if CHINESE_FONT:
            try:
                popup.title_font_name = CHINESE_FONT
            except:
                pass
        popup.open()


    
    def show_history(self, instance):
        """显示历史记录"""
        all_scores = self.data_manager.get_all_scores()
        
        if not all_scores:
            self.show_popup('历史记录', '暂无历史记录')
            return
        
        # 创建历史记录内容
        history_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(text='历史记录', size_hint_y=None, height=40, font_size=20, bold=True)
        if CHINESE_FONT:
            title_label.font_name = CHINESE_FONT
        history_layout.add_widget(title_label)
        
        # 创建滚动视图
        scroll = ScrollView(size_hint=(1, 1))
        scroll_content = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))
        
        # 按日期排序（最新的在前）
        sorted_dates = sorted(all_scores.keys(), reverse=True)
        
        for date in sorted_dates:
            score_data = all_scores[date]
            score = score_data.get('score', 0)
            desc = score_data.get('desc', '无')
            
            # 创建单条记录布局
            record_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80, padding=5)
            
            date_label = Label(text=f'日期: {date}', size_hint_y=None, height=25, font_size=16)
            if CHINESE_FONT:
                date_label.font_name = CHINESE_FONT
            record_layout.add_widget(date_label)
            
            score_label = Label(text=f'分数: {score}', size_hint_y=None, height=25, font_size=14)
            if CHINESE_FONT:
                score_label.font_name = CHINESE_FONT
            record_layout.add_widget(score_label)
            
            desc_label = Label(text=f'描述: {desc}', size_hint_y=None, height=25, font_size=14)
            if CHINESE_FONT:
                desc_label.font_name = CHINESE_FONT
            record_layout.add_widget(desc_label)
            
            # 添加分隔线
            separator = Label(text='─' * 30, size_hint_y=None, height=5, font_size=10)
            if CHINESE_FONT:
                separator.font_name = CHINESE_FONT
            scroll_content.add_widget(record_layout)
            scroll_content.add_widget(separator)
        
        scroll.add_widget(scroll_content)
        history_layout.add_widget(scroll)
        
        # 关闭按钮
        close_button = Button(text='关闭', size_hint_y=None, height=40)
        if CHINESE_FONT:
            close_button.font_name = CHINESE_FONT
        close_button.bind(on_press=lambda x: history_popup.dismiss())
        history_layout.add_widget(close_button)
        
        # 创建弹窗
        history_popup = Popup(
            title='历史记录',
            content=history_layout,
            size_hint=(0.8, 0.8),
            title_size=20
        )
        if CHINESE_FONT:
            try:
                history_popup.title_font_name = CHINESE_FONT
            except:
                pass
        history_popup.open()
    
if __name__ == '__main__':
    ScoreApp().run()

