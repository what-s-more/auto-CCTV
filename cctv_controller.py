import os
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# ================== 配置区域 ==================
# 不再需要指定 msedgedriver.exe 路径
# 使用系统安装的 Edge 浏览器
WAIT_TIMEOUT = 10
# =============================================

# 频道URL映射（保持不变）
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
        
        # 自动使用系统安装的 Edge 浏览器
        # 不指定路径，让 Selenium 自动查找
        self.service = Service()
        
        # 浏览器实例
        self.driver = None
        self.wait = None
        self.WAIT_TIMEOUT = WAIT_TIMEOUT

    def find_edge_path(self):
        """尝试在常见位置查找 Edge 浏览器路径"""
        possible_paths = [
            # Windows 10/11 默认安装位置
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            # Windows 用户目录
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
            # 通过注册表查找（备用方案）
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # 如果没找到，返回 None 让 Selenium 使用默认方式
        return None

    def open_channel(self, img_file):
        try:
            # 如果已经有浏览器实例，先关闭
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            
            # 设置浏览器路径（如果找到）
            edge_path = self.find_edge_path()
            if edge_path:
                self.edge_options.binary_location = edge_path
            
            # 启动浏览器，使用系统安装的 Edge
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
            try:
                self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                print("✅ 页面已加载")
            except Exception as e:
                print(f"⚠️ 页面加载超时，但继续运行: {e}")
            
            return True
        except Exception as e:
            print(f"❌ 打开频道失败: {e}")
            print("尝试清理并重新启动浏览器...")
            
            # 尝试清理进程
            try:
                if self.driver:
                    self.driver.quit()
            except:
                pass
            
            # 提供解决方案
            print("\n解决方案:")
            print("1. 确保已安装 Microsoft Edge 浏览器")
            print("2. 运行命令: pip install selenium --upgrade")
            print("3. 如果仍失败，请从 Microsoft 官网下载 Edge 驱动:")
            print("   https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
            
            return False

    def close_browser(self):
        if self.driver:
            try:
                self.driver.quit()
                print("浏览器已关闭")
            except Exception as e:
                print(f"关闭浏览器时出错: {e}")
            finally:
                self.driver = None

    def exit_program(self):
        self.close_browser()