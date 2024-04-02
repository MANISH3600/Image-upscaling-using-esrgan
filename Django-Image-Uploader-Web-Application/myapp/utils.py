from PIL import Image
import os
import subprocess
import tempfile

def enhance_image(image):
    temp_image_path = None
    output_image_path = None
    
    try:
        print(image)
        print("1")
        # Preprocessing: Resize the image if needed
        with Image.open(image) as img:

            print(img.mode)
            # Convert the image to RGB mode if it's in RGBA mode
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Save the resized image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
                temp_image_path = temp_image.name
                img.save(temp_image, format='JPEG')
            print("Second")

        # Define paths for the model and weights
        vulcan_path = "ml_model/realesrgan-ncnn-vulkan.exe"
        # Define paths for the temporary output enhanced image
        output_image_path = temp_image_path + '_enhanced.jpg'
        print("3")
        # Call the RealesRGAN model to enhance the image
        subprocess.run([vulcan_path, '-i', temp_image_path, '-o', output_image_path], check=True)
        # Post-processing: Read the enhanced image content
        with open(output_image_path, 'rb') as enhanced_image_file:
            enhanced_image_content = enhanced_image_file.read()

        return enhanced_image_content
    except Exception as e:
        # Handle exceptions
        print("Error occurred during image enhancement:", e)
        return None
    finally:
        # Cleanup temporary files
        try:
            if temp_image_path:
                os.remove(temp_image_path)
            if output_image_path:
                os.remove(output_image_path)
        except Exception as e:
            print("Error occurred during temporary file cleanup:", e)
