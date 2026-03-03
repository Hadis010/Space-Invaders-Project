#!/usr/bin/env python
# coding: utf-8
"""
@author: MUNKHTUUL Khosbayar && DINI Hafsa
"""
# In[8]:


#try:   import as appropriate for 2.x vs. 3.x
import tkinter as tk
import tkinter.messagebox as tkMessageBox
#except:
    #import Tkinter as tk
    #import tkMessageBox
import json 

class Score(object):
        def __init__(self,nom,points,temps):
            self.nom=nom
            self.points=points
            self.temps=temps
        def toFile(self,fich):
            f=open(fich,"w")
            s=self
            json.dump(s.__dict__,f)
            f.close()
        def __str__(self):
            
            return  self.nom+"["+str(self.points)+","+str(self.temps)+"]"
            
        @classmethod
        def fromfile(self,fich):
            f = open(fich,"r")
            d = json.load(f)
            snew=Score(d["nom"],d["points"], d["temps"])
            f.close()
            return snew

class  Resultat(object):
    def __init__(self):
        self.Lescores=[]
    def ajout(self,score):
        self.lesscores.append(score)
    def __str__(self):
        chaine=str(self.Lescores[0])
        for e in self.lescores[1:]:
            chaine=chaine+","+str(self.Lescores[e])
        return  chaine
    
    
    @classmethod
    def fromFile(cls,fich):
        f = open(fich,"r")
        #chargement
        tmp = json.load(f)
        liste = []
        for d in tmp:
            #créer un score
            s=Score(d["nom"],d["points"],d["temps"])
            #l'ajouter dans la liste
            liste.append(s)
        res=Resultat()
        res.Lescores=liste
        f.close();
        return res
    
    def toFile(self,fich):
        f = open(fich,"w")
        tmp = []
        for s in self.Lescores:
        #créer un dictionnaire
            d = {}
            d["nom"] = s.nom
            d["points"] = s.points
            d["temps"] = s.temps
            tmp.append(d)
        json.dump(tmp,f)
        f.close();
    
class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width=600
        height=600
        self.frame = tk.Frame(self.root,width=width,height=height)
        self.frame.pack(padx=10,pady=10)
        self.canvas=tk.Canvas(self.frame,width=400,height=400)
        self.accueil=tk.PhotoImage(file="lose.png")
        self.image=self.canvas.create_image(200,200,image=self.accueil)
        self.player=tk.Entry(self.root)
        self.canvas.create_window(200,350, window=self.player)
        labelp = tk.Label(self.root,text= " enter your name:")
        self.canvas.create_window(80,350, window=labelp)
        self.canvas.pack()
        self.label=tk.Label(self.frame,text="Welcome in SpaceInvaders !! click on the button to start ")
        self.button=tk.Button(self.frame,text="START",command=self.play)
        self.button.pack(side="bottom")
        self.label.pack(side="bottom")
        self.root.mainloop()
    def play(self):
        self.canvas.destroy()
        self.label.destroy()
        self.button.destroy()
        self.game = Game(self.frame,self.root,self.getuser())
        self.game.start_animation()
        self.root.mainloop()
        
    def getuser(self):
        return self.player.get()


# In[9]:


