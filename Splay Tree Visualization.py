import tkinter as tk
from tkinter import *
root = Tk()

class Node:
    """Node Objekt kann linkes und rechtes kind, und predecessor haben, hat einen Key und Data"""
    def __init__(self, key, data):
        self.key = key
        self.left = None
        self.right = None
        self.p = None
        self.data = data
        self.px = 0
        self.py = 0
        self.t = 0

class SplayTree(Node):
    """Ein Splaybaum mit Knoten(nodes) wird initialisiert und der vorgänger wird fesgelegt"""
    def __init__(self, key, data):
        Node.__init__(self, key, data)
        self.root = None                                #useless
        if not self.p:                                  #für alle Knoten in Tree
            self.root = Node(self.key, data)
            self.r = self.root
        self.numrot = 0
        self.pot = 1
        self.count = 0
        self.countr = 0
        self.countl = 0

    def Splay(self, x):
        """initialisiert splaystep und gibt print befehle zurück"""
        print("Splay an Knoten:", x.key)
        self.numrot = 0

        self.potvorher = self.Potential(self.root)
        self.potx = self.TreeWalk(x)
        self.pottroot = self.TreeWalk(self.root)
        while x.p:
            self.SplayStep(x)

        print("2^Rotationen:", 2**self.numrot)
        print("2^Potential vorher:", self.potvorher)
        print("2^Potential nachher:", self.Potential(x))
        print("2^amortisierte Rotationen:", str(((2**self.numrot)*(self.Potential(self.root)))) + "/" + str(self.potvorher))
        print("2^obere Schranke:" ,str(2*(self.pottroot)**3) + "/" + str((self.potx)**3))

    def SplayStep(self, x):
        """rotatiert damit gesuchte knoten die wurzel ist"""
        if not x.p:
            return

        elif not x.p.p and x == x.p.left:           #Zick
            self.rotateright(x.p)

        elif not x.p.p and x == x.p.right:          #Zack
            self.rotateleft(x.p)

        elif x == x.p.left and x.p == x.p.p.left:       #ZickZickR
            self.rotateright(x.p.p)
            self.rotateright(x.p)

        elif x == x.p.right and x.p == x.p.p.right:     #ZickZickL
            self.rotateleft(x.p.p)
            self.rotateleft(x.p)

        elif x == x.p.left and x.p == x.p.p.right:      #ZickZackRL
            self.rotateright(x.p)
            self.rotateleft(x.p)
            #self.rotaterightleft(x.p.p)

        else:                                           #ZickZackLR
            self.rotateleft(x.p)
            self.rotateright(x.p)
            #self.rotateleftright(x.p.p) -zickzag 3b

    def search(self, key):
        """rekursiv; sucht knoten und wendet splay an ihm"""
        if not self.r:
            self.r = self.pred
            self.Splay(self.r)
            return None

        elif key == self.r.key:
            if key == self.r.key:
                self.Splay(self.r)
                return self.r                        #splay auch wenn es knoten nicht gibt
            

        if key < self.r.key:
            self.pred =  self.r
            self.r = self.r.left
            return self.search(key)

        else:
            self.pred = self.r
            self.r = self.r.right
            return self.search(key)

    def insert(self, key, data):
        self.z = Node(key, data)
        self.y = None
        self.x = self.root

        while self.x:
            self.y = self.x

            if self.z.key < self.x.key:
                self.x = self.x.left

            else:
                self.x = self.x.right

        self.z.p = self.y

        if not self.y:                              #useless, empty tree
            self.root = self.z

        elif self.z.key < self.y.key:
            self.y.left = self.z

        else:
            self.y.right = self.z

        self.Splay(self.z)

    def transplant(self, u, v):
        if not u.p:
            self.root = v

        elif u == u.p.left:
            u.p.left = v

        else:
            u.p.right = v

        if v:
            v.p = u.p

    def treemin(self, x):
        while x.left:
            x = x.left
        return x

    def delete(self, key):
        """sucht den zuentfernenden key und löscht ihn und hängt die Teilbäume wieder ran"""
        node = self.search(key)

        if not node:                                #node existiert nicht
            self.r = self.root
            return

        elif node.left or node.right:
            if node:
                if not node.left:
                    self.transplant(node, node.right)

                elif not node.right:
                    self.transplant(node, node.left)

                else:                               #ist ein blatt
                    y = self.treemin(node.right)

                    if y.p != node:
                        self.transplant(y, y.right)
                        y.right = node.right
                        y.right.p = y

                    self.transplant(node,y)
                    y.left = node.left
                    y.left.p = y
            self.r = self.root

    def rotateright(self, x):
        self.numrot += 1                            #anzahl rotationen

        y = x.left
        if not x.p:
            self.root = y

        elif x.p.left == x:
            x.p.left = y

        else:
            x.p.right = y

        y.p = x.p
        x.left = y.right

        if x.left:
            x.left.p = x

        y.right = x
        x.p = y
        self.r = self.root                          #neuer root wird gemerkt

    def rotateleft(self,x):
        self.numrot += 1                            #anzahl rotationen

        y = x.right
        if not x.p:
            self.root = y

        elif x.p.left == x:
            x.p.left = y

        else:
            x.p.right = y

        y.p = x.p
        x.right = y.left

        if x.right:
            x.right.p = x

        y.left = x
        x.p = y
        self.r = self.root                          #neuer root wird gemerkt

    def TreeWalk(self, x):
        if x:
            self.callTreeWalk(x)
            count = self.count
            self.count = 0
            return count

    def callTreeWalk(self, x):
        if x:
            self.callTreeWalk(x.left)
            self.count += 1
            self.callTreeWalk(x.right)

    def Potential(self, x):
        """Mit TreeWalk wird das Potential und mit dem count des Teilbaums multipliziert."""
        self.callPotential(x)
        pot = self.pot
        self.pot = 1
        return pot

    def callPotential(self, x):
        if x:
            self.pot *= self.TreeWalk(x)                #log wird ausgeglichen
            self.callPotential(x.left)
            self.callPotential(x.right)

    def Depth(self, x):
        """Maximum der linken oder rechten Teilbäume wird zurückgegeben"""
        if x:
            if x.left:
                self.callDepthleft(x.left) 
            if x.right:
                self.callDepthright(x.right)
            countr = self.countr
            countl = self.countl
            self.countr = 0
            self.countl = 0
            return max(countr, countl)

    def callDepthleft(self, x):
        if x:
            self.callDepthleft(x.left)
            self.countl += 1
            self.callDepthleft(x.right)

    def callDepthright(self, x):
        if x:
            self.callDepthright(x.left)
            self.countr += 1
            self.callDepthright(x.right)

    def koordinaten(self, node, t, c):
        """jeder Knoten kriegt eine Position als Attribut"""

        if t == 0 or not node.p:                          #root
            node.px = 400
            node.py = 400/ (self.T.Depth(self.T.root) + 2)

        else:
            print(node.p.key, "p", node.p.px)
            if node == node.p.right:
                node.px=node.p.px + 800*2**(-t-1)
                node.py=node.p.py + 50

            elif node == node.p.left:
                node.px=node.p.px-800*2**(-t-1)
                node.py=node.p.py + 50

        print(node.px, node.py, t, self.T.Depth(node), node.key)
        self.circle(node, node.px, node.py, c)

    def draw(self, c):
        self.T.root.t = 0
        c.delete("all")
        self.allnode(self.T.root, self.T.root.t, c)

