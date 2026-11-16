from pathlib import Path
from PIL import Image, ImageDraw

folder = Path(r"C:\Users\HP\.codex\visualizations\2026\07\28\019faabb-03f0-7721-a83a-520605149e89\revision-tesis")
pages = sorted(folder.glob('page-*.jpg'))
for group_index in range(0, len(pages), 12):
    group = pages[group_index:group_index + 12]
    sheet = Image.new('RGB', (1600, 2000), 'white')
    draw = ImageDraw.Draw(sheet)
    for position, path in enumerate(group):
        image = Image.open(path).convert('RGB')
        image.thumbnail((380, 450))
        x = (position % 4) * 400 + 10
        y = (position // 4) * 650 + 35
        sheet.paste(image, (x, y))
        draw.text((x, 10 + (position // 4) * 650), f'Página {group_index + position + 1}', fill='black')
    sheet.save(folder / f'contact-{group_index // 12 + 1}.jpg', quality=90)
print(len(pages))
