from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.text import LabelBase
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
        'assets/fonts/SourceHanSansCN-Regular.otf',  # 思源黑体
        'assets/fonts/SourceHanSansCN-Regular.ttf',
        'assets/fonts/NotoSansCJK-Regular.ttf',       # Noto Sans CJK
        'assets/fonts/NotoSansCJK-Regular.otf',
        'assets/fonts/DroidSansFallback.ttf',        # Droid Sans Fallback
    ]
    
    # 检查打包的字体文件
    for font_path in bundled_fonts:
        if os.path.exists(font_path):
            return font_path
    
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
        # 如果找不到系统字体，返回None，稍后会尝试使用资源路径
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
        # 在Android上，如果字体在assets目录，需要使用资源路径
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        if is_android and CHINESE_FONT_PATH.startswith('assets/'):
            # Android上使用资源路径
            font_name = 'ChineseFont'
            LabelBase.register(name=font_name, fn_regular=CHINESE_FONT_PATH)
            CHINESE_FONT = font_name
            FONT_AVAILABLE = True
        else:
            # 其他平台使用文件路径
            font_name = 'ChineseFont'
            LabelBase.register(name=font_name, fn_regular=CHINESE_FONT_PATH)
            CHINESE_FONT = font_name
            FONT_AVAILABLE = True
        print(f"中文字体已注册: {CHINESE_FONT_PATH}")
    except Exception as e:
        print(f"警告: 字体注册失败: {e}")
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
    'app_title': ('每日分数记录', 'Daily Score Record'),
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
            if CHINESE_FONT:
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
        score_label = create_label(f'{get_text("today_score")}:', size_hint_x=0.25, font_size=normal_font_size - 2)
        score_input_layout.add_widget(score_label)
        self.score_input = TextInput(
            multiline=False,
            input_filter='int',
            hint_text=get_text('input_score'),
            size_hint_x=0.45,
            font_size=normal_font_size - 2
        )
        if CHINESE_FONT:
            self.score_input.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.score_input)
        self.save_button = Button(text=get_text('save'), size_hint_x=0.3, on_press=self.save_score, font_size=normal_font_size - 2)
        if CHINESE_FONT:
            self.save_button.font_name = CHINESE_FONT
        score_input_layout.add_widget(self.save_button)
        main_layout.add_widget(score_input_layout)
        
        # 分数描述输入
        desc_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=input_height, spacing=spacing_val)
        desc_label = create_label(f'{get_text("score_desc")}:', size_hint_x=0.25, font_size=normal_font_size - 2)
        desc_input_layout.add_widget(desc_label)
        self.desc_input = TextInput(
            multiline=False,
            hint_text=get_text('input_desc'),
            size_hint_x=0.75,
            font_size=normal_font_size - 2
        )
        if CHINESE_FONT:
            self.desc_input.font_name = CHINESE_FONT
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
            font_size=normal_font_size
        )
        main_layout.add_widget(self.today_score_label)
        
        # 当天描述显示
        self.today_desc_label = create_label(
            f'{get_text("today_desc_label")}: {get_text("none")}',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size - 2
        )
        main_layout.add_widget(self.today_desc_label)
        
        # 总分显示
        self.total_score_label = create_label(
            f'{get_text("total_score")}: 0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size
        )
        main_layout.add_widget(self.total_score_label)
        
        # 平均分显示
        self.avg_score_label = create_label(
            f'{get_text("avg_score")}: 0.0',
            size_hint_y=None,
            height=label_height,
            font_size=normal_font_size
        )
        main_layout.add_widget(self.avg_score_label)
        
        # 按钮布局（查看历史记录和修改历史记录）
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=button_height, spacing=spacing_val)
        
        # 查看历史记录按钮
        history_button = Button(
            text=get_text('view_history'),
            size_hint_x=0.5,
            font_size=normal_font_size,
            on_press=self.show_history
        )
        if CHINESE_FONT:
            history_button.font_name = CHINESE_FONT
        button_layout.add_widget(history_button)
        
        # 修改历史记录按钮
        edit_button = Button(
            text=get_text('edit_history'),
            size_hint_x=0.5,
            font_size=normal_font_size,
            on_press=self.show_edit_history
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
        content_label = Label(text=message)
        if CHINESE_FONT:
            content_label.font_name = CHINESE_FONT
        popup = Popup(
            title=title,
            content=content_label,
            size_hint=(0.8 if is_android else 0.6, 0.3),
            title_size=16 if is_android else 18
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
        is_android = os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ
        all_scores = self.data_manager.get_all_scores()
        
        if not all_scores:
            self.show_popup(get_text('history_title'), get_text('no_history'))
            return
        
        # 创建历史记录内容
        padding_val = 8 if is_android else 10
        spacing_val = 8 if is_android else 10
        history_layout = BoxLayout(orientation='vertical', padding=padding_val, spacing=spacing_val)
        
        # 标题
        title_label = Label(text=get_text('history_title'), size_hint_y=None, height=35 if is_android else 40, font_size=18 if is_android else 20, bold=True)
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
            record_height = 70 if is_android else 80
            record_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=record_height, padding=5)
            
            label_height = 22 if is_android else 25
            date_label = Label(text=f'{get_text("date")}: {date}', size_hint_y=None, height=label_height, font_size=14 if is_android else 16)
            if CHINESE_FONT:
                date_label.font_name = CHINESE_FONT
            record_layout.add_widget(date_label)
            
            score_label = Label(text=f'{get_text("score")}: {score}', size_hint_y=None, height=label_height, font_size=12 if is_android else 14)
            if CHINESE_FONT:
                score_label.font_name = CHINESE_FONT
            record_layout.add_widget(score_label)
            
            desc_label = Label(text=f'{get_text("desc")}: {desc}', size_hint_y=None, height=label_height, font_size=12 if is_android else 14)
            if CHINESE_FONT:
                desc_label.font_name = CHINESE_FONT
            record_layout.add_widget(desc_label)
            
            # 添加分隔线
            separator = Label(text='─' * 20, size_hint_y=None, height=4, font_size=8)
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
        edit_layout = BoxLayout(orientation='vertical', padding=padding_val, spacing=spacing_val)
        
        # 标题
        title_label = Label(text=get_text('edit_title'), size_hint_y=None, height=35 if is_android else 40, font_size=18 if is_android else 20, bold=True)
        if CHINESE_FONT:
            title_label.font_name = CHINESE_FONT
        edit_layout.add_widget(title_label)
        
        # 日期选择区域 - 年、月、日三级选择器
        date_select_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=spacing_val)
        
        # 日期标签
        date_label = Label(text=f'{get_text("select_date")}:', size_hint_y=None, height=30 if is_android else 35, font_size=14 if is_android else 16)
        if CHINESE_FONT:
            date_label.font_name = CHINESE_FONT
        date_select_layout.add_widget(date_label)
        
        # 年、月、日选择器布局
        date_picker_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45 if is_android else 50, spacing=spacing_val)
        
        # 年份选择器（当前年份前后各10年）
        current_year = datetime.now().year
        year_values = [str(i) for i in range(current_year - 10, current_year + 11)]
        year_label = Label(text=f'{get_text("year")}:', size_hint_x=0.15, font_size=14 if is_android else 16)
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
        month_label = Label(text=f'{get_text("month")}:', size_hint_x=0.15, font_size=14 if is_android else 16)
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
        day_label = Label(text=f'{get_text("day")}:', size_hint_x=0.15, font_size=14 if is_android else 16)
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
        score_edit_label = Label(text=f'{get_text("score")}:', size_hint_x=0.3, font_size=14 if is_android else 16)
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
        desc_edit_label = Label(text=f'{get_text("desc")}:', size_hint_x=0.3, font_size=14 if is_android else 16)
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

