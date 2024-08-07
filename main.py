from datetime import datetime as dt
from game.game import game as game
from game import tool
import pygame
import time
if __name__ == '__main__':
    tool.blit_text(game.screen,game.unifont_36,"A是左   S是中   D是右",(255,255,255),(320,400),True)
    tool.blit_text(game.screen,game.unifont_36,"按ESC退出    按F切換全螢幕",(255,255,255),(320,440),True)
    screen = pygame.display.get_surface()
    mouse_timer = time.time()
    while True:
        pygame.time.Clock().tick(120)
        a=False
        
        if game.state == "animation":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            if game.boss_check:
                game.dragon_animation()
            game.blit_animate_board()
            if time.time()-game.timer>1:
                if game.score<=0:
                    game.state = "lose"
                else:
                    game.level+=1
                    if game.boss_check:
                        game.state = "boss_attack"
                        game.boss_attack_timer = time.time()
                        game.fireball_pos = 0
                        game.explode_index = 0
                        game.boss_attack()
                    elif game.level>game.total_level:
                        game.state = "boss_entrance"
                        game.screen.fill((0,0,0))
                        tool.blit_dialog(game.screen,game.unifont_36,["巨龍出現了!!!"],(255,255,255),(320,140),center=True,size=(600,100))
                        tool.blit_image(game.screen,game.score_slime_img,(10,440))
                        tool.blit_text(game.screen,game.unifont_36,str(game.score),(255,255,255),(60,440),center=False)
                        
                    else:
                        game.state = "game"
                        game.construct_game()
                        game.update([-1])
        elif game.state == "game":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            if game.boss_check:
                game.dragon_animation()
            game.blit_animate_board()
        elif game.state == "boss_entrance":
            game.animate_board.fill((0,0,0))
            game.boss_entrance_animation()
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
        elif game.state == "boss_game":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
        elif game.state == "slime_attack":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.dragon_animation()
            game.slime_attack()
            game.slime_animation()
            game.blit_animate_board()
        elif game.state == "back_pack_teaching":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.back_pack_teaching()
        elif game.state == "start_animate":
            if time.time()-game.start_timer>2.5:
                time.sleep(0.5)
                game.start_timer = time.time()
                game.state = "start_animate2"
            else:
                if time.time()-game.start_timer-0.5>=0:
                    game.screen.fill((0,0,0))
                    tool.blit_image(game.screen,game.PurpleFox,(320,220),center=True)
                    tool.blit_text(game.screen,game.unifont_36,"Presented by 7tail_PurpleFox",(255,255,255),(320,440),center=True)
                    img=pygame.Surface((640,480))
                    img.fill((0,0,0))
                    img.set_alpha(abs(250-250*(time.time()-game.start_timer-0.5)))
                    game.screen.blit(img,(0,0))
                else:
                    game.screen.fill((0,0,0))
        elif game.state == "boss_attack":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.boss_attack()
            game.blit_animate_board()
        elif game.state == "lose":
            game.construct_lose()
        elif game.state == "win":
            game.construct_win()
        elif game.state == "doctor_game":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_doctor_game()
        elif game.state == "doctor_game_win":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_doctor_game_win()
        elif game.state == "doctor_game_lose":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_doctor_game_lose()
        elif game.state == "doctor_no_1":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_doctor_no_1()
        elif game.state == "doctor_no_2":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_doctor_no_2()
        elif game.state == "rebirth":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_rebirth()
        elif game.state == "draw":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
            game.blit_score_boss()
            game.blit_draw()
        elif game.state == "start_animate2":
            game.screen.fill((0,0,0))
            game.animate_board.fill((0,0,0))
            if time.time()-game.start_timer>6:
                pygame.mixer.music.play(-1)
                game.state = "game"
                game.construct_game()
                game.game([-1])
            elif time.time()-game.start_timer>3:
                text=["他想找巨龍算帳","你能幫他嗎?"]
                tool.blit_dialog(game.screen,game.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
            else:
                text=["這是史萊姆","他的家被巨龍毀了"]
                tool.blit_dialog(game.screen,game.unifont_36,text,(255,255,255),(320,140),center=True,size=(600,100))
            game.backgroud_scroll()
            game.forest_pos = 0
            img=pygame.transform.scale(game.score_slime_img,(60,60))
            tool.blit_image(game.animate_board,img,(290,280))
            game.blit_animate_board()
        screen.fill((0,0,0))
        screen.blit(game.screen,(0,0))
        if time.time()-mouse_timer>3 and pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                a=True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    a=True
                    break
                elif event.key == pygame.K_f:
                    if(screen.get_flags()&pygame.FULLSCREEN):
                        screen=pygame.display.set_mode((640,480))
                    else:
                        screen=pygame.display.set_mode((640,480),pygame.FULLSCREEN)
                elif event.key == pygame.K_a:
                    game.update([1])
                elif event.key == pygame.K_s:
                    game.update([0])
                elif event.key == pygame.K_d:
                    game.update([2])
                elif event.key in range(48,58):
                    game.update([int(event.key)-48])
                else:
                    game.update([-1])
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)
                mouse_timer = time.time()
                
        if a:
            break
        pygame.display.update()

