import pygame
from . import tool, setup, question
import os
import time
import random


class Game:
    def __init__(self):
        self.screen = pygame.Surface((640,480))
        self.screen.fill((0,0,0))
        self.state = "start"
        self.unifont_36 = setup.fonts_36["unifont"]
        self.timer=time.time()
        self.question_list = question.question_list
        self.choose_question_multiple_choice_list = question.choose_question_mutiple_choice_list
        self.question = None
        self.choice_list = []
        self.forest_img = pygame.transform.scale(setup.forest_img,(setup.forest_img.get_width()*180//setup.forest_img.get_height(),180))
        self.forest_pos = 0
        self.slime_imgs = [pygame.transform.scale(slime,(60,60)) for slime in setup.slime_imgs]
        self.slime_list = [[0,320,5]]#[slime_imgs_id,x,jump_scale]
        self.score = 1
        self.score_slime_img = pygame.transform.scale(setup.img_list["slime"],(40,40))
        self.slime_timer = time.time()
        
    def update(self,data:list):
        if self.state == "start":
            self.start(data)
        elif self.state == "game":
            self.game(data)
    
    def start(self,data:list):
        if data!=[]:
            self.state = "game"
            self.construct_game()
            self.game([-1])
    def game(self,data):
        if data[0]==0 or data[0]==1 or data[0]==2:
            self.screen.fill((0,0,0))
            if self.question.reward==1:
                text = "史萊姆們的數量變成"+str(self.choice_list[data[0]].choice_num)+"倍了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
                self.score*=float(self.choice_list[data[0]].choice_num)
            elif self.question.reward==2:
                text = "史萊姆們增加"+str(self.choice_list[data[0]].choice_num)+"隻同伴了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
                self.score+=float(self.choice_list[data[0]].choice_num)
            elif self.question.reward==3:
                text = "史萊姆們減少"+str(self.choice_list[data[0]].choice_num)+"隻同伴了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
                self.score-=float(self.choice_list[data[0]].choice_num)
            elif self.question.reward==4:
                text = "史萊姆們的數量剩下"+str(self.choice_list[data[0]].choice_num)+"分之一倍了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
                self.score/=float(self.choice_list[data[0]].choice_num)
            self.state = "animation"
            self.timer = time.time()
        self.score = int(round(self.score,0))
        self.score = max(0,self.score)
        while len(self.slime_list)<self.score:
            self.slime_list.append([random.randint(0,4),random.randint(0,640),random.randint(1,10)])
        while len(self.slime_list)>self.score:
            self.slime_list.pop()
        if len(self.slime_list)>30:
            self.slime_list = self.slime_list[len(self.slime_list)-30:]
        tool.blit_image(self.screen,self.score_slime_img,(10,440))
        tool.blit_text(self.screen,self.unifont_36,str(self.score),(255,255,255),(60,440),center=False)
        
    def construct_game(self):
        self.screen.fill((0,0,0))
        question_id=random.randint(0,len(self.question_list)-1)
        self.question=self.question_list[question_id]
        while self.question.type==0 and (self.question.reward==3 or self.question.reward==4) and self.score<=5:
            question_id=random.randint(0,len(self.question_list)-1)
            self.question=self.question_list[question_id]
        if self.question.type==0:
            tool.blit_dialog(self.screen,self.unifont_36,self.question.question,(255,255,255),(320,80),center=True,size=(600,100))
            self.choice_list = random.sample(self.choose_question_multiple_choice_list,3)
            if self.question.reward==1 or self.question.reward==4:
                while self.choice_list[0].choice_num=="0" or self.choice_list[1].choice_num=="0" or self.choice_list[2].choice_num=="0":
                    self.choice_list = random.sample(self.choose_question_multiple_choice_list,3)
            tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[1].choice],(255,255,255),(110,200),center=True,size=(180,80))
            tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[0].choice],(255,255,255),(320,200),center=True,size=(180,80))
            tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[2].choice],(255,255,255),(530,200),center=True,size=(180,80))
    def backgroud_scroll(self):
        self.forest_pos-=2
        if -1*self.forest_pos>self.forest_img.get_width():
            self.forest_pos=0
        for i in range(640//self.forest_img.get_width()+3):
            self.screen.blit(self.forest_img,(self.forest_pos+(i-1)*self.forest_img.get_width(),260))
        
    def slime_animation(self):
        if time.time()-self.slime_timer>0.1:
            self.slime_timer = time.time()
            for i in range(len(self.slime_list)):
                self.slime_list[i][0]+=1
                if self.slime_list[i][0]>4:
                    self.slime_list[i][0]=0
        for slime in self.slime_list:
            jump = 0
            if slime[0]==2 or slime[0]==4:
                jump = -30*slime[2]/10
            elif slime[0]==3:
                jump = -60*slime[2]/10
            elif slime[0]==0:
                slime[2]=random.randint(1,10)
            self.screen.blit(self.slime_imgs[slime[0]],(slime[1],360+jump))

game=Game()