from GameManager import Game, Leaderboard
from tkinter import *
from functools import partial

STORE_NAME = 'Stevenson'

def show_howto():
	info = Tk()
	info.title('How to Play')
	info.geometry('500x500+500+0')
	info.resizable(FALSE, FALSE)

	txtHowto = Text(info, wrap=WORD)
	txtHowto.pack()

	text = game.how_to_play()
	txtHowto.insert('end', text)
	txtHowto['state'] = 'disabled'

def show_leaderboard():
	info = Tk()
	info.title('Top Scores')
	info.geometry('450x500+500+0')
	info.resizable(FALSE, FALSE)

	txtBoard = Text(info, wrap=WORD)
	txtBoard.grid(column=0, row=0, sticky=(N,W,E,S))

	s = Scrollbar(info, orient=VERTICAL, command=txtBoard.yview)
	s.grid(column=1, row=0, sticky=(N,S))

	txtBoard['yscrollcommand'] = s.set

	info.grid_columnconfigure(0, weight=1)
	info.grid_rowconfigure(0, weight=1)

	text = leaderboard.display()
	txtBoard.insert('end', text)
	txtBoard['state'] = 'disabled'

def show_catalog():
	catalog = Tk()
	catalog.title('Store Catalog')
	catalog.geometry('500x500+500+0')
	catalog.resizable(FALSE, FALSE)

	lstCatalog = Text(catalog)
	lstCatalog.grid(column=0, row=0, sticky=(N,W,E,S))

	s = Scrollbar(catalog, orient=VERTICAL, command=lstCatalog.yview)
	s.grid(column=1, row=0, sticky=(N,S))

	lstCatalog['yscrollcommand'] = s.set

	catalog.grid_columnconfigure(0, weight=1)
	catalog.grid_rowconfigure(0, weight=1)

	lines = game._store.display_catalog()
	lstCatalog.insert('end', lines)
	lstCatalog['state'] = 'disabled'

def leaderboard_entry(text, window):
	leaderboard.add_entry(text.get(), game.elapsed_time)
	log.set('Successfully submitted to leaderboard.')
	window.destroy()

def leaderboard_prompt():
	username = Tk()
	username.title('Username')
	username.geometry('+125+100')
	username.resizable(FALSE, FALSE)

	lblPrompt = Label(username, text='Enter a username for the leaderboard:')
	entName = Entry(username)
	btnEnter = Button(username, text='Submit', command=partial(leaderboard_entry, entName, username))

	lblPrompt.pack()
	entName.pack()
	btnEnter.pack()

def play_game():
	game.start()

	lblLog['fg'] = 'green'
	log.set('The game has started!')

	update_labels()
	toggle_entries(True)
	clear_entries()

def submit():
	if game.is_correct(aisle.get(), sector.get()):
		lblLog['fg'] = 'green'
		log.set('Correct!')

		clear_entries()
		game.new_round()

		if game.elapsed_time:
			log.set('The game has ended. Time: ' + str(round(game.elapsed_time, 3)))
			leaderboard_prompt()
			resetUI()
		else:
			update_labels()
	else:
		lblLog['fg'] = 'red'
		log.set('Incorrect. Try again.')

def update_labels():
	target_item.set('Item: ' + game.item.get_display_name())
	current_round.set('Round #: ' + str(game.round) + ' of ' + str(game.max_rounds))

def clear_labels():
	target_item.set('Item:')
	current_round.set('Round #:')

def clear_entries():
	aisle.set('')
	sector.set('')

def toggle_entries(state):
	if state:
		entAisle.config(state='normal')
		entSector.config(state='normal')
		btnSubmit.config(state='normal')
	else:
		entAisle.config(state='readonly')
		entSector.config(state='readonly')
		btnSubmit.config(state=DISABLED)

def resetUI():
	clear_labels()
	clear_entries()
	toggle_entries(False)

game = Game(STORE_NAME, 3, 4, 2, 2)
leaderboard = Leaderboard(STORE_NAME)

window = Tk()
window.title('Shuffle Shopper')
window.geometry('500x600')
window.resizable(FALSE, FALSE)

btnStart = Button(window, text='Start Game', command=play_game)
btnCatalog = Button(window, text='Catalog', command=show_catalog)
btnLeaderboard = Button(window, text='Leaderboard', command=show_leaderboard)
btnHelp = Button(window, text='How to Play', command=show_howto)

current_round = StringVar()
current_round.set('Round #:')
target_item = StringVar()
target_item.set('Item:')
aisle = StringVar()
sector = StringVar()
name = StringVar()
name.set('test')
log = StringVar()

lblRound = Label(window, textvariable=current_round)
lblTargetItem = Label(window, textvariable=target_item)
lblAisle = Label(window, text='Aisle:')
entAisle = Entry(window, width='5', textvariable=aisle, state='readonly')
lblSector = Label(window, text='Sector:')
entSector = Entry(window, width='5', textvariable=sector, state='readonly')
btnSubmit = Button(window, text='Submit', command=submit, state=DISABLED)
lblLog = Label(window, width='50', textvariable=log)

btnStart.grid(padx=15, pady=10, row=0, column=0, sticky=(N,W,E,S))
btnCatalog.grid(padx=15, pady=10, row=1, column=0, sticky=(N,W,E,S))
btnLeaderboard.grid(padx=15, pady=10, row=2, column=0, sticky=(N,W,E,S))
btnHelp.grid(padx=15, pady=10, row=3, column=0, sticky=(N,W,E,S))

lblRound.grid(padx=25, row=0, column=1, columnspan=3, sticky=W)
lblTargetItem.grid(padx=25, row=1, column=1, columnspan=3, sticky=W)
lblAisle.grid(padx=25, row=2, column=1, sticky=W)
entAisle.grid(row=2, column=2)
lblSector.grid(padx=25, row=3, column=1, sticky=W)
entSector.grid(row=3, column=2)
btnSubmit.grid(padx=15, row=3, column=3, columnspan=1)
lblLog.grid(padx=15, row=4, column=0, columnspan=4)

window.mainloop()