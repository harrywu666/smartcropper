# SmartCropper - iPhone 17 Pro 裁切工具

一款专为 iPhone 17 Pro (1206:2622) 比例设计的智能图片裁切工具。

## 功能特性

✨ **可视化裁切编辑器**
- 拖拽调整裁切框位置和大小
- 比例自动锁定（1206:2622）
- 裁切框默认撑满图片并居中
- 四角控制点精确调整

🎯 **极致画质**
- 高质量保存（quality=95，视觉无损）
- 禁用色度子采样（subsampling=0）
- 保持原图色彩完整性

💫 **简单易用**
- 拖拽图片即可使用
- 实时预览裁切效果
- 自动保存到原文件夹

## 使用方法

### 方式一：运行可执行文件（推荐）

**位置**：`dist\SmartCropper.exe`

1. 双击运行 `SmartCropper.exe`
2. 拖拽图片到窗口
3. 调整裁切框（拖动框体移动，拖动角控制点调整大小）
4. 点击"确认裁切"
5. 裁切后的图片自动保存在原图片文件夹，文件名为 `@iPhone 17 Pro.扩展名`

**无需 Python 环境**，可在任何 Windows 电脑上直接运行。

### 方式二：从源码运行

需要 Python 3.8+

```bash
# 安装依赖
pip install pillow windnd

# 运行程序
python pure_cropper.py
```

## 项目结构

```
SmartCropper/
├── pure_cropper.py          # 主程序
├── crop_editor.py           # 裁切编辑器窗口
├── cropper.py               # 裁切核心逻辑
├── icon.ico                 # 应用图标
├── README.md                # 项目说明
├── .gitignore               # Git 忽略配置
└── dist/
    └── SmartCropper.exe    # 可执行文件 ⭐
```

## 技术实现

- **GUI 框架**：Tkinter
- **图片处理**：Pillow (PIL)
- **拖拽支持**：windnd
- **打包工具**：PyInstaller

## 核心参数

- **目标比例**：1206:2622 (iPhone 17 Pro)
- **保存质量**：95 (视觉无损)
- **色度采样**：禁用 (subsampling=0)

## 打包说明

如需重新打包，运行：

```bash
pyinstaller --onefile --windowed --name="SmartCropper" --icon=icon.ico --add-data="crop_editor.py;." pure_cropper.py
```

生成的可执行文件位于 `dist\SmartCropper.exe`

> 注：打包时需要包含 `crop_editor.py` 模块

## 许可

本工具为个人使用，请勿用于商业用途。

---

**Enjoy! 🎉**
