from cProfile import label
from cgitb import text
from distutils.command.config import config
import tkinter as tk
from array import array
from decimal import ROUND_UP
from email import message_from_binary_file
import json
from operator import countOf
from posixpath import join
from pydoc import Helper
from random import random, randrange,choice
from tkinter import font
from turtle import color, width
import numpy as np
import pandas as pd
from copy import copy, deepcopy
from tkinter import messagebox 

# Pre-Requuisite
Item=[
    {"itemkey":1,"Item_Width":1,"Item_Height":1,"Availability":1,"ItemName":"1*1"},
    {"itemkey":2,"Item_Width":2,"Item_Height":1,"Availability":2,"ItemName":"1*2"},
    {"itemkey":3,"Item_Width":3,"Item_Height":1,"Availability":3,"ItemName":"1*3"},
    {"itemkey":4,"Item_Width":4,"Item_Height":1,"Availability":4,"ItemName":"1*4"},
    {"itemkey":5,"Item_Width":2,"Item_Height":2,"Availability":4,"ItemName":"2*2"},
    {"itemkey":6,"Item_Width":3,"Item_Height":3,"Availability":9,"ItemName":"3*3"},
]
ItemColor=[
    {"item_ID":1,"Color":"darkseagreen1"},
    {"item_ID":2,"Color":"lightskyblue"},
    {"item_ID":3,"Color":"azure"},
    {"item_ID":4,"Color":"cadetblue1"},
    {"item_ID":5,"Color":"chartreuse"},
    {"item_ID":6,"Color":"darkorchid1"},
    {"item_ID":7,"Color":"lightseagreen"}
]
Item_List=[]
#BoardSize
Width=5
Height=5
Player_Step=(Width-1)*(Height-1)
MainGrid=[]
SubGrid=[]
Label=[]
my_label=tk.Label
window = tk.Tk()


#Function
def get_item_by_key(key,keyName,ListName):
    return next((item for item in ListName if item[keyName] == key), None)

def Initiate_Game():
    global MainGrid 
    global SubGrid 
    global my_label
    global Label
    SubGrid = np.full((Width,Height),-1)
    MainGrid = Plot_Item(np.zeros((Width,Height)))
    # Initialize the game

    List=[dict['itemkey'] for dict in Item_List]
    List.sort()
    row_numb=0
    for Data in set(List):
        itemDetails=get_item_by_key(Data,"itemkey",Item)
        my_label=tk.Label(window,text='Item'+ str(itemDetails["ItemName"]) +' left: '+ str(List.count(Data)))
        Label.append(my_label)
        my_label.pack(side="left",expand=True)
        row_numb+=1

def Plot_Item(array):
    global Player_Step
    array_height, array_width = np.array(array).shape
    itemcount=array_height if array_height>array_width else array_width
    mx_Grid=array_height*array_width
    item_width=0
    item_height=0
    item_availability=0
    key_Value=1

    while mx_Grid-round(mx_Grid*0.2)>item_availability and len(Item_List)<itemcount:
        ItemKey=randrange(0,len(Item)-1)
        In_Item=Item[ItemKey]
        item_width=In_Item["Item_Width"]
        item_height=In_Item["Item_Height"]
        Height=randrange(0,array_height)
        Width=randrange(0,array_width)
    
        if array[Height,Width]==0:
                if (array[Height:Height+item_height, Width:Width+item_width] == 0).all() and ((Width+item_width)<=array_width and (Height+item_height)<=array_height):          
                    array[Height:Height+item_height, Width:Width+item_width]+=key_Value
                    item_dict={"Key_Value":key_Value,"itemkey":In_Item["itemkey"]}
                    Item_List.append(item_dict)
                    item_availability+=In_Item["Availability"]         
                    key_Value+=1         
                    
                elif (array[Height:Height+item_width, Width:Width+item_height] == 0).all() and (Height+item_width)<=array_height and (Width+item_height)<=array_width :
                    array[Height:Height+item_width, Width:Width+item_height]+=key_Value
                    item_dict={"Key_Value":key_Value,"itemkey":In_Item["itemkey"]}
                    Item_List.append(item_dict)
                    item_availability+=In_Item["Availability"]     
                    key_Value+=1        
    
    Player_Step=item_availability if item_availability>Player_Step else Player_Step

    return array

def Check_Move(x,y):
    LocX=int(x)
    LocY=int(y)
    global Player_Step
   
    if (MainGrid[LocX,LocY]>0):
        itemColor=get_item_by_key(int(MainGrid[LocX,LocY]),"item_ID",ItemColor)
        buttons[x][y].config(text=int(MainGrid[LocX,LocY]),state=tk.DISABLED,bg =itemColor["Color"],fg='black')
    else:
        buttons[x][y].config(text="X",state=tk.DISABLED,bg = "orange",fg="black")
    
    SubGrid[LocX,LocY]=MainGrid[LocX,LocY]
    MainGrid[LocX,LocY]=0
    Update_Info()
   
    #Return True And return break in Python

    if ((MainGrid[:]==0).all()):
        Win(True)
    else:
        Player_Step-=1
        step_label.config(text="Player Step : "+ str(Player_Step))
        Win(False) if Player_Step==0 else None
            
def Update_Info():
    global Label
    global my_label
    row_numb=0
    
    # Clear Info
    [label.destroy() for label in Label]
    Label.clear()
    
    # Check Item Object
    flat_array=np.unique((MainGrid.flatten())[MainGrid.flatten()>0])  
    Map_Item = {data['Key_Value']: data['itemkey'] for data in Item_List}
    item_keys=[Map_Item[int(key)] for key in flat_array]
    item_keys.sort()
    
    # ReConfig label into UI
    for Data in set(item_keys): 
        itemDetails=get_item_by_key(Data,"itemkey",Item)
        my_label=tk.Label(window,text='Item'+ str(itemDetails["ItemName"]) +' left: '+ str(item_keys.count(Data)))
        Label.append(my_label)
        my_label.pack(side="left",expand=True)
        row_numb+=1

def Win(BolWin):
    info_title='Game Over'
    info_Msg="Congratulation! You had WON the Game" if (BolWin) else "Game Over! You had lose the Game!"
    dialogbox=tk.messagebox.showinfo(info_title,info_Msg)
    
    window.destroy()
    # Initiate_Game()
       
# Create UI Element
# Set Up UI
window.title("Treasure Hunt Game")

strStep="Player Step : "+ str(Player_Step)
step_label = tk.Label(window, text=strStep)
step_label.pack()

button_frame = tk.Frame(window)
button_frame.pack()

buttons = []
for i in range(Width):
    row = []
    for j in range(Height):
        button = tk.Button(button_frame, text="", width=6, height=3)
        button.config(command=lambda x=i, y=j: Check_Move(x, y))
        button.grid(row=i, column=j)
        row.append(button)
    buttons.append(row)

Initiate_Game()

window.mainloop()
