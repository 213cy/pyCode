import asyncio
import winsound


class GameController():

    def __init__(self, ControlSet={'dx': 0.0011, 'dy': 0.002}, *, transQueue = None,dispInfoFcn=None):
        self.loopFlag = True
        self.hookList=[]
        # self.methodDict={'displayON':danmuDispON, 'displayOFF':danmuDispOFF ,'other': otherCMD}
        self.CS = ControlSet
        self.queue = transQueue
        self.disp = dispInfoFcn if dispInfoFcn else self.donothing

    @staticmethod
    def donothing(*a,**b):
        pass


    def danmuDispON(self, player, xxx):
        if player != 'admin':
            return
        if self.transDanmu not in self.hookList:
            self.hookList.append( self.transDanmu )

    def danmuDispOFF(self, player, xxx):
        if player != 'admin':
            return
        self.hookList.remove( self.transDanmu )

    
    def otherCMD(self, player, cmd):
        print(f'来自 {player} 的未知命令({str(cmd)})!')

    def transDanmu(self, data):
        self.queue.put(data)

    def updateControlSet(self, player, value):
        self.CS['dx'] = self.CS['dx'] * value**(0.2)
        self.CS['dy'] = self.CS['dy'] * value**(0.2)
    

    async def controlARun( self , danmuList ):

        while self.loopFlag:

            if danmuList:
                name,cmd = danmuList.pop(0)
                self.disp(f'<<<    get data= ( {name} : {cmd} )')
                
                try:
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    # winsound.Beep(200, 1000)
                except Exception:
                    pass

                if len( self.hookList ) :
                    for method in self.hookList:
                        method((name,cmd))

                if type(cmd)==float :
                    parm = cmd
                    self.updateControlSet(name,parm)

                if type(cmd) == str :
                    tmp=cmd.split('=')
                    M = getattr(self, tmp[0] , None)
                    parm = float(tmp[1]) if tmp[1:] else 1
                    if hasattr(M,'__call__'):
                        M(name,parm)
                    else:
                        self.otherCMD(name,cmd)



            await asyncio.sleep(0.2)
            # time.sleep(1)
        print( 'game logic thread done!' )


    def controlRun(self, lst):
        asyncio.run( self.controlARun( lst ) )

    def stopLoop(self):
        self.loopFlag = False