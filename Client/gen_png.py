from pdf2image import convert_from_path
import shutil
import os
from progressbar import ProgressBar

path = 'PowerPoint/u22.pdf'
images = convert_from_path(path)

shutil.rmtree('Tmp/')
os.mkdir("Tmp/")

p = ProgressBar(0, len(images))
i = 0
for image in images:
    image.save('Tmp/page{}.png'.format(i + 1), 'png')
    i += 1
    p.update(i)
