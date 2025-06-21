# -*- coding: utf-8 -*-
""" 
@file:      start_task.py
@time:      2024/8/30 上午3:22
@author:    sMythicalBird
"""
from threading import Thread
from pynput.keyboard import Key, Listener

from utils.task import task_zero, task_money, task_code, task_fight, task_daily

# 全局任务控制组件引用
task_control_card = None

def set_task_control_card(card):
    """设置任务控制卡片引用"""
    global task_control_card
    task_control_card = card

# 测试更新情况


def key_event(task):
    def on_press(key):
        if key == Key.f12:
            task.stop()
            return False
        if key == Key.f11:
            task.pause()
        if key == Key.f10:
            task.restart()
        # 检查任务是否已停止，如果停止则退出监听
        if not getattr(task, '_running', True):
            return False
        return None

    try:
        with Listener(on_press=on_press) as listener:
            # 定期检查任务状态，如果任务停止则退出监听
            while getattr(task, '_running', True):
                listener.join(timeout=1)  # 每秒检查一次
                if not listener.running:
                    break
    except Exception as e:
        print(f"键盘监听器异常: {e}")


# 任务——零号空洞
def zero_task():
    global task_control_card
    
    # 设置任务状态
    if task_control_card:
        task_control_card.set_current_task("zero")
    
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_zero,))
    key_thread.start()

    # 导入任务
    import event_handling.zero
    import event_handling.fight.fight_zero

    # 任务开始
    task_zero.run()


# 任务-拿命验收
def money_task():
    global task_control_card
    
    # 设置任务状态
    if task_control_card:
        task_control_card.set_current_task("money")
    
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_money,))
    key_thread.start()

    # 导入任务
    import event_handling.money

    # 任务开始
    task_money.run()


def fight_task():
    global task_control_card
    
    # 设置任务状态
    if task_control_card:
        task_control_card.set_current_task("fight")
    
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_fight,))
    key_thread.start()

    # 导入任务
    import event_handling.fight.fight_only

    # 任务开始
    task_fight.run()


# 任务——兑换码
def redemption_code():
    global task_control_card
    
    # 设置任务状态
    if task_control_card:
        task_control_card.set_current_task("code")
    
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_code,))
    key_thread.start()

    # 导入任务
    import event_handling.code

    # 任务开始
    task_code.run()

# 自动化日常任务
def daily():
    global task_control_card
    
    # 设置任务状态
    if task_control_card:
        task_control_card.set_current_task("daily")
    
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_daily,))
    key_thread.start()

    # 导入任务
    import event_handling.daily

    # 任务开始
    task_daily.run()


def new_account():
    # 监听运行状态
    key_thread = Thread(target=key_event, args=(task_daily,))
    key_thread.start()

    # 导入任务
    import event_handling.test

    # 任务开始
    task_daily.run()




def start_task(action):
    if action == "zero":
        print("start zero task")
        Thread(target=zero_task).start()
    elif action == "money":
        print("start money task")
        Thread(target=money_task).start()
    elif action == "fight":
        print("start fight task")
        Thread(target=fight_task).start()
    elif action == "daily":
        print("start daily task")
        Thread(target=daily).start()


if __name__ == '__main__':
    start_task('daily')
    # new_account()