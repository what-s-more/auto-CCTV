# Auto-CCTV

一个自动打开 CCTV 频道的 Python 应用程序。

## 功能

- 提供图形界面选择不同的 CCTV 频道
- 自动使用 Edge 浏览器打开选定频道的直播页面
- 支持多个 CCTV 频道（CCTV-1 到 CCTV-17 以及国际频道）

## 安装

1. 克隆此仓库：
git clone https://github.com/你的用户名/auto-CCTV.git


2. 安装依赖：
pip install -r requirements.txt


3. 安装 Edge WebDriver：
- 下载与你的 Edge 浏览器版本匹配的 WebDriver
- 将其放在 `edgedriver_win64/` 目录下

## 使用

运行应用程序：
python cctv_viewer.py


## 依赖

- Python 3.x
- Selenium
- tkinter
- Pillow (PIL)

## 注意

此应用程序使用 Selenium 控制 Edge 浏览器，需要安装对应版本的 Edge WebDriver。
