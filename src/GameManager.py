from Store import Store
import Item
import random

import time
import sqlite3

ROUNDS = 5
MAX_AISLES = 3
MAX_SECTORS = 3
SECTOR_HEIGHT = 2
SECTOR_WIDTH = 2

class Game:
	def __init__(self, name, max_aisles=MAX_AISLES, max_sectors=MAX_SECTORS, sector_height=SECTOR_HEIGHT, sector_width=SECTOR_WIDTH, rounds=ROUNDS):
		self._store = Store(name, max_aisles, max_sectors, sector_height, sector_width)
		self.max_rounds = rounds

		self._running = False
		self._start_time = None
		self.elapsed_time = None
		self.round = 0
		self.item = None

	def how_to_play(self):
		response = '''Shuffle Shopper is a game based on finding items in a store as quickly as possible. A store has a catalog that lists all the locations of items.

When the game is started, you will be given the name of an item. You will need to find the item in the catalog, or, if you're an expert, you'll have the item's aisle and sector memorized! 

Enter the item's aisle and sector. If it is correct, you will be prompted with the next item. If it is not correct, you will have to try again. 

Continue to enter the location of items you are prompted with until all rounds are completed. Your time will be displayed and added to the leaderboard. 

Good luck and have fun!'''

		return response

	def start(self):
		self.reset()
		self._running = True
		self._start_time = time.time()
		self.new_round()

	def stop(self):
		self._running = False
		self.elapsed_time = time.time() - self._start_time

	def reset(self):
		self._running = False
		self._start_time = None
		self.elapsed_time = None
		self.round = 0
		self.item = None

	def generate_item(self):
		self.item = self._store.get_random_item()

	def is_correct(self, aisle, sector):
		return (aisle == str(self.item._location._aisle)) and (sector == str(self.item._location._sector))

	def new_round(self):
		self.generate_item()
		self.round += 1

		if self.round > self.max_rounds:
			self.stop()

class Leaderboard:
	def __init__(self, leaderboard_name):
		self._conn = sqlite3.connect('Leaderboard.db') #connection string
		self._c = self._conn.cursor()
		self._table_name = leaderboard_name

		self._c.execute('CREATE TABLE IF NOT EXISTS {0}(ID INTEGER PRIMARY KEY, Username TEXT, Time_Elapsed REAL)'.format(self._table_name))

	def __del__(self):
		self._conn.commit()
		self._conn.close()

	def add_entry(self, username, time_elapsed):
		self._c.execute('INSERT INTO {0}(Username, Time_Elapsed) VALUES(?, ?)'.format(self._table_name), (username, time_elapsed))
		self._conn.commit()

	def display(self):
		self._c.execute('SELECT Username, Time_Elapsed FROM {0} ORDER BY Time_Elapsed'.format(self._table_name))

		board = ''
		board += '{0:^5}|{1:^30}|{2:^20}\n'.format('Rank', 'Username', 'Time Elapsed')
		board += ('-'*58 + '\n')
		entries = self._c.fetchall()
		for rank in range(0, len(entries)):
			board += '{0:^5}|{1:<30}|{2:>20.3f}s\n'.format(rank + 1, entries[rank][0], entries[rank][1])
		return board

		