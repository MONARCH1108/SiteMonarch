import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\abhay\OneDrive\Desktop\Blog Site\AbhayBlog\content\posts"
attachments_dir = r"C:\Users\abhay\OneDrive\Desktop\Blog Site\images"
static_images_dir = r"C:\Users\abhay\OneDrive\Desktop\Blog Site\AbhayBlog\static\images"

# Ensure the static_images_dir exists
if not os.path.exists(static_images_dir):
    os.makedirs(static_images_dir)
    print(f"Created directory: {static_images_dir}")

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        print(f"Processing file: {filepath}")
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png or .jpg)
        images = re.findall(r'\[\[([^]]*\.(?:png|jpg))\]\]', content, re.IGNORECASE)
        print(f"Found images: {images}")
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Check if the image exists in the source directory
            image_source = os.path.join(attachments_dir, image)
            image_destination = os.path.join(static_images_dir, image)
            
            if os.path.exists(image_source):
                try:
                    print(f"Copying {image_source} to {image_destination}")
                    shutil.copy(image_source, static_images_dir)
                except Exception as e:
                    print(f"Error copying {image_source}: {e}")
            else:
                print(f"Image not found: {image_source}")

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