class TreeVisualizer(SplayTree):
    def __init__(self, root):
        """Visualisiert den SplayBaum"""
        self.frame = Frame(root)
        self.frame.grid()
        self.countr = 1
        self.countl = 1

        #Button - Construct
        self.b = Button(root, text = 'Construct',
                        activebackground = "pink", command = self.get)
        self.b.grid(row = 2, column = 1,
                    ipadx = 20, pady = 2, padx = 10, sticky = "e")

        #Entry
        self.g = Entry(root)
        self.g.grid(row =0, column =1)
        self.h = Entry(root)
        self.h.grid(row=1, column = 1)

        #Entry Label
        self.m = Label(root, text= 'Key')
        self.m.grid(row = 0 , column = 0)
        self.n = Label(root, text = 'Data')
        self.n.grid(row = 1, column = 0)

    def get(self):
        self.b.destroy()
        g = int(self.g.get())
        h = self.h.get()
        #global T
        self.T = SplayTree(g, h)
        self.canvas = Canvas(root, width = 800, height = 400, bg = "white")
        self.canvas.grid(row= 4, column = 1)
        self.draw(self.canvas)

        #self.frame.quit()
        self.button()

    def button(self):
        """buttons von Suchbaum-Operationen werden kreiert und ein command zugeteilt"""
        self.m.grid(sticky = "n", column = 0)
        self.g.grid(ipadx = 100, sticky = "n")
        self.n.grid(sticky = "n", column = 0)
        self.h.grid(ipadx = 100, sticky = "n")

        self.g.delete(0, "end")
        self.h.delete(0, "end")

        self.i = Button(root, text = 'Insert',
                   activebackground = "light green",
                   command = self.ins)
        self.i.grid(row = 2, column = 1,
               ipadx = 20, pady = 2, sticky = "n")

        self.j = Button(root, text = 'Delete',
                   activebackground = "light green",
                   command = self.d)
        self.j.grid(row = 2, column = 2,
               ipadx = 20, pady = 2, sticky = "n")

        self.k = Button(root, text = 'Search',
                   activebackground = "light green",
                   command = self.s)
        self.k.grid(row = 2, column = 0,
               ipadx = 20, pady = 2, sticky = "n")

        #self.frame.quit()

    def s(self):
        self.i.destroy()
        self.j.destroy()
        self.k.destroy()

        g = int(self.g.get())
        h = self.h.get()
        print(self.T.search(g))
        self.draw(self.canvas)
        self.button()

    def d(self):
        self.i.destroy()
        self.j.destroy()
        self.k.destroy()

        g = int(self.g.get())
        h = self.h.get()
        self.T.delete(g)
        self.draw(self.canvas)
        self.button()

    def ins(self):
        self.i.destroy()
        self.j.destroy()
        self.k.destroy()

        g = int(self.g.get())
        h = self.h.get()
        self.T.insert(g, h)
        self.draw(self.canvas)
        self.button()

    def allnode(self, node, t, c):
        """TreeWalk über jeden Knoten"""
        self.koordinaten(node, node.t, c)
        if node.right:
            node.right.t = node.t + 1
            self.allnode(node.right, node.right.t, c)
            c.create_line(node.px + 20, node.py + 20, node.right.px,
                          node.right.py)
        if node.left:
            node.left.t = node.t + 1
            self.allnode(node.left, node.left.t, c)
            c.create_line(node.px, node.py + 20, node.left.px + 20,
                          node.left.py)

    def circle(self, node, x, y, c):
        """malt einen Knoten"""
        c.create_oval(x, y,
                      (x) + 20, (y) + 20, fill="pink")
        c.create_text(x + 10, y + 10, text = node.key)


app = TreeVisualizer(root)
root.mainloop()
