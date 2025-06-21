# -*- coding: utf-8 -*-
"""
@file: task_control_card.py
@time: 2024/12/21
@author: Assistant
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from qfluentwidgets import (
    CardWidget,
    PushButton,
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    TeachingTip,
    InfoBarIcon,
    TeachingTipTailPosition,
)
from utils.task import task_zero, task_money, task_fight, task_daily, task_code


class TaskControlCard(CardWidget):
    """任务控制卡片"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # 当前运行的任务
        self.current_task = None
        self.task_name = ""
        self._was_running = False  # 用于跟踪任务之前的运行状态
        
        # 初始化UI
        self.init_ui()
        
        # 定时器检查任务状态
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # 每秒检查一次

    def init_ui(self):
        self.setFixedHeight(80)
        
        # 主布局
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(16, 12, 16, 12)
        
        # 状态标签
        self.status_label = QLabel("任务状态：未运行", self)
        self.status_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        
        # 控制按钮
        self.pause_button = PushButton("暂停", self)
        self.pause_button.setIcon(FluentIcon.PAUSE)
        self.pause_button.clicked.connect(self.pause_task)
        self.pause_button.setEnabled(False)
        
        self.resume_button = PushButton("恢复", self)
        self.resume_button.setIcon(FluentIcon.PLAY)
        self.resume_button.clicked.connect(self.resume_task)
        self.resume_button.setEnabled(False)
        
        self.stop_button = PushButton("停止", self)
        self.stop_button.setIcon(FluentIcon.CLOSE)
        self.stop_button.clicked.connect(self.stop_task)
        self.stop_button.setEnabled(False)
        
        # 布局排列
        self.hBoxLayout.addWidget(self.status_label)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.pause_button)
        self.hBoxLayout.addWidget(self.resume_button)
        self.hBoxLayout.addWidget(self.stop_button)
        
    def set_current_task(self, task_name: str):
        """设置当前运行的任务"""
        self.task_name = task_name
        self._was_running = False  # 初始化状态跟踪变量
        
        # 根据任务名称获取任务对象
        task_map = {
            "zero": task_zero,
            "money": task_money,
            "fight": task_fight,
            "daily": task_daily,
            "code": task_code,
        }
        
        self.current_task = task_map.get(task_name)
        
        if self.current_task:
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.update_status()
            
    def update_status(self):
        """更新任务状态显示"""
        if not self.current_task:
            self.reset_ui_state()
            return
            
        # 检查任务状态
        is_running = getattr(self.current_task, '_running', False)
        is_pause = getattr(self.current_task, '_pause', False)
        
        # 调试信息
        print(f"DEBUG: task_name={self.task_name}, is_running={is_running}, is_pause={is_pause}")
        
        # 任务已经停止运行，重置UI状态
        if not is_running and self.task_name:
            # 检查是否是任务刚结束（之前在运行，现在停止了）
            if hasattr(self, '_was_running') and self._was_running:
                print(f"DEBUG: Task {self.task_name} has finished, resetting UI state")
                self.reset_ui_state()
                return
            else:
                # 任务准备状态（还未开始运行）
                task_display_name = self.get_task_display_name()
                self.status_label.setText(f"任务状态：{task_display_name} - 准备中")
                self.pause_button.setEnabled(True)
                self.resume_button.setEnabled(False)
                self.stop_button.setEnabled(True)
        elif is_pause:
            # 任务暂停状态
            task_display_name = self.get_task_display_name()
            self.status_label.setText(f"任务状态：{task_display_name} - 已暂停")
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        elif is_running:
            # 任务运行状态
            task_display_name = self.get_task_display_name()
            self.status_label.setText(f"任务状态：{task_display_name} - 运行中")
            self.pause_button.setEnabled(True)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            # 任务未运行状态
            self.reset_ui_state()
            
        # 记录当前运行状态，用于下次检测任务是否刚结束
        self._was_running = is_running
    
    def reset_ui_state(self):
        """重置UI状态到未运行状态"""
        self.status_label.setText("任务状态：未运行")
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.current_task = None
        self.task_name = ""
        self._was_running = False
    
    def get_task_display_name(self):
        """获取任务显示名称"""
        return {
            "zero": "零号空洞",
            "money": "拿命验收",
            "fight": "战斗任务",
            "daily": "日常任务",
            "code": "兑换码"
        }.get(self.task_name, self.task_name)
            
    def pause_task(self):
        """暂停任务"""
        if self.current_task and self.current_task._running:
            self.current_task.pause()
            self.show_info_bar("任务已暂停。也可以使用 F11 键暂停", "info")
            self.update_status()
            
    def resume_task(self):
        """恢复任务"""
        if self.current_task and self.current_task._running:
            self.current_task.restart()
            self.show_info_bar("任务已恢复。也可以使用 F10 键恢复", "success")
            self.update_status()
            
    def stop_task(self):
        """停止任务"""
        if self.current_task:
            self.current_task.stop()
            self.show_info_bar("任务已停止。也可以使用 F12 键停止", "warning")
            # 立即重置UI状态
            self.reset_ui_state()
            
    def show_info_bar(self, message: str, info_type):
        """显示信息提示"""
        if info_type == "success":
            icon = InfoBarIcon.SUCCESS
        elif info_type == "warning":
            icon = InfoBarIcon.WARNING
        else:
            icon = InfoBarIcon.INFORMATION
        
        TeachingTip.create(
            target=self.stop_button,
            icon=icon,
            title="任务控制",
            content=message,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP,
            duration=3000,
            parent=self
        )