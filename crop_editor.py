"""
裁切编辑器 - 可视化裁切框调整窗口
"""
import tkinter as tk
from PIL import Image, ImageTk


class CropEditor:
    """裁切编辑器窗口"""
    def __init__(self, parent, image_path, on_confirm):
        self.parent = parent
        self.image_path = image_path
        self.on_confirm = on_confirm
        
        # 创建窗口
        self.window = tk.Toplevel(parent)
        self.window.title("裁切编辑器 - iPhone 17 Pro")
        self.window.geometry("900x700")
        self.window.configure(bg='#ffffff')
        
        # 加载原始图片
        self.original_image = Image.open(image_path)
        self.orig_w, self.orig_h = self.original_image.size
        
        # 目标比例
        self.target_ratio = 1206 / 2622
        
        # 计算显示尺寸（缩放图片适应窗口）
        max_display_width = 800
        max_display_height = 550
        
        scale_w = max_display_width / self.orig_w
        scale_h = max_display_height / self.orig_h
        self.scale = min(scale_w, scale_h, 1.0)  # 不放大，只缩小
        
        self.display_w = int(self.orig_w * self.scale)
        self.display_h = int(self.orig_h * self.scale)
        
        # 创建UI
        self.create_ui()
        
        # 初始化裁切框（居中，占80%）
        self.init_crop_box()
        
        # 拖拽状态
        self.dragging = False
        self.resizing = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.resize_handle = None  # 'nw', 'ne', 'sw', 'se'
        
    def create_ui(self):
        """创建界面元素"""
        # 标题
        title_label = tk.Label(
            self.window,
            text="拖动裁切框调整位置，拖动角控制点调整大小",
            font=("Microsoft YaHei UI", 10),
            bg='#ffffff',
            fg='#64748b'
        )
        title_label.pack(pady=(20, 10))
        
        # Canvas 容器
        canvas_frame = tk.Frame(self.window, bg='#000000')
        canvas_frame.pack(padx=20, pady=10)
        
        # 创建 Canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.display_w,
            height=self.display_h,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # 显示图片
        display_image = self.original_image.resize(
            (self.display_w, self.display_h),
            Image.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(display_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # 绘制半透明遮罩（初始化为空，后面会更新）
        self.mask_ids = []
        
        # 绘制裁切框矩形
        self.crop_rect = self.canvas.create_rectangle(
            0, 0, 100, 100,
            outline='#FFC107',
            width=3,
            dash=(8, 4)
        )
        
        # 绘制四个角控制点
        self.handles = {}
        handle_size = 12
        for pos in ['nw', 'ne', 'sw', 'se']:
            handle = self.canvas.create_oval(
                0, 0, handle_size, handle_size,
                fill='#FFC107',
                outline='#ffffff',
                width=2
            )
            self.handles[pos] = handle
        
        # 绑定鼠标事件
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        # 按钮区域
        btn_frame = tk.Frame(self.window, bg='#ffffff')
        btn_frame.pack(pady=20)
        
        # 按钮样式
        btn_style = {
            'font': ('Microsoft YaHei UI', 11, 'bold'),
            'padx': 30,
            'pady': 10,
            'relief': tk.FLAT,
            'cursor': 'hand2'
        }
        
        reset_btn = tk.Button(
            btn_frame,
            text="重置居中",
            bg='#e2e8f0',
            fg='#1e293b',
            command=self.reset_crop,
            **btn_style
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="取消",
            bg='#e2e8f0',
            fg='#1e293b',
            command=self.cancel,
            **btn_style
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        confirm_btn = tk.Button(
            btn_frame,
            text="确认裁切",
            bg='#4f46e5',
            fg='#ffffff',
            command=self.confirm,
            **btn_style
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        
    def init_crop_box(self):
        """初始化裁切框位置（撑满图片，居中）"""
        # 计算在显示图片上的初始裁切框（尽可能撑满）
        current_ratio = self.display_w / self.display_h
        
        if current_ratio > self.target_ratio:
            # 图片太宽，裁切框以高度撑满
            crop_h = self.display_h
            crop_w = int(crop_h * self.target_ratio)
            # 水平居中
            self.crop_x = (self.display_w - crop_w) // 2
            self.crop_y = 0
        else:
            # 图片太高或刚好，裁切框以宽度撑满
            crop_w = self.display_w
            crop_h = int(crop_w / self.target_ratio)
            # 垂直居中
            self.crop_x = 0
            self.crop_y = (self.display_h - crop_h) // 2
        
        self.crop_w = crop_w
        self.crop_h = crop_h
        
        self.update_crop_display()
    
    def update_crop_display(self):
        """更新裁切框显示"""
        x1, y1 = self.crop_x, self.crop_y
        x2, y2 = self.crop_x + self.crop_w, self.crop_y + self.crop_h
        
        # 更新矩形
        self.canvas.coords(self.crop_rect, x1, y1, x2, y2)
        
        # 更新控制点位置
        handle_size = 12
        offset = handle_size // 2
        
        positions = {
            'nw': (x1 - offset, y1 - offset),
            'ne': (x2 - offset, y1 - offset),
            'sw': (x1 - offset, y2 - offset),
            'se': (x2 - offset, y2 - offset)
        }
        
        for pos, handle in self.handles.items():
            px, py = positions[pos]
            self.canvas.coords(handle, px, py, px + handle_size, py + handle_size)
        
        # 更新遮罩
        self.update_mask()
        
    def update_mask(self):
        """更新半透明遮罩"""
        # 删除旧遮罩
        for mask_id in self.mask_ids:
            self.canvas.delete(mask_id)
        self.mask_ids = []
        
        # 创建四个遮罩矩形（裁切框外部）
        x1, y1 = self.crop_x, self.crop_y
        x2, y2 = self.crop_x + self.crop_w, self.crop_y + self.crop_h
        
        # 上
        if y1 > 0:
            m = self.canvas.create_rectangle(
                0, 0, self.display_w, y1,
                fill='black',
                stipple='gray50',
                outline=''
            )
            self.mask_ids.append(m)
        
        # 下
        if y2 < self.display_h:
            m = self.canvas.create_rectangle(
                0, y2, self.display_w, self.display_h,
                fill='black',
                stipple='gray50',
                outline=''
            )
            self.mask_ids.append(m)
        
        # 左
        if x1 > 0:
            m = self.canvas.create_rectangle(
                0, y1, x1, y2,
                fill='black',
                stipple='gray50',
                outline=''
            )
            self.mask_ids.append(m)
        
        # 右
        if x2 < self.display_w:
            m = self.canvas.create_rectangle(
                x2, y1, self.display_w, y2,
                fill='black',
                stipple='gray50',
                outline=''
            )
            self.mask_ids.append(m)
        
        # 将裁切框和控制点置于顶层
        self.canvas.tag_raise(self.crop_rect)
        for handle in self.handles.values():
            self.canvas.tag_raise(handle)
    
    def on_mouse_down(self, event):
        """鼠标按下"""
        # 检查是否点击控制点
        for pos, handle in self.handles.items():
            x1, y1, x2, y2 = self.canvas.coords(handle)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.resizing = True
                self.resize_handle = pos
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                return
        
        # 检查是否点击裁切框内部
        x1, y1 = self.crop_x, self.crop_y
        x2, y2 = self.crop_x + self.crop_w, self.crop_y + self.crop_h
        
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            self.dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
    
    def on_mouse_move(self, event):
        """鼠标拖动"""
        if self.resizing:
            self.handle_resize(event)
        elif self.dragging:
            self.handle_drag(event)
    
    def on_mouse_up(self, event):
        """鼠标释放"""
        self.dragging = False
        self.resizing = False
        self.resize_handle = None
    
    def handle_drag(self, event):
        """处理拖动移动"""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        new_x = self.crop_x + dx
        new_y = self.crop_y + dy
        
        # 边界限制
        if new_x < 0:
            new_x = 0
        if new_y < 0:
            new_y = 0
        if new_x + self.crop_w > self.display_w:
            new_x = self.display_w - self.crop_w
        if new_y + self.crop_h > self.display_h:
            new_y = self.display_h - self.crop_h
        
        self.crop_x = new_x
        self.crop_y = new_y
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        self.update_crop_display()
    
    def handle_resize(self, event):
        """处理调整大小（保持比例）"""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        handle = self.resize_handle
        
        # 根据拖动的角计算新尺寸
        if handle == 'se':  # 右下角
            new_w = self.crop_w + dx
            new_h = int(new_w / self.target_ratio)
        elif handle == 'sw':  # 左下角
            new_w = self.crop_w - dx
            new_h = int(new_w / self.target_ratio)
            new_x = self.crop_x + dx
        elif handle == 'ne':  # 右上角
            new_w = self.crop_w + dx
            new_h = int(new_w / self.target_ratio)
            new_y = self.crop_y - (new_h - self.crop_h)
        elif handle == 'nw':  # 左上角
            new_w = self.crop_w - dx
            new_h = int(new_w / self.target_ratio)
            new_x = self.crop_x + dx
            new_y = self.crop_y - (new_h - self.crop_h)
        else:
            return
        
        # 最小尺寸限制
        if new_w < 50 or new_h < 50:
            return
        
        # 边界检查
        if handle in ['sw', 'nw']:
            if new_x < 0 or new_x + new_w > self.display_w:
                return
            self.crop_x = new_x
        else:
            if self.crop_x + new_w > self.display_w:
                return
        
        if handle in ['ne', 'nw']:
            if new_y < 0 or new_y + new_h > self.display_h:
                return
            self.crop_y = new_y
        else:
            if self.crop_y + new_h > self.display_h:
                return
        
        self.crop_w = new_w
        self.crop_h = new_h
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        self.update_crop_display()
    
    def reset_crop(self):
        """重置裁切框为居中"""
        self.init_crop_box()
    
    def cancel(self):
        """取消编辑"""
        self.window.destroy()
    
    def confirm(self):
        """确认裁切"""
        # 将显示坐标转换为原图坐标
        real_x = int(self.crop_x / self.scale)
        real_y = int(self.crop_y / self.scale)
        real_w = int(self.crop_w / self.scale)
        real_h = int(self.crop_h / self.scale)
        
        crop_box = {
            'x': real_x,
            'y': real_y,
            'width': real_w,
            'height': real_h
        }
        
        self.window.destroy()
        self.on_confirm(self.image_path, crop_box)
