import numpy as np
import matplotlib.pyplot as plt
import random as r

g=12 #g
N=1000 #taille map
n=70 #nombre de boules
R=N//30 #rayon boules
L=N//20 
M=[[0 for _ in range(N+1)]for _ in range(N+1)]
d={}
dt=0.005
t=100000
s=1 #decris le changement d'étape
hh=int(N*15/10) #hauteur barriere
p=2.15 #coeff de la pente
yo,xo=int(N/2),int(N*15/10) #position de l'obstacle
rrr=105 #rayon obstacle

e=0.7 #coefficient d'amortissement boule/sol
e1=1 #coefficient d'amortissement boule/boule
def compatible(x,y,d):
    if (x,y)==(0,0):
        return False
    for j in d:
        a,b,_,_=d[j]
        if ((x-a)**2 +(y-b)**2)< 4* R**2:
            return False
    return True

for l in range(n):
    x,y=0,0
    while compatible(x,y,d)==False:
        x,y=r.randint(R,N-R-L),r.randint(L+R,N-R-L)
    d[l]=(x,y,(0,0),(0,0))

########
def poids(d):
    for j in d:
        x,y,v,a=d[j]
        ax,ay=a
        ax+=g
        a=ax,ay
        d[j]=x,y,v,a
    return d


def maj_vitesse(d,d1):
    for j in d:
        x1,y1,v1,a1=d1[j]
        x,y,v,a=d[j]
        vx1,vy1=v1
        vx,vy=v
        ax1,ay1=a1
        ax,ay=a 
        v=(vx+(ax+ax1)*dt/2,vy+(ay+ay1)*dt/2)
        d[j]=x,y,v,(ax,ay)
    return d

def maj_position(d,d1):
    for j in d:
        x1,y1,v1,a1=d1[j]
        x,y,v,a=d[j]
        vx1,vy1=v1
        vx,vy=v
        x=x+(vx+vx1)*dt/2
        y=y+(vy+vy1)*dt/2
        d[j]=x,y,v,a
    return d

def bords_bas(d,s):
    for j in d:
        x,y,v,_=d[j]
        vx,vy=v
        if x>s*N-R-L and vx>2:
               vx=-e*vx
               v=(vx,vy)
               d[j]=x,y,v,_ 
        elif x>s*N-R-L and vx>-1 and vx<2: 
               d[j]=x,y,(0,vy),(0,0)
        else:
               d[j]=x,y,v,(g,0)
        if y>N-R-L and vy>0.5:
            v=(vx,e*-vy)
            d[j]=x,y,v,_
        if y<R+L and vy<0.5:
            v=(vx,e*-vy)
            d[j]=x,y,v,_
        if (y>N-R-L or y<R+L) and vy>-0.5 and vy<0.5:
            d[j]=x,y,(vx,0),_
        if s==2: 
           if abs(x - (hh-20) - y/p) <=2 and y<N*p/5 and y>10:
              q=np.arctan(p)
              va=vx*np.cos(q)+vy*np.sin(q)
              vb=-vx*np.sin(q)+vy*np.cos(q)
              vb=-e*vb
              vx=va*np.cos(q)-vb*np.sin(q)
              vy=va*np.sin(q)+vb*np.cos(q)
              v=(vx,vy)
              d[j]=x,y,v,_
           if abs(x - (hh-20) - (N-y)/p) <=2 and y> N - N*p/5 and y<N-10:
               q=np.arctan(-p)
               va=vx*np.cos(q)+vy*np.sin(q)
               vb=-vx*np.sin(q)+vy*np.cos(q)
               vb=-e*vb
               vx=va*np.cos(q)-vb*np.sin(q)
               vy=va*np.sin(q)+vb*np.cos(q)
               v=(vx,vy)
               d[j]=x,y,v,_
    return(d)

def obstacle(d):
    for j in d:
        x,y,v,a=d[j]
        x1,y1,v1=xo,yo,(0,0)
        if ((x-x1)**2 +(y-y1)**2)<(R+rr)**2:
            if y!=y1:
                q=np.arctan((x1-x)/(y1-y))
            else:
                q=np.pi               
            vx,vy=v
            vx1,vy1=v1
            va=-vx*np.cos(q) + vy*np.sin(q)
            vb=vx*np.sin(q) + vy*np.cos(q)          
            vb=-vb
            vx=-va*np.cos(q) + vb*np.sin(q)
            vy=va*np.sin(q) + vb*np.cos(q)
            v=(vx,vy)
            d[j]=x,y,v,a
    return d


def maj_matrice(d,s):
    M=[[0 for _ in range(N+1)]for _ in range(2*N+1)]
    for i in range(0,N):
        for t in range(8):
          M[s*N-L+t][i]=1
          M[2*i][N-L+t]=1
          M[2*i][L-t]=1
    for i in range (hh,hh+(int(2*N/10) )):
        j=int(i*p - hh*p)
        for t in range(20):
          M[i+t][j]=1
          M[i+t][-j]=1
    for j in d:
        x,y,_,_=d[j]
        x,y=int(x),int(y)
        for i in range(x-R,x+R):
          for j in range(y-R,y+R):
             if ((x-i)**2 +(y-j)**2)<R**2:
                 M[i][j]=2
    for i in range(xo-rr,xo+rr):
        for j in range(yo-rr,yo+rr):
            if ((xo-i)**2 + (yo-j)**2)<rr**2:
              M[i][j]=1
    return M


    
