import time
import cv2
import numpy as np
from mss import mss
import os
import threading
import logging
import msvcrt  # 导入msvcrt库用于基本键盘输入捕获
import sys

# 确保中文显示正常
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Windows系统下msvcrt库可用
KEYBOARD_LIB_AVAILABLE = True

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 屏幕录制类
class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.output_folder = "recordings"
        self.keyboard_events = []
        self.recording_start_time = 0
        self.keyboard_thread = None
        self.stop_keyboard_thread = False
        self.keyboard_listener = None
        # 特殊按键映射
        self.special_keys = {
            b'\r': '[回车]',
            b'\t': '[Tab]',
            b' ': '[空格]'
        }
        # 确保输出文件夹存在
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            logging.info(f"创建输出文件夹: {self.output_folder}")
    
    def start_recording(self):
        # 创建文件名，使用当前时间戳
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_folder, f"screen_recording_{timestamp}.mp4")
        keyboard_log_file = os.path.join(self.output_folder, f"keyboard_log_{timestamp}.txt")
        
        # 设置录制参数
        fps = 15.0  # 帧率
        
        # 记录开始时间
        self.recording_start_time = time.time()
        self.keyboard_events = []  # 清空键盘事件列表
        self.stop_keyboard_thread = False
        logging.info(f"开始录制，视频文件: {output_file}")
        logging.info(f"键盘日志文件: {keyboard_log_file}")
        
        # 创建一个简单的键盘记录文件，写入初始信息
        try:
            with open(keyboard_log_file, 'w', encoding='utf-8') as f:
                f.write("键盘输入记录\n")
                f.write(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
            logging.info(f"已创建初始键盘日志文件")
        except Exception as e:
            logging.error(f"创建键盘日志文件失败: {str(e)}")
        
        # 启动键盘记录线程
        if KEYBOARD_LIB_AVAILABLE:
            self.keyboard_thread = threading.Thread(target=self.record_keyboard)
            self.keyboard_thread.daemon = False  # 确保线程不会在主线程结束时被强制终止
            self.keyboard_thread.start()
            logging.info("键盘记录线程已启动")
        
        # 使用mss捕获屏幕
        with mss() as sct:
            # 获取主显示器的分辨率
            monitor = sct.monitors[1]  # 主显示器
            
            # 定义编码器和创建VideoWriter对象
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_file, fourcc, fps, 
                                 (monitor["width"], monitor["height"]))
            
            print(f"开始录制屏幕...")
            print(f"录制文件将保存到: {output_file}")
            print(f"键盘输入将记录到: {keyboard_log_file}")
            print("按 'q' 键停止录制")
            print(f"键盘输入捕获模式: {'实际按键捕获' if KEYBOARD_LIB_AVAILABLE else '系统状态记录'}")
            print("请尝试按下一些按键进行测试...")
            
            self.recording = True
            last_time = time.time()
            
            # 如果不使用keyboard库，则使用每秒记录系统状态的方式
            last_status_time = last_time if not KEYBOARD_LIB_AVAILABLE else 0
            status_counter = 0
            
            try:
                while self.recording:
                    # 捕获屏幕
                    img = sct.grab(monitor)
                    
                    # 转换为OpenCV格式
                    frame = np.array(img)
                    # 转换颜色空间 BGR -> RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    
                    # 写入视频文件
                    out.write(frame)
                    
                    # 如果不使用keyboard库，则每秒记录一次系统状态
                    if not KEYBOARD_LIB_AVAILABLE:
                        current_time = time.time()
                        if current_time - last_status_time >= 1.0:
                            status_counter += 1
                            relative_time = current_time - self.recording_start_time
                            status_event = f"[{relative_time:.3f}s] 系统状态更新 #{status_counter}"
                            self.keyboard_events.append(status_event)
                            logging.info(f"记录系统状态: {status_event}")
                            last_status_time = current_time
                    
                    # 控制帧率
                    current_time = time.time()
                    elapsed = current_time - last_time
                    if elapsed < 1.0 / fps:
                        time.sleep(1.0 / fps - elapsed)
                    last_time = current_time
                    
                    # 如果不使用keyboard库（现在使用pynput），检查录制状态
                    # pynput的按键检测在on_press回调中处理
                    
            except KeyboardInterrupt:
                logging.warning("检测到键盘中断")
            finally:
                # 停止键盘记录线程
                self.recording = False
                self.stop_keyboard_thread = True
                if KEYBOARD_LIB_AVAILABLE and self.keyboard_thread:
                    logging.info("等待键盘记录线程结束")
                    self.keyboard_thread.join(timeout=2.0)  # 等待键盘线程结束，最多等待2秒
                
                # 清理资源
                out.release()
                # cv2.destroyAllWindows()
                
                # 保存键盘输入记录
                logging.info(f"尝试保存键盘事件，共 {len(self.keyboard_events)} 个事件")
                self.save_keyboard_events(keyboard_log_file)
                
                print("\n录制已停止")
                print(f"视频文件已保存: {output_file}")
                print(f"键盘输入记录已保存: {keyboard_log_file}")
                print(f"记录的事件数量: {len(self.keyboard_events)}")
    
    def record_keyboard(self):
        """使用msvcrt库记录键盘输入的线程函数"""
        logging.info("键盘记录线程开始运行")
        
        try:
            while not self.stop_keyboard_thread:
                # 检查是否有按键按下
                if msvcrt.kbhit():
                    # 读取按键
                    key = msvcrt.getch()
                    
                    # 计算相对时间
                    relative_time = time.time() - self.recording_start_time
                    
                    # 处理特殊情况：如果是扩展键（如方向键等），需要再读取一个字节
                    if key == b'\x00' or key == b'\xe0':
                        # 读取第二个字节
                        key += msvcrt.getch()
                        
                        # 简单处理一些常见的扩展键
                        if key == b'\xe0H':
                            key_name = '[↑]'
                        elif key == b'\xe0P':
                            key_name = '[↓]'
                        elif key == b'\xe0K':
                            key_name = '[←]'
                        elif key == b'\xe0M':
                            key_name = '[→]'
                        elif key == b'\x00;':
                            key_name = '[F1]'
                        elif key == b'\x00<':
                            key_name = '[F2]'
                        elif key == b'\x00=':
                            key_name = '[F3]'
                        else:
                            key_name = f'[特殊键:{key.hex()}]'
                    # 处理常规字符键和一些特殊字符
                    else:
                        # 检查是否是特殊字符
                        if key in self.special_keys:
                            key_name = self.special_keys[key]
                        # Esc键
                        elif key == b'\x1b':
                            key_name = '[ESC]'
                        # Backspace键
                        elif key == b'\x08':
                            key_name = '[退格]'
                        # Delete键
                        elif key == b'\x7f':
                            key_name = '[Delete]'
                        # 普通字符
                        else:
                            try:
                                key_name = key.decode('utf-8', errors='replace')
                            except:
                                key_name = f'[字符:{key.hex()}]'
                    
                    # 创建事件记录
                    event = f"[{relative_time:.3f}s] 按下: {key_name}"
                    self.keyboard_events.append(event)
                    logging.info(f"记录按键: {key_name}")
                    print(f"捕获到按键: {key_name}")
                    
                    # 检查是否按下q键停止录制
                    if key_name.lower() == 'q':
                        logging.info("检测到 'q' 键，准备停止录制")
                        self.recording = False
                        self.stop_keyboard_thread = True
                        break
                
                # 短暂休眠以减少CPU使用率
                time.sleep(0.01)
                
        except Exception as e:
            logging.error(f"键盘记录线程发生错误: {str(e)}")
            print(f"警告: 键盘记录功能遇到问题 - {str(e)}")
        finally:
            logging.info("键盘记录线程结束")
    
    # msvcrt不支持按键释放事件，只记录按键按下事件
    
    def save_keyboard_events(self, file_path):
        """保存键盘事件到文件"""
        try:
            logging.info(f"正在保存键盘事件到: {file_path}")
            # 追加模式打开文件
            with open(file_path, 'a', encoding='utf-8') as f:
                for event in self.keyboard_events:
                    f.write(event + "\n")
                
                f.write("-" * 50 + "\n")
                f.write(f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总事件数: {len(self.keyboard_events)}")
            logging.info(f"键盘事件保存成功，文件大小: {os.path.getsize(file_path)} 字节")
        except Exception as e:
            logging.error(f"保存键盘事件失败: {str(e)}")
            print(f"错误: 无法保存键盘事件记录 - {str(e)}")
    
    def record(self):
        logging.info("开始屏幕录制")
        try:
            # 开始录制
            self.start_recording()
        except Exception as e:
            logging.error(f"录制过程中发生错误: {str(e)}")
            print(f"错误: {str(e)}")
        finally:
            logging.info("录制完成，所有资源已清理")

# 使用说明
if __name__ == "__main__":
    print("屏幕录制工具")
    print("功能: 录制屏幕并记录实际键盘输入")
    print(f"键盘输入捕获状态: {'可用 (使用msvcrt)' if KEYBOARD_LIB_AVAILABLE else '不可用'}")
    print("注意：请确保已安装必要的依赖包")
    print("安装命令: pip install mss opencv-python numpy")
    print("\n")
    
    recorder = ScreenRecorder()
    recorder.record()