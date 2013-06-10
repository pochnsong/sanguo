#coding=utf8

import pygame

MOUSE_RIGHT_DOWN=1 #鼠标右键 按下
MOUSE_LEFT_DOWN=2 #鼠标左键 按下
MOUSE_RIGHT_UP=3 #鼠标右键 松开
MOUSE_LEFT_UP=4 #鼠标右键 松开
MOUSE_MIDDLE_DOWN=5 #鼠标中键键 按下
MOUSE_MIDDLE_UP=6 #鼠标中键键 松开

MOUSE_MIDDLE_FORWARD=7 #滚轮前滚
MOUSE_MIDDLE_BACKWARD=8 #滚轮后滚

MOUSE_MOTION=9 #鼠标移动
MOUSE_LEFT_MOVE=10 #鼠标左键按下并移动
MOUSE_RIGHT_MOVE=11 #鼠标左键按下并移动

FRAME_QUIT=12

def EVENT(event):
    if event.type==pygame.MOUSEBUTTONDOWN :
        if event.button==1:
            return MOUSE_LEFT_DOWN
        elif event.button==3:
            return MOUSE_RIGHT_DOWN
        elif event.button==2:
            return MOUSE_MIDDLE_DOWN
        elif event.button==4:
            return MOUSE_MIDDLE_FORWARD
        elif event.button==5:
            return MOUSE_MIDDLE_BACKWARD

    elif event.type==pygame.MOUSEBUTTONUP:
        if event.button==1:
            return MOUSE_LEFT_UP
        elif event.button==3:
            return MOUSE_RIGHT_UP
        elif event.button==2:
            return MOUSE_MIDDLE_UP
        
    elif event.type==pygame.MOUSEMOTION:
        if event.buttons==(1,0,0):
            return MOUSE_LEFT_MOVE
        elif event.buttons==(0,0,1):
            return MOUSE_RIGHT_MOVE
        
        return MOUSE_MOTION

    elif event.type==pygame.QUIT:
        return FRAME_QUIT
