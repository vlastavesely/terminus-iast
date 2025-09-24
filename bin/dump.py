#!/usr/bin/python3
# vim:set ts=4

from sys import argv
from terminus.terminus import Terminus

file = f'{argv[1]}.png'

terminus = Terminus.create('orig')

image = terminus[int(argv[1], 16)]
print('Saving {file} …')
image.save(f'{file}')

terminus.save()
