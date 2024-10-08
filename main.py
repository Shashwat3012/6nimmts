from random import randint
from exceptions import CardNotInHandException, CardParseError

def print_deck(deck):
	print("Current deck situation:")
	for row in deck:
		print(row)

def print_players(players):
	print("Players situation:")
	for num, cards in players.items():
		print(f"Player {num}: {cards}")

def set_up_cards(cards):
	# returns a list containing the card decks.
	# card format is [number, cattle]

	num_of_cards = 105
	# setting up the cards
	for i in range(1, num_of_cards):
		curr_card = [i]
		if i % 5 == 0:
			if i % 10 == 0: 
				# 3 cattles
				curr_card.append(3)	
			elif i % 11 == 0: 
				# 7 cattles oops
				curr_card.append(7)
			else: 
				# 2 cattles
				curr_card.append(2)
			
		elif i % 11 == 0:
			# 5 cattles
			curr_card.append(5)
		else:
			curr_card.append(1)
		cards.append(curr_card)
	# print(cards)
	return cards

def distribute_cards(num_of_players, cards):
	# returns dictionary of each player 1 to num_of_players,
	# with values of a list containing the cards they have in hand
	players = {}
	smallest_index = 0
	largest_index = len(cards) - 1
	for j in range(num_of_players):
		j += 1
		if j not in players:
			players[j] = []
		for _ in range(10):
			index = randint(smallest_index, largest_index)
			# print(smallest_index, largest_index)
			curr_card = cards[index]
			cards.pop(index)
			largest_index -= 1
			players[j].append(curr_card)
	# print("sanity check for number of cards returned:",
	# len(cards) == 104 - num_of_players * 10)
	return [players, cards]

def find_largest_cards_in_row(row):
	num_of_cols = 5
	empty_card = [0, 0]
	card = empty_card
	for l in range(num_of_cols - 1, 0, -1):
		curr_card = row[l]
		prev_card = row[l - 1]
		print("index:", l)
		print("curr card:", curr_card)
		print("prev card:", prev_card)
		if curr_card == empty_card and prev_card != empty_card:
			print("true.")
			card = prev_card
			print("card:", card)
	return card

def set_up_decks(cards, deck):
	num_of_rows = 4
	# setting up empty deck
	deck = [make_new_row([0, 0]) for _ in range(num_of_rows)]

	smallest_index = 0
	largest_index = len(cards) - 1
	initial_cards = []
	for _ in range(num_of_rows):
		index = randint(smallest_index, largest_index)
		curr_card = cards[index]
		cards.pop(index)
		largest_index -= 1
		initial_cards.append(curr_card)
	initial_cards.sort(key = lambda x: x[0])
	for j, card in enumerate(initial_cards):
		deck[j][0] = card

	# print(deck)
	return [deck, cards]

