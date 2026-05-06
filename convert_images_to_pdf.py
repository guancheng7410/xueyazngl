from PIL import Image
import os

# Save the three images provided by user and combine into PDF
# The images are uploaded as attachments in the conversation

# First, let's create image files from the uploaded images
# Image 1: First page of the document
# Image 2: Second page of the document  
# Image 3: Third page of the document

# Read and process images
images_dir = '/workspace/images_temp'
os.makedirs(images_dir, exist_ok=True)

# Save uploaded images to files
image_files = []
for i in range(1, 4):
    src_path = f'/workspace/image_{i}.png'
    if os.path.exists(src_path):
        image_files.append(src_path)
    else:
        # Try other possible locations
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            alt_path = f'/workspace/image_{i}{ext}'
            if os.path.exists(alt_path):
                image_files.append(alt_path)
                break

print(f"Found {len(image_files)} images")
print("Image files:", image_files)
