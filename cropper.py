import os
from PIL import Image
import sys

def smart_crop(input_path, output_path):
    """
    智能裁切图片为 1206:2622 比例
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 原始尺寸
            orig_w, orig_h = img.size
            
            # 目标比例 1206 : 2622
            target_ratio = 1206 / 2622
            current_ratio = orig_w / orig_h
            
            print(f"原始尺寸: {orig_w}x{orig_h}, 当前比例: {current_ratio:.4f}")
            print(f"目标比例: {target_ratio:.4f}")

            if current_ratio > target_ratio:
                # 图片太宽，保持高度不变，裁切宽度
                # 新宽度 = 高度 * 目标比例
                new_h = orig_h
                new_w = round(new_h * target_ratio)
                print(f"处理方式: 太宽，裁切左右。裁切后的宽度: {new_w}")
            else:
                # 图片太高（或正好），保持宽度不变，裁切高度
                # 新高度 = 宽度 / 目标比例
                new_w = orig_w
                new_h = round(new_w / target_ratio)
                print(f"处理方式: 太高，裁切上下。裁切后的高度: {new_h}")

            # 计算裁切框 (left, top, right, bottom) - 中心裁切
            left = (orig_w - new_w) / 2
            top = (orig_h - new_h) / 2
            right = (orig_w + new_w) / 2
            bottom = (orig_h + new_h) / 2

            # 执行裁切
            cropped_img = img.crop((left, top, right, bottom))
            
            # 保存结果 (使用高质量保存)
            # 如果文件夹不存在则创建
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cropped_img.save(output_path, quality=95, subsampling=0)
            
            print(f"成功保存到: {output_path}")
            print(f"最终尺寸: {cropped_img.size[0]}x{cropped_img.size[1]} (比例: {cropped_img.size[0]/cropped_img.size[1]:.4f})")
            return True

    except Exception as e:
        print(f"处理失败 {input_path}: {e}")
        return False

def manual_crop(input_path, output_dir, crop_box):
    """
    根据用户指定的裁切框进行裁切
    :param input_path: 输入图片路径
    """
    try:
        with Image.open(input_path) as img:
            # 解析裁切框参数
            if isinstance(crop_box, dict):
                # Canvas 坐标格式：x, y, width, height
                left = crop_box['x']
                top = crop_box['y']
                right = left + crop_box['width']
                bottom = top + crop_box['height']
            else:
                # PIL 坐标格式：left, top, right, bottom
                left, top, right, bottom = crop_box
            
            print(f"手动裁切框: left={left}, top={top}, right={right}, bottom={bottom}")
            
            # 执行裁切
            cropped_img = img.crop((left, top, right, bottom))
            
            # 保存结果（高质量保存）
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cropped_img.save(output_path, quality=95, subsampling=0)
            
            print(f"成功保存到: {output_path}")
            print(f"最终尺寸: {cropped_img.size[0]}x{cropped_img.size[1]}")
            return True
            
    except Exception as e:
        print(f"手动裁切失败 {input_path}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python cropper.py <input_image_or_directory> [output_directory]")
        return

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    if os.path.isfile(input_path):
        # 处理单文件
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, filename)
        smart_crop(input_path, output_path)
    elif os.path.isdir(input_path):
        # 处理目录
        files = [f for f in os.listdir(input_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if not files:
            print("未找到支持的图片文件")
            return
        
        for f in files:
            in_p = os.path.join(input_path, f)
            out_p = os.path.join(output_dir, f)
            print(f"\n正在处理: {f}...")
            smart_crop(in_p, out_p)
    else:
        print("无效的输入路径")

if __name__ == "__main__":
    main()
