import numpy as np
import matplotlib.pyplot as plt
import random as r
"""
Ici contaminé=alerté
Contamination direct: une personne contaminé collé à un autre non contaminé le devient instantanement
Contamination pseudo-direct: si une personne bloc le chemin d'une personne contaminé alors il le devient
Vitesse: donner un coefficient de vitesse au point leur faisant avancé plusieurs cases en même temps (qui dépende du nombre de voisin, de l'inertie...)
Obstacle: qui bloque/ comment contourner si besoin?
Mouvements aléatoires des non-contaminés
Zone de danger: pour que tt le monde soit contaminé au bout d'un long temps

                                                                                                      
"""
cpt=0
while cpt<1:
    n=100 #taille map
    h=500 #nombre de points/personnes sur la map
    v=10#perimetre de propagation
    s=4 #taille sortie
    N=500 #nombre d'étape
    
    M=[[0 for _ in range(n)] for _ in range(n)]
    d={}
    # for j in range(10,21):
    #     M[20][j]=4
    #     M[j][20]=4
    for i in range(s):
        for j in range(s):
            M[i][j]=3
    M[s-1][s-1]=0
            
    for i in range(h+1):
        x,y=r.randint(0,n-1),r.randint(0,n-1)
        while M[x][y]!=0:
            x,y=r.randint(0,n-1),r.randint(0,n-1)
        d[i]=(x,y,0,0,0)  #position,état,voisins,voisins alértés
        M[x][y]=1
    
    
    def compteur_voisin(d,M):
        for i in d:
           x,y,a,b,c=d[i]
           cpt=0
           alert=0
           for x0 in range (2*v+1):
               if x-v+x0>=0 and x-v+x0<n:
                   for y0 in range (2*v+1):
                       if y-v+y0>=0 and y-v+y0<n:
                           if (x-v+x0,y-v+y0)!=(x,y):
                              if M[x-v+x0][y-v+y0]!=0 and M[x-v+x0][y-v+y0]!=3 and M[x-v+x0][y-v+y0]!=4:
                                 cpt+=1
                              if M[x-v+x0][y-v+y0]==2:
                                  alert+=1  
           d[i]=(x,y,a,cpt,alert)
        return d
    
    def maj_etat(d,M):
        for i in d:
           x,y,a,b,c=d[i] #b,c=voisins,voisins alertés
           if a!=3:
             if b!=0:
                P=[0 for _ in range (b)]
                for j in range (c):
                   P[j]=1
                if P[r.randint(0,b-1)]==1:
                   M[x][y]=2
                   d[i]=(x,y,1,b,c)
        return d,M
    
    def deb(d,i):
       A,B,C,D,E=d[0]
       M[A][B]=2
       d[i]=(A,B,1,D,E)
       return d
    
    def random_move(d,M):
        for k in d:
         x,y,a,b,c=d[k]
         if a==1:
            m=r.randint(0,1)      
            i,j=x,y
            if x==0 and M[x][y-1]==0:
                m=2
                j-=1
            if y==0 and M[x-1][y]==0:
                m=2
                i-=1
            if y!=0 and m==1 and M[x-1][y]==0:
                i-=1
            if x!=0 and m==0 and M[x][y-1]==0:
                j-=1
            if M[x][y-1]==3 or M[x-1][y]==3 :
                d[k]=i,j,3,b,c
                M[x][y]=0
            if (i,j)!=(x,y):
                d[k]=(i,j,a,b,c)
                M[i][j]=M[x][y]
                M[x][y]=0
        return d,M
         
    """
    Condition de contact affaiblie(si une direction est impossible, l'autre est effectué)
    """
    def random_move(d,M):
        for k in d:
         x,y,a,b,c=d[k]
         if a==1:
            m=r.randint(0,1)      
            i,j=x,y
            if x==0 and M[x][y-1]==0:
                m=2
                j-=1
            if y==0 and M[x-1][y]==0:
                m=2
                i-=1
            if x!=0 and m==1:
               if M[x-1][y]==0:
                   i-=1
               elif y!=0 and M[x][y-1]==0:
                   j-=1
            if y!=0 and m==0:
                if M[x][y-1]==0:
                  j-=1
                elif x!=0 and M[x-1][y]==0:
                   i-=1
            if M[x][y-1]==3 or M[x-1][y]==3 :
                d[k]=i,j,3,b,c
                M[x][y]=0
            if (i,j)!=(x,y):
                d[k]=(i,j,a,b,c)
                M[i][j]=M[x][y]
                M[x][y]=0
        return d,M        
               
    def last(M,i):
        cpt=0
        for k in range(n):
            for j in range(n):
                if M[k][j]==1 or M[k][j]==2:
                    cpt+=1
        if cpt==0:
            return i
        return N
            
    
    def show(n, M,d):
        plt.figure()
        d=deb(d,0)
        k=N
        i=0
        while i<=N and k==N:
            plt.imshow(M,cmap='seismic')
            '''start = update(start, rules_gol)
            plt.gca()'''
            i+=1 
            k=last(M,i)       
            plt.show()
            d,M=maj_etat(d,M)
            d,M=random_move(d,M)
            d=compteur_voisin(d,M)
        print(k)
    cpt+=1
    show(n,M,d)
    
