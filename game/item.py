from . import setup
import pygame
class item:
    def __init__(self, name, description:list,img,attack_multiplier=1,defense_multiplier=1,category_id=0):
        self.name = name
        self.description = description
        self.img = img
        self.attack_multiplier = attack_multiplier
        self.defense_multiplier = defense_multiplier#受到傷害時的減傷倍率，因為是用乘的要減傷的話要小於1
        self.category_id = category_id
    def ability(self):
        if self.category_id == 0:
            text=[]
            if self.attack_multiplier == 1 and self.defense_multiplier != 1:
                if self.defense_multiplier > 1:
                    text.append("受到傷害時增加"+str(self.defense_multiplier)+"倍傷害")
                else:
                    text.append("受到傷害時減少"+str(round(1-self.defense_multiplier,1))+"倍傷害")
            elif self.attack_multiplier != 1 and self.defense_multiplier == 1:
                if self.attack_multiplier > 1:
                    text.append("攻擊時增加"+str(self.attack_multiplier)+"倍傷害")
                else:
                    text.append("攻擊時減少"+str(round(1-self.attack_multiplier,1))+"倍傷害")
            elif self.attack_multiplier != 1 and self.defense_multiplier != 1:
                if self.attack_multiplier > 1:
                    text.append("攻擊時增加"+str(self.attack_multiplier)+"倍傷害")
                else:
                    text.append("攻擊時減少"+str(round(1-self.attack_multiplier,1))+"倍傷害")
                if self.defense_multiplier > 1:
                    text.append("受到傷害時增加"+str(self.defense_multiplier)+"倍傷害")
                else:
                    text.append("受到傷害時減少"+str(round(1-self.defense_multiplier,1))+"倍傷害")
            else:
                text.append("無特殊效果")
            return text
        elif self.category_id == 1:
            return ["在死掉時消耗後復活"]
        elif self.category_id == 2:
            return ["增加數量時必定增加史萊姆"]
        elif self.category_id == 3:
            return ["回合結束時減少20%的史萊姆"]
        else:
            return ["未知"]
item_list=[item("勇者的聖劍",["傳說中的聖劍","據說可以將巨龍一刀斃命","但這明顯只是個謠言"],pygame.transform.scale(setup.img_list["sword"],(160,160)),1.5,1,0),
           item("勇者的盾牌",["傳說中的盾牌","據說可以完全抵擋巨龍的火焰","但這明顯只是個謠言"],pygame.transform.scale(setup.img_list["shield"],(160,160)),1,0.5,0),
           item("希望之花朵",["一朵散發著光芒的花","只要有人倒下就能使之復活","所以，不要停下來啊"],pygame.transform.scale(setup.img_list["flower"],(160,160)),1,1,1),
           item("史萊姆春藥",["既然史萊姆們的春天還沒到","那就強制讓它到吧❤"],pygame.transform.scale(setup.img_list["potion"],(160,160)),1,1,2),]



curse_list=[item("詭異的肖像",["    一幅詭異的肖像    ","據說會吸取靈魂","這好像不是謠言"],pygame.transform.scale(setup.img_list["portrait"],(160,160)),0.8,1.2,0),
            item("末日的畫像",["一幅據說是預言世界末日景象的畫像","但是畫得太抽象了，沒有人看得懂"],pygame.transform.scale(setup.img_list["draw"],(160,160)),1,1,3),]

