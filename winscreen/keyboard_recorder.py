import msvcrt
import time
import datetime
import threading
import os

# 确保中文显示正常
os.environ['PYTHONIOENCODING'] = 'utf-8'

class KeyboardRecorder:
    def __init__(self):
        self.recording = False
        self.stop_event = threading.Event()
        self.events = []
        self.start_time = None
        self.log_file = None
        
        # 特殊按键映射
        self.special_keys = {
            b'\r': '[回车]',
            b'\t': '[Tab]',
            b' ': '[空格]',
            b'\x1b': '[ESC]',
            b'\x08': '[退格]',
            b'\x7f': '[Delete]',
        }
        
        # 扩展键映射
        self.extended_keys = {
            b'H': '[↑]',
            b'P': '[↓]',
            b'K': '[←]',
            b'M': '[→]',
            b';': '[F1]',
            b'<': '[F2]',
            b'=': '[F3]',
            b'>': '[F4]',
            b'?': '[F5]',
            b'@': '[F6]',
            b'A': '[F7]',
            b'B': '[F8]',
            b'C': '[F9]',
            b'D': '[F10]',
        }
    
    def start_recording(self):
        """开始录制键盘输入"""
        # 生成日志文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"keyboard_recording_{timestamp}.txt"
        
        # 准备录制
        self.recording = True
        self.stop_event.clear()
        self.events = []
        self.start_time = time.time()
        
        print(f"键盘记录已开始")
        print(f"日志将保存到: {self.log_file}")
        print("按 'q' 键停止录制")
        print("按任意键进行测试...")
        
        # 创建初始日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"键盘输入记录\n")
            f.write(f"开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n")
        
        # 开始记录键盘输入
        self._record_keys()
    
    def _record_keys(self):
        """记录键盘输入的主循环"""
        try:
            while self.recording:
                # 检查是否有按键按下
                if msvcrt.kbhit():
                    # 读取按键
                    key = msvcrt.getch()
                    
                    # 计算相对时间
                    relative_time = time.time() - self.start_time
                    
                    # 处理扩展键
                    if key == b'\x00' or key == b'\xe0':
                        # 读取第二个字节
                        second_byte = msvcrt.getch()
                        key_name = self.extended_keys.get(second_byte, f'[特殊键:{second_byte.hex()}]')
                    else:
                        # 处理常规字符
                        if key in self.special_keys:
                            key_name = self.special_keys[key]
                        else:
                            try:
                                key_name = key.decode('utf-8', errors='replace')
                            except:
                                key_name = f'[字符:{key.hex()}]'
                    
                    # 创建事件记录
                    event_text = f"[{relative_time:.3f}s] 按下: {key_name}"
                    self.events.append(event_text)
                    
                    # 打印并保存事件
                    print(f"捕获按键: {key_name}")
                    self._save_event(event_text)
                    
                    # 检查是否按下q键停止
                    if key_name.lower() == 'q':
                        print("检测到q键，停止录制")
                        self.stop_recording()
                        break
                
                # 短暂休眠以减少CPU使用率
                time.sleep(0.01)
        
        except Exception as e:
            print(f"发生错误: {str(e)}")
            self.stop_recording()
    
    def _save_event(self, event_text):
        """保存单个事件到日志文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(event_text + "\n")
        except Exception as e:
            print(f"保存事件失败: {str(e)}")
    
    def stop_recording(self):
        """停止录制"""
        if self.recording:
            self.recording = True
            self.stop_event.set()
            
            # 保存总结信息
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write("-" * 50 + "\n")
                    f.write(f"结束时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"总录制时间: {(time.time() - self.start_time):.2f}秒\n")
                    f.write(f"记录的按键数量: {len(self.events)}\n")
            except Exception as e:
                print(f"保存总结信息失败: {str(e)}")
            
            print(f"\n键盘记录已停止")
            print(f"日志已保存到: {self.log_file}")
            print(f"记录的按键数量: {len(self.events)}")

def main():
    print("=== 键盘记录工具 ===")
    print("功能: 捕获并记录键盘输入")
    print("使用方法:")
    print("1. 开始后，按任意键进行测试")
    print("2. 按 'q' 键停止录制")
    print("3. 日志将保存在当前目录")
    print("-" * 50)
    
    recorder = KeyboardRecorder()
    
    try:
        recorder.start_recording()
    except KeyboardInterrupt:
        print("\n检测到Ctrl+C，停止录制")
        recorder.stop_recording()

if __name__ == "__main__":
    main()