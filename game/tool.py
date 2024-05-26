import pygame
import os

def load_image(path, accept={"png", "jpg", "bmp", "gif"}):
    #載入圖片
    #accept:可接受的檔案類型
    #return:圖片物件dict
    images={}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext[1:].lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img=img.convert()
            images[name]=img
    return images

def get_image(sheet,x,y,w,h,colorkey=None,scale=1):
    #切割圖片
    #sheet:圖片物件
    #x,y,w,h:切割區域
    #return:圖片物件
    img=pygame.Surface((w,h))
    img.blit(sheet,(0,0),(x,y,w,h))#將sheet的(x,y,w,h)區域貼到img上
    img.set_colorkey(colorkey)#設定透明色(和colorkey相同的顏色會變透明)
    img=pygame.transform.scale(img,(int(w*scale),int(h*scale)))#縮放
    return img

def load_font(path, size, accept={"ttf","otf"}):
    #accept:可接受的檔案類型
    #return:圖片物件dict
    fonts={}
    for f in os.listdir(path):
        name, ext = os.path.splitext(f)
        if ext[1:].lower() in accept:
            font=pygame.font.Font(os.path.join(path, f),size)
            fonts[name]=font
    return fonts

def blit_text(screen,font,text,color,pos,center=False):
    #顯示文字
    #screen:畫布
    #text:文字
    #font:字型
    #color:顏色
    #pos:位置
    img=font.render(text,True,color)
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
        
def blit_dialog(screen,font,text_list,color,pos,size=[],center=False,frame_width=5,frame_color=(255,255,255),background_color=(0,0,0),width_blank=10,height_blank=5):
    #顯示對話框
    #screen:畫布
    #text_list:文字列表
    #font:字型
    #color:顏色
    #pos:位置
    #size:對話框大小
    #center:是否置中
    #frame_width:邊框寬度
    #frame_color:邊框顏色
    #background_color:背景顏色
    w = len(max(text_list,key=len))*font.size("  ")[0]+2*frame_width+2*width_blank
    h = len(text_list)*font.get_height()+2*frame_width+2*height_blank
    if size==[]:
        size=(w,h)
    img=pygame.Surface(size)
    img.fill(frame_color)
    img2=pygame.Surface((size[0]-2*frame_width,size[1]-2*frame_width))
    img2.fill(background_color)
    img3=pygame.Surface((w-2*frame_width,h-2*frame_width))
    img3.fill(background_color)
    for i,text in enumerate(text_list):
        blit_text(img3,font,text,color,(img3.get_width()//2,height_blank+(i+0.5)*font.get_height()),center=True)
    if(img3.get_width()>img2.get_width()):
        img3=pygame.transform.scale(img3,(img2.get_width(),img3.get_height()*img2.get_width()//img3.get_width()))
    blit_image(img2,img3,(img2.get_width()//2,img2.get_height()//2),center=True)
    img.blit(img2,(frame_width,frame_width))
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
def blit_image(screen,img,pos,center=False):
    #顯示圖片
    #screen:畫布
    #img:圖片
    #pos:位置
    #center:是否置中
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
def blit_rectangle(screen,color,pos,size,center=False):
    #顯示矩形
    #screen:畫布
    #color:顏色
    #pos:位置
    #size:大小
    #center:是否置中
    img=pygame.Surface(size)
    img.fill(color)
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)