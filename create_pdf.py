from PIL import Image
import os
import io
import base64

# 创建临时图片文件（使用用户上传的图片数据）
# 注意：这里的图片数据需要从用户提供的图片中提取

# 方法：使用img工具读取用户提供的图片，然后保存并转换为PDF
print("准备将图片转换为PDF...")

# 检查是否存在图片文件
image_paths = []
for ext in ['.png', '.jpg', '.jpeg']:
    for i in range(1, 4):
        path = f'/workspace/image_{i}{ext}'
        if os.path.exists(path):
            image_paths.append(path)

print(f"找到 {len(image_paths)} 个图片文件")

if len(image_paths) == 3:
    # 打开所有图片并转换为PDF
    pdf_pages = []
    for path in image_paths:
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        pdf_pages.append(img)
    
    # 保存为PDF
    output_path = '/workspace/www/电子认证业务合规告知函.pdf'
    pdf_pages[0].save(
        output_path,
        save_all=True,
        append_images=pdf_pages[1:],
        resolution=150.0,
        quality=95
    )
    print(f"成功创建PDF: {output_path}")
else:
    print("未找到所有图片文件，请先上传3张图片到/workspace目录")