"""
SmartCropper - iPhone 17 Pro 智能裁切工具
支持拖拽上传和可视化裁切框编辑
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import windnd

from crop_editor import CropEditor
from cropper import manual_crop


def resource_path(relative_path):
    """获取资源的绝对路径，兼容 PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class App:
    """主应用程序窗口"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("iPhone 17 Pro 裁切工具")
        self.root.geometry("600x500")
        self.root.configure(bg='#ffffff')
        
        # 设置图标
        self._setup_icon()
        
        # 配色方案
        self.colors = {
            'bg': '#ffffff',
            'primary': '#4f46e5',
            'primary_light': '#eef2ff',
            'text_main': '#1e293b',
            'text_dim': '#64748b',
            'success': '#10b981',
            'border': '#e2e8f0'
        }
        
        # 设置样式
        self._setup_styles()
        
        # 创建UI
        self._create_ui()
        
        # 注册拖拽回调
        windnd.hook_dropfiles(self.root, func=self.on_drop)
    
    def _setup_icon(self):
        """设置窗口图标"""
        try:
            icon_p = resource_path('icon.ico')
            if os.path.exists(icon_p):
                self.root.iconbitmap(icon_p)
        except:
            pass
    
    def _setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.colors['bg'])
        style.configure("TLabel", background=self.colors['bg'], 
                       font=("Microsoft YaHei UI", 10), 
                       foreground=self.colors['text_main'])
        style.configure("Header.TLabel", 
                       font=("Microsoft YaHei UI", 20, "bold"), 
                       foreground=self.colors['primary'])
        style.configure("Sub.TLabel", 
                       font=("Microsoft YaHei UI", 10), 
                       foreground=self.colors['text_dim'])
    
    def _create_ui(self):
        """创建主界面"""
        # 主容器
        self.main_frame = ttk.Frame(self.root, padding="40")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        ttk.Label(
            self.main_frame, 
            text="Smart Cropper", 
            style="Header.TLabel"
        ).pack(pady=(0, 5))
        
        ttk.Label(
            self.main_frame, 
            text="为您精准适配 iPhone 17 Pro 比例 (1206:2622)", 
            style="Sub.TLabel"
        ).pack(pady=(0, 30))
        
        # 拖拽区域
        self.drop_container = tk.Frame(
            self.main_frame, 
            bg=self.colors['primary_light'], 
            highlightthickness=2, 
            highlightbackground=self.colors['primary'], 
            highlightcolor=self.colors['primary'], 
            bd=0
        )
        self.drop_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.drop_label = tk.Label(
            self.drop_container, 
            text="拖拽图片到此区域\n\n(支持 JPG, PNG, WEBP)", 
            bg=self.colors['primary_light'], 
            fg=self.colors['primary'],
            font=("Microsoft YaHei UI", 12, "bold"),
            pady=40
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        self.status_label = tk.Label(
            self.main_frame, 
            textvariable=self.status_var, 
            font=("Microsoft YaHei UI", 9), 
            bg=self.colors['bg'],
            fg=self.colors['text_dim']
        )
        self.status_label.pack(pady=(20, 0))
    
    def on_drop(self, files):
        """拖拽文件回调 - 打开裁切编辑器"""
        for file_path in files:
            path_str = file_path.decode('gbk') if isinstance(file_path, bytes) else file_path
            
            # 检查文件类型
            if path_str.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                self.status_var.set("正在打开编辑器...")
                self.root.update()
                
                # 打开裁切编辑器
                CropEditor(self.root, path_str, self.on_crop_confirmed)
                break  # 一次只处理一张图片
    
    def on_crop_confirmed(self, image_path, crop_box):
        """裁切确认回调"""
        self.status_var.set("正在裁切...")
        self.root.update()
        
        output_dir = os.path.dirname(image_path)
        result = manual_crop(image_path, output_dir, crop_box)
        
        if result:
            self.status_var.set("完成！已保存到原文件夹")
            self.drop_container.configure(highlightbackground=self.colors['success'])
            self.status_label.configure(fg=self.colors['success'])
            
            messagebox.showinfo(
                "处理成功", 
                f"图片已成功裁切！\n\n"
                f"保存位置：{os.path.dirname(result)}\n"
                f"保存名称：{os.path.basename(result)}"
            )
        else:
            self.status_var.set("裁切失败")
            messagebox.showerror("错误", "图片裁切失败，请重试")


def main():
    """程序入口"""
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
