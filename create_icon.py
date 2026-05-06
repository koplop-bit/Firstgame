from PIL import Image
import os

def create_icon():
    try:
        img_path = 'images/pixil-frame-0.png'
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            # Створимо просту іконку якщо немає картинки
            img = Image.new('RGB', (256, 256), color = (73, 109, 137))
        else:
            img = Image.open(img_path)
            
        # Ensure image is square and has alpha channel
        img = img.convert("RGBA")
        img.save('icon.ico', format='ICO', sizes=[(32, 32), (64, 64), (128, 128), (256, 256)])
        print("Icon created successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_icon()
