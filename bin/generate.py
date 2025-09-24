#!/usr/bin/python3
# vim:set ts=4

from glob import glob
from os.path import basename
from pathlib import Path
from PIL import Image
from terminus.terminus import Terminus

terminus = Terminus.create('orig')
terminus.family_name = 'Terminus IAST'

for file in Path('glyph').glob('**'):
	if file.is_dir():
		continue
	name = basename(file)[0:-4]
	char = int(name, 16)
	image = Image.open(file)
	terminus[char] = image

terminus.save()
