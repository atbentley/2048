from game import Game

if __name__ == '__main__':
	game = Game(4)

	cmds = {'w': game.move_up,
		'a': game.move_left,
		's': game.move_down,
		'd': game.move_right}

	print game

	c = raw_input(">>>")
	while game.solvable and c in cmds:
		if cmds[c]():
			game.add_tile()
		print game
		c = raw_input(">>>")
		