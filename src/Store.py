import Item
import random

class Store:
	def __init__(self, name, max_aisles, max_sectors, sector_height, sector_width):
		self._catalog = []
		self._name = name
		self._max_aisles = max_aisles
		self._max_sectors = max_sectors
		self._sector_height = sector_height
		self._sector_width = sector_width

	def display_catalog(self):
		display = ''
		for aisle in range(len(self._catalog)):
			display += ('Aisle ' + str(aisle+1) + '\n')
			for sector in range(len(self._catalog[aisle])):
				display += ('\tSector ' + str(sector+1) + '\n')
				for item in self._catalog[aisle][sector]:
					display += ('\t\t' + item.get_display_name() + '\n')
		return display

	def get_item(self, aisle, sector, position):
		return self._catalog[aisle][sector][position]

class RandomStore(Store):
	def __init__(self, name, max_aisles, max_sectors, sector_height, sector_width):
		super().__init__(name, max_aisles, max_sectors, sector_height, sector_width)
		self._setup_random_catalog()

	def _setup_random_catalog(self):
		#point to item data list
		items = Item.ITEM_DATA

		for aisle in range(0, self._max_aisles):
			#add an aisle to catalog
			self._catalog.append([])

			for sector in range(0, self._max_sectors):
				#add a sector to aisle
				self._catalog[aisle].append([])

				#populate sector based on height and width dimensions
				for _ in range(0, self._sector_height * self._sector_width):
					item_location = Item.ItemLocation(aisle+1, sector+1)
					try:
						item_data = Item.get_random_item_data(items)
						i = Item.Item(item_location, item_data)
					#if items is empty, get_random_item_data throws error
					#no item data can be obtained, create 'empty' item at location
					except ValueError:
						i = Item.Item(item_location)

					self._catalog[aisle][sector].append(i)

	#return random item from catalog
	def get_random_item(self):
		aisle = random.randint(0, self._max_aisles - 1)
		sector = random.randint(0, self._max_sectors - 1)
		position = random.randint(0, self._sector_height * self._sector_width - 1)

		item = self.get_item(aisle, sector, position)
		return item
