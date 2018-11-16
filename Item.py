class Item:
	def __init__(self, item_location, item_data=['', 'Empty']):
		self._name = item_data[0]
		self._brand = item_data[1]
		self._location = item_location

	def __eq__(self, other):
		if isinstance(other, Item):
			return (self._location == other._location and self.get_display_name() == other.get_display_name())
		else:
			return False

	def get_display_name(self):
		return self._brand + ' ' + self._name

class ItemLocation:
	def __init__(self, aisle, sector):
		self._aisle = aisle
		self._sector = sector

	def __eq__(self, other):
		if isinstance(other, ItemLocation):
			return (self._aisle == other._aisle and self._sector == other._sector)
		else:
			return False

ITEM_DATA = [
{'name':'Mayonnaise', 'brands':{"Hellman's", 'Kraft', "Duke's"}},
{'name':'Coffee', 'brands':{'Maxwell House', 'Green Mountain', 'Folgers', 'McCafe'}},
{'name':'Dressing', 'brands':{'Hidden Valley', 'Wish-Bone', 'Kraft'}},
{'name':'Rice', 'brands':{'Minute', "Uncle Ben's", 'Mahatma', "Zatarain's"}},
{'name':'Ketchup', 'brands':{'Heinz', "Hunt's", "French's"}},
{'name':'Cereal', 'brands':{'Post', "Kellogg's", 'Quaker'}},
{'name':'Chips', 'brands':{'Utz', 'Frito-Lay', 'Pringles'}},
{'name':'Spaghetti', 'brands':{'Barilla', 'Ronzoni', 'San Giorgio'}},
{'name':'Canned Tuna', 'brands':{'Starkist', 'BumbleBee', 'Chicken of the Sea'}},
{'name':'Canned Vegetables', 'brands':{"Libby's", 'Green Giant', 'Del Monte'}},
{'name':'Canned Soup', 'brands':{'Progresso', "Campbell's", 'Lipton'}},
{'name':'Canned Fruit', 'brands':{'Dole', 'Del Monte'}},
{'name':'Juice', 'brands':{'V8', "Welch's", 'Ocean Spray'}},
{'name':'Cookies', 'brands':{'Oreo', 'Chips Ahoy', 'Keebler', 'Pepperidge Farm'}},
{'name':'Crackers', 'brands':{'Ritz', 'Cheez-It', 'Nabisco', 'Zesta'}},
{'name':'Popcorn', 'brands':{'Orville', 'Pop Secret', 'Smart Food', 'Skinny Girl'}},
{'name':'Nuts', 'brands':{'Emerald', 'Planters', 'Blue Diamond'}}
]

def get_random_item_data(index, item_list):
	name = item_list[index]['name']
	brand = item_list[index]['brands'].pop()

	if len(item_list[index]['brands']) == 0:
		del item_list[index]

	return [name, brand]