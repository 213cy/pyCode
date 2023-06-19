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

functionlists = BuiltinFunctions()
functionlists.sort()
##print(functionlists[0:4])
##print(len(functionlists),type(functionlists) )
""""""
class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.blocks = self.createWidget()
        print(len(self.blocks))
        self.pack()
       
    def createWidget(self):
        block = []
        t = Block(self, 'Python Built-in Functions' ,26, functionlists )
        t.grid(row=1,column=0)
        block.append( t )

        t = Block(self, 'A', 10, [] )
        t.grid(row=0,column=1)
        block.append( t )

        t = Block(self, 'B', 10, [] )
        t.grid(row=0,column=2)
        block.append( t )

        t = Block(self, 'C', 10, [] )
        t.grid(row=0,column=3)
        block.append( t )

        t = Block(self, 'D', 5, [] )
        t.grid(row=1,column=1)
        block.append( t )

        t = Block(self, 'E', 5, [] )
        t.grid(row=1,column=2)
        block.append( t )

        t = Block(self, 'F', 5, [] )
        t.grid(row=1,column=3)
        block.append( t )
        
        return block
            
class Block(Frame):

    def __init__(self, master, name, h, listvars):
        super().__init__(master)
        self.bg='cyan'
        self.borderwidth=5
        self.padx=10
        self.pady=10
        self.justify=20
        self.relief = 'GROOVE'
        self.listvar = listvars
        self.tkvar = StringVar(value=self.listvar)
        count = len(listvars)
        atitle = f'{name} ({len(listvars)})'
        self.createWidget(count, h, atitle)
##        self.pack()

    def createWidget(self,count,h,atitle):
        print(atitle)

        self.tFrame = LabelFrame(self,bg='lightyellow',text='ttttt',padx=10,pady=10, height=100, width=200)
        self.tFrame.pack(side = TOP,fill=Y)
        self.bFrame = LabelFrame(self,bg='red',text='bbbbb',padx=10,pady=10)
        self.bFrame.pack(side = BOTTOM ,fill=X)
        
        self.aLab = Label(self.tFrame, text=atitle,bg='cyan' ) # {len(self.listvar)}
        
##        
##        self.yScroll = Scrollbar(self, orient=VERTICAL)
####        t.grid(row=0, column=1, sticky=tk.N+tk.S)
##        self.xScroll = Scrollbar(self, orient=HORIZONTAL)
##
##        
##        self.lbox = Listbox(self, listvariable = self.tkvar,
##                            height=h, width=30 ,
####                            justify='right',
##                            selectmode=EXTENDED,  #MULTIPLE,
##                            xscrollcommand=self.xScroll.set,
##                            yscrollcommand=self.yScroll.set)
####        print(len(self.tkvar.get() ))        
##        for i in range(1,count,2):
##            self.lbox.itemconfigure(i, background='#f0f0ff')
##            
##        self.lbox.selection_set(0)
        
##        self.xScroll['command'] = self.lbox.xview
##        self.yScroll['command'] = self.lbox.yview


        self.aLab.pack()
        
##        self.xScroll.pack(side='bottom',fill=X)
##        self.lbox.pack(side='left')        
##        self.yScroll.pack(side='left', fill=Y)
           
        self.bbtn = Button( self.bFrame, text='>>>',relief = GROOVE )     
        self.bbtn.pack(side=LEFT)
        self.bbtn2 = Button( self.bFrame, text=atitle )       
        self.bbtn2.pack(side=LEFT)
        
    def songhua(e,x):
        messagebox.showinfo('asdfs','sdfsd')
        print(33*'*')


root = Tk()
myapp = App(root)
##myapp = Block(root)
##myapp.mainloop()

root.mainloop()
