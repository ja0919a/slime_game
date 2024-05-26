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
        self.slime_list = [[0,290,5]]#[slime_imgs_id,x,jump_scale]
        self.score = 1
        self.score_slime_img = pygame.transform.scale(setup.img_list["slime"],(40,40))
        self.slime_timer = time.time()
        self.level = 1
        self.total_level = 3
        self.animate_board=pygame.Surface((1280,360))
        self.animate_board_scale = 1
        self.dragon_imgs = [pygame.transform.scale(dragon,(300,300)) for dragon in setup.dragon_imgs]
        self.dragon_timer = time.time()
        self.dragon_list = [[0,960,0]]#[dragon_imgs_id,x,y]
        self.dragon_max_hp = 3000
        self.dragon_hp = self.dragon_max_hp
        self.slime_attack_list = []
        self.slime_attack_timer = time.time()
        self.boss_check = False
        self.item_list = []
        self.item_list_having = []
        self.back_pack_check = False
        self.back_pack_open = False
        self.back_pack_next_state = "game"
        self.win=False
        
    def update(self,data:list):
        if self.state == "start":
            self.start(data)
        elif self.state == "game":
            self.game(data)
        elif self.state == "lose":
            self.start(data)
        elif self.state == "boss_game":
            self.boss_game(data)
        elif self.state == "win":
            self.start(data)
        elif self.state == "back_pack":
            if data[0]==9:
                self.back_pack_open = not self.back_pack_open
                self.state = self.back_pack_next_state
                if self.back_pack_next_state == "game":
                    self.game([-1])
                elif self.back_pack_next_state == "boss_game":
                    self.boss_game([-1])
    def start(self,data:list):
        if data!=[]:
            self.win=False
            self.state = "game"
            self.construct_game()
            self.game([-1])
    def game(self,data):
        tool.blit_dialog(self.screen,self.unifont_36,self.question.question,(255,255,255),(320,80),center=True,size=(600,100))
        tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[1].choice],(255,255,255),(110,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[0].choice],(255,255,255),(320,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[2].choice],(255,255,255),(530,200),center=True,size=(180,80))
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
        elif data[0]==9 and self.back_pack_check:
            self.back_pack_open = not self.back_pack_open
        if self.boss_check:
            self.blit_score_boss()
        else:
            self.blit_score()
        if self.back_pack_open:
            self.state = "back_pack"
            self.back_pack_next_state = "game"
            self.blit_back_pack()
        
    def construct_game(self):
        self.screen.fill((0,0,0))
        question_id=random.randint(0,len(self.question_list)-1)
        self.question=self.question_list[question_id]
        while self.question.type==0 and (self.question.reward==3 or self.question.reward==4) and self.score<=5:
            question_id=random.randint(0,len(self.question_list)-1)
            self.question=self.question_list[question_id]
        if self.question.type==0:
            self.choice_list = random.sample(self.choose_question_multiple_choice_list,3)
            if self.question.reward==1 or self.question.reward==4:
                while self.choice_list[0].choice_num=="0" or self.choice_list[1].choice_num=="0" or self.choice_list[2].choice_num=="0":
                    self.choice_list = random.sample(self.choose_question_multiple_choice_list,3)
            
    def backgroud_scroll(self):
        self.forest_pos-=2
        if -1*self.forest_pos>self.forest_img.get_width():
            self.forest_pos=0
        for i in range(640//self.forest_img.get_width()+6):
            self.animate_board.blit(self.forest_img,(self.forest_pos+(i-1)*self.forest_img.get_width(),180))
        
    def slime_animation(self):
        if time.time()-self.slime_timer>0.07:
            self.slime_timer = time.time()
            for i in range(len(self.slime_list)):
                self.slime_list[i][0]+=1
                if self.slime_list[i][0]>4:
                    self.slime_list[i][0]=0
        for slime in self.slime_list:
            jump = 0
            if slime[0]==2 or slime[0]==4:
                jump = -50*slime[2]/10
            elif slime[0]==3:
                jump = -80*slime[2]/10
            elif slime[0]==0:
                slime[2]=random.randint(1,10)
            self.animate_board.blit(self.slime_imgs[slime[0]],(slime[1],280+jump))
    def construct_lose(self):
        self.screen.fill((0,0,0))
        tool.blit_text(self.screen,self.unifont_36,"你輸了",(255,255,255),(320,240),center=True)
        tool.blit_text(self.screen,self.unifont_36,"按Remote Control上任意鍵重新開始",(255,255,255),(320,400),center=True)
    def boss_entrance_animation(self):
        if self.animate_board_scale<2:
            self.animate_board_scale+=0.01
            tool.blit_dialog(self.screen,self.unifont_36,[""],(255,255,255),(320,458),center=True,size=(200,30),frame_width=2)
            tool.blit_rectangle(self.screen,(255,255,255),(225,448),(190*(self.animate_board_scale-1),20),center=False)
        else:
            self.animate_board_scale=2
            self.boss_check = True
            self.state = "boss_game"
            self.construct_boss_game()
            self.boss_game([-1])
            
    def blit_animate_board(self):
        temp=self.animate_board.copy()
        temp=pygame.transform.scale(temp,(1280/self.animate_board_scale,360/self.animate_board_scale))
        #temp=tool.get_image(temp,0,360/self.animate_board_scale-180,640,180)
        temp=tool.get_image(temp,0,360-self.animate_board_scale*180,640,180)
        rect=temp.get_rect()
        rect.bottomleft=(0,440)
        self.screen.blit(temp,rect.topleft)
    def dragon_animation(self):
        if time.time()-self.dragon_timer>0.1:
            self.dragon_timer = time.time()
            for i in range(len(self.dragon_list)):
                self.dragon_list[i][0]+=1
                if self.dragon_list[i][0]>3:
                    self.dragon_list[i][0]=0
        for dragon in self.dragon_list:
            self.animate_board.blit(self.dragon_imgs[dragon[0]],(dragon[1],dragon[2]))
    def construct_boss_game(self):
        self.screen.fill((0,0,0))
        tool.blit_dialog(self.screen,self.unifont_36,["要做什麼呢?"],(255,255,255),(320,80),center=True,size=(600,100))
        tool.blit_dialog(self.screen,self.unifont_36,["攻擊"],(255,255,255),(110,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,["救救我","史萊姆博士!"],(255,255,255),(320,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,["增加數量"],(255,255,255),(530,200),center=True,size=(180,80))
    def boss_game(self,data:list):
        tool.blit_dialog(self.screen,self.unifont_36,["要做什麼呢?"],(255,255,255),(320,80),center=True,size=(600,100))
        tool.blit_dialog(self.screen,self.unifont_36,["攻擊"],(255,255,255),(110,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,["救救我","史萊姆博士!"],(255,255,255),(320,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,["增加數量"],(255,255,255),(530,200),center=True,size=(180,80))
        if data[0]==0 or data[0]==1 or data[0]==2:
            self.screen.fill((0,0,0))
            if data[0]==1:
                self.state = "slime_attack"
                self.slime_attack_list = []
                self.boss_accumulate = 0
                self.slime_attack()
            elif data[0]==0:
                self.back_pack_check = True
                self.construct_boss_game()
                self.update([-1])
            elif data[0]==2:
                self.state = "game"
                self.construct_game()
                self.game([-1])
        elif data[0]==9 and self.back_pack_check:
            self.back_pack_open = not self.back_pack_open
        self.blit_score_boss()
        if self.back_pack_open:
            self.state = "back_pack"
            self.back_pack_next_state = "boss_game"
            self.blit_back_pack()
    def blit_score_boss(self):
        self.score = int(round(self.score,0))
        self.score = max(0,self.score)
        while len(self.slime_list)<self.score:
            self.slime_list.append([random.randint(0,4),random.randint(0,580),random.randint(1,10)])
        while len(self.slime_list)>self.score:
            self.slime_list.pop()
        if len(self.slime_list)>70:
            self.slime_list = self.slime_list[len(self.slime_list)-70:]
            self.slime_list[0]=[0,290,5]
        tool.blit_image(self.screen,self.score_slime_img,(10,440))
        tool.blit_text(self.screen,self.unifont_36,str(self.score),(255,255,255),(60,440),center=False)
        tool.blit_dialog(self.screen,self.unifont_36,[""],(255,255,255),(320,458),center=True,size=(200,30),frame_width=2)
        tool.blit_rectangle(self.screen,(255,255,255),(225,448),(190*(self.dragon_hp/self.dragon_max_hp),20),center=False)
        if self.back_pack_check:
            tool.blit_dialog(self.screen,self.unifont_36,["背包"],(255,255,255),(600,458),center=True,size=(60,30))
    def blit_score(self):
        self.score = int(round(self.score,0))
        self.score = max(0,self.score)
        while len(self.slime_list)<self.score:
            self.slime_list.append([random.randint(0,4),random.randint(0,580),random.randint(1,10)])
        while len(self.slime_list)>self.score:
            self.slime_list.pop()
        if len(self.slime_list)>70:
            self.slime_list = self.slime_list[len(self.slime_list)-70:]
            self.slime_list[0]=[0,290,5]
        tool.blit_image(self.screen,self.score_slime_img,(10,440))
        tool.blit_text(self.screen,self.unifont_36,str(self.score),(255,255,255),(60,440),center=False)
        tool.blit_text(self.screen,self.unifont_36,str(self.level)+"/"+str(self.total_level),(255,255,255),(320,458),center=True)
        if self.back_pack_check:
            tool.blit_dialog(self.screen,self.unifont_36,["背包"],(255,255,255),(600,458),center=True,size=(60,30))
    def slime_attack(self):
        if self.score<20:
            n=self.score
        else:
            n=20
        if len(self.slime_attack_list)<n and time.time()-self.slime_attack_timer>0.2:
            self.slime_attack_timer = time.time()
            self.slime_attack_list.append([290,280])
        check = False
        for i in range(len(self.slime_attack_list)):
            self.slime_attack_list[i][0]+=20
            self.slime_attack_list[i][1]=130/164000*(self.slime_attack_list[i][0]-800)*(self.slime_attack_list[i][0]-800)+20
            if self.slime_attack_list[i][0]==1110:
                self.boss_accumulate+=1
                self.dragon_hp-=self.score/n
                temp=self.dragon_imgs[self.dragon_list[0][0]].copy()
                pixels = pygame.PixelArray(temp)
                # Iterate over each pixel
                for x in range(temp.get_width()):
                    for y in range(temp.get_height()):
                        # Check if the pixel is black
                        if pixels[x, y] == temp.map_rgb((0, 0, 0)):
                            # Replace black pixel with white pixel
                            pixels[x, y] = (255, 255, 255)
                # Delete the pixel array to update the surface
                del pixels
                self.animate_board.blit(temp,(960,0))
            if self.slime_attack_list[i][1]<360:
                check = True
            img=pygame.transform.scale(self.score_slime_img,(60,60))
            self.animate_board.blit(img,(self.slime_attack_list[i][0],self.slime_attack_list[i][1]))
        self.dragon_hp = max(0,self.dragon_hp)
        self.blit_score_boss()
        tool.blit_dialog(self.screen,self.unifont_36,["對巨龍造成"+str(int(round(self.boss_accumulate*self.score/n,0)))+"傷害"],(255,255,255),(320,140),center=True,size=(600,100))
        if not check and len(self.slime_attack_list)!=0:
            if self.dragon_hp==0:
                self.state = "win"
                self.construct_win()
                self.score = 1
                self.slime_list = [[0,290,5]]
                self.level = 1
                self.dragon_hp = self.dragon_max_hp
                self.animate_board_scale = 1
                self.back_pack_check = False
                self.boss_check = False
                self.back_pack_open = False
                self.item_list = []
                self.item_list_having = []
                self.win=True
                
            else:
                self.state = "boss_game"
                self.construct_boss_game()
                self.boss_game([-1])
    def blit_back_pack(self):
       img=pygame.Surface((640,480))
       img.fill((0,0,0))
       img.set_alpha(100)
       self.screen.blit(img,(0,0))
    def construct_win(self):
        self.screen.fill((0,0,0))
        tool.blit_text(self.screen,self.unifont_36,"你贏了",(255,255,255),(320,240),center=True)
        tool.blit_text(self.screen,self.unifont_36,"按Remote Control上任意鍵重新開始",(255,255,255),(320,400),center=True)
game=Game()