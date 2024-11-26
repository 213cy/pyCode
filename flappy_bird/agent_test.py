from flappy import Game
# import flappy
import random

class agent():
    def __init__(self, disp_flag = False):
        self.counter = 0
        self.disp_flag = disp_flag

    def train(self, loss):
        if self.disp_flag is True:
            print('train',loss)

    def act(self, v):
        if self.disp_flag is True:
            print(v)
        self.counter += 1
        a=random.randint(1,350)

        if v[-1] is False and v[-2] > 3 :
            loss = v[-2]
            self.train(loss)
            return 5 # reset flag = 5

        if a > self.counter:
            return 0
        else:
            self.counter = 0
            return 1 

class game_controller():
    def __init__(self,  number_of_birds):
        self.game = Game( number_of_birds, isobserv = True )
        game_stat, frame_stat = self.game.play_step([0]) # start
        # self.pipe_default = (627, 683, 403, 231)
        self.pipe_default =  frame_stat['pipe']
        self.data = dict.fromkeys(range(number_of_birds),None)

    def step(self,acts):
        data,done = self.data,False
        game_stat, frame_stat = self.game.play_step(acts)

        if game_stat == Game.stat['run']:
            pass
        elif game_stat == Game.stat['over']:
            done = True
        elif game_stat == Game.stat['end']:
            self.game.state = Game.stat['init']
        elif game_stat == Game.stat['wait']:
            self.game.state = Game.stat['run']

        if not done:
            dat2 = frame_stat['pipe'] + self.pipe_default
            for k in frame_stat['bird']:
                ind = k[0]
                reward = (k[1],)
                alive = (k[2],)
                dat1 = k[3:]
                self.data[ind] = list( dat1 + dat2[0] + dat2[1] + reward + alive)

        return data, done

if __name__ == '__main__':
    number_of_birds = 3

    agents = [ agent() for k in range(number_of_birds) ]
    agents[0] = agent(True)
    acts = number_of_birds * [0]
    
    contrl = game_controller(number_of_birds)
    game_over = False

    while not game_over:
        data,game_over=contrl.step(acts)
        # game_stat, frame_stat = game.play_step(acts)
        for k,v in data.items():
            acts[k] = agents[k].act(v)


        # print(acts)

    print('asdfsd')
