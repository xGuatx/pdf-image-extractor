import os
from pdf2image import convert_from_path
from PIL import Image
import math

# Chemin du PDF
pdf_path = 'ton_fichier.pdf'

# Répertoire temporaire pour stocker les images des pages
output_dir = 'images_pages'
os.makedirs(output_dir, exist_ok=True)

# Convertir chaque page du PDF en image haute résolution (600 DPI)
print("Conversion du PDF en images...")
pages = convert_from_path(pdf_path, dpi=600, fmt='png')

# Sauvegarde des images individuelles
image_paths = []
for i, page in enumerate(pages):
    img_path = os.path.join(output_dir, f'page_{i+1:03d}.png')
    page.save(img_path, 'PNG')
    image_paths.append(img_path)

# Regrouper les images par 3 et concaténer
group_size = 3
num_groups = math.ceil(len(image_paths) / group_size)

concat_output_dir = 'images_concatenees'
os.makedirs(concat_output_dir, exist_ok=True)

for group_index in range(num_groups):
    group_images = []
    for i in range(group_size):
        idx = group_index * group_size + i
        if idx < len(image_paths):
            img = Image.open(image_paths[idx])
            group_images.append(img)

    # Calcul de la largeur et de la hauteur totale
    max_width = max(img.width for img in group_images)
    total_height = sum(img.height for img in group_images)

    # Nouvelle image blanche (fond blanc)
    new_img = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))

    # Coller les images les unes sous les autres
    y_offset = 0
    for img in group_images:
        new_img.paste(img, (0, y_offset))
        y_offset += img.height

    # Sauvegarde de l'image concaténée
    concat_path = os.path.join(concat_output_dir, f'concat_{group_index+1:02d}.png')
    new_img.save(concat_path, 'PNG', quality=100)
    print(f'Image concaténée sauvegardée : {concat_path}')

print("Traitement terminé.")

