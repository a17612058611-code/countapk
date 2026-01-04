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
    
    # 检测是否在Android上运行
    is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
    
    if is_android:
        # Android系统：使用系统默认中文字体（DroidSansFallback或NotoSansCJK）
        # Android系统字体通常位于/system/fonts/，但Kivy会自动使用系统字体
        # 返回None让Kivy使用系统默认字体，它应该支持中文
        return None
    elif system == 'Darwin':  # macOS
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
    # Linux 或其他系统
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
    # Android或未找到字体：使用Kivy默认字体（Android系统字体应该支持中文）
    # 在Android上，不设置font_name让系统使用默认字体
    CHINESE_FONT = None

# 配置Kivy默认字体（Android上使用系统字体）
try:
    # 尝试设置默认字体，如果失败则使用系统默认
    if CHINESE_FONT:
        Config.set('kivy', 'default_font', [CHINESE_FONT])
except:
    pass


class ScoreApp(App):
    def build(self):
        self.data_manager = DataManager()
        
        # 检测是否在Android上运行
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        
        # 根据平台调整布局参数
        if is_android:
            # Android: 较小的padding和spacing，适合小屏幕
            padding_val = 10
            spacing_val = 8
            title_font_size = 20
            normal_font_size = 14
            label_height = 35
            input_height = 45
            button_height = 45
        else:
            # 桌面: 较大的padding和spacing
            padding_val = 20
            spacing_val = 15
            title_font_size = 24
            normal_font_size = 18
            label_height = 40
            input_height = 50
            button_height = 50
        
        # 主布局容器（使用ScrollView包装以支持滚动）
        root = BoxLayout(orientation='vertical')
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=padding_val, spacing=spacing_val, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # 创建ScrollView以支持滚动
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(main_layout)
        root.add_widget(scroll)
        
        # 辅助函数：创建带中文字体的Label
        def create_label(text, **kwargs):
            label = Label(text=text, **kwargs)
            # 在Android上，不设置font_name让系统使用默认中文字体
            # 在桌面系统上，如果找到了字体文件则使用
            if CHINESE_FONT and not is_android:
                label.font_name = CHINESE_FONT
            return label
        
        # 标题
        title = create_label(
            '每日分数记录',
            size_hint_y=None,
            height=label_height * 1.5,
            font_size=title_font_size,
            bold=True
        )
        main_layout.add_widget(title)
        
        # 日期显示
        self.date_label = create_label(
            f'日期: {datetime.now().strftime("%Y-%m-%d")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size
        )
        main_layout.add_widget(self.date_label)
        
        # 当天分数输入区域
        score_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=input_height, spacing=spacing_val)
        score_label = create_label('今天分数:', size_hint_x=0.25, font_size=normal_font_size - 2)
        score_input_layout.add_widget(score_label)
        self.score_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text='输入分数(0-100)',
            size_hint_x=0.45,
            font_size=normal_font_size - 2
        )
        if CHINESE_FONT and not is_android:
            self.score_input.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.score_input)
        self.save_button = Button(text='保存', size_hint_x=0.3, on_press=self.save_score, font_size=normal_font_size - 2)
        if CHINESE_FONT and not is_android:
            self.save_button.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.save_button)
        main_layout.add_widget(score_input_layout)
        
        # 分数描述输入
        desc_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=input_height, spacing=spacing_val)
        desc_label = create_label('分数描述:', size_hint_x=0.25, font_size=normal_font_size - 2)
        desc_input_layout.add_widget(desc_label)
        self.desc_input = TextInput(
            multiline=False,
            hint_text='输入描述',
            size_hint_x=0.75,
            font_size=normal_font_size - 2
        )
        if CHINESE_FONT and not is_android:
            self.desc_input.font_name = CHINESE_FONT
        desc_input_layout.add_widget(self.desc_input)
        main_layout.add_widget(desc_input_layout)
        
        # 分隔线
        separator = create_label('─' * 20, size_hint_y=None, height=15)
        main_layout.add_widget(separator)
        
        # 当天分数显示
        self.today_score_label = create_label(
            '今天分数: 未记录',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size
        )
        main_layout.add_widget(self.today_score_label)
        
        # 当天描述显示
        self.today_desc_label = create_label(
            '今天描述: 无',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size - 2
        )
        main_layout.add_widget(self.today_desc_label)
        
        # 总分显示
        self.total_score_label = create_label(
            '总分: 0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size
        )
        main_layout.add_widget(self.total_score_label)
        
        # 平均分显示
        self.avg_score_label = create_label(
            '平均分: 0.0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size
        )
        main_layout.add_widget(self.avg_score_label)
        
        # 查看历史记录按钮
        history_button = Button(
            text='查看历史记录',
            size_hint_y=None,
            height=button_height,
            font_size=normal_font_size,
            on_press=self.show_history
        )
        if CHINESE_FONT and not is_android:
            history_button.font_name = CHINESE_FONT
        main_layout.add_widget(history_button)
        
        # 更新显示
        self.update_display()
        
        # 定时更新日期（每天更新）
        Clock.schedule_interval(self.update_date, 60)  # 每分钟检查一次
        
        return root
    
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
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        content_label = Label(text=message)
        if CHINESE_FONT and not is_android:
            content_label.font_name = CHINESE_FONT
        popup = Popup(
            title=title,
            content=content_label,
            size_hint=(0.8 if is_android else 0.6, 0.3),
            title_size=16 if is_android else 18
        )
        # Popup的title_font属性在某些版本可能不支持，使用title_font_name
        if CHINESE_FONT and not is_android:
            try:
                popup.title_font_name = CHINESE_FONT
            except:
                pass
        popup.open()


    
    def show_history(self, instance):
        """显示历史记录"""
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        all_scores = self.data_manager.get_all_scores()
        
        if not all_scores:
            self.show_popup('历史记录', '暂无历史记录')
            return
        
        # 创建历史记录内容
        padding_val = 8 if is_android else 10
        spacing_val = 8 if is_android else 10
        history_layout = BoxLayout(orientation='vertical', padding=padding_val, spacing=spacing_val)
        
        # 标题
        title_label = Label(text='历史记录', size_hint_y=None, height=35 if is_android else 40, font_size=18 if is_android else 20, bold=True)
        if CHINESE_FONT and not is_android:
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
            record_height = 70 if is_android else 80
            record_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=record_height, padding=5)
            
            label_height = 22 if is_android else 25
            date_label = Label(text=f'日期: {date}', size_hint_y=None, height=label_height, font_size=14 if is_android else 16)
            if CHINESE_FONT and not is_android:
                date_label.font_name = CHINESE_FONT
            record_layout.add_widget(date_label)
            
            score_label = Label(text=f'分数: {score}', size_hint_y=None, height=label_height, font_size=12 if is_android else 14)
            if CHINESE_FONT and not is_android:
                score_label.font_name = CHINESE_FONT
            record_layout.add_widget(score_label)
            
            desc_label = Label(text=f'描述: {desc}', size_hint_y=None, height=label_height, font_size=12 if is_android else 14)
            if CHINESE_FONT and not is_android:
                desc_label.font_name = CHINESE_FONT
            record_layout.add_widget(desc_label)
            
            # 添加分隔线
            separator = Label(text='─' * 20, size_hint_y=None, height=4, font_size=8)
            if CHINESE_FONT and not is_android:
                separator.font_name = CHINESE_FONT
            scroll_content.add_widget(record_layout)
            scroll_content.add_widget(separator)
        
        scroll.add_widget(scroll_content)
        history_layout.add_widget(scroll)
        
        # 关闭按钮
        close_button = Button(text='关闭', size_hint_y=None, height=40 if is_android else 45, font_size=14 if is_android else 16)
        if CHINESE_FONT and not is_android:
            close_button.font_name = CHINESE_FONT
        close_button.bind(on_press=lambda x: history_popup.dismiss())
        history_layout.add_widget(close_button)
        
        # 创建弹窗
        history_popup = Popup(
            title='历史记录',
            content=history_layout,
            size_hint=(0.95 if is_android else 0.8, 0.9 if is_android else 0.8),
            title_size=18 if is_android else 20
        )
        if CHINESE_FONT and not is_android:
            try:
                history_popup.title_font_name = CHINESE_FONT
            except:
                pass
        history_popup.open()
    
if __name__ == '__main__':
    ScoreApp().run()