def place_card(players, player, card, deck):
	# places current player's card to the deck
	num_of_rows = 4
	num_of_cols = 5
	empty_card = [0, 0]

	# first, check if card is in player's hand
	if card not in players[player]:
		return [players, deck]

	row = deck[0]
	row_index = 0
	smallest_card = find_largest_cards_in_row(row)

	print("smallest card:", smallest_card)
	# if card is smallest than any of the rows
	print("card is smallest", is_larger_card(smallest_card, card))
	if is_larger_card(smallest_card, card):
		print("here")
		# choose a row to take all cards
		
		if player == 1: # yourself
			row_index = input("You've chosen a card that is smaller than any of the cards in the row. Please choose a row number (1 to 4) to take all cards in the row: ")
			row_index = int(row_index)
		
		else:
			row_index = 1
			
		if row_index < 1 or row_index > num_of_rows:
			row_index = input("The row number you inputted is not valid. Please enter a number between 1 to 4: ")
		row_index -= 1
		row = deck[row_index]
		for c in row:
			players[player].append(c)

		# place current card to new row
		deck[row_index] = make_new_row(card)


	# if row is full:
	elif is_row_full(row):
		# take all cards in the row...
		for c in row:
			players[player].append(c)

		# ...and place current card to deck
		deck[row_index] = make_new_row(card)

	# else, place card
	else:
		# determines which row to place
		for i in range(num_of_rows - 1):
			curr_row = deck[i]
			next_row = deck[i + 1]
			
			# find current last card in row
			curr_small_card = curr_row[0]
			curr_large_card = next_row[0]
			# print("initial large card:", curr_large_card, "initial small card:", curr_small_card)
			for j in range(num_of_cols - 1, 1, -1):
				curr_card = curr_row[j]
				next_card = next_row[j]
				if curr_card == empty_card and curr_row[j - 1] != empty_card:
					curr_small_card = curr_row[j - 1]
				if next_card == empty_card and next_row[j - 1] != empty_card:
					curr_large_card = next_row[j - 1]

			# print("large card:", curr_large_card, "small card:", curr_small_card)
			if is_larger_card(card, curr_small_card) and is_larger_card(curr_large_card, card):
				# this is the current row
				# print("here jusseyo")
				row = curr_row
				row_index = i
				# print("card is between large and small card:", True)
				break

			# largest card case
			elif is_larger_card(card, curr_large_card):
				# print("here!")
				row = next_row
				row_index = i + 1
				# print("card is largest:", True)

		# print("current row situation: ", row)
		row = place_single_card(row, card)
		# print("row after placed: ", row)
		deck[row_index] = row

	# don't forget to remove current card from player's hand
	curr_card_index = players[player].index(card)
	players[player].pop(curr_card_index)
	return [players, deck]

def make_new_row(first_card):
	empty_card = [0, 0]
	return [first_card, empty_card, empty_card, empty_card, empty_card]

def place_single_card(row, card):
	empty_card = [0, 0]
	for i, c in enumerate(row):
		# print("card index in row:", i, "card:", c)
		if c == empty_card:
			row[i] = card
			break
	return row

def is_row_full(row):
	empty_card = [0, 0]
	if row[4] != empty_card:
		return True

def is_larger_card(curr_card, compared_card):
	return curr_card[0] > compared_card[0]

def determine_winners(players):
	current_winner = None
	winning_penalty = 0
	for p, cards in players.items():
		current_penalty = 0
		for c in cards:
			current_penalty += c[1]
		if winning_penalty > current_penalty:
			winning_penalty = current_penalty
			current_winner = p
	return f'The winner is Player {current_winner}! Congratulations.'

def parse_card(card):
	try:
		card = list(card)
		card = card[1:-1]
		number, cattle = int(card[0]), int(card[-1])
		return [number, cattle]
	except ValueError:
		raise CardParseError()

def check_card_in_hand(card, current_deck):
	condition = card in current_deck
	if condition:
		return condition
	raise CardNotInHandException()

def play_game():
	try:
		print("Welcome to 6nimmts!") 
		mode = input("Which difficulty would you like to play? Please enter Easy or Normal: ")
		if mode == "Debug":
			simulate_debug()
		else:
			simulate(mode)
	except KeyboardInterrupt:
		print("Bye!")
		exit()

