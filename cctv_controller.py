import os
import sys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver import EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ================== 配置区域 ==================
def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 根据是否打包环境设置edge driver路径
if getattr(sys, 'frozen', False):
    # 如果是打包环境
    edge_driver_path = resource_path("edgedriver_win64/msedgedriver.exe")
else:
    # 如果是开发环境
    edge_driver_path = "D:/111/edgedriver_win64/msedgedriver.exe"

WAIT_TIMEOUT = 10
# =============================================

# 频道URL映射
CHANNEL_URLS = {
    "01.png": "https://tv.cctv.com/live/cctv1/",
    "02.png": "https://tv.cctv.com/live/cctv2/",
    "03.png": "https://tv.cctv.com/live/cctv3/",
    "04+as.png": "https://tv.cctv.com/live/cctv4asia/",
    "04+eu.png": "https://tv.cctv.com/live/cctv4europe/",
    "04+am.png": "https://tv.cctv.com/live/cctv4america/",
    "05.png": "https://tv.cctv.com/live/cctv5/",
    "05+.png": "https://tv.cctv.com/live/cctv5plus/",
    "06.png": "https://tv.cctv.com/live/cctv6/",
    "07.png": "https://tv.cctv.com/live/cctv7/",
    "08.png": "https://tv.cctv.com/live/cctv8/",
    "09.png": "https://tv.cctv.com/live/cctv9/",
    "10.png": "https://tv.cctv.com/live/cctv10/",
    "11.png": "https://tv.cctv.com/live/cctv11/",
    "12.png": "https://tv.cctv.com/live/cctv12/",
    "13.png": "https://tv.cctv.com/live/cctv13/",
    "14.png": "https://tv.cctv.com/live/cctv14/",
    "15.png": "https://tv.cctv.com/live/cctv15/",
    "16.png": "https://tv.cctv.com/live/cctv16/",
    "17.png": "https://tv.cctv.com/live/cctv17/"
}

class CCTVController:
    def __init__(self):
        # 配置 Edge 选项
        self.edge_options = EdgeOptions()
        self.edge_options.add_argument('--log-level=3')
        self.edge_options.add_argument('--silent')
        self.edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.service = Service(executable_path=edge_driver_path)
        
        # 浏览器实例
        self.driver = None
        self.wait = None
        self.WAIT_TIMEOUT = WAIT_TIMEOUT

    def open_channel(self, img_file):
        try:
            # 如果已经有浏览器实例，先关闭
            if self.driver:
                self.driver.quit()
            
            # 启动浏览器
            self.driver = webdriver.Edge(service=self.service, options=self.edge_options)
            self.wait = WebDriverWait(self.driver, self.WAIT_TIMEOUT)
            
            # 最大化浏览器窗口
            self.driver.maximize_window()
            
            # 获取频道URL
            url = CHANNEL_URLS.get(img_file, "https://tv.cctv.com/")
            
            # 打开频道页面
            self.driver.get(url)
            print(f"正在打开频道: {img_file} - {url}")
            
            # 等待页面加载完成
            self.wait.until(EC.title_contains("CCTV"))
            print("✅ 页面已加载")
            
            return True
        except Exception as e:
            print(f"❌ 打开频道失败: {e}")
            return False
    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("浏览器已关闭")

    def exit_program(self):
        if self.driver:
            self.driver.quit()