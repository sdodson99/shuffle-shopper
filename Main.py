from GameManager import Game, Leaderboard
from tkinter import *
from functools import partial

STORE_NAME = 'Stevenson'
AISLES = 3
SECTORS = 4
SECTOR_HEIGHT = 2
SECTOR_WIDTH = 2
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600

def show_howto():
	txtInfo['state'] = 'normal'
	txtInfo.delete(1.0, END)
	text = game.how_to_play()
	txtInfo.insert('end', text)
	txtInfo['state'] = 'disabled'

def show_leaderboard():
	txtInfo['state'] = 'normal'
	txtInfo.delete(1.0, END)
	text = leaderboard.display()
	txtInfo.insert('end', text)
	txtInfo['state'] = 'disabled'

def show_catalog():
	txtInfo['state'] = 'normal'
	txtInfo.delete(1.0, END)
	lines = game._store.display_catalog()
	txtInfo.insert('end', lines)
	txtInfo['state'] = 'disabled'

def leaderboard_entry(text, window):
	leaderboard.add_entry(text.get(), game.elapsed_time)
	log.set('Successfully submitted to leaderboard.')
	window.destroy()

def leaderboard_prompt():
	username = Tk()
	username.title('Username')

	width = 450
	height = 100
	positionRight = int(username.winfo_screenwidth()/2 - width/2)
	positionDown = int(username.winfo_screenheight()/2 - height/2)

	username.geometry('{}x{}+{}+{}'.format(width, height, positionRight, positionDown))
	username.resizable(FALSE, FALSE)

	lblPrompt = Label(username, text='Your time was {0}. Enter a username for the leaderboard:'.format(round(game.elapsed_time, 3)))
	entName = Entry(username)
	btnEnter = Button(username, text='Submit', command=partial(leaderboard_entry, entName, username))

	lblPrompt.pack()
	entName.pack()
	btnEnter.pack()

def play_game():
	game.start()
	show_catalog()

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

game = Game(STORE_NAME, AISLES, SECTORS, SECTOR_HEIGHT, SECTOR_WIDTH)
leaderboard = Leaderboard(STORE_NAME)

window = Tk()
window.title('Shuffle Shopper')
positionRight = int(window.winfo_screenwidth()/2 - WINDOW_WIDTH/2)
positionDown = int(window.winfo_screenheight()/2 - WINDOW_HEIGHT/2)
window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, positionRight, positionDown))
window.resizable(FALSE, FALSE)

current_round = StringVar()
current_round.set('Round #:')
target_item = StringVar()
target_item.set('Item:')
aisle = StringVar()
sector = StringVar()
log = StringVar()

btnStart = Button(window, text='Start Game', command=play_game)
btnCatalog = Button(window, text='Catalog', command=show_catalog)
btnLeaderboard = Button(window, text='Leaderboard', command=show_leaderboard)
btnHelp = Button(window, text='How to Play', command=show_howto)
lblRound = Label(window, textvariable=current_round)
lblTargetItem = Label(window, textvariable=target_item)
lblAisle = Label(window, text='Aisle:')
entAisle = Entry(window, width='5', textvariable=aisle, state='readonly')
lblSector = Label(window, text='Sector:')
entSector = Entry(window, width='5', textvariable=sector, state='readonly')
btnSubmit = Button(window, text='Submit', command=submit, state=DISABLED)
lblLog = Label(window, width='50', textvariable=log)
frmInfo = Frame(window, borderwidth=2, relief='sunken', width=500, height=400)
txtInfo = Text(frmInfo, wrap=WORD, state='disabled')
scrInfo = Scrollbar(frmInfo, orient=VERTICAL, command=txtInfo.yview)

frmInfo.grid_propagate(0)
txtInfo['yscrollcommand'] = scrInfo.set

btnStart.grid(padx=15, pady=10, row=0, column=0, sticky=(N,W,E,S))
btnCatalog.grid(padx=15, pady=10, row=1, column=0, sticky=(N,W,E,S))
btnLeaderboard.grid(padx=15, pady=10, row=2, column=0, sticky=(N,W,E,S))
btnHelp.grid(padx=15, pady=10, row=3, column=0, sticky=(N,W,E,S))
lblRound.grid(padx=25, row=0, column=1, columnspan=3, sticky=W)
lblTargetItem.grid(padx=25, row=1, column=1, columnspan=3, sticky=W)
lblAisle.grid(padx=25, row=2, column=1, sticky=W)
entAisle.grid(row=2, column=2,sticky=W)
lblSector.grid(padx=25, row=3, column=1, sticky=W)
entSector.grid(row=3, column=2, sticky=W)
btnSubmit.grid(padx=15, row=3, column=3, columnspan=1, sticky=W)
lblLog.grid(row=4, column=0, columnspan=4)
frmInfo.grid(row=5, column=0, columnspan=4)
txtInfo.grid(column=0, row=0, sticky=(N,W,E,S))
scrInfo.grid(column=1, row=0, sticky=(N,S))

frmInfo.grid_columnconfigure(0, weight=1)
frmInfo.grid_rowconfigure(0, weight=1)

window.mainloop()