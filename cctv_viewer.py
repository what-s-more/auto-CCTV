import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

from cctv_controller import CCTVController

class CCTVViewer:
    def __init__(self, root):
        self.root = root
        self.controller = CCTVController()
        self.root.title("CCTV 频道选择器")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # 添加此行以最大化窗口
        
        # 设置字体大小
        self.default_font = ("微软雅黑", 14)
        self.large_font = ("微软雅黑", 16, "bold")
        self.title_font = ("微软雅黑", 24, "bold")
        self.button_font = ("微软雅黑", 40, "bold")
        self.channel_font = ("微软雅黑", 14, "bold")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(self.main_frame, text="选择 CCTV 频道", font=self.title_font)
        title_label.pack(pady=(0, 20))
        
        # 创建频道按钮区域
        self.create_channel_buttons()

    def create_channel_buttons(self):
        # 创建可滚动的框架
        canvas_frame = ttk.Frame(self.main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 创建画布和滚动条
        canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建退出按钮并放置在Canvas内的右侧
        exit_btn = tk.Button(
            canvas,
            text="退出程序",
            command=self.exit_program,
            font=self.button_font,
            bg="#f44336",
            fg="white",
            relief="raised",
            bd=3,
            cursor="hand2",
            width=12, 
            height=10
        )
        # 将退出按钮放置在Canvas中，位于scrollable_frame右侧
        canvas.create_window((canvas.winfo_reqwidth(), 0), window=exit_btn, anchor="ne", tags="exit_btn")
        
        # 监听画布大小变化，确保退出按钮始终在右上角
        def on_canvas_configure(event):
            canvas.coords("exit_btn", event.width - 10, 10)
            
        canvas.bind("<Configure>", on_canvas_configure)
        
        # 加载图片并创建按钮
        img_dir = resource_path("img")
        if os.path.exists(img_dir):
            row, col = 0, 0
            # 按照频道编号排序
            image_files = sorted(os.listdir(img_dir), key=lambda x: (
                int(x.split('.')[0]) if x.split('.')[0].isdigit() else 
                int(x.split('+')[0]) if '+' in x and x.split('+')[0].isdigit() else
                999,
                x
            ))
            
            for img_file in image_files:
                if img_file.endswith(".png"):
                    img_path = os.path.join(img_dir, img_file)
                    if os.path.exists(img_path):
                        try:
                            # 加载并调整图片大小（放大到200x110）
                            img = Image.open(img_path)
                            img = img.resize((200, 110), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(img)
                            
                            # 创建按钮
                            btn = tk.Button(
                                scrollable_frame,
                                image=photo,
                                command=lambda f=img_file: self.open_channel(f),
                                bd=3,
                                relief="raised",
                                bg="#f0f0f0",
                                activebackground="#e0e0e0"
                            )
                            btn.image = photo  # 保持引用
                            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
                            
                            # 添加频道标签（放大字体）
                            channel_name = img_file.replace(".png", "").replace("+", "plus")
                            channel_label = tk.Label(
                                scrollable_frame, 
                                text=f"CCTV-{channel_name}", 
                                font=self.channel_font,
                                bg="white",
                                fg="black"
                            )
                            channel_label.grid(row=row+1, column=col, padx=5, pady=(0, 15), sticky="n")
                            
                            # 配置网格权重实现弹性布局
                            scrollable_frame.columnconfigure(col, weight=1)
                            
                            col += 1
                            if col > 4:  # 每行5个按钮
                                col = 0
                                row += 2
                        except Exception as e:
                            print(f"无法加载图片 {img_file}: {e}")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def open_channel(self, img_file):
        self.controller.open_channel(img_file)

    def close_browser(self):
        self.controller.close_browser()

    def exit_program(self):
        self.controller.close_browser()  # 先关闭浏览器
        self.controller.exit_program()   # 再退出程序
        self.root.quit()

    def open_channel(self, img_file):
        self.controller.open_channel(img_file)

    def close_browser(self):
        self.controller.close_browser()

    def exit_program(self):
        self.controller.exit_program()
        self.root.quit()

def main():
    root = tk.Tk()
    # 设置全局字体
    root.option_add("*Font", "微软雅黑 14")
    app = CCTVViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()