import time
import cv2
import numpy as np
from mss import mss
from pynput import keyboard
import os

# 屏幕录制类
class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.output_folder = "recordings"
        # 确保输出文件夹存在
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def start_recording(self):
        # 创建文件名，使用当前时间戳
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_folder, f"screen_recording_{timestamp}.mp4")
        
        # 设置录制参数
        fps = 15.0  # 帧率
        
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
            print("按 'q' 键停止录制")
            
            self.recording = True
            last_time = time.time()
            
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
                    
                    # 显示录制状态（可选）
                    # cv2.imshow("Screen Recording", frame)
                    
                    # 检查是否按下q键停止
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     break
                    
                    # 控制帧率
                    current_time = time.time()
                    elapsed = current_time - last_time
                    if elapsed < 1.0 / fps:
                        time.sleep(1.0 / fps - elapsed)
                    last_time = current_time
            
            except KeyboardInterrupt:
                pass
            finally:
                # 清理资源
                self.recording = False
                out.release()
                # cv2.destroyAllWindows()
                print("\n录制已停止")
                print(f"视频文件已保存: {output_file}")
    
    def on_press(self, key):
        try:
            # 按q键停止录制
            if key.char == 'q':
                self.recording = False
                return False  # 停止监听器
        except AttributeError:
            pass
    
    def record(self):
        # 启动键盘监听器
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        
        # 开始录制
        self.start_recording()
        
        # 等待监听器结束
        listener.join()

# 使用说明
if __name__ == "__main__":
    print("屏幕录制工具")
    print("注意：请确保已安装必要的依赖包")
    print("安装命令: pip install mss opencv-python pynput numpy")
    print("\n")
    
    recorder = ScreenRecorder()
    recorder.record()