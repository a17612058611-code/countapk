from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.resources import resource_find, resource_add_path
from datetime import datetime
import json
import os
import platform
import calendar
from data_manager import DataManager

# 配置中文字体
def get_chinese_font():
    """获取系统支持中文的字体文件路径"""
    system = platform.system()
    
    # 检测是否在Android上运行
    is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
    
    # 优先使用打包的字体文件（适用于Android和所有平台）
    bundled_fonts = [
        'assets/fonts/SourceHanSansSC-Regular.otf',  # 思源黑体（简体中文）
        'assets/fonts/SourceHanSansSC-Normal.otf',   # 思源黑体 Normal
        'assets/fonts/SourceHanSansCN-Regular.otf',  # 思源黑体（兼容旧名称）
        'assets/fonts/SourceHanSansCN-Regular.ttf',
        'assets/fonts/NotoSansCJK-Regular.ttf',       # Noto Sans CJK
        'assets/fonts/NotoSansCJK-Regular.otf',
        'assets/fonts/DroidSansFallback.ttf',        # Droid Sans Fallback
    ]
    
    # 检查打包的字体文件
    for font_path in bundled_fonts:
        # 先尝试直接文件路径
        if os.path.exists(font_path):
            return font_path
        # 在Android上，尝试使用resource_find查找资源
        if is_android:
            try:
                resource_font = resource_find(font_path)
                if resource_font:
                    return resource_font
            except:
                pass
    
    # Android系统：尝试使用系统字体路径
    if is_android:
        android_fonts = [
            '/system/fonts/NotoSansCJK-Regular.ttf',
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/Roboto-Regular.ttf',  # 作为fallback
        ]
        for font_path in android_fonts:
            if os.path.exists(font_path):
                return font_path
        # 如果找不到系统字体，返回None
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
CHINESE_FONT_PATH = get_chinese_font()

# 注册字体
CHINESE_FONT = None
FONT_AVAILABLE = False
if CHINESE_FONT_PATH:
    try:
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        
        # 在Android上，如果字体路径是assets/开头，尝试添加资源路径
        if is_android and CHINESE_FONT_PATH.startswith('assets/'):
            try:
                # 尝试添加assets目录到资源路径
                if os.path.exists('assets'):
                    resource_add_path('assets')
            except:
                pass
            
            # 尝试使用resource_find查找资源
            try:
                resource_font = resource_find(CHINESE_FONT_PATH)
                if resource_font:
                    CHINESE_FONT_PATH = resource_font
            except:
                pass
        
        # 注册字体
        font_name = 'ChineseFont'
        LabelBase.register(name=font_name, fn_regular=CHINESE_FONT_PATH)
        CHINESE_FONT = font_name
        FONT_AVAILABLE = True
        print(f"中文字体已注册: {CHINESE_FONT_PATH}")
    except Exception as e:
        print(f"警告: 字体注册失败: {e}")
        import traceback
        traceback.print_exc()
        CHINESE_FONT = None
        FONT_AVAILABLE = False

# 测试字体是否支持中文
if CHINESE_FONT:
    try:
        # 尝试创建一个测试Label来验证字体
        test_label = Label(text='测试', font_name=CHINESE_FONT)
        # 如果字体不支持中文，文本可能会显示为方块或乱码
        # 这里我们假设如果字体注册成功，就认为支持中文
        FONT_AVAILABLE = True
        Config.set('kivy', 'default_font', [CHINESE_FONT])
        print(f"Kivy默认字体已设置为: {CHINESE_FONT}")
    except Exception as e:
        print(f"警告: 设置默认字体失败: {e}")
        FONT_AVAILABLE = False

