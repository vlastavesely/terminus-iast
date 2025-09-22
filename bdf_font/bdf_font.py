#!/usr/bin/python3
# vim:set ts=4

from bdf_font.glyph import Glyph
from bdflib.model import Font, Glyph as FontGlyph
from bdflib import reader, writer
from typing import Union

PropertyValue = Union[bytes, int]

class BdfFont(Font):
	def __new__(cls, file_name: str):
		with open(file_name, 'rb') as f:
			font = reader.read_bdf(f)
		font.__class__ = cls
		return font

	def __init__(self, file_name: str) -> None:
		# already initialised
		pass

	def __getitem__(self, key: Union[bytes, int]) -> Union[PropertyValue, FontGlyph]:
		ret = super().__getitem__(key)
		if isinstance(ret, FontGlyph):
			ret.__class__ = Glyph
			print(ret)
		return ret

	def save(self, file_name: str) -> None:
		with open(file_name, 'wb') as f:
			writer.write_bdf(self, f)