def simulate_debug():
	win_condition = False
	cards = []

	# modify your card here
	deck = [[[13, 1], [0, 0], [0, 0], [0, 0], [0, 0]],
		[[14, 1], [0, 0], [0, 0], [0, 0], [0, 0]],
		[[23, 1], [0, 0], [0, 0], [0, 0], [0, 0]],
		[[87, 1], [0, 0], [0, 0], [0, 0], [0, 0]]]
	cards = set_up_cards(cards)
	players, cards = distribute_cards(4, cards)

	# modify your own cards
	players[1] = [[32, 1], [96, 1], [45, 2], [23, 1], [17, 1], [56, 1], [3, 1], [85, 2], [11, 5]]
	# deck, cards = set_up_decks(cards, deck)

	# initial deck condition
	print_deck(deck)
	# initial player condition
	print_players(players)

	# 3 turns
	for _ in range(3):
		print("Here are your cards:", players[1])
		cards_to_place = []

		for i in range(4):
			if len(players[i + 1]) == 0: # winner, card is empty
				print(f"Player {i + 1} wins! Congratulations.")
				win_condition = True
				break
			if i == 0:
				print("Your turn")
			else:
				print(f"Player {i + 1}'s turn")
			cards = players[i+1]
			# if player is yourself
			if i == 0:
				print("Please type the card that you would like to place")
				card = input("(Type in format, [<number>, <cattle>]): ")
				try:
					card = parse_card(card)
					# print("parsed card: ", card)
					check_card_in_hand(card, cards)
				except CardParseError:
					card = input("The card format you've entered is invalid. Please enter the card again:")
				except CardNotInHandException:
					card = input("Error: The card you inputted is not in your hand! Please retype the card that you would like to place: ")

			# brute force algo, selecting the worst card
			else:
				cards.sort(key = lambda x:x[0])
				cards.sort(key = lambda x:x[1], reverse = True)
				card = cards[0]
			print("chosen card:", card)
			if type(card) == str:
				# print("hell yeah.")
				card = card[1:len(card) - 1]
				card = card.split(',')
				card = [int(card[0]), int(card[1])]
				# print(card)
			cards_to_place.append((card, i))
		if win_condition:
			break

		cards_to_place.sort(key = lambda x: x[0][0])
		for c, p in cards_to_place:
			players, deck = place_card(players, p + 1, c, deck)
			print('---')
			print_deck(deck)	
		print('---')
		print("end of turn")
		print_deck(deck)

	if win_condition:
		print("Thanks for playing!")
		exit()
	print('===')
	print("final deck condition:")
	print_deck(deck)
	print("---")
	print("final players condition:")
	print_players(players)
	print("calculating winner...")
	print(determine_winners(players))

def simulate(difficulty):
	if difficulty not in ['Easy', 'Normal']:
		difficulty = input("The difficulty you've entered is invalid! Please either enter Easy or Normal: ")

	win_condition = False
	cards = []

	deck = []
	cards = set_up_cards(cards)
	players, cards = distribute_cards(4, cards)
	deck, cards = set_up_decks(cards, deck)

	# initial deck condition
	print_deck(deck)

	# 10 turns
	for _ in range(10):
		print("Here are your cards:", players[1])
		cards_to_place = []

		for i in range(4):
			if len(players[i + 1]) == 0: # winner, card is empty
				print(f"Player {i + 1} wins! Congratulations.")
				win_condition = True
				break

			if i == 0:
				print("Your turn")
			else:
				print(f"Player {i + 1}'s turn")
			cards = players[i+1]

			# if player is yourself
			if i == 0:
				print("Please type the card that you would like to place")
				card = input("(Type in format, [<number>, <cattle>]): ")
				try:
					card = parse_card(card)
					check_card_in_hand(card, cards)
				except CardParseError:
					card = input("The card format you've entered is invalid. Please enter the card again:")
				except CardNotInHandException:
					card = input("Error: The card you inputted is not in your hand! Please retype the card that you would like to place: ")

			# brute force algo, selecting the worst card
			else: # bot
				if difficulty == 'Easy':
					card = cards[randint(0, len(cards) - 1)]
				else: # normal difficulty
					cards.sort(key = lambda x:x[0])
					cards.sort(key = lambda x:x[1], reverse = True)
					card = cards[0]
			print("chosen card:", card)
			if type(card) == str:
				# print("hell yeah.")
				card = card[1:len(card) - 1]
				card = card.split(',')
				card = [int(card[0]), int(card[1])]
				# print(card)
			cards_to_place.append((card, i))

		if win_condition:
			break
		cards_to_place.sort(key = lambda x: x[0][0])

		for c, p in cards_to_place:
			players, deck = place_card(players, p + 1, c, deck)
			print('---')
			print_deck(deck)	
		print('---')
		print("end of turn")
		print_deck(deck)

	if win_condition:
		ask_play_again()
	print('===')
	print("final deck condition:")
	print_deck(deck)
	print("---")
	print("calculating winner...")
	print(determine_winners(players))
	ask_play_again()

def ask_play_again():
	play_again = input("Would you like to play again? Type Yes or No: ")
	if play_again == "Yes":
		difficulty = input("Which difficulty you would like to play? Type Easy or Normal: ")
		simulate(difficulty)
	else:
		print("Thanks for playing! Hope to see you again.")
		exit()

play_game()