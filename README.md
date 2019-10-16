#Splay-Tree-visualization-with-Tkinter---Python

A binary tree has parents and children vertices; from each parent vertice there can maximum be 2 children vertices.

##Splay Tree
A Splay Tree enables basic operations such as search, insert and delete to happen in O(logn) amortized time.

##The Code
The code itself consists of a backend and a front end part. In the backend, all possible rotations that are needed to rotate the splay tree are defined; furthermore when to do which rotation.
In the frontend the tkinter library is used to create a GUI that enables the user to insert the root vertice, and then be able to search, delete or insert more vertices.
When the button is pressed, the according operation is done in the background and all necessary vertices are given to the GUI and shown on the canvas as a tree.
