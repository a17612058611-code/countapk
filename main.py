"""
主应用启动文件
只包含应用启动相关的代码
"""
from kivy.app import App
from data_manager import DataManager
from pages.home_page import HomePage
from pages.history_page import HistoryPage
from pages.edit_history_page import EditHistoryPage
from widgets.ui_utils import show_message_popup


class ScoreApp(App):
    """主应用类"""
    
    def build(self):
        """构建应用界面"""
        self.data_manager = DataManager()
        
        # 初始化页面管理器
        self.history_page = HistoryPage(
            self.data_manager,
            self.show_popup,
            self.show_edit_record,
            self.update_home_display
        )
        
        self.edit_history_page = EditHistoryPage(
            self.data_manager,
            self.show_popup,
            self.update_home_display,
            self.refresh_history
        )
        
        # 创建首页
        home_page = HomePage(
            self.data_manager,
            self.show_history,
            self.show_edit_history,
            self.show_popup
        )
        
        # 保存home_page引用，用于更新显示
        self.home_page = home_page
        
        return home_page
    
    def show_popup(self, title, message):
        """显示弹窗"""
        show_message_popup(title, message)
    
    def show_history(self):
        """显示历史记录"""
        self.history_page.show_history()
    
    def show_edit_history(self):
        """显示编辑历史记录界面"""
        self.edit_history_page.show_edit_record()
    
    def show_edit_record(self, date_str):
        """显示编辑指定日期的记录界面"""
        self.edit_history_page.show_edit_record(date_str)
    
    def update_home_display(self):
        """更新首页显示"""
        if hasattr(self, 'home_page'):
            self.home_page.update_display()
    
    def refresh_history(self):
        """刷新历史记录（如果打开的话）"""
        if hasattr(self.history_page, 'history_popup') and self.history_page.history_popup:
            try:
                from kivy.clock import Clock
                self.history_page.history_popup.dismiss()
                Clock.schedule_once(lambda dt: self.history_page.show_history(), 0.2)
            except:
                pass


if __name__ == '__main__':
    ScoreApp().run()