# 文本字典：中英文对照
TEXTS = {
    'app_title': ('拾光ZM', 'Shi Guang ZM'),
    'date': ('日期', 'Date'),
    'today_score': ('今天分数', 'Today Score'),
    'score_desc': ('分数描述', 'Score Description'),
    'input_score': ('输入分数(0-100)', 'Enter Score (0-100)'),
    'input_desc': ('输入描述', 'Enter Description'),
    'save': ('保存', 'Save'),
    'today_score_label': ('今天分数', 'Today Score'),
    'today_desc_label': ('今天描述', 'Today Description'),
    'total_score': ('总分', 'Total Score'),
    'avg_score': ('平均分', 'Average Score'),
    'not_recorded': ('未记录', 'Not Recorded'),
    'none': ('无', 'None'),
    'view_history': ('查看历史记录', 'View History'),
    'edit_history': ('修改历史记录', 'Edit History'),
    'history_title': ('历史记录', 'History'),
    'no_history': ('暂无历史记录', 'No History'),
    'edit_title': ('修改历史记录', 'Edit History'),
    'select_date': ('选择日期', 'Select Date'),
    'year': ('年', 'Year'),
    'month': ('月', 'Month'),
    'day': ('日', 'Day'),
    'score': ('分数', 'Score'),
    'desc': ('描述', 'Description'),
    'save_edit': ('保存修改', 'Save Changes'),
    'close': ('关闭', 'Close'),
    'success': ('成功', 'Success'),
    'error': ('错误', 'Error'),
    'tip': ('提示', 'Tip'),
    'score_saved': ('分数已保存', 'Score Saved'),
    'record_updated': ('的记录已更新', "'s record updated"),
    'record_created': ('的记录已创建', "'s record created"),
    'enter_score': ('请输入分数', 'Please Enter Score'),
    'score_range': ('分数范围应在0-100之间', 'Score must be between 0-100'),
    'invalid_number': ('请输入有效的数字', 'Please Enter Valid Number'),
    'save_failed': ('保存失败', 'Save Failed'),
    'update_failed': ('更新失败', 'Update Failed'),
    'select_complete_date': ('请选择完整的日期（年、月、日）', 'Please Select Complete Date (Year, Month, Day)'),
    'invalid_date': ('日期格式无效', 'Invalid Date Format'),
    'no_history_to_edit': ('暂无历史记录可修改', 'No History to Edit'),
    'edit': ('编辑', 'Edit'),
    'delete': ('删除', 'Delete'),
    'delete_confirm': ('确定要删除这条记录吗？', 'Are you sure you want to delete this record?'),
    'record_deleted': ('记录已删除', 'Record Deleted'),
    'delete_failed': ('删除失败', 'Delete Failed'),
    'confirm': ('确定', 'Confirm'),
}

def get_text(key):
    """获取文本（根据字体支持情况返回中文或英文）"""
    if key in TEXTS:
        return TEXTS[key][0] if FONT_AVAILABLE else TEXTS[key][1]
    return key


