# -*- coding: utf-8 -*-
""" 
@file:      main_window.py
@time:      2024/8/11 下午1:21
@author:    sMythicalBird
"""

from qfluentwidgets import MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon
from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from .config_interface import ConfigInterface
from .fight_edit_interface import FightEditInterface
from .code_interface import CodeInterface
from .api.check_update import check_update
from pathlib import Path
from PySide6.QtGui import QIcon

app_icon = Path(__file__).parent.parent / "resources/img/gui/app.jpg"


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        # 初始化窗口ui
        self.init_ui()
        # 初始化窗口导航
        self.init_navigation()
        # # 检查更新
        # check_update()
    
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 停止所有正在运行的任务
        from utils.task import task_zero, task_money, task_fight, task_daily, task_code
        from start_task import task_control_card
        
        tasks = [task_zero, task_money, task_fight, task_daily, task_code]
        for task in tasks:
            if hasattr(task, '_running') and task._running:
                task.stop()
        
        # 重置任务控制卡片状态
        if task_control_card:
            task_control_card.reset_ui_state()
        
        # 接受关闭事件
        event.accept()
        super().closeEvent(event)

    def init_ui(self):
        self.setWindowIcon(QIcon(str(app_icon)))
        self.setWindowTitle("Fairy Auto")
        self.resize(960, 640)

    def init_navigation(self):
        # 添加主页导航页
        self.addSubInterface(HomeInterface(), FluentIcon.HOME, self.tr("主页"))

        # 添加战斗编辑页面
        self.addSubInterface(FightEditInterface(), FluentIcon.EDIT, self.tr("战斗设计"))

        self.addSubInterface(CodeInterface(), FluentIcon.CODE, self.tr("兑换码"))

        # 添加配置页面
        self.addSubInterface(
            ConfigInterface(),
            FluentIcon.SAVE,
            self.tr("配置"),
            position=NavigationItemPosition.BOTTOM,
        )

        # 添加设置页面
        self.addSubInterface(
            SettingInterface(),
            FluentIcon.SETTING,
            self.tr("设置"),
            position=NavigationItemPosition.BOTTOM,
        )