####
def double_contact(d,s):
    for j in d:
        c=-1
        for k in d:
            x,y,v,a=d[j]
            x1,y1,v1,a1=d[k]
            if ((x-x1)**2 +(y-y1)**2)<4*R**2:
                vx1,vy1=v1
                if x>s*N-R-L-10:
                   if vx1**2+vy1**2<20:
                      c+=1
        if c==2:
            d[j]=x,y,(0,0),a
    return d
            
def contact(d,h,s):
    f=[]
    for j in d:
     if j not in f:
        for k in d:
           if j!=k and h[j,k]==0:
              x,y,v,a=d[j]
              x1,y1,v1,a1=d[k]
              if ((x-x1)**2 +(y-y1)**2)<4*R**2:
                  f.append(k)
                  h[j,k]=0
                  if y!=y1:
                     q=np.arctan((x1-x)/(y1-y))
                  else:
                      q=np.arccos(0)                
                  vx,vy=v
                  vx1,vy1=v1
                  va=-vx*np.cos(q) + vy*np.sin(q)
                  va1= -vx1*np.cos(q) + vy1*np.sin(q)
                  vb=vx*np.sin(q) + vy*np.cos(q)
                  vb1=vx1*np.sin(q ) +vy1*np.cos(q)           
                  vb,vb1=vb1,vb
                  va,va1=e1*va,e1*va1
                  vx=-va*np.cos(q) + vb*np.sin(q)
                  vy=va*np.sin(q) + vb*np.cos(q)
                  vx1=-va1*np.cos(q) + vb1*np.sin(q)
                  vy1=va1*np.sin(q) + vb1*np.cos(q)
                  if x>s*N-L-R and vx>0:
                         vx=0
                  if x1>s*N-L-R and vx1>0:
                         vx1=0
                  v=(vx,vy)
                  v1=(vx1,vy1)
                  d[j]=x,y,v,a
                  d[k]=x1,y1,v1,a1
    return d,h

def controle(d,s):
    Sup=[]
    for j in d:
        x,y,v,_=d[j]
        vx,vy=v
        if vx**2 + vy**2<9 and x>s*N-R-L-2:
            v=(0,0)
            d[j]=x,y,v,_
        if x>9*N/5:
            Sup.append(j)
    for j in Sup:
        del(d[j]) #élimine les boules du bas
    return(d)

"""
Projections: si x1,y1>x,y
va1=vx1*np.cos(q)+vy1*np.sin(q)
vb1=-vx1*np.sin(q)+vy1*np.cos(q)


vx1=va1*np.cos(q)-vb1*np.sin(q)
vy1=va1*np.sin(q)+vb1*np.cos(q)
   """ 
h={}
for j in d:
    for k in d:
        h[(j,k)]=0


def maj_h(h):
    for i in h:
        if h[i]!=0:
            h[i]-=1
    return h  

def vtot(d):
    vtot=0
    for j in d:
        _,_,v,_=d[j]
        vx,vy=v
        vtot+=np.sqrt(vx**2 + vy**2)
    return vtot



d=poids(d)

d0=d.copy()
d1=d.copy() #contient les valeurs de d avant la mise à jour

for k in range (10):
   rr=rrr 
   for l in range(n):
       x,y=0,0
       while compatible(x,y,d)==False:
           x,y=r.randint(R,N-R-L),r.randint(L+R,N-R-L)
       d[l]=(x,y,(0,0),(0,0))
   d=poids(d)
   d0=d.copy()
   for i in range(t):
     h= maj_h(h)
     d1=d.copy()
     d=maj_position(d,d1)
     d,h=contact(d,h,s)
     d=maj_vitesse(d,d1)
     d=bords_bas(d,s)
     d=double_contact(d,s)
     d=controle(d,s)
     d=obstacle(d)
     if len(d)<int(n/10):
        print(i)  
        break
     if i%500==0:
       M=maj_matrice(d,s)
       plt.figure()
       plt.imshow(M, cmap='magma_r')
       plt.show()
     if s==1 and i%10000 ==9999:
        s=2
        if s==2:
            d=poids(d)
   s=1
   print('hello')      

"""d=d0
   s=1
   for i in range(t):
      h= maj_h(h)
      d1=d
      d=maj_position(d,d1)
      d,h=contact(d,h,s)
      d=maj_vitesse(d,d1)
      d=bords_bas(d,s)
      d=double_contact(d,s)
      d=controle(d,s)
      if len(d)<int(n/10):
          print(i)
          break
      if i%2500==0:
         M=maj_matrice(d,s)
         plt.figure()
         plt.imshow(M, cmap='magma_r')
         plt.show()
      if s==1 and i%10000 ==9999: 
          s=2
          if s==2:
              d=poids(d)"""
