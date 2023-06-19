# startprocessandloadmodule
# start process and load module

import multiprocessing
import winsound

# 改变下面两行isrun的值,并预测程序的输出
isrunA = True #False
isrunB = True #False

a,b,c,d=2,[2,2,2],[2,2],multiprocessing.Value('d',22)
def bbb(a,b,c,d):
##    global a,b,c,d
    a,b[1],c=1,1,[1,1]
    d.value=11

    if isrunA : winsound.Beep(200,1000)
    print('1111  ',a,b,c,d.value)


if __name__=='__main__':
    p1 = multiprocessing.Process(target=bbb,args=(a,b,c,d))
    p1.start()
    if isrunB : p1.join()  
    print('2222  ',a,b,c,d.value)

print('3333  ',a,b,c,d.value)

a=('load Module'':::::::'
 'end'
     '   endendendend')
print(a)