class Game(object):
    def __init__(self, frame,root,player):
        self.frame = frame
        self.root=root
        self.defender = Defender()
        self.fleet=Fleet()
        self.height =600
        self.width =self.fleet.get_width() #la largeur de la fleet des aliens
        self.points=tk.Label(self.root,text="score : "+str(self.defender.score)) #affichage de score de joueur
        self.player=tk.Label(self.root,text="player : "+str(player)) #affichage de nom de joueur
        self.player.pack(side="top")
        self.points.pack(side="top")
        self.canvas = tk.Canvas(self.frame,width=self.width,height=self.height,bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
    def animation(self):
        if self.fleet.smash==True:
            fenetre=tk.Tk() #création d'une nouvelle fenêtre
            tk.Label(fenetre,text="Oups,YOU LOST !!").grid(sticky="snew")
            fenetre.mainloop()
        elif self.fleet.shoot==50:  #si tous les aliens sont morts
            fenetre=tk.Tk() #création d'une nouvelle fenêtre
            tk.Label(fenetre,text="Yey,YOU WON !! votre score: "+str(self.defender.score)).grid(sticky="nsew")
            fenetre.mainloop()
        else :
            self.move_aliens_fleet()
            self.move_bullets() 
            self.fleet.manage_touched_aliens_by(self.canvas,self.defender)
            self.canvas.after(80, self.animation) #on appelle la fonction animation dans 100ms
    def start_animation(self):
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.canvas.after(50, self.animation)
    def move_bullets(self):
        #mouvement de bullet 
        for i in self.defender.fired_bullets :
            if i != None:
                i.move_in(self.canvas)
            
    def move_aliens_fleet(self):
        #mouvement de fleet 
        if self.fleet.smash == False: 
            self.fleet.move_in(self.canvas,self.defender)  
        
    def keypress(self, event):
        dx=0
        if event.keysym =='Left': #si on appuie sur la flèche gauche 
            dx = - self.defender.move_delta
        elif event.keysym =='Right': #si on appuie sur la flèche droite
            dx = self.defender.move_delta
        self.defender.move_in(self.canvas,dx) #mouvement de defender 
        
        if event.keysym =='space': #si on appuie sur la flèche espace 
            x0,y0,x1,y1=self.canvas.coords(self.defender.id) #les coordonnées de defender 
            if len(self.defender.fired_bullets) < self.defender.max_fired_bullets : # si le nombre des éléments dans la liste < nombre max de bullet
                self.defender.fire(self.canvas,x0,y0) #appel de la fonction fire de defender 


# In[10]:


class Defender(object):
    def __init__(self):
        self.width = 20
        self.height = 20
        self.move_delta = 20
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []
        self.score=0
    def install_in(self, canvas):
        x0=(int(canvas.cget('width'))//2)-(self.width// 2)
        y0=int(canvas.cget('height'))-self.height
        self.id=canvas.create_rectangle(x0,y0,x0+self.width,y0+self.height, fill='blue') #on dessine l'image de defender
    def move_in(self,canvas,dx):
        x0,y0,x1,y1=canvas.coords(self.id) #coordonées de defender
        #conditions lorsque le defender touche un de bord gauche ou droite 
        if x0-20 <= 0: 
            dx =dx + 40
        if x1+20 >= int(canvas.cget('width')):
             dx =dx - 40
        canvas.move(self.id,dx,0) #déplacement de defender 
    def fire(self, canvas,x0,y0):
        bullet=Bullet(self) #on crée une instance de la classe bullet 
        self.fired_bullets.append(bullet) #on l'ajoute à la liste de bullets tirés par le defender 
        self.fired_bullets[-1].install_in(canvas,x0,y0) #on dessine le bullet


# In[11]:


# création de l'objet bullet 
class Bullet(object):
    def __init__(self, shooter):  
        self.radius = 5
        self.color = "red"
        self.speed = 30
        self.id = None
        self.shooter = shooter
    def install_in(self, canvas,x0,y0):
        self.canvas=canvas
        xc=x0+self.radius   #x0,y0 sont les coordonnées du point haut gauche du defender
        yc=y0-self.radius
        self.id=canvas.create_oval(xc, yc, xc+2*self.radius, yc-2*self.radius,
        fill=self.color) #on déssine un ovale qui est le bullet dans le canvas du game 
    def move_in(self,canvas):
        y=canvas.coords(self.id)[1] # on récupère l'ordonné du point haut gauche de l'ovale
        if y < 0 : # si l'ordonné dépasse le bord supérieur du canvas 
            canvas.delete(self) #on supprime l'objet bullet du canvas
            self.shooter.fired_bullets.remove(self) #on supprime le bullet de la liste fired_bullets[] du defender
            self.shooter.score-=1 #score
        canvas.move(self.id,0,-self.speed) #le déplacement du bullet dans le canvas


# In[12]:


class Alien(object):
    def __init__(self,file_path):
        self.id = None
        self.alive = True
        self.image=tk.PhotoImage(file=file_path)
        self.collision_image=tk.PhotoImage(file="explosion.gif")
    def touched_by(self, canvas, projectile):
        # on parcourt la liste des bullets tirés et on vérifie si ça touche des aliens
        for i in projectile.fired_bullets: 
            x0=canvas.coords(i.id)[0] #x0,y0,x1,y1 sont les coordonnées de la bullet
            y0=canvas.coords(i.id)[1]
            x1=canvas.coords(i.id)[2]
            y1=canvas.coords(i.id)[3]
            xg=canvas.coords(self.id)[0] #coordonnées de l'alien
            yg=canvas.coords(self.id)[1]
            xd=xg+50
            yd=yg+40 
            if (x0 >= xg and x0 <= xd ) and ( x1 >= xg and x1 <= xd ) and (yg >= y0): # si la bullet touche l'alien 
                projectile.fired_bullets.remove(i) # on supprime la bullet de la liste fired bullet 
                canvas.delete(i.id) #supprimer l'image du bullet du canvas
                self.install_in(canvas, xg, yg, self.collision_image,"alien_mort") #afficher l'image de la collision 
                canvas.after(30, self.remove_image(canvas)) #on retire l'image de la collision
                self.alive=False 
            return  self.alive # retourne la valeur de self alive
    def install_in(self, canvas, x, y, image, tag):
        self.canvas=canvas
        self.id=canvas.create_image(x,y,image=image,tags=tag) #on dessine l'image de l'alien dans le canvas
    def move_in(self, canvas, dx, dy):
        canvas.move(self.id,dx,dy)  # déplacement de l'alien 
    def remove_image(self,canvas):
        canvas.delete(self.collision_image) #supprimer l'image de la collision


# In[13]:


class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        fleet_size =self.aliens_lines * self.aliens_columns
        self.aliens_fleet = []
        self.smash=False # la valeur boolean  qui vérifie  s'il y a un collison entre le fleet des aliens at le defender
        self.shoot=0 #le nombre des aliens tirés dessus
    def install_in(self, canvas):
        x=140
        y=40
        for i in range (self.aliens_lines):
            for j in range (self.aliens_columns):
                alien=Alien("alien.gif")
                alien.install_in(canvas,x,y,alien.image,"alien_vivant")
                self.aliens_fleet.append(alien) # on ajoute l'objet alien à la liste de aliens_fleet 
                x+=70 # le self.aliens_inner_gap + la largeur de l'image
            x=140  # on retourne au debut de la ligne suivant
            y+=60 
    def get_width(self):
        return self.aliens_columns*70+self.aliens_inner_gap*9+40 # le largeur de la fleet
              
    def move_in(self, canvas,shooter):
        cwidth = int(canvas.cget("width"))# recupération de la largeur de canvas 
        x1,y1,x2,y2=canvas.bbox("alien_vivant")  #les coordonnées des aliens vivants
        xs=canvas.coords(shooter.id)[0] #coordonées de defender
        ys=canvas.coords(shooter.id)[1]
        if x2>cwidth or x1<0:# si la fleet touche les bords gauche ou droite 
            self.alien_x_delta=-self.alien_x_delta #inverser le sens de mouvement selon l'axe des abscisses
            self.alien_y_delta=self.alien_y_delta
            canvas.move("alien_vivant",0,self.alien_y_delta) #déplacer les aliens vivants vers le bas 
        canvas.move("alien_vivant",self.alien_x_delta,0) 
        if y2 >= ys : # si la fleet touche le defender 
                self.smash=True
             
    def manage_touched_aliens_by(self,canvas,defender):
        for i in self.aliens_fleet:
             if i.touched_by(canvas,defender) == False: #la valeur de self.alive retournée par chaque alien de la fleet 
                canvas.delete(i)                    # on supprime l'alien  
                self.aliens_fleet.remove(i)         # on le retire de la liste des aliens 
                self.shoot+=1                       
                defender.score+=10                  # score


# In[15]:


SpaceInvaders()


# In[ ]:





# In[ ]:





# In[ ]:




