import random
import pygame as pg
from config import settings
from units import Tower
from units import TimedHint , StringInfo



BLOCK_LENGTH = L = settings.L
SCREENRECT = settings.SCREENRECT
XN = settings.XN
YN = settings.YN
CLIENTRECT = CR = settings.CLIENTRECT
COLOR = settings.COLOR


def route_module_constant_update():
    globals().update(vars(settings))


def route_module_constant_dump():
    tmp = {}
    ggg = globals()
    for k in vars(settings):
        tmp[k] = ggg.get(k, None)
    return tmp

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
INF = 999

class Block():
    def __init__(self, x, y):
        self.sprite = None
        self.Vpos = pg.Vector2(x, y)
        self.index = y*XN+x
        self.rect = pg.Rect(CR.x+x*L, CR.y+y*L, L, L)
        self.occupied = False

        tmp = []
        if y != 0:
            tmp.append(self.index - XN)
        if x != 0:
            tmp.append(self.index - 1)
        if y != YN-1:
            tmp.append(self.index + XN)
        if x != XN-1:
            tmp.append(self.index + 1)

        self.neighbours = tmp
        self.parent = []
        self.distance = INF

    def __repr__(self):
        return f'<Block #{self.index} at ({int(self.Vpos.x)},{int(self.Vpos.y)})>'

    def click(self):
        if self.occupied is False:
            self.sprite.kill()
        elif self.sprite is not None:
            self.sprite.add( self.sprite.containers )
        else:
            self.sprite = Tower(self.rect.center)





class BlockManager():

    @staticmethod
    def update_blocks_state_from_dest(queue):
        # 根据给定的终点队列,更新其他失能节点的parent和distance
        # BFS Breadth First Search
        while len(queue):
            tmp = queue.pop(0)
            dist = tmp.distance + 1
            for k in tmp.neighbours:
                if not k.occupied:
                    if k.distance > dist:
                        k.distance = dist
                        k.parent.clear()
                        k.parent.append(tmp)
                        if k not in queue:
                            queue.append(k)
                    elif k.distance == dist:
                        if tmp not in k.parent:
                            k.parent.append(tmp)
                        # 此处k in queue 必然为 True,不用添加k到queue
                        # 因为dist已经不是最大值,说明之前k就已经被添加到了queue
                        # 再加上dist总是递增的,添加是发生在dist更小的时候
                        # 以后的dist会更大,再次添加也不会使其它节点距离更小

    @staticmethod
    def get_frontier_blocks_of_disable_blocks(block):

        # queue - 失去所有父节点,需要被重新计算最短距离的节点队列
        queue = [] 
        # queue 的初始化
        for k in block.neighbours:
                if not k.occupied:
                    if block in k.parent:
                        k.parent.remove(block)
                        if len(k.parent) == 0:
                            k.distance=INF
                            queue.append(k)

        # queue的边界节点
        frontier = []
        while len(queue):
            # 一个失能节点
            tmp = queue.pop(0)
            # tmp.distance = INF
            # tmp.parent.clear()
            for k in tmp.neighbours:
                if not k.occupied:
                    # 考察的临近节点k源自失能节点,
                    # 是为了保证该节点不是已确定的失能节点
                    if tmp in k.parent:
                        if k not in frontier:
                            frontier.append(k)

                        k.parent.remove(tmp)
                        if len(k.parent) == 0:
                            # 仅源自失能节点的 节点一定是失能节点
                            k.distance=INF
                            queue.append(k)
                            # 失能节点一定不是边界
                            frontier.remove(k)
                            # TimedHint((200,0,0,111), k.rect.center ) 

        return frontier

    def __init__(self,window):
        self.blocklist = [Block(x, y) for y in range(YN) for x in range(XN)]
        for b in self.blocklist:
            b.neighbours = [self.blocklist[k] for k in b.neighbours]
        self.startBlock = self.blocklist[random.randrange(XN*YN)]
        self.endBlock = self.blocklist[random.randrange(XN*YN)]
        while self.endBlock is self.startBlock or self.endBlock in self.startBlock.neighbours:
            self.endBlock = self.blocklist[random.randrange(XN*YN)]

        d1 = self.startBlock.rect.topleft
        d2 = self.endBlock.rect.topleft
        window.door_update(d1,d2)
        self.win = window

        self.endBlock.distance = 0
        self.endBlock.parent = []

        queue = [self.endBlock]
        self.update_blocks_state_from_dest(queue)

        window.road_update(self.get_road_points())

   
    def get_road_points(self):
        tmp = self.startBlock
        road = [tmp.rect.center]
        while tmp != self.endBlock:
            aaa = tmp.parent
            tmp = aaa.pop(random.randrange(len(aaa)))
            aaa.insert(0, tmp)
            road.append(tmp.rect.center)
        return road

    def debug_display_all_info(self):
        for k in self.blocklist:
            StringInfo(str(k.distance), k.rect.topleft ) 
            # StringInfo(str(len(k.parent)), k.rect.center ) 
            StringInfo(str(k.occupied)[0], k.rect.center ) 

    def debug_display_block_info(self,block):
        k = block
        StringInfo(str(k.distance), k.rect.topleft ) 
        # StringInfo(str(len(k.parent)), k.rect.center ) 
        StringInfo(str(k.occupied)[0], k.rect.center ) 
    

    def click(self, pos):
        if not CLIENTRECT.collidepoint(pos):
            return
        
        x, y = pos
        indx, indy = (x-CR.x)//L, (y-CR.y)//L
        posIndex = indx + indy * XN

        clicked_block = self.blocklist[posIndex]

        # self.debug_display_block_info(clicked_block)

        if clicked_block is self.endBlock:
            return

        if clicked_block.occupied:

            clicked_block.parent.clear() 
            clicked_block.distance=INF

            tmp = list(k for k in clicked_block.neighbours if not k.occupied)
            aaa=min(k.distance for k in tmp)
            frontier = list(filter(lambda item:item.distance == aaa, tmp))

            clicked_block.occupied = False
            clicked_block.click()

            self.update_blocks_state_from_dest(frontier)


        else:
            # 先假设该块已经被占据了
            clicked_block.occupied = True

            frontier = self.get_frontier_blocks_of_disable_blocks(clicked_block)
            for k in frontier:
                TimedHint((0,200,0,111), k.rect.center ) 
            self.update_blocks_state_from_dest(frontier)


            if self.startBlock.distance==INF:
                StringInfo("can't plant tower in this block!!!")
                
                # 若此时终点无法到达 则还原
                clicked_block.occupied = False
                frontier = [clicked_block]
                self.update_blocks_state_from_dest(frontier)

            else:
                # 若此时终点可以到达 则还原
                clicked_block.click()
 

        self.win.road_update(self.get_road_points())
        self.win.screen_display()


        # self.debug_display_all_info()

        # print([k.index for k in frontier ] )



