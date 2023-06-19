import pandas as pd
import numpy as np
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime


mpl.rcParams['toolbar'] = 'None'

##fig = plt.figure()
##fig = plt.figure(figsize=(12.8 ,  7.19))
##fig=plt.gcf()
fig = plt.figure(figsize=(0.6*16 ,  0.6*9))
fig.patch.set_facecolor('#9ACD32')#'0.2')
plt.ioff()
#fig.tight_layout()


cmap = plt.get_cmap('Pastel2')#('Set2')#
cmap2 = mpl.colors.ListedColormap(cmap.colors,'mycmap')
cmap2.set_over('0.96')

gs = fig.add_gridspec (2,3, width_ratios=(2, 5.3, 2), height_ratios=(1, 1),
                       left=0.01, right=0.99, bottom=0.01, top=0.99,
                       wspace=0.01, hspace=0.01)
ax = fig.add_subplot(gs[:,1],xlim=(-0.4,30.4),ylim=(-0.4,30.4))
ax.invert_yaxis()
ax.set_aspect('equal')
##ax.set_axis_off()
ax1 = fig.add_subplot (gs[0,0], fc = cmap.colors[0])
ax1.set_adjustable( 'datalim')
ax1.set_aspect('equal')
ax1.set_autoscale_on(False)
##ax1.autoscale(False)
##ax1.set_ylim(0,534/210)
##ax1.set_xlim((0,1))

ax1.set_ylim((0,1.3))
#ax1.set_axis_off()
ax2 = fig.add_subplot (gs[0,2], fc = cmap.colors[1])
##ax2.set_axis_off()
ax3 = fig.add_subplot (gs[1,0], fc = cmap.colors[2], xticks=[], yticks=[])
##ax3.set_axis_off()
ax4 = fig.add_subplot (gs[1,2], fc = cmap.colors[4], xticks=[], yticks=[])
##ax4.set_axis_off()


n=31
(x,y)=np.meshgrid(range(n),range(n))
a1=np.arange(30)
a2=a1/40
z=a1[:,None] @ a2[None,:]

fig.sca(ax)
gameboard = plt.pcolormesh(x, y, z.astype('uint'), cmap=cmap2 , norm=plt.Normalize(0,cmap.N),
                           edgecolors='k',linewidths=0.01,zorder=0,
                          ) #
gamemap = gameboard.get_array()




class player():
    """..........."""
    a=np.arange(-15.5,16,1)
    b=a*a
    c=b[:,None] + b[None,:]
    d=255*(c<0.5*0.5+15.5*15.5)
    alpha=Image.fromarray(d.astype('uint8'),'L')
        
    def __init__(self, t=0, p=(15,15),v=0.1,d=(-2,1), filename='m.jpg'):
        #super().__init__(*args, **kwargs)
        self.team = t
        self.name = 'MathWorks'
        self.position= p
        self.velocity= v
        x,y=d; l=abs( x+1j*y)
        self.direction = (x/l, y/l)
        self.bump = 0
        self.target = (25,25)
        
        self.Image = Image.open(filename).resize((40,40))
        IM=Image.open(filename).resize((32,32))
        IM.putalpha( player.alpha )
        self.pic = ax.imshow(IM, interpolation='none')
        self.pic.set_extent((p[0]-0.8,p[0]+0.8,p[1]+0.8,p[1]-0.8) )
             
    def updatePosition(self):
        k = self.velocity
        x,y =   ( v+k*d for v,d in zip(self.position,self.direction)   )
        self.position = (x,y)
        self.pic.set_extent((x-0.8,x+0.8,y+0.8,y-0.8) )
        if x<0 or y<0 or x>=30 or y>=30 :
            return -1
        return int(x) + 30*int(y)

    def composeDirecton(self,primalD):
        x,y = self.position
        xt,yt=self.target
        dtx,dty =  xt-x,yt-y
        dpx,dpy = primalD

        temp = (dtx+1j*dty) / (dpx+1j*dpy)
        x,y = temp.real,temp.imag
        if x<=0 :
            return primalD
##        l1 = abs(temp)
        l2 = abs(dtx+1j*dty)
        x,y = dtx*x/l2 + dpx*y , dty*x/l2 + dpy*y
        l = abs(x + 1j* y)
        return x/l,y/l

        



        
    def updateDirection(self):
        dx,dy = self.direction
        if dx == 0:
            self.direction=player.composeDirecton (self, (dx,-dy) )
            return
        if dy ==0:
            self.direction=player.composeDirecton (self, (-dx,dy) )
        k = self.velocity
        x,y = self.position
        x0,y0 = x-k*dx , y-k*dy
        xc,yc = max(int(x),int(x0)),max(int(y),int(y0))
##        print(f'as{dx: <8.2f}{dy: <8.2f}   {xc: <8.2f}{yc: <8.2f}df')
        dxc,dyc = x0-xc, y0-yc

        if abs( dy*dxc) >  abs(dyc*dx):
##            breakpoint()
            self.direction=player.composeDirecton (self, (dx,-dy) )
        else:
            self.direction=player.composeDirecton (self, (-dx,dy) )
                
        

##        if int(x0) is int(x):
##            self.direction=(dx,-dy)
##        elif int(y0) is int(y):
##            self.direction=(-dx,dy)
##        else:
##            self.direction=(-dx,-dy)
                
        

gp = player()

#patch = mpl.patches.Circle((10.8, 10.8), radius=0.8, transform=ax.transData)
#patch = mpl.patches.Circle((10.5, 10.5), radius=0.5)
#im.set_clip_path(patch)
for n in range(6):
##    mpl.image.AxesImage(
    ax1.imshow(gp.Image, extent=(0.05,0.05+1.3/8,1.3*n/7,1.3*n/7+1.3/8) )#, transform=ax1.transAxes )
    

    
ax1.text(0.25, 1.3*5/7+1.3/8/2, gp.name,
     #   horizontalalignment='left',  verticalalignment='top',
##         transform=ax1.transAxes,
         bbox={'facecolor': 'red', 'alpha': 0.4, 'pad': 4,'lw':0})


fig.show()
fig.canvas.draw()
##plt.show()gamemap[2]


def run(data):

    domain =  gp.updatePosition()
        
    if domain < 0 :
        print( f'{gamemap[domain]},{domain}')
        gameboard.set_array( gamemap )
        gp.updateDirection()
    elif gamemap[domain] != gp.team :
        print( f'{gamemap[domain]},{domain}')
        gameboard.set_array( gamemap )
        gp.updateDirection()
        gamemap[domain] = gp.team
        gp.bump =gp.bump+1
##        print( f'bump times: {gp.bump}  # direction: {gp.direction}  # position: {gp.position}')

    
    
    #p.set_extent( (k + data/50 for k in p.get_extent() ) )
    if gp.bump > 400 :
        ani.event_source.stop()
        #ani.pause()

    return gameboard,gp.pic,
#ani = animation.FuncAnimation(fig, run, data_gen, interval=40, init_func=init)
ani = mpl.animation.FuncAnimation(fig, run, interval=20, blit=True)

input('--> ')

'''
imgplot = ax.imshow(img)
transform = mpl.transforms.Affine2D().translate(tx, ty)
imgplot.set_transform(transform + ax.transData)
'''
