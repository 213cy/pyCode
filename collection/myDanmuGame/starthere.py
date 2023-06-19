import threading
from queue import Queue
import logging
import asyncio
# # # # # # # # # # # # # #
import scopeGame
import getDanmu
import gameLogic


logging.basicConfig(filename='aaa.txt', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


lock = threading.Lock()


def displayDebugInfo(infoStr):
    # lock.acquire()
    with lock:
        print(threading.current_thread().name, infoStr)
    # lock.release()
    logging.debug(f'{threading.current_thread().name} {infoStr}')


monitorQ = Queue()
danmuList = []
ControlSet = {'dx': 0.0011, 'dy': 0.002}

displayDebugInfo = None
# danmu = getDanmu.simDanmu(dispInfoFcn=displayDebugInfo)
danmu = getDanmu.bilibiliDanmu(dispInfoFcn=displayDebugInfo)
game = scopeGame.ScopeGame(ControlSet)
control = gameLogic.GameController(
    ControlSet, transQueue=monitorQ, dispInfoFcn=displayDebugInfo)


async def gameARun(danmuList):
    await asyncio.gather(control.controlARun(danmuList),
                         game.gameARun())


def gameRun(danmuList):
    # control.controlRun(danmuList)
    asyncio.run(gameARun(danmuList))

######################################


def sendCmd( cmd = None):
    if cmd :
        danmuList.insert(0, ('admin', cmd))
    else:
        a = input('(type exit to quit)===> ')
        while a != 'exit':
            danmuList.insert(0, ('admin', a))
            print(f'send cmd: {a}')
            a = input('(type exit to quit)===> ')

    print('send command done!')


def end():
    danmu.stopLoop()
    control.stopLoop()
    game.stopLoop()


def displayCmd(n=5):
    danmuList.insert(0, ('admin', 'danmuDispON'))

    for k in range(n):
        a, b = monitorQ.get()
        print(f'===> {a} {b} ')

    danmuList.insert(0, ('admin', 'danmuDispOFF'))


def threadInfo():
    print('current Thread: ', hex(threading.current_thread().ident))
    print('all Threads: ', list(map(lambda a: hex(a.ident), threading.enumerate())))


if __name__ == '__main__':

    tr1 = threading.Thread(target=gameRun, name='server', args=(danmuList,))
    tr2 = threading.Thread(target=danmu.danmuCapture,
                           name='client', args=(danmuList,))
    tr1.start()
    tr2.start()
    ##tr1.join ()
    ##tr2.join ()

    print('exitexitexitexitexit')
