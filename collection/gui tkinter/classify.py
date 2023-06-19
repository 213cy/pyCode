from tkinter import *
from tkinter import messagebox

from inspect import signature

def BuiltinFunctions():
    a=0
    r=[]
    b = vars(__builtins__)
    for f,g in b.items():
    #     print('\t\t',f,g)
    #     if isclass(g) and issubclass(g,BaseException):
        if  hasattr( g ,'__cause__' ) :
            continue
        elif type(g)!=type and type(g)!=type(abs):
    #         print('xxxxx', f, g)
            continue
        else: 
            a += 1
            try:
                t = str(signature(g))
                r.append(f+t)
##                print(f, t)
            except ValueError:
                t = g.__doc__
                r.append(t[0:t.find('\n')])
##                print(f,'*',t[t.find('('):t.find('\n')] )
##    print(a,len(r))
    return r

def InitFuncs( isNew ):
    if isNew :
        temp= BuiltinFunctions()
        temp.sort()
        return [ temp, [], [], [], [], [], [] ]

    with open('functiongroups.txt') as f:
            temp = eval( f.read() )
    return list( temp.values() )
        
""""""
class App(Frame):
    heightListbox = [26, 13, 13, 13, 10, 10, 10]
    rowBlock = [0, 0, 0, 0, 1, 1, 1]
    colBlock = [0, 1, 2, 3, 1, 2, 3]
    rowspanBlock = [2, 1, 1, 1, 1, 1, 1]
    nameBlock = [ 'Python Built-in Functions','A', 'B', 'C', 'D', 'E', 'F']
    def __init__(self, master, isNew=False):
        super().__init__(master)
        
        self.blockfuncs = InitFuncs( isNew )
        self.blocks = self.createWidget()
        self.pack()

##        self['highlightthickness'] =2
##        self['takefocus'] =1
        self['bg']='LightYellow'
        
        self.mainblock = 1
        self.setmainlbox( 1 )

        self.bind_all('<Control-s>', self.__saveGroups )
       
    def createWidget(self):
        block = []
        for k in range(7):
            t = Block(self, k, App.nameBlock[k], App.heightListbox[k], self.blockfuncs[k] )
            t.grid( row=App.rowBlock[k], column=App.colBlock[k], rowspan=App.rowspanBlock[k] )
##        t.grid(row=0, column=1, sticky=tk.N+tk.S)
            block.append( t )
        return block

    def setmainlbox(self, sID):
        for k in range(7):
            if k != sID:
                self.blocks[k]['bg']='SystemButtonFace'
                self.blocks[k].aBtn['relief']='groove'
            else:
                self.blocks[k]['bg']='LightBlue'
                self.blocks[k].aBtn['relief']='raised'
        self.mainblock = sID
        
    def upadatAll(self ,sID=None):
        if sID is None :
            sID = self.mainblock
        else:
            self.setmainlbox( sID )
            
        for k in range(7):
            if k != sID:
                temp =[  self.blockfuncs[k][n] for n in self.blocks[k].lbox.curselection() ]
##                print(temp)
                self.blockfuncs[sID].extend( temp )
                for n in temp :  self.blockfuncs[k].remove(n) 
                self.blocks[k].updateListbox(  )

        self.blockfuncs[sID].sort()
        self.blocks[sID].updateListbox(  )

    def __saveGroups(self, e):
        if messagebox.askokcancel('Confirm  Overwrite',
                                  '''Save current function groups into file "functiongroups.txt".\n\
Are you sure you want to overwrite the old contents ?''') :
            with open('functiongroups.txt', mode='w') as f:
                f.write(   str(  {k:m for k,m in zip(App.nameBlock, self.blockfuncs ) }  ) )
    

        
class Block(Frame):

    def __init__(self, master, ID, name, h, listvars):
        super().__init__(master)

        self.master = master
        self.ID = ID
        self.name = name
        self.tkvar = StringVar( value=listvars)

        self.createWidget(h, len(listvars) )
        self.updateTitle( )

        self['borderwidth']=5

        self.bind('<Button-1>', self.setmain )

    def createWidget(self, h, count):
        self.aBtn = Button(self, relief='groove') 
        
        self.yScroll = Scrollbar(self, orient=VERTICAL)
        self.xScroll = Scrollbar(self, orient=HORIZONTAL)
        self.lbox = Listbox(self, listvariable = self.tkvar, height=h, width=30 ,
                            selectmode=EXTENDED,  #MULTIPLE,
##                            justify='right',
                            )
##        self.lbox.selection_set(0)
        for i in range(1,count,2):
            self.lbox.itemconfigure(i, background='#f0f0ff')
        
        self.xScroll['command'] = self.lbox.xview
        self.yScroll['command'] = self.lbox.yview
        self.lbox['xscrollcommand']=self.xScroll.set
        self.lbox['yscrollcommand']=self.yScroll.set
        
        self.aBtn.bind("<Button-1>", self.addfuncs)
        self.lbox.bind('<<ListboxSelect>>', self.updateTitle )
        self.lbox.bind('<Key-Return>', self.returnTyped )
        self.lbox.bind('<Double-1>', self.doubleClicked )

        self.aBtn.pack()
        self.xScroll.pack(side='bottom',fill=X)
        self.lbox.pack(side='left')        
        self.yScroll.pack(side='left', fill=Y)
           
        
    def addfuncs(self,e):
        self.master.upadatAll( self.ID )

    def setmain(self, e):
        self.master.setmainlbox( self.ID )
        
    def returnTyped(self, e):
        self.master.upadatAll( )

    def doubleClicked(self, e):
        self.master.upadatAll( )
            
    def updateTitle(self, e=None ):
##        global even
##        even = e
        self.aBtn['text']= '  >>>  %s (%s/%s) ' % (self.name, len(self.lbox.curselection()), len(self.master.blockfuncs[self.ID]) )
        
    def updateListbox(self):
        self.tkvar.set( self.master.blockfuncs[self.ID] )
        temp = self.lbox.curselection()
##        print(temp)
        if temp :  self.lbox.selection_clear(min(temp), max(temp) )
        self.updateTitle()

        
root = Tk()
root.title('Classify python built-in functions <ctrl+s to save>')
root.geometry("+50+50")
myapp = App(root) # , True )
##myapp = Block(root)
myapp.mainloop()
##root.mainloop()
