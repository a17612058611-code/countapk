"""
配置和工具函数模块
包含字体配置、文本字典等全局配置
"""
import os
import platform
from kivy.core.text import LabelBase
from kivy.resources import resource_find, resource_add_path

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
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/NotoSansCJK-Regular.otf',
        ]
        for font_path in android_fonts:
            if os.path.exists(font_path):
                return font_path
    
    # macOS系统
    elif system == 'Darwin':
        mac_fonts = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
            '/System/Library/Fonts/Helvetica.ttc',
        ]
        for font_path in mac_fonts:
            if os.path.exists(font_path):
                return font_path
    
    # Windows系统
    elif system == 'Windows':
        windows_fonts = [
            'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
        ]
        for font_path in windows_fonts:
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
        from kivy.uix.label import Label
        from kivy.config import Config
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

def is_android():
    """检测是否在Android上运行"""
    return os.path.exists('/system/build.prop') or 'ANDROID_ARGUMENT' in os.environ

