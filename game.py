import pygame
from . import tool, setup, question
import os
import time
import random
import sys

class Game:
    def __init__(self):
        self.screen = pygame.Surface((640,480))
        self.screen.fill((0,0,0))
        self.state = "prologue"
        self.unifont_36 = setup.fonts_36["unifont"]
        self.timer=time.time()
        self.question_list = question.question_list
        self.choose_question_multiple_choice_list = question.choose_question_mutiple_choice_list
        self.question = None
        self.choice_list = []
        self.forest_img = pygame.transform.scale(setup.forest_img,(setup.forest_img.get_width()*180//setup.forest_img.get_height(),180))
        self.forest_pos = 0
        self.slime_imgs = [pygame.transform.scale(slime,(40,40)) for slime in setup.slime_imgs]
        self.slime_list = [[0,320]]#[slime_imgs_id,x]
        self.score = 1
        
    def update(self,data:list):
        if self.state == "start":
            #self.prologue()
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
            elif self.question.reward==2:
                text = "史萊姆們增加"+str(self.choice_list[data[0]].choice_num)+"隻同伴了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
            elif self.question.reward==3:
                text = "史萊姆們減少"+str(self.choice_list[data[0]].choice_num)+"隻同伴了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
            elif self.question.reward==4:
                text = "史萊姆們的數量剩下"+str(self.choice_list[data[0]].choice_num)+"分之一倍了!"
                tool.blit_dialog(self.screen,self.unifont_36,[text],(255,255,255),(320,140),center=True,size=(600,100))
            self.state = "animation"
            self.timer = time.time()
        
    def prologue(self):
        screen = pygame.display.set_mode((640, 480))
        font = pygame.font.Font("resource/font/unifont.otf", 36)
        clock = pygame.time.Clock()
        text_lines = [
        "這個世界中，存在著各式各樣的魔物",
        "有的種類人畜無害",
        "有些成為人們賴以果腹的食物",
        "有些則以凶殘出名",
        "而史萊姆就是其中一種攻擊慾低的魔物",
        "不幸的是，一隻殘暴的惡龍作惡多端",
        "佔據了住在山谷附近史萊姆一族的家園",
        "史萊姆們為了奪回家園，向惡龍發起攻勢",
        "靠著數量的優勢，集結史萊姆大軍",
        "以打敗惡龍為目標吧！"
        ]
        line_index = 0
        start_time = pygame.time.get_ticks()
        display_time = 3000
        show_text = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((0, 0, 0))
            current_time = pygame.time.get_ticks()
            if show_text:
                text = font.render(text_lines[line_index], True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                screen.blit(text, text_rect)
                if current_time - start_time >= display_time:
                    line_index += 1
                    start_time = current_time
                    if line_index >= len(text_lines):
                        show_text = False
                        running = False
            pygame.display.flip()
            screen.blit(game.screen,(0,0))
            clock.tick(60)                        
        game.state = "start"
            

        print("hfhfhf")
                    


    def construct_game(self):
        self.screen.fill((0,0,0))
        question_id=random.randint(0,len(self.question_list)-1)
        self.question=self.question_list[question_id]
        if self.question.type==0:
            tool.blit_dialog(self.screen,self.unifont_36,self.question.question,(255,255,255),(320,80),center=True,size=(600,100))
            self.choice_list = random.sample(self.choose_question_multiple_choice_list,3)
            tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[1].choice],(255,255,255),(110,200),center=True,size=(180,80))
            tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[0].choice],(255,255,255),(320,200),center=True,size=(180,80))
            tool.blit_dialog(self.screen,self.unifont_36,[self.choice_list[2].choice],(255,255,255),(530,200),center=True,size=(180,80))
    def backgroud_scroll(self):
        self.forest_pos+=2
        if self.forest_pos>self.forest_img.get_width():
            self.forest_pos=0
        for i in range(640//self.forest_img.get_width()+2):
            self.screen.blit(self.forest_img,(self.forest_pos+(i-1)*self.forest_img.get_width(),260))
        
        

game=Game()