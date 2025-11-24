import keyboard
import time
import os

# 键盘输入测试脚本 - 使用keyboard库
print("键盘输入测试脚本 (使用keyboard库)")
print("此脚本用于测试keyboard库是否能正常捕获键盘输入")
print("按任意键进行测试，按ESC键退出")
print("-" * 50)

key_events = []
start_time = time.time()
log_file = "test_keyboard_log.txt"

# 定义按键处理函数
def on_press(event):
    relative_time = time.time() - start_time
    key_name = event.name
    
    # 特殊按键处理
    if key_name == 'space':
        key_name = '[空格]'
    elif key_name == 'enter':
        key_name = '[回车]'
    elif key_name == 'backspace':
        key_name = '[退格]'
    elif key_name == 'tab':
        key_name = '[Tab]'
    elif key_name == 'shift':
        key_name = '[Shift]'
    elif key_name == 'ctrl':
        key_name = '[Ctrl]'
    elif key_name == 'alt':
        key_name = '[Alt]'
    elif key_name == 'esc':
        key_name = '[ESC]'
    
    event_text = f"[{relative_time:.3f}s] 按下: {key_name}"
    key_events.append(event_text)
    print(event_text)

# 注册按键钩子
keyboard.on_press(on_press)
print("已注册按键钩子")

# 记录开始时间
start_time = time.time()
timeout = 10  # 10秒超时

try:
    print(f"开始监听键盘输入，{timeout}秒后自动退出或按ESC键立即退出...")
    
    # 等待ESC键或超时
    while time.time() - start_time < timeout:
        if keyboard.is_pressed('esc'):
            print("检测到ESC键，退出测试")
            break
        time.sleep(0.1)
    
    if time.time() - start_time >= timeout:
        print(f"已超时 {timeout} 秒，自动退出")
        
except KeyboardInterrupt:
    print("\n检测到键盘中断，退出测试")
except Exception as e:
    print(f"发生错误: {str(e)}")
finally:
    # 清理钩子
    keyboard.unhook_all()
    print("已清理所有键盘钩子")
    
    # 保存事件到文件
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("键盘输入测试记录 (keyboard库)")
            f.write(f"\n开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            f.write("\n" + "-" * 50)
            
            for event in key_events:
                f.write("\n" + event)
            
            f.write("\n" + "-" * 50)
            f.write(f"\n结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            f.write(f"\n总事件数: {len(key_events)}")
        
        print(f"\n测试完成！")
        print(f"共记录 {len(key_events)} 个键盘事件")
        print(f"日志文件已保存到: {os.path.abspath(log_file)}")
    except Exception as e:
        print(f"保存日志失败: {str(e)}")
    
    print("测试结束")