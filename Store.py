import Item
import random

class Store:
	def __init__(self, name, max_aisles, max_sectors, sector_height, sector_width):
		self._catalog = {}
		self._name = name
		self._max_aisles = max_aisles
		self._max_sectors = max_sectors
		self._sector_height = sector_height
		self._sector_width = sector_width

		self._setup_random_catalog()

	def _setup_random_catalog(self):
		items = Item.ITEM_DATA.copy()
		for a in range(1, self._max_aisles+1):
			self._catalog[a] = {}
			for s in range(1, self._max_sectors+1):
				self._catalog[a][s] = []
				for h in range(0, self._sector_height):
					for w in range(0, self._sector_width):
						item_location = Item.ItemLocation(a, s)
						try:
							index = random.randint(0, len(items) - 1)
							item_data = Item.get_random_item_data(index, items)
							i = Item.Item(item_location, item_data)
						except ValueError:
							i = Item.Item(item_location)
						self._catalog[a][s].append(i)

	def display_catalog(self):
		display = ''
		for a in self._catalog.keys():
			display += ('Aisle ' + str(a) + '\n')
			for s in self._catalog[a].keys():
				display += ('\tSector ' + str(s) + '\n')
				for item in self._catalog[a][s]:
					display += ('\t\t' + item.get_display_name() + '\n')
		return display

	def get_sector(self, aisle, sector):
		return self._catalog[aisle][sector]

	def get_random_item(self):
		aisle = random.randint(1, self._max_aisles)
		sector = random.randint(1, self._max_sectors)
		shelf = random.randint(0, self._sector_height)
		position = random.randint(0, self._sector_width)

		items = self.get_sector(aisle, sector)
		item = items[shelf * position - 1]
		return item
