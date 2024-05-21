import re, time, json, threading, requests, traceback, sys, importlib
from datetime import datetime as dt
import paho.mqtt.client as mqtt
import DAN
from game.game import game as game
from game import tool
import pygame
SA_module_name = 'SA'
if len(sys.argv)>1: SA_module_name = ((sys.argv[1]).split('.'))[0]
SA = importlib.import_module(SA_module_name)

def df_func_name(df_name):
    return re.sub(r'-', r'_', df_name)

MQTT_broker = getattr(SA,'MQTT_broker', None)
MQTT_port = getattr(SA,'MQTT_port', 1883)
MQTT_User = getattr(SA,'MQTT_User', None)
MQTT_PW = getattr(SA,'MQTT_PW', None)
MQTT_encryption = getattr(SA,'MQTT_encryption', None)
device_model = getattr(SA,'device_model', None)
device_name = getattr(SA,'device_name', None)
ServerURL = getattr(SA,'ServerURL', None)
device_id = getattr(SA,'device_id', None)
if device_id==None: device_id = DAN.get_mac_addr()
IDF_list = getattr(SA,'IDF_list', [])
ODF_list = getattr(SA,'ODF_list', [])
exec_interval = getattr(SA,'exec_interval', 1)
IDF_funcs = {}
for idf in IDF_list:
    IDF_funcs[idf] = getattr(SA, df_func_name(idf), None)
ODF_funcs = {}
for odf in ODF_list:
    ODF_funcs[odf] = getattr(SA, df_func_name(odf), None)

def on_connect(client, userdata, flags, rc):
    global DISCONNECT
    if not rc:
        if DISCONNECT: DISCONNECT = False
        print('[{}] MQTT broker: {}'.format(dt.now().strftime('%Y-%m-%d %H:%M:%S'), MQTT_broker))
        if ODF_list == []:
            print('ODF_list is not exist.')
            return
        topic_list=[]
        for odf in ODF_list:
            topic = '{}//{}'.format(device_id, odf)
            topic_list.append((topic,0))
        if topic_list != []:
            r = client.subscribe(topic_list)
            if r[0]: print('Failed to subscribe topics. Error code:{}'.format(r))
    else: print('Connect to MQTT borker failed. Error code:{}'.format(rc))

DISCONNECT = False
def on_disconnect(client, userdata,  rc):
    global DISCONNECT
    print('[{}] MQTT disconnected.'.format(dt.now().strftime('%Y-%m-%d %H:%M:%S')))
    DISCONNECT = True
    #client.reconnect()

def on_message(client, userdata, msg):
    samples = json.loads(msg.payload)
    ODF_name = msg.topic.split('//')[1]
    if ODF_funcs.get(ODF_name):
        ODF_data = samples['samples'][0][1]
        ODF_funcs[ODF_name](ODF_data)
    else:
        print('ODF function "{}" is not existed.'.format(ODF_name))

def mqtt_pub(client, deviceId, IDF, data):
    topic = '{}//{}'.format(deviceId, IDF)
    sample = [str(dt.today()), data]
    payload  = json.dumps({'samples':[sample]})
    status = client.publish(topic, payload)
    if status[0]: print('[{}] Failed in pub: topic:{}, status:{}'.format(dt.now().strftime('%Y-%m-%d %H:%M:%S') , topic, status))

def check_df_funcs_exist(IDF_list, ODF_list):
    print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    for idf in IDF_list:
        if not IDF_funcs.get(idf):
            print('IDF function "{}" is not existed.'.format(idf))
    for odf in ODF_list:
        if not ODF_funcs.get(odf):
            print('ODF function "{}" is not existed.'.format(odf))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')

def on_register(result):
    func = getattr(SA, 'on_register', None)
    print('[{}] Register successfully.'.format(dt.now().strftime('%Y-%m-%d %H:%M:%S')))
    check_df_funcs_exist(IDF_list, ODF_list)
    time.sleep(0.3)
    if func: func(result)

def MQTT_config(client):
    client.username_pw_set(MQTT_User, MQTT_PW)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    if MQTT_encryption: client.tls_set()
    client.connect(MQTT_broker, MQTT_port, keepalive=60)

