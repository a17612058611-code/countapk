import json
import os
from datetime import datetime


class DataManager:
    """数据管理类，负责分数的存储和读取"""
    
    def __init__(self, data_file='scores.json'):
        """
        初始化数据管理器
        :param data_file: 数据文件路径
        """
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self):
        """加载数据文件"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_data(self):
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def save_score(self, date, score, desc=''):
        """
        保存某一天的分数
        :param date: 日期字符串，格式：YYYY-MM-DD
        :param score: 分数（整数）
        :param desc: 描述（字符串）
        """
        if date not in self.data:
            self.data[date] = {}
        
        self.data[date]['score'] = score
        if desc:
            self.data[date]['desc'] = desc
        else:
            self.data[date]['desc'] = ''
        
        self.save_data()
    
    def get_score(self, date):
        """
        获取某一天的分数
        :param date: 日期字符串，格式：YYYY-MM-DD
        :return: 包含score和desc的字典，如果不存在返回None
        """
        return self.data.get(date)
    
    def get_all_scores(self):
        """
        获取所有日期的分数
        :return: 字典，key为日期，value为包含score和desc的字典
        """
        return self.data.copy()
    
    def delete_score(self, date):
        """
        删除某一天的分数
        :param date: 日期字符串
        """
        if date in self.data:
            del self.data[date]
            self.save_data()
            return True
        return False
    
    def update_score(self, date, score, desc=''):
        """
        更新某一天的分数和描述
        :param date: 日期字符串，格式：YYYY-MM-DD
        :param score: 分数（整数）
        :param desc: 描述（字符串）
        :return: 如果日期存在返回True，否则返回False
        """
        if date in self.data:
            self.data[date]['score'] = score
            if desc:
                self.data[date]['desc'] = desc
            else:
                self.data[date]['desc'] = ''
            self.save_data()
            return True
        return False

