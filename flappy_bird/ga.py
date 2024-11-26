from flappy import Game
# import flappy

if __name__ == '__main__':
    number_of_birds = 2

    game = Game(number_of_birds)
    while True:
        game_stat, frame_stat = game.play_step(isobserved=True)
        if game_stat == Game.stat['over']:
            break
        elif game_stat == Game.stat['end']:
            game.state = Game.stat['init']
        elif game_stat == Game.stat['wait']:
            game.state = Game.stat['run']

        print(str(len(frame_stat['pipe'])))
    print('asdfsd')
