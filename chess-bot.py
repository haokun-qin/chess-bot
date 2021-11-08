import discord
import os
import berserk
import chess
import chess.svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM



game = 0
draw_offer = 0
move_number = 0
moves = []

client = discord.Client()
session = berserk.TokenSession('lip_Xh7YPXr1khBPlzIH5PKt')
chess_client = berserk.Client(session=session)

board = chess.Board()


@client.event
async def on_ready():
  print('{0.user} has been initialized'
  .format(client))

@client.event
async def on_message(message):
  global game
  global move_number
  global moves
  global draw_offer
  global board
  if message.author == client.user:
    return
  
  msg = message.content

  if message.content.startswith('#move white '): 

  	if (move_number%2 == 1):
  		await message.channel.send('It is black to move.')
  		return 

  	if(game == 1):
  		move = msg.split("#move white ",1)[1]

  		try:
  			board.push_san(move)
  		except:
  			await message.channel.send('Invalid Move.')
  			return 

  		print(board)

  		moves.append(move)

  		print(move_number)
  		print(moves[move_number])
  		move_number = move_number + 1
  		await message.channel.send('```' + str(board) + '```')
  	else:
  		await message.channel.send('Game has not been initialized.')


  if message.content.startswith('#move black '): 
  	
  	if (move_number%2 == 0):
  		await message.channel.send('It is white to move.')
  		return 

  	if(game == 1):
  		move = msg.split("#move black ",1)[1]


  		try:
  			board.push_san(move)
  		except:
  			await message.channel.send('Invalid Move.')
  			return 

  		print(board)

  		moves.append(move)

  		print(move_number)
  		print(moves[move_number])
  		move_number = move_number + 1
  		await message.channel.send('```' + str(board) + '```')
  	else:
  		await message.channel.send('Game has not been initialized.')


  if (message.content == '#undo move'):
  	 board.pop()
  	 move_number = move_number - 1
  	 moves.pop()
  	 print(board)
  	 await message.channel.send('```' + str(board) + '```')
  	 await message.channel.send('Move undone.')


  if (message.content == '#print record'):
  	record = ""
  	n = 0
  	for move in moves:
  		if ((n % 2) == 0):
  			record = record + str(int((n/2)+ 1)) + '.' + ' ' + move
  			n = n + 1
  		else:
  			record = record + ' ' + move + '\n'
  			n = n + 1

  	await message.channel.send('```' + record + '```')

  if (message.content == '#claim checkmate'):
  	await message.channel.send(board.is_checkmate())

  if (message.content == '#claim stalemate'):
  	await message.channel.send(board.is_stalemate())

  if (message.content == '#claim threefold repetition'):
  	await message.channel.send(board.can_claim_threefold_repetition())

  if (message.content == '#claim fifty moves'):
  	await message.channel.send(board.can_claim_fifty_moves())

  if (message.content == '#claim draw'):
  	await message.channel.send(board.can_claim_draw())

  if (message.content == '#offer draw'):
  	draw_offer = 1
  	await message.channel.send('A draw has been offered.\nRespond with "#I accept" or "#I decline"')

  if (message.content == '#I accept'):
  	if (draw_offer == 1):
  	    draw_offer = 0
  	    await message.channel.send('The game is drawn.')
  	    game = 0
  	else:
  		await message.channel.send('No draw offer sent.')

  if (message.content == '#I decline'):
  	if (draw_offer == 1):
  	    draw_offer = 0
  	    await message.channel.send('The game continues.')
  	else:
  		await message.channel.send('No draw offer sent.')

  if (message.content == '#start chess game'):
  	if (game == 0):
  	    game = 1
  	    await message.channel.send('```' + str(board) + '```')
  	    await message.channel.send('Game has been initialized.')
  	else:
  		await message.channel.send('Game has already been initialized.')


  if (message.content == '#reset game'):
  	draw_offer = 0
  	game = 0
  	move_number = 0
  	board = chess.Board()
  	moves = []
  	await message.channel.send('Game Reset.')
  	await message.channel.send('```' + str(board) + '```')


  if (message.content == '#chess help'):
  	await message.channel.send('```"#start chess game" starts a chess game.\n"#move white [a]"" performs move [a] for white.\n"#move black [b]" performs move [b] for black.\n'
  		+ '"#reset game" resets the game.\n"#claim checkmate" checks if there is a checkmate on the board.\n'
  		+ '"#claim stalemate" checks if there is a stalemate on the board.\n"#claim threefold repetition" checks if there is a threefold repetition on the board.\n"'
  		+ '"#claim fifty moves" checks if a 50 move draw can be claimed.\n"#claim draw" checks if a draw can be claimed.\n"#offer draw" offers a draw\n"#undo move" undoes the last move.\n'
  		+ '"#print record" prints the record of the current game.```')





client.run(os.getenv('BOT-TOKEN'))  