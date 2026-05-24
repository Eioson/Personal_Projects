from PIL import Image

# Convert PNG to ICO
def convert_to_ico(png_path, ico_path, sizes=[(256, 256)]):
    try:
        img = Image.open(png_path)
        img.save(ico_path, format='ICO', sizes=sizes)
        print(f"Successfully converted {png_path} to {ico_path}")
        return True
    except Exception as e:
        print(f"Error converting to ICO: {e}")
        return False

if __name__ == "__main__":
    png_path = r"C:\Users\Edison Pates\Documents\Forbidden content\AMRAAM-Chan hum.png"
    ico_path = r"C:\Users\Edison Pates\Documents\Forbidden content\AMRAAM-Chan hum.ico"
    convert_to_ico(png_path, ico_path)
