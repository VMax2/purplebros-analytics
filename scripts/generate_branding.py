import base64
from io import BytesIO
import os
from PIL import Image, ImageDraw

def generate():
    root = r'C:\Users\Max\Umami-Customization-x-Antigravity'
    loghi_dir = os.path.join(root, 'loghi')
    branding_dir = os.path.join(root, 'branding')
    
    scuro_path = os.path.join(loghi_dir, 'PurpleBros-Scuro.jpg')
    if not os.path.exists(scuro_path):
        print(f"File non trovato: {scuro_path}")
        return

    im_scuro = Image.open(scuro_path)
    cx, cy = 520, 421
    box = (cx - 360, cy - 360, cx + 360, cy + 360)
    crop_scuro = im_scuro.crop(box)

    # Maschera circolare antialiased
    # Per avere bordi ultra-morbidi, generiamo una maschera 4x e poi facciamo il downscale
    mask_large = Image.new('L', (720 * 4, 720 * 4), 0)
    draw_large = ImageDraw.Draw(mask_large)
    draw_large.ellipse((4 * 4, 4 * 4, 716 * 4, 716 * 4), fill=255)
    mask = mask_large.resize((720, 720), Image.Resampling.LANCZOS)

    scuro_rgba = crop_scuro.convert('RGBA')
    scuro_rgba.putalpha(mask)

    # 1. Master PNG
    master_path = os.path.join(branding_dir, 'master-badge-scuro.png')
    scuro_rgba.save(master_path, format='PNG')
    print(f"✔ Generato: {master_path}")

    # 2. Favicon 16x16
    fav16_path = os.path.join(branding_dir, 'favicon-16x16.png')
    fav16 = scuro_rgba.resize((16, 16), Image.Resampling.LANCZOS)
    fav16.save(fav16_path, format='PNG')
    print(f"✔ Generato: {fav16_path}")

    # 3. Favicon 32x32
    fav32_path = os.path.join(branding_dir, 'favicon-32x32.png')
    fav32 = scuro_rgba.resize((32, 32), Image.Resampling.LANCZOS)
    fav32.save(fav32_path, format='PNG')
    print(f"✔ Generato: {fav32_path}")

    # 4. Apple Touch Icon 180x180
    apple_path = os.path.join(branding_dir, 'apple-touch-icon.png')
    apple = scuro_rgba.resize((180, 180), Image.Resampling.LANCZOS)
    apple.save(apple_path, format='PNG')
    print(f"✔ Generato: {apple_path}")

    # 5. Multi-size Favicon.ico (16, 32, 48, 64)
    ico_path = os.path.join(branding_dir, 'favicon.ico')
    fav_master = scuro_rgba.resize((256, 256), Image.Resampling.LANCZOS)
    fav_master.save(
        ico_path,
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
    )
    print(f"✔ Generato: {ico_path}")

    # 6. logo.svg (utilizzato da Umami nella navbar e nel login)
    fav512 = scuro_rgba.resize((512, 512), Image.Resampling.LANCZOS)
    buf = BytesIO()
    fav512.save(buf, format='PNG', optimize=True)
    b64_png = base64.b64encode(buf.getvalue()).decode('utf-8')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <image href="data:image/png;base64,{b64_png}" width="512" height="512" />
</svg>
'''
    svg_path = os.path.join(branding_dir, 'logo.svg')
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✔ Generato: {svg_path}")

if __name__ == '__main__':
    generate()