DAN.profile['dm_name'] = device_model
DAN.profile['df_list'] = IDF_list + ODF_list  
if device_name: DAN.profile['d_name']= device_name
if MQTT_broker: DAN.profile['mqtt_enable'] = True

result = DAN.device_registration_with_retry(ServerURL, device_id)
if MQTT_broker:
    mqttc = mqtt.Client()
    MQTT_config(mqttc)
    mqttc.loop_start()
on_register(result)

def push(idf, IDF_data):
    if MQTT_broker:
        mqtt_pub(mqttc, device_id, idf, IDF_data)
    else: 
        DAN.push(idf, IDF_data)

def DF_function_handler():
    for idf in IDF_list:
        if not IDF_funcs.get(idf): continue
        IDF_data = IDF_funcs.get(idf)()
        if IDF_data == None: continue
        if type(IDF_data) is not tuple: IDF_data=[IDF_data]
        if MQTT_broker: mqtt_pub(mqttc, device_id, idf, IDF_data)
        else: DAN.push(idf, IDF_data)
        time.sleep(0.001)
    if not MQTT_broker: 
        for odf in ODF_list:
            if not ODF_funcs.get(odf): continue
            ODF_data = DAN.pull(odf)
            if ODF_data == None: continue
            ODF_funcs.get(odf)(ODF_data)
            time.sleep(0.001)

def reconnect(client):
    client.disconnect()
    client.loop_stop()
    time.sleep(0.5)
    print('[{}] MQTT reconnect...'.format(dt.now().strftime('%Y-%m-%d %H:%M:%S')))
    while True:
        try:
            client.reconnect()
            break
        except BaseException as err:
            ExceptionHandler(err)
    client.loop_start()
    time.sleep(0.5)

def ExceptionHandler(err):
    if isinstance(err, KeyboardInterrupt):
        DAN.deregister()
        print(' Bye~')
        exit()
    elif str(err).find('mac_addr not found:') != -1:
        print('Reg_addr is not found. Try to re-register...')
        DAN.device_registration_with_retry(ServerURL, device_id)
    else:
        exception = traceback.format_exc()
        print(exception)
        time.sleep(1)    



if __name__ == '__main__':
    tool.blit_text(game.screen,game.unifont_36,"Server : "+ServerURL,(255,255,255),(320,80),True)
    tool.blit_text(game.screen,game.unifont_36,"Model : "+device_model,(255,255,255),(320,120),True)
    tool.blit_text(game.screen,game.unifont_36,"Device Name : "+device_name,(255,255,255),(320,160),True)
    tool.blit_text(game.screen,game.unifont_36,"按Remote Control上任意鍵確認連線",(255,255,255),(320,400),True)
    tool.blit_text(game.screen,game.unifont_36,"按ESC退出    按F切換全螢幕",(255,255,255),(320,440),True)
    screen = pygame.display.get_surface()
    while True:
        try:
            if DISCONNECT: reconnect(mqttc)
            DF_function_handler()
            time.sleep(exec_interval)
        except BaseException as err:
            ExceptionHandler(err)
        pygame.time.Clock().tick(120)
        a=False
        if game.state == "animation":
            game.animate_board.fill((0,0,0))
            game.backgroud_scroll()
            game.slime_animation()
            game.blit_animate_board()
            if time.time()-game.timer>1:
                if game.score<=0:
                    game.state = "lose"
                    game.construct_lose()
                    game.score = 1
                    game.slime_list = [[0,290,5]]
                    game.level = 1
                    game.dragon_hp = 100
                    game.animate_board_scale = 1
                else:
                    game.level+=1
                    if game.level>game.total_level:
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
            game.blit_animate_board()
        elif game.state == "boss_entrance":
            game.animate_board.fill((0,0,0))
            game.boss_entrance_animation()
            game.backgroud_scroll()
            game.slime_animation()
            game.dragon_animation()
            game.blit_animate_board()
        screen.fill((0,0,0))
        screen.blit(game.screen,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                DAN.deregister()
                a=True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    DAN.deregister()
                    a=True
                    break
                elif event.key == pygame.K_f:
                    if(screen.get_flags()&pygame.FULLSCREEN):
                        screen=pygame.display.set_mode((640,480))
                    else:
                        screen=pygame.display.set_mode((640,480),pygame.FULLSCREEN)
                
        if a:
            break
        pygame.display.update()

