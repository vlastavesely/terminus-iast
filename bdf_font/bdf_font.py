#!/usr/bin/python3
# vim:set ts=4

from bdflib.model import Font
from bdflib import reader, writer

class BdfFont(Font):
	def __new__(cls, file_name: str):
		with open(file_name, 'rb') as f:
			font = reader.read_bdf(f)
		font.__class__ = cls
		return font

	def __init__(self, file_name: str) -> None:
		# already initialised
		pass

	def save(self, file_name: str) -> None:
		with open(file_name, 'wb') as f:
			writer.write_bdf(self, f)