class ScoreApp(App):
    def build(self):
        self.data_manager = DataManager()
        
        # 检测是否在Android上运行
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        
        # 根据平台调整布局参数（增大字体和按钮尺寸，参考Widgetable应用）
        if is_android:
            # Android: 增大字体和按钮，参考Widgetable应用
            padding_val = 20
            spacing_val = 15
            title_font_size = 32  # 增大标题字体
            normal_font_size = 22  # 增大普通字体
            label_height = 50
            input_height = 70  # 增大输入框高度
            button_height = 70  # 增大按钮高度
        else:
            # 桌面: 更大的字体和间距
            padding_val = 30
            spacing_val = 20
            title_font_size = 36
            normal_font_size = 24
            label_height = 50
            input_height = 70
            button_height = 70
        
        # 主布局容器（使用ScrollView包装以支持滚动）
        root = BoxLayout(orientation='vertical')
        
        # 设置浅蓝色背景
        with root.canvas.before:
            Color(0.85, 0.92, 1.0, 1)  # 浅蓝色 (RGB: 217, 235, 255)
            root.rect = Rectangle(size=root.size, pos=root.pos)
        
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        root.bind(pos=update_rect, size=update_rect)
        
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
            if CHINESE_FONT:
                label.font_name = CHINESE_FONT
            return label
        
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
        
        # 日期显示（增大字体）
        self.date_label = create_label(
            f'{get_text("date")}: {datetime.now().strftime("%Y-%m-%d")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.3, 0.3, 0.3, 1)  # 深灰色文字
        )
        main_layout.add_widget(self.date_label)
        
        # 当天分数输入区域（增大字体和按钮）
        score_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=input_height, spacing=spacing_val)
        score_label = create_label(f'{get_text("today_score")}:', size_hint_x=0.3, font_size=normal_font_size, color=(0.3, 0.3, 0.3, 1))
        score_input_layout.add_widget(score_label)
        self.score_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text=get_text('input_score'),
            size_hint_x=0.4,
            font_size=normal_font_size,
            background_color=(1, 1, 1, 1),  # 白色背景
            foreground_color=(0.2, 0.2, 0.2, 1)  # 深灰色文字
        )
        if CHINESE_FONT:
            self.score_input.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.score_input)
        self.save_button = Button(
            text=get_text('save'), 
            size_hint_x=0.3, 
            on_press=self.save_score, 
            font_size=normal_font_size + 2,  # 增大字体
            background_color=(0.615686, 0.964706, 0.615686, 1),  # 浅绿色背景 #9df69d
            color=(1, 1, 1, 1),  # 白色文字
            bold=True  # 加粗
        )
        if CHINESE_FONT:
            self.save_button.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.save_button)
        main_layout.add_widget(score_input_layout)
        
        # 分数描述输入（增大字体，高度约2行字体）
        desc_input_height = int(input_height * 1.8)  # 大约2行字体的高度（基于input_height的1.8倍）
        desc_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=desc_input_height, spacing=spacing_val)
        desc_label = create_label(f'{get_text("score_desc")}:', size_hint_x=0.3, font_size=normal_font_size, color=(0.3, 0.3, 0.3, 1))
        desc_input_layout.add_widget(desc_label)
        self.desc_input = TextInput(
            multiline=False,
            hint_text=get_text('input_desc'),
            size_hint_x=0.7,
            font_size=normal_font_size,
            background_color=(1, 1, 1, 1),  # 白色背景
            foreground_color=(0.2, 0.2, 0.2, 1),  # 深灰色文字
            padding_y=[normal_font_size * 0.5, normal_font_size * 0.5]  # 增加上下内边距
        )
        if CHINESE_FONT:
            self.desc_input.font_name = CHINESE_FONT
        desc_input_layout.add_widget(self.desc_input)
        main_layout.add_widget(desc_input_layout)
        
        # 分隔线
        separator = create_label('─' * 20, size_hint_y=None, height=15)
        main_layout.add_widget(separator)
        
        # 当天分数显示（增大字体）
        self.today_score_label = create_label(
            f'{get_text("today_score_label")}: {get_text("not_recorded")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.today_score_label)
        
        # 当天描述显示（增大字体）
        self.today_desc_label = create_label(
            f'{get_text("today_desc_label")}: {get_text("none")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.3, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.today_desc_label)
        
        # 总分显示（增大字体）
        self.total_score_label = create_label(
            f'{get_text("total_score")}: 0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.total_score_label)
        
        # 平均分显示（增大字体）
        self.avg_score_label = create_label(
            f'{get_text("avg_score")}: 0.0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.avg_score_label)
        
        # 按钮布局（查看历史记录和修改历史记录）
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=button_height, spacing=spacing_val)
        
        # 查看历史记录按钮（增大字体和按钮）
        history_button = Button(
            text=get_text('view_history'),
            size_hint_x=0.5,
            font_size=normal_font_size + 2,  # 稍微增大字体
            on_press=self.show_history,
            background_color=(1.0, 0.92, 0.80, 1),  # 浅橙色背景
            color=(1, 1, 1, 1),  # 白色文字
            bold=True  # 加粗
        )
        if CHINESE_FONT:
            history_button.font_name = CHINESE_FONT
        button_layout.add_widget(history_button)
        
        # 修改历史记录按钮（增大字体和按钮）
        edit_button = Button(
            text=get_text('edit_history'),
            size_hint_x=0.5,
            font_size=normal_font_size + 2,  # 稍微增大字体
            on_press=self.show_edit_history,
            background_color=(1.0, 0.92, 0.80, 1),  # 浅橙色背景
            color=(1, 1, 1, 1),  # 白色文字
            bold=True  # 加粗
        )
        if CHINESE_FONT:
            edit_button.font_name = CHINESE_FONT
        button_layout.add_widget(edit_button)
        
        main_layout.add_widget(button_layout)
        
        # 更新显示
        self.update_display()
        
        # 定时更新日期（每天更新）
        Clock.schedule_interval(self.update_date, 60)  # 每分钟检查一次
        
        return root
    
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
    
    def show_popup(self, title, message):
        """显示弹窗"""
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        
        # 创建内容布局
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 消息标签
        content_label = Label(text=message, size_hint_y=1)
        if CHINESE_FONT:
            content_label.font_name = CHINESE_FONT
        content_layout.add_widget(content_label)
        
        # 创建弹窗
        popup = Popup(
            title=title,
            content=content_layout,
            size_hint=(0.8 if is_android else 0.6, 0.35 if is_android else 0.3),
            title_size=16 if is_android else 18
        )
        # Popup的title_font属性在某些版本可能不支持，使用title_font_name
        if CHINESE_FONT:
            try:
                popup.title_font_name = CHINESE_FONT
            except:
                pass
        
        # 关闭按钮
        close_button = Button(text=get_text('close'), size_hint_y=None, height=40 if is_android else 45, font_size=14 if is_android else 16)
        if CHINESE_FONT:
            close_button.font_name = CHINESE_FONT
        close_button.bind(on_press=lambda x: popup.dismiss())
        content_layout.add_widget(close_button)
        
        popup.open()


    
    def show_history(self, instance):
        """显示历史记录"""
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        all_scores = self.data_manager.get_all_scores()
        
        if not all_scores:
            self.show_popup(get_text('history_title'), get_text('no_history'))
            return
        
        # 创建历史记录内容
        padding_val = 8 if is_android else 10
        spacing_val = 8 if is_android else 10
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
        title_label = Label(text=get_text('history_title'), size_hint_y=None, height=35 if is_android else 40, font_size=18 if is_android else 20, bold=True, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
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
            desc = score_data.get('desc', get_text('none'))
            
            # 创建单条记录布局
            record_height = 100 if is_android else 110  # 增加高度以容纳按钮
            record_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=record_height, padding=5)
            
            # 信息区域
            info_layout = BoxLayout(orientation='vertical', size_hint_y=1)
            label_height = 22 if is_android else 25
            date_label = Label(text=f'{get_text("date")}: {date}', size_hint_y=None, height=label_height, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
            if CHINESE_FONT:
                date_label.font_name = CHINESE_FONT
            info_layout.add_widget(date_label)
            
            score_label = Label(text=f'{get_text("score")}: {score}', size_hint_y=None, height=label_height, font_size=12 if is_android else 14, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
            if CHINESE_FONT:
                score_label.font_name = CHINESE_FONT
            info_layout.add_widget(score_label)
            
            desc_label = Label(text=f'{get_text("desc")}: {desc}', size_hint_y=None, height=label_height, font_size=12 if is_android else 14, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
            if CHINESE_FONT:
                desc_label.font_name = CHINESE_FONT
            info_layout.add_widget(desc_label)
            record_layout.add_widget(info_layout)
            
            # 按钮区域
            button_height = 35 if is_android else 40
            button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=button_height, spacing=5)
            
            # 编辑按钮
            edit_btn = Button(
                text=get_text('edit'),
                size_hint_x=0.5,
                font_size=12 if is_android else 14,
                background_color=(0.4, 0.7, 1.0, 1),  # 浅蓝色
                color=(1, 1, 1, 1)  # 白色文字
            )
            if CHINESE_FONT:
                edit_btn.font_name = CHINESE_FONT
            edit_btn.bind(on_press=lambda x, d=date: self.edit_record_from_history(d, history_popup))
            button_layout.add_widget(edit_btn)
            
            # 删除按钮
            delete_btn = Button(
                text=get_text('delete'),
                size_hint_x=0.5,
                font_size=12 if is_android else 14,
                background_color=(1.0, 0.5, 0.5, 1),  # 浅红色
                color=(1, 1, 1, 1)  # 白色文字
            )
            if CHINESE_FONT:
                delete_btn.font_name = CHINESE_FONT
            delete_btn.bind(on_press=lambda x, d=date: self.delete_record_from_history(d, history_popup))
            button_layout.add_widget(delete_btn)
            
            record_layout.add_widget(button_layout)
            
            # 添加分隔线
            separator = Label(text='─' * 20, size_hint_y=None, height=4, font_size=8, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
            if CHINESE_FONT:
                separator.font_name = CHINESE_FONT
            scroll_content.add_widget(record_layout)
            scroll_content.add_widget(separator)
        
        scroll.add_widget(scroll_content)
        history_layout.add_widget(scroll)
        
        # 关闭按钮
        close_button = Button(text=get_text('close'), size_hint_y=None, height=40 if is_android else 45, font_size=14 if is_android else 16)
        if CHINESE_FONT:
            close_button.font_name = CHINESE_FONT
        close_button.bind(on_press=lambda x: history_popup.dismiss())
        history_layout.add_widget(close_button)
        
        # 创建弹窗
        history_popup = Popup(
            title=get_text('history_title'),
            content=history_layout,
            size_hint=(0.95 if is_android else 0.8, 0.9 if is_android else 0.8),
            title_size=18 if is_android else 20
        )
        if CHINESE_FONT:
            try:
                history_popup.title_font_name = CHINESE_FONT
            except:
                pass
        history_popup.open()
    
    def delete_record_from_history(self, date, history_popup):
        """从历史记录中删除一条记录"""
        # 显示确认对话框
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        confirm_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        confirm_label = Label(text=get_text('delete_confirm'), size_hint_y=1)
        if CHINESE_FONT:
            confirm_label.font_name = CHINESE_FONT
        confirm_layout.add_widget(confirm_label)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        
        # 确认按钮
        yes_button = Button(text=get_text('confirm'), size_hint_x=0.5)
        if CHINESE_FONT:
            yes_button.font_name = CHINESE_FONT
        button_layout.add_widget(yes_button)
        
        # 取消按钮
        no_button = Button(text=get_text('close'), size_hint_x=0.5)
        if CHINESE_FONT:
            no_button.font_name = CHINESE_FONT
        button_layout.add_widget(no_button)
        
        confirm_layout.add_widget(button_layout)
        
        confirm_popup = Popup(
            title=get_text('tip'),
            content=confirm_layout,
            size_hint=(0.7 if is_android else 0.5, 0.3 if is_android else 0.25),
            title_size=16 if is_android else 18
        )
        if CHINESE_FONT:
            try:
                confirm_popup.title_font_name = CHINESE_FONT
            except:
                pass
        
        def confirm_delete(instance):
            try:
                if self.data_manager.delete_score(date):
                    # 删除成功
                    confirm_popup.dismiss()
                    history_popup.dismiss()
                    self.update_display()  # 更新主界面显示
                    self.show_popup(get_text('success'), get_text('record_deleted'))
                    # 重新打开历史记录
                    Clock.schedule_once(lambda dt: self.show_history(None), 0.1)
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
    
    def edit_record_from_history(self, date, history_popup):
        """从历史记录中编辑一条记录"""
        # 关闭历史记录弹窗
        history_popup.dismiss()
        # 打开编辑界面，并设置日期
        self.show_edit_record(date)
    
    def show_edit_record(self, date_str):
        """显示编辑指定日期的记录界面"""
        # 解析日期
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
        
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        
        # 创建修改历史记录界面
        padding_val = 8 if is_android else 10
        spacing_val = 8 if is_android else 10
        edit_layout = BoxLayout(orientation='vertical', padding=[padding_val, padding_val - 3, padding_val, padding_val], spacing=spacing_val)  # 顶部padding减少3像素，让标题上移
        
        # 标题
        
        # 设置浅黄色背景
        with edit_layout.canvas.before:
            Color(1.0, 0.98, 0.90, 1)  # 浅黄色 (RGB: 255, 250, 230)
            edit_layout.rect = Rectangle(size=edit_layout.size, pos=edit_layout.pos)
        
        def update_edit_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        edit_layout.bind(pos=update_edit_rect, size=update_edit_rect)
        
        title_label = Label(text=get_text('edit_title'), size_hint_y=None, height=40 if is_android else 45, font_size=22 if is_android else 24, bold=True, color=(0.2, 0.2, 0.2, 1))  # 黑色文字，字号更大
        if CHINESE_FONT:
            title_label.font_name = CHINESE_FONT
        edit_layout.add_widget(title_label)
        
        # 日期选择区域 - 年、月、日三级选择器
        date_select_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=spacing_val)
        
        # 日期标签
        date_label = Label(text=f'{get_text("select_date")}:', size_hint_y=None, height=30 if is_android else 35, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            date_label.font_name = CHINESE_FONT
        date_select_layout.add_widget(date_label)
        
        # 年、月、日选择器布局
        date_picker_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        
        # 年份选择器
        year_values = [str(i) for i in range(year - 10, year + 11)]
        year_label = Label(text=f'{get_text("year")}:', size_hint_x=0.15, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            year_label.font_name = CHINESE_FONT
        date_picker_layout.add_widget(year_label)
        
        self.year_spinner = Spinner(
            text=str(year),
            values=year_values,
            size_hint_x=0.28,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.year_spinner.font_name = CHINESE_FONT
        self.year_spinner.bind(text=self.update_day_spinner)
        date_picker_layout.add_widget(self.year_spinner)
        
        # 月份选择器
        month_values = [str(i) for i in range(1, 13)]
        month_label = Label(text=f'{get_text("month")}:', size_hint_x=0.15, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            month_label.font_name = CHINESE_FONT
        date_picker_layout.add_widget(month_label)
        
        self.month_spinner = Spinner(
            text=str(month),
            values=month_values,
            size_hint_x=0.28,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.month_spinner.font_name = CHINESE_FONT
        self.month_spinner.bind(text=self.update_day_spinner)
        date_picker_layout.add_widget(self.month_spinner)
        
        # 日期选择器
        day_label = Label(text=f'{get_text("day")}:', size_hint_x=0.15, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            day_label.font_name = CHINESE_FONT
        date_picker_layout.add_widget(day_label)
        
        days = self.get_days_in_month(year, month)
        day_values = [str(i) for i in range(1, days + 1)]
        self.day_spinner = Spinner(
            text=str(min(day, days)),
            values=day_values,
            size_hint_x=0.28,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.day_spinner.font_name = CHINESE_FONT
        self.day_spinner.bind(text=self.on_date_components_selected)
        date_picker_layout.add_widget(self.day_spinner)
        
        date_select_layout.add_widget(date_picker_layout)
        edit_layout.add_widget(date_select_layout)
        
        # 分数输入区域
        score_edit_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        score_edit_label = Label(text=f'{get_text("score")}:', size_hint_x=0.3, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            score_edit_label.font_name = CHINESE_FONT
        score_edit_layout.add_widget(score_edit_label)
        
        self.edit_score_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text=get_text('input_score'),
            size_hint_x=0.7,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.edit_score_input.font_name = CHINESE_FONT
        score_edit_layout.add_widget(self.edit_score_input)
        edit_layout.add_widget(score_edit_layout)
        
        # 描述输入区域
        desc_edit_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        desc_edit_label = Label(text=f'{get_text("desc")}:', size_hint_x=0.3, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            desc_edit_label.font_name = CHINESE_FONT
        desc_edit_layout.add_widget(desc_edit_label)
        
        self.edit_desc_input = TextInput(
            multiline=False,
            hint_text=get_text('input_desc'),
            size_hint_x=0.7,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.edit_desc_input.font_name = CHINESE_FONT
        desc_edit_layout.add_widget(self.edit_desc_input)
        edit_layout.add_widget(desc_edit_layout)
        
        # 按钮区域
        button_edit_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        
        # 保存修改按钮
        save_edit_button = Button(
            text=get_text('save_edit'),
            size_hint_x=0.5,
            font_size=14 if is_android else 16,
            on_press=self.save_edit
        )
        if CHINESE_FONT:
            save_edit_button.font_name = CHINESE_FONT
        button_edit_layout.add_widget(save_edit_button)
        
        # 关闭按钮
        close_edit_button = Button(
            text=get_text('close'),
            size_hint_x=0.5,
            font_size=14 if is_android else 16,
            on_press=lambda x: self.edit_popup.dismiss()
        )
        if CHINESE_FONT:
            close_edit_button.font_name = CHINESE_FONT
        button_edit_layout.add_widget(close_edit_button)
        
        edit_layout.add_widget(button_edit_layout)
        
        # 创建弹窗
        self.edit_popup = Popup(
            title=get_text('edit_title'),
            content=edit_layout,
            size_hint=(0.95 if is_android else 0.7, 0.65 if is_android else 0.55),
            title_size=18 if is_android else 20
        )
        if CHINESE_FONT:
            try:
                self.edit_popup.title_font_name = CHINESE_FONT
            except:
                pass
        
        # 加载该日期的数据
        Clock.schedule_once(lambda dt: self.on_date_components_selected(), 0.1)
        
        self.edit_popup.open()
    
    def get_days_in_month(self, year, month):
        """获取指定年月的天数"""
        return calendar.monthrange(int(year), int(month))[1]
    
    def update_day_spinner(self, *args):
        """当年或月改变时，更新日期选择器的天数"""
        if hasattr(self, 'year_spinner') and hasattr(self, 'month_spinner') and hasattr(self, 'day_spinner'):
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
        if hasattr(self, 'year_spinner') and hasattr(self, 'month_spinner') and hasattr(self, 'day_spinner'):
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
    
    def show_edit_history(self, instance):
        """显示修改历史记录界面"""
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        
        # 创建修改历史记录界面
        padding_val = 8 if is_android else 10
        spacing_val = 8 if is_android else 10
        edit_layout = BoxLayout(orientation='vertical', padding=[padding_val, padding_val - 3, padding_val, padding_val], spacing=spacing_val)  # 顶部padding减少3像素，让标题上移
        
        # 设置浅黄色背景
        with edit_layout.canvas.before:
            Color(1.0, 0.98, 0.90, 1)  # 浅黄色 (RGB: 255, 250, 230)
            edit_layout.rect = Rectangle(size=edit_layout.size, pos=edit_layout.pos)
        
        def update_edit_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        edit_layout.bind(pos=update_edit_rect, size=update_edit_rect)
        
        # 标题
        title_label = Label(text=get_text('edit_title'), size_hint_y=None, height=40 if is_android else 45, font_size=22 if is_android else 24, bold=True, color=(0.2, 0.2, 0.2, 1))  # 黑色文字，字号更大
        if CHINESE_FONT:
            title_label.font_name = CHINESE_FONT
        edit_layout.add_widget(title_label)
        
        # 日期选择区域 - 年、月、日三级选择器
        date_select_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=spacing_val)
        
        # 日期标签
        date_label = Label(text=f'{get_text("select_date")}:', size_hint_y=None, height=30 if is_android else 35, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
        if CHINESE_FONT:
            date_label.font_name = CHINESE_FONT
        date_select_layout.add_widget(date_label)
        
        # 年、月、日选择器布局
        date_picker_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        
        # 年份选择器（当前年份前后各10年）
        current_year = datetime.now().year
        year_values = [str(i) for i in range(current_year - 10, current_year + 11)]
        year_label = Label(text=f'{get_text("year")}:', size_hint_x=0.15, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
        if CHINESE_FONT:
            year_label.font_name = CHINESE_FONT
        date_picker_layout.add_widget(year_label)
        
        self.year_spinner = Spinner(
            text=str(current_year),
            values=year_values,
            size_hint_x=0.28,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.year_spinner.font_name = CHINESE_FONT
        self.year_spinner.bind(text=self.update_day_spinner)
        date_picker_layout.add_widget(self.year_spinner)
        
        # 月份选择器
        month_values = [str(i) for i in range(1, 13)]
        month_label = Label(text=f'{get_text("month")}:', size_hint_x=0.15, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
        if CHINESE_FONT:
            month_label.font_name = CHINESE_FONT
        date_picker_layout.add_widget(month_label)
        
        current_month = datetime.now().month
        self.month_spinner = Spinner(
            text=str(current_month),
            values=month_values,
            size_hint_x=0.28,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.month_spinner.font_name = CHINESE_FONT
        self.month_spinner.bind(text=self.update_day_spinner)
        date_picker_layout.add_widget(self.month_spinner)
        
        # 日期选择器
        day_label = Label(text=f'{get_text("day")}:', size_hint_x=0.15, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
        if CHINESE_FONT:
            day_label.font_name = CHINESE_FONT
        date_picker_layout.add_widget(day_label)
        
        current_day = datetime.now().day
        days = self.get_days_in_month(current_year, current_month)
        day_values = [str(i) for i in range(1, days + 1)]
        self.day_spinner = Spinner(
            text=str(min(current_day, days)),
            values=day_values,
            size_hint_x=0.28,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.day_spinner.font_name = CHINESE_FONT
        self.day_spinner.bind(text=self.on_date_components_selected)
        date_picker_layout.add_widget(self.day_spinner)
        
        date_select_layout.add_widget(date_picker_layout)
        edit_layout.add_widget(date_select_layout)
        
        # 分数输入区域
        score_edit_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        score_edit_label = Label(text=f'{get_text("score")}:', size_hint_x=0.3, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字
        if CHINESE_FONT:
            score_edit_label.font_name = CHINESE_FONT
        score_edit_layout.add_widget(score_edit_label)
        
        self.edit_score_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text=get_text('input_score'),
            size_hint_x=0.7,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.edit_score_input.font_name = CHINESE_FONT
        score_edit_layout.add_widget(self.edit_score_input)
        edit_layout.add_widget(score_edit_layout)
        
        # 描述输入区域
        desc_edit_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        desc_edit_label = Label(text=f'{get_text("desc")}:', size_hint_x=0.3, font_size=14 if is_android else 16, color=(0.2, 0.2, 0.2, 1))  # 黑色文字)
        if CHINESE_FONT:
            desc_edit_label.font_name = CHINESE_FONT
        desc_edit_layout.add_widget(desc_edit_label)
        
        self.edit_desc_input = TextInput(
            multiline=False,
            hint_text=get_text('input_desc'),
            size_hint_x=0.7,
            font_size=14 if is_android else 16
        )
        if CHINESE_FONT:
            self.edit_desc_input.font_name = CHINESE_FONT
        desc_edit_layout.add_widget(self.edit_desc_input)
        edit_layout.add_widget(desc_edit_layout)
        
        # 按钮区域
        button_edit_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        
        # 保存修改按钮
        save_edit_button = Button(
            text=get_text('save_edit'),
            size_hint_x=0.5,
            font_size=14 if is_android else 16,
            on_press=self.save_edit
        )
        if CHINESE_FONT:
            save_edit_button.font_name = CHINESE_FONT
        button_edit_layout.add_widget(save_edit_button)
        
        # 关闭按钮
        close_edit_button = Button(
            text=get_text('close'),
            size_hint_x=0.5,
            font_size=14 if is_android else 16,
            on_press=lambda x: self.edit_popup.dismiss()
        )
        if CHINESE_FONT:
            close_edit_button.font_name = CHINESE_FONT
        button_edit_layout.add_widget(close_edit_button)
        
        edit_layout.add_widget(button_edit_layout)
        
        # 创建弹窗
        self.edit_popup = Popup(
            title=get_text('edit_title'),
            content=edit_layout,
            size_hint=(0.95 if is_android else 0.7, 0.65 if is_android else 0.55),
            title_size=18 if is_android else 20
        )
        if CHINESE_FONT:
            try:
                self.edit_popup.title_font_name = CHINESE_FONT
            except:
                pass
        
        # 初始化当前日期的数据
        self.on_date_components_selected()
        
        self.edit_popup.open()
    
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
            self.update_display()
            self.edit_popup.dismiss()
            
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
    
if __name__ == '__main__':
    ScoreApp().run()

