from turtle import *

class War3Map:
    teamColors = [(0.9, 0.2, 0.2), (0.2, 0.2, 0.9),
                  (0.9, 0.9, 0.2), (0.2, 0.9, 0.2)]

    def __init__(self, playerCount=5, teamCount=4):
        teamCount=4
        self.teamCount = teamCount
        self.dw = pow(pow(1j, 1j), -4j/teamCount)
        self.playerCount = playerCount
        self.teams = []
        for k in range(teamCount):
            self.teams.append(Team(self, k, War3Map.teamColors[k]))

    def update(self, team, player, pxy):
        rw = complex(pxy[0], pxy[1])/pow(self.dw, team)
        for k in range(self.teamCount):
            if k == team:
                continue
            a = rw*pow(self.dw, k)
            self.teams[k].update(player, (a.real, a.imag))


class Team:
    A = 50
    r = [pow(m, 0.5)+pow(n, 0.5) for m, n in zip(range(6), range(1, 7))]
    w = [0,   1.1331,   2.0358,   2.7819,   3.4325,   4.0168]

    def __init__(self, newmap, tN, tC):
        self.warmap = newmap
        self.teamOrd = tN
        self.color = tC
        self.players = []
        self.XYcoor = Team.genxy(tN)
        for k in range(newmap.playerCount):
            p = Point(self, k, self.XYcoor[k])
            self.players.append(p)

        t = Turtle()
        t.ht()
        t.pensize(8)
        self.Line = t
        self.lineUpdate()

    def update(self, playerOrd, pxy, isbubble=False):
        self.players[playerOrd].update(pxy)
        self.XYcoor[playerOrd] = pxy
        self.lineUpdate()
        if isbubble:
            self.warmap.update(self.teamOrd, playerOrd, pxy)

    def lineUpdate(self):
        t = self.Line
        t.clear()
        t.penup()
        t.setpos(self.XYcoor[0])
        t.pendown()
        for k in range(1, self.warmap.playerCount):
            t.setpos(self.XYcoor[k])

    @classmethod
    def genxy(cls, n):
        c = cls.A*pow(1j, n)
        coorRW = [c*a*pow(2, b*1j) for a, b in zip(cls.r, cls.w)]
        return [(k.real, k.imag) for k in coorRW]


class Point(Turtle):

    def __init__(self, team, playerOrd, pos):
        # Turtle.__init__(self)
        # super(Point,self).__init__()
        super().__init__()

        self.shape("circle")
        self.resizemode('user')
        self.turtlesize(1.2, 1.2, 6)
        self.penup()

        self.team = team
        self.color(team.color)
        self.playerOrd = playerOrd
        self.setpos(pos)

        self.onclick(self.glow)     # clicking on turtle turns fillcolor red,
        self.onrelease(self.unglow)
        self.ondrag(self.shift)

    def shift(self, x, y):
        # self.setpos((x, y))
        tracer(False)
        self.team.update(self.playerOrd, (x, y), True)
        tracer(True)

    def update(self, pos):
        self.setpos(pos)

    def glow(self, x, y):
        self.fillcolor("white")

    def unglow(self, x, y):
        self.fillcolor(self.team.color)


def main():
    War3Map()
    return "EVENTLOOP"


if __name__ == "__main__":
    # mode("logo")
    tracer(False)
    msg = main()
    tracer(True)
    print(msg)
    mainloop()
