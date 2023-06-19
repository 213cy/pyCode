import mmap
import struct

# https://github.com/sides/war3structs
# https://github.com/sides/war3observer
# 本代码应用场景是war3 1.31版,单机观看录像时,
# 通过访问war3进程中的共享内存文件"War3StatsObserverSharedMemory"
# 来获取一些游戏数据

# ++++++++++++++++++++++++++++

def DisplayGameInfo():
        mm = mmap.mmap(-1, 526, "War3StatsObserverSharedMemory",
              offset=0,     access=mmap.ACCESS_READ)

        b = mm.read(); len(b)
        c = struct.unpack('=4xI?IB256s256s', b)
        struct.calcsize('=4xI?IB256s256s')


        ObserverGame = {
          "refresh_rate": c[0],
          "is_in_game": c[1],
          "game_time": c[2],# in ms
          "players_count": c[3],
          "game_name": c[4].rstrip(b'\x00').decode(),
          "map_name": c[5].rstrip(bytes([0])).decode()
        }

        mm.close(); mm.closed

        m,ms=divmod(c[2],60000)
        s,ms=divmod(ms,1000)
        print(f"  ======== Game Info   ({m}'{s}''{ms}ms)   ========")
        for k, v in ObserverGame.items(): print(f'{k:30}', v, sep='\t')
        print(3*'\n')

# ++++++++++++++++++++++++++++

g = mmap.ALLOCATIONGRANULARITY

rpTable = {0x01: 'HUMAN', 0x02: 'ORC', 0x04: 'NIGHTELF',
    0x08: 'UNDEAD', 0x10: 'DEMON', 0x20: 'RANDOM', 0x40: 'SELECTABLE'}
raceTable = ['UNKNOWN', 'HUMAN', 'ORC', 'UNDEAD', 'NIGHTELF', 'DEMON',
             'LAST', 'OTHER', 'CREEP', 'COMMONER', 'CRITTER', 'NAGA']
typeTable = ['EMPTY', 'PLAYER', 'COMPUTER',
    'NEUTRAL', 'OBSERVER', 'NONE', 'OTHER']


# war3structs.observer.ObserverPlayer.sizeof() = 6416738
# 上面这个结构的长度可能是魔兽较新版本中的
# myObserverPlayer.sizeof() = 2510604


def GetObserverPlayerStruct(ConvertedPlayerId):
        
        PlayerId = ConvertedPlayerId-1
        p = 526 + 2510604*PlayerId

        mm = mmap.mmap(-1, g, "War3StatsObserverSharedMemory",
                        offset=p//g * g,     access=mmap.ACCESS_READ)
        mm.seek(p % g)

        fmt = '=36s6BI3B13I'
        b = mm.read(struct.calcsize(fmt))
        c = struct.unpack(fmt, b)
        mm.close(); mm.closed

        ObserverPlayer = {
                "name": c[0].rstrip(bytes([0])).decode(),
                "race_preference": rpTable[c[1]],
                "race": raceTable[c[2]],
                "id": c[3],
                "team_index": c[4],
                "team_color": c[5],
                "type": typeTable[c[6]],
                "handicap": c[7],
                "game_result": ['VICTORY', 'DEFEAT', 'TIE', 'IN_PROGRESS'][c[8]],
                "slot_state": ['EMPTY', 'PLAYING', 'LEFT'][c[9]],
                "ai_difficulty": ['EASY', 'NORMAL', 'INSANE'][c[10]],
                "apm": c[11],
                "apm_realtime": c[12],
                "gold": c[13],
                "gold_mined": c[14],
                "gold_taxed": c[15],
                "gold_tax": c[16],
                "lumber": c[17],
                "lumber_harvested": c[18],
                "lumber_taxed": c[19],
                "lumber_tax": c[20],
                "food_max": c[21],
                "food": c[22],
                "heroes_count": c[23]
        }

        return ObserverPlayer

def playerinfo(player):
        PlayerSturct=GetObserverPlayerStruct(player)
        print(f"  ====== Player >>> {player}({PlayerSturct['type']}) <<< Info ======")
        for k,v in PlayerSturct.items() : print(f'{k:30}',v,sep='\t')
# ++++++++++++++++++++++++++++
if __name__ == '__main__':
        DisplayGameInfo()
        playerinfo(1)




# bytes(filter(None,b))
