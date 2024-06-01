import pygame
from . import tool, setup, question, item
import os
import time
import random


class Game:
    def __init__(self):
        self.screen = pygame.Surface((640,480))
        self.screen.fill((0,0,0))
        self.PurpleFox = pygame.transform.scale(setup.img_list["7tail_PurpleFox"],(350,setup.img_list["7tail_PurpleFox"].get_height()*350//setup.img_list["7tail_PurpleFox"].get_width()))
        self.start_timer = time.time()
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
        self.total_level = 15
        self.animate_board=pygame.Surface((1280,360))
        self.animate_board_scale = 1
        self.dragon_imgs = [pygame.transform.scale(dragon,(300,300)) for dragon in setup.dragon_imgs]
        self.dragon_timer = time.time()
        self.dragon_list = [[0,960,0]]#[dragon_imgs_id,x,y]
        self.dragon_max_hp = 7000
        self.dragon_hp = self.dragon_max_hp
        self.slime_attack_list = []
        self.slime_attack_timer = time.time()
        self.boss_check = False
        self.item_list = item.item_list
        self.item_list_having = [0 for i in range(len(self.item_list))]
        self.curse_list = item.curse_list
        self.curse_list_having = [0 for i in range(len(self.curse_list))]
        self.back_pack_check = False
        self.back_pack_open = False
        self.back_pack_next_state = "game"
        self.back_pack_teaching_index = 0
        self.boss_attack_timer = time.time()
        self.doctor_question_list = question.doctor_question_list
        self.doctor_game_index = 0
        self.doctor_game_timer = time.time()
        self.explode_imgs = [pygame.transform.scale(explode,(3840,2160)) for explode in setup.explode_imgs]
        self.fireball_pos = 0
        self.explode_index=0
        self.rebirth_timer = time.time()
        self.explode_sound = setup.sound_list["explode"]
        self.correct_answer1_sound = setup.sound_list["correct_answer1"]
        self.correct_answer2_sound = setup.sound_list["correct_answer2"]
        self.wrong_answer1_sound = setup.sound_list["wrong_answer1"]
        self.wrong_answer2_sound = setup.sound_list["wrong_answer2"]
    def update(self,data:list):
        if self.state == "start":
            self.start(data)
        elif self.state == "game":
            self.game(data)
        elif self.state == "lose":
            self.state = "game"
            self.construct_game()
            self.game([-1])
        elif self.state == "boss_game":
            self.boss_game(data)
        elif self.state == "win":
            self.state = "game"
            self.construct_game()
            self.game([-1])
        elif self.state == "back_pack":
            if data[0]==9:
                self.back_pack_open = not self.back_pack_open
                self.state = self.back_pack_next_state
                if self.back_pack_next_state == "game":
                    self.screen.fill((0,0,0))
                    self.game([-1])
                elif self.back_pack_next_state == "boss_game":
                    self.screen.fill((0,0,0))
                    self.boss_game([-1])
            elif data[0]>=1 and data[0]<=6:
                self.state = "item_description"
                self.blit_item_description(data[0])
        elif self.state == "item_description":
            self.blit_back_pack()
            self.state = "back_pack"
        elif self.state == "back_pack_teaching":
            self.back_pack_teaching_index+=1
        elif self.state == "doctor_game":
            self.doctor_game(data)
    def start(self,data:list):
        if data!=[]:
            self.screen.fill((0,0,0))
            self.start_timer = time.time()
            self.state = "start_animate"
    def game(self,data):
        tool.blit_dialog(self.screen,self.unifont_36,self.question.question,(255,255,255),(320,80),center=True,size=(600,100))
        tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[1].choice],(255,255,255),(110,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[0].choice],(255,255,255),(320,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[2].choice],(255,255,255),(530,200),center=True,size=(180,80))
        if data[0]==0 or data[0]==1 or data[0]==2:
            self.correct_answer1_sound.play()
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
            self.update_score()
        elif data[0]==9 and self.back_pack_check:
            self.back_pack_open = not self.back_pack_open
        if self.boss_check:
            self.blit_score_boss()
        else:
            self.blit_score()
        if self.back_pack_open:
            self.state = "back_pack"
            self.back_pack_next_state = "game"
            img=pygame.Surface((640,480))
            img.fill((0,0,0))
            img.set_alpha(100)
            self.screen.blit(img,(0,0))
            self.blit_back_pack()
        
    def construct_game(self):
        self.screen.fill((0,0,0))
        question_id=random.randint(0,len(self.question_list)-1)
        self.question=self.question_list[question_id]
        while self.question.type==0 and (self.question.reward==3 or self.question.reward==4) and self.score<=5:
            question_id=random.randint(0,len(self.question_list)-1)
            self.question=self.question_list[question_id]
        if self.item_list_having[3]==1:
            while self.question.reward!=1 and self.question.reward!=2:
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
        self.reset()
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
            self.correct_answer1_sound.play()
            self.screen.fill((0,0,0))
            if data[0]==1:
                self.state = "slime_attack"
                self.slime_attack_list = []
                self.boss_accumulate = 0
                self.slime_attack()
            elif data[0]==0:
                if not self.back_pack_check:
                    self.back_pack_check = True
                    self.state = "back_pack_teaching"
                    self.back_pack_teaching_index = 0
                else:
                    if all(self.item_list_having):
                        self.state = "doctor_no_1"
                        self.doctor_game_timer = time.time()
                    else:
                        self.construct_doctor_game()
                        self.state = "doctor_game"
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
            img=pygame.Surface((640,480))
            img.fill((0,0,0))
            img.set_alpha(100)
            self.screen.blit(img,(0,0))
            self.blit_back_pack()
    def blit_score_boss(self):
        tool.blit_image(self.screen,self.score_slime_img,(10,440))
        tool.blit_text(self.screen,self.unifont_36,str(self.score),(255,255,255),(60,440),center=False)
        tool.blit_dialog(self.screen,self.unifont_36,[""],(255,255,255),(320,458),center=True,size=(200,30),frame_width=2)
        tool.blit_rectangle(self.screen,(255,255,255),(225,448),(190*(self.dragon_hp/self.dragon_max_hp),20),center=False)
        if self.back_pack_check:
            tool.blit_dialog(self.screen,self.unifont_36,["狀態"],(255,255,255),(600,458),center=True,size=(60,30))
    def blit_score(self):
        tool.blit_image(self.screen,self.score_slime_img,(10,440))
        tool.blit_text(self.screen,self.unifont_36,str(self.score),(255,255,255),(60,440),center=False)
        tool.blit_text(self.screen,self.unifont_36,str(self.level)+"/"+str(self.total_level),(255,255,255),(320,458),center=True)
        if self.back_pack_check:
            tool.blit_dialog(self.screen,self.unifont_36,["狀態"],(255,255,255),(600,458),center=True,size=(60,30))
    def update_score(self):
        self.score = int(round(self.score,0))
        self.score = max(0,self.score)
        if len(self.slime_list)<self.score:
            if self.score>70:
                self.slime_list = [[random.randint(0,4),random.randint(0,580),random.randint(1,10)] for i in range(70)]
                self.slime_list[0]=[0,290,5]
            else:
                while len(self.slime_list)<self.score:
                    self.slime_list.append([random.randint(0,4),random.randint(0,580),random.randint(1,10)])
        while len(self.slime_list)>self.score:
            self.slime_list.pop()
        if len(self.slime_list)>70:
            self.slime_list = self.slime_list[len(self.slime_list)-70:]
            self.slime_list[0]=[0,290,5]
    def slime_attack(self):
        if self.score<20:
            n=self.score
        else:
            n=20
        if len(self.slime_attack_list)<n and time.time()-self.slime_attack_timer>0.1:
            self.slime_attack_timer = time.time()
            self.slime_attack_list.append([290,280])
        check = False
        for i in range(len(self.slime_attack_list)):
            self.slime_attack_list[i][0]+=20
            self.slime_attack_list[i][1]=130/164000*(self.slime_attack_list[i][0]-800)*(self.slime_attack_list[i][0]-800)+20
            if self.slime_attack_list[i][0]==1110:
                self.wrong_answer2_sound.play()
                self.boss_accumulate+=1
                damage=self.score/n
                for j in range(len(self.item_list)):
                    if self.item_list_having[j]!=0 and self.item_list[j].category_id==0:
                        damage*=self.item_list[j].attack_multiplier
                for j in range(len(self.curse_list)):
                    if self.curse_list_having[j]!=0 and self.curse_list[j].category_id==0:
                        damage*=self.curse_list[j].attack_multiplier
                self.dragon_hp-=damage
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
        damage=self.score/n
        for i in range(len(self.item_list)):
            if self.item_list_having[i]!=0 and self.item_list[i].category_id==0:
                damage*=self.item_list[i].attack_multiplier
        for i in range(len(self.curse_list)):
            if self.curse_list_having[i]!=0 and self.curse_list[i].category_id==0:
                damage*=self.curse_list[i].attack_multiplier
        damage=int(round(self.boss_accumulate*damage,0))
        tool.blit_dialog(self.screen,self.unifont_36,["對巨龍造成"+str(damage)+"傷害"],(255,255,255),(320,140),center=True,size=(600,100))
        if not check and len(self.slime_attack_list)!=0:
            if self.dragon_hp==0:
                self.state = "win"
                self.construct_win()
                
            else:
                self.state = "boss_attack"
                self.boss_attack_timer = time.time()
                self.fireball_pos = 0
                self.explode_index=0
                self.boss_attack()
    def blit_back_pack(self):
        
        tool.blit_rectangle(self.screen,(255,255,255),(320,260),(500,420),center=True)
        tool.blit_rectangle(self.screen,(0,0,0),(320,260),(480,400),center=True)
        tool.blit_dialog(self.screen,self.unifont_36,[" 道具 "],(255,255,255),(320,80),center=True,size=(100,40),frame_width=2,frame_color=(0,0,0))
        tool.blit_dialog(self.screen,self.unifont_36,[" 詛咒 "],(255,255,255),(320,250),center=True,size=(100,40),frame_width=2,frame_color=(0,0,0))
        tool.blit_dialog(self.screen,self.unifont_36,["按1~6查看物品描述"],(255,255,255),(320,440),center=True,size=(250,40),frame_width=2,frame_color=(0,0,0))
        for i in range(len(self.item_list_having)):
            img = pygame.transform.scale(self.item_list[i].img,(110,110))
            tool.blit_image(self.screen,img,(140+120*i,140),center=True)
            tool.blit_dialog(self.screen,self.unifont_36,[str(self.item_list[i].name)],(255,255,255),(140+120*i,215),center=True,size=(120-3,30),frame_width=2)
            if self.item_list_having[i]==0:
                temp=pygame.Surface((110,110))
                temp.fill((0,0,0))
                temp.set_alpha(100)
                tool.blit_image(self.screen,temp,(140+120*i,140),center=True)
                temp=pygame.Surface((120,30))
                temp.fill((0,0,0))
                temp.set_alpha(100)
                tool.blit_image(self.screen,temp,(140+120*i,215),center=True)
        for i in range(len(self.curse_list_having)):
            img = pygame.transform.scale(self.curse_list[i].img,(110,110))
            tool.blit_image(self.screen,img,(240+160*i,320),center=True)
            tool.blit_dialog(self.screen,self.unifont_36,[str(self.curse_list[i].name)],(255,255,255),(240+160*i,395),center=True,size=(120-3,30),frame_width=2)
            if self.curse_list_having[i]==0:
                temp=pygame.Surface((110,110))
                temp.fill((0,0,0))
                temp.set_alpha(100)
                tool.blit_image(self.screen,temp,(240+160*i,320),center=True)
                temp=pygame.Surface((120,30))
                temp.fill((0,0,0))
                temp.set_alpha(100)
                tool.blit_image(self.screen,temp,(240+160*i,395),center=True)
            
    def construct_win(self):
        self.screen.fill((0,0,0))
        img=pygame.transform.scale(setup.img_list["slime"],(100,100))
        for i in range(12):
            for j in range(13):
                tool.blit_image(self.screen,img,(-65+i*70,-20+j*40),center=True)
        tool.blit_image(self.screen,self.dragon_imgs[2],(320,240),center=True)
        tool.blit_dialog(self.screen,self.unifont_36,["你贏了!","按Remote Control上任意鍵重新開始"],(255,255,255),(320,405),center=True,size=(600,150))
        self.reset()
    def back_pack_teaching(self):
        img=pygame.Surface((640,480))
        img.fill((0,0,0))
        img.set_alpha(100)
        self.screen.blit(img,(0,0))
        doctor=pygame.transform.scale(setup.img_list["slime_doctor"],(350,350))
        if(self.back_pack_teaching_index==0):
            tool.blit_dialog(self.screen,self.unifont_36,["我是史萊姆博士"],(255,255,255),(320,140),center=True,size=(600,130))
            tool.blit_image(self.screen,doctor,(320,320),center=True)
        elif(self.back_pack_teaching_index==1):
            tool.blit_dialog(self.screen,self.unifont_36,["我最討厭不會數學的史萊姆了"],(255,255,255),(320,140),center=True,size=(600,130))
            tool.blit_image(self.screen,doctor,(320,320),center=True)
        elif(self.back_pack_teaching_index==2):
            tool.blit_dialog(self.screen,self.unifont_36,["回答我的問題","答對的話我會送你道具"],(255,255,255),(320,140),center=True,size=(600,130))
            tool.blit_image(self.screen,doctor,(320,320),center=True)
        elif(self.back_pack_teaching_index==3):
            tool.blit_dialog(self.screen,self.unifont_36,["答錯的話則會給予詛咒"],(255,255,255),(320,140),center=True,size=(600,130))
            tool.blit_image(self.screen,doctor,(320,320),center=True)
        elif(self.back_pack_teaching_index==4):
            tool.blit_dialog(self.screen,self.unifont_36,["答錯的話則會給予詛咒"],(255,255,255),(320,140),center=True,size=(600,130))
            tool.blit_image(self.screen,doctor,(320,320),center=True)
            tool.blit_dialog(self.screen,self.unifont_36,["不僅如此","我還會當掉你的必修學分"],(255,255,255),(320,430),center=True)
        elif(self.back_pack_teaching_index==5):
            tool.blit_dialog(self.screen,self.unifont_36,["按9能查看目前擁有的道具和詛咒"],(255,255,255),(320,140),center=True,size=(600,130))
            tool.blit_image(self.screen,doctor,(320,320),center=True)
        else:
            self.state = "boss_game"
            self.construct_boss_game()
            self.boss_game([-1])
    def boss_attack(self):
        fireball=pygame.transform.scale(setup.img_list["fireball"],(100,100))
        if time.time()-self.boss_attack_timer>0.1 and self.fireball_pos<760:
            self.fireball_pos+=60
            self.boss_attack_timer=time.time()
            if self.fireball_pos>=760:
                self.explode_sound.play()
        
        if self.fireball_pos>=760:
            if time.time()-self.boss_attack_timer>0.2 and self.explode_index<8:
                self.explode_index+=1
                self.boss_attack_timer=time.time()
            tool.blit_image(self.animate_board,self.explode_imgs[self.explode_index],(320,250),center=True)
            damage = 10+self.score//2
            for i in range(len(self.item_list)):
                if self.item_list_having[i]!=0 and self.item_list[i].category_id==0:
                    damage*=self.item_list[i].defense_multiplier
            for i in range(len(self.curse_list)):
                if self.curse_list_having[i]!=0 and self.curse_list[i].category_id==0:
                    damage*=self.curse_list[i].defense_multiplier
            damage = int(round(damage,0))
            tool.blit_dialog(self.screen,self.unifont_36,["巨龍殺死了"+str(damage)+"隻史萊姆!"],(255,255,255),(320,140),center=True,size=(600,100))
            self.blit_score_boss()
            if self.explode_index==7:
                self.explode_index=0
                if self.score<damage and self.item_list_having[2]==1:
                    self.item_list_having[2]=0
                    self.rebirth_timer = time.time()
                    self.state = "rebirth"
                elif self.score<damage:
                    self.score-=damage
                    self.score = max(0,self.score)
                    self.state = "lose"
                    self.construct_lose()
                else:
                    if self.curse_list_having[1]==1:
                        self.rebirth_timer = time.time()
                        self.state = "draw"
                        self.score-=damage
                        self.score = max(0,self.score)
                        self.update_score()
                        self.screen.fill((0,0,0))
                    else:
                        self.state = "boss_game"
                        self.score-=damage
                        self.score = max(0,self.score)
                        self.update_score()
                        self.construct_boss_game()
                        self.boss_game([-1])
        else:
            tool.blit_image(self.animate_board,fireball,(1080-self.fireball_pos,100+210*self.fireball_pos/760),center=True)
            tool.blit_dialog(self.screen,self.unifont_36,["巨龍殺死了0隻史萊姆!"],(255,255,255),(320,140),center=True,size=(600,100))
    def reset(self):
        self.score = 1
        self.slime_list = [[0,290,5]]
        self.level = 1
        self.dragon_hp = self.dragon_max_hp
        self.animate_board_scale = 1
        self.back_pack_check = False
        self.boss_check = False
        self.back_pack_open = False
        self.item_list_having = [0 for i in range(len(self.item_list))]
        self.curse_list_having = [0 for i in range(len(self.curse_list))]
        self.back_pack_teaching_index = 0
        self.doctor_game_index = 0
    def blit_item_description(self,index:int):
        tool.blit_rectangle(self.screen,(255,255,255),(320,260),(500,420),center=True)
        tool.blit_rectangle(self.screen,(0,0,0),(320,260),(480,400),center=True)
        if index>=0 and index<=4:
            img=pygame.transform.scale(self.item_list[index-1].img,(110,110))
            tool.blit_image(self.screen,img,(320,120),center=True)
            tool.blit_dialog(self.screen,self.unifont_36,[str(self.item_list[index-1].name)],(255,255,255),(320,220),center=True,size=(130,30),frame_width=2,frame_color=(0,0,0))
            tool.blit_dialog(self.screen,self.unifont_36,self.item_list[index-1].description,(255,255,255),(320,300),center=True,size=(300,120),frame_color=(0,0,0))
            tool.blit_dialog(self.screen,self.unifont_36,self.item_list[index-1].ability(),(255,255,255),(320,420),center=True,size=(300,70),frame_color=(0,0,0))
        elif index>=5 and index<=6:
            index-=5
            img=pygame.transform.scale(self.curse_list[index].img,(110,110))
            tool.blit_image(self.screen,img,(320,120),center=True)
            tool.blit_dialog(self.screen,self.unifont_36,[str(self.curse_list[index].name)],(255,255,255),(320,220),center=True,size=(130,30),frame_width=2,frame_color=(0,0,0))
            tool.blit_dialog(self.screen,self.unifont_36,self.curse_list[index].description,(255,255,255),(320,300),center=True,size=(300,120),frame_color=(0,0,0))
            tool.blit_dialog(self.screen,self.unifont_36,self.curse_list[index].ability(),(255,255,255),(320,420),center=True,size=(300,70),frame_color=(0,0,0))
    def construct_doctor_game(self):
        self.screen.fill((0,0,0))
        question_id=random.randint(0,len(self.doctor_question_list)-1)
        self.question=self.doctor_question_list[question_id]
        if self.question.type==1:
            self.choice_list = random.sample(self.question.choice,3)
            if self.question.answer not in self.choice_list:
                self.choice_list[0].choice = self.question.answer
    def blit_doctor_game(self):
        img=pygame.Surface((640,480))
        img.fill((0,0,0))
        img.set_alpha(100)
        self.screen.blit(img,(0,0))
        doctor=pygame.transform.scale(setup.img_list["slime_doctor"],(350,350))
        tool.blit_dialog(self.screen,self.unifont_36,self.question.question,(255,255,255),(320,80),center=True,size=(600,100))
        tool.blit_dialog(self.screen,self.unifont_36,self.choice_list[1],(255,255,255),(110,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,self.choice_list[0],(255,255,255),(320,200),center=True,size=(180,80))
        tool.blit_dialog(self.screen,self.unifont_36,self.choice_list[2],(255,255,255),(530,200),center=True,size=(180,80))
        tool.blit_image(self.screen,doctor,(320,360),center=True)
    def doctor_game(self,data):
        if data[0]==1 or data[0]==2 or data[0]==0:
            ans=self.choice_list.index(self.question.answer)
            if data[0]==ans:
                self.correct_answer2_sound.play()
                self.state = "doctor_game_win"
                temp=[]
                for i in range(len(self.item_list_having)):
                    if self.item_list_having[i]==0:
                        temp.append(i)
                if len(temp)!=0:
                    index=random.choice(temp)
                    self.item_list_having[index]=1
                    self.doctor_game_index=index
                self.doctor_game_timer = time.time()
            else:
                self.wrong_answer1_sound.play()
                self.state = "doctor_game_lose"
                temp=[]
                for i in range(len(self.curse_list_having)):
                    if self.curse_list_having[i]==0:
                        temp.append(i)
                if len(temp)!=0:
                    index=random.choice(temp)
                    self.curse_list_having[index]=1
                    self.doctor_game_index=index
                else:
                    self.state = "doctor_no_2"
                self.doctor_game_timer = time.time()
    def blit_doctor_game_win(self):
        if time.time()-self.doctor_game_timer>1.5:
            self.screen.fill((0,0,0))
            self.blit_score_boss()
            self.state = "boss_attack"
            self.boss_attack_timer = time.time()
            self.fireball_pos = 0
            self.explode_index=0
            self.boss_attack()
        else:
            img=pygame.Surface((640,480))
            img.fill((0,0,0))
            img.set_alpha(100)
            self.screen.blit(img,(0,0))
            item_img=pygame.transform.scale(self.item_list[self.doctor_game_index].img,(160,160))
            tool.blit_image(self.screen,item_img,(320,360),center=True)
            text=["你答對了!","史萊姆博士將"+self.item_list[self.doctor_game_index].name+"送給你了!"]
            tool.blit_dialog(self.screen,self.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
    def blit_doctor_game_lose(self):
        if time.time()-self.doctor_game_timer>1.5:
            self.screen.fill((0,0,0))
            self.blit_score_boss()
            self.state = "boss_attack"
            self.boss_attack_timer = time.time()
            self.fireball_pos = 0
            self.explode_index=0
            self.boss_attack()
        else:
            img=pygame.Surface((640,480))
            img.fill((0,0,0))
            img.set_alpha(100)
            self.screen.blit(img,(0,0))
            curse_img=pygame.transform.scale(self.curse_list[self.doctor_game_index].img,(160,160))
            tool.blit_image(self.screen,curse_img,(320,360),center=True)
            text=["你答錯了!","史萊姆博士將"+self.curse_list[self.doctor_game_index].name+"塞給你了!"]
            tool.blit_dialog(self.screen,self.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
    def blit_doctor_no_1(self):
        if time.time()-self.doctor_game_timer>1.5:
            self.screen.fill((0,0,0))
            self.blit_score_boss()
            self.state = "boss_game"
            self.construct_boss_game()
            self.boss_game([-1])
        else:
            img=pygame.Surface((640,480))
            img.fill((0,0,0))
            img.set_alpha(100)
            self.screen.blit(img,(0,0))
            doctor=pygame.transform.scale(setup.img_list["slime_doctor"],(350,350))
            tool.blit_image(self.screen,doctor,(320,360),center=True)
            text=["你已經擁有所有道具了!","不如收下這張物聯網的加簽單吧"]
            tool.blit_dialog(self.screen,self.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
    def blit_doctor_no_2(self):
        if time.time()-self.doctor_game_timer>1.5:
            self.screen.fill((0,0,0))
            self.blit_score_boss()
            self.state = "boss_attack"
            self.boss_attack_timer = time.time()
            self.fireball_pos = 0
            self.explode_index=0
            self.boss_attack()
        else:
            img=pygame.Surface((640,480))
            img.fill((0,0,0))
            img.set_alpha(100)
            self.screen.blit(img,(0,0))
            doctor=pygame.transform.scale(setup.img_list["slime_doctor"],(350,350))
            tool.blit_image(self.screen,doctor,(320,360),center=True)
            text=["你已經擁有所有詛咒了!","史萊姆博士只好把你的必修學分當掉了!"]
            tool.blit_dialog(self.screen,self.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
    def blit_rebirth(self):
        if time.time()-self.rebirth_timer>1.5:
            if self.curse_list_having[1]==1:
                self.state = "draw"
                self.rebirth_timer = time.time()
            else:
                self.state = "boss_game"
                self.construct_boss_game()
                self.boss_game([-1])
        else:
            text=["希望之花的力量","將你復活了"]
            tool.blit_dialog(self.screen,self.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
    def blit_draw(self):
        if time.time()-self.rebirth_timer>1.5:
            self.score-=self.score//5
            self.score = max(0,self.score)
            if self.score==0:
                self.state = "lose"
                self.construct_lose()
            else:
                self.state = "boss_game"
                self.construct_boss_game()
                self.boss_game([-1])
        else:
            text=["末日的畫像","帶走了"+str(self.score//5)+"隻史萊姆"]
            tool.blit_dialog(self.screen,self.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
game=Game()