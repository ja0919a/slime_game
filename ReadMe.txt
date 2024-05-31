resource資料夾:放圖片、字體、音效
game資料夾:遊戲主體
setup.py放一些預設物件
game.py遊戲主要運作
tool.py一些自製function
question.py題目

運行main.py開始遊戲
remote control 上只需要toggle和keypad 都連上dummy control

教程
1. 打開https://6.iottalk.tw(如果想換一個可以在SA.py上的ServerURL更改)
2. 進入Project
3. select project -> add a project
4. Model -> Remote Control 點選 1 keypad, 1 toggle
5. Model -> Dummy Device 點選 Dummy Control
6. 將keypad和Dummy Control連線，toggle和Dummy Control連線
7. 打開https://6.iottalk.tw/RemoteControl/+你喜歡的名字(ex : https://6.iottalk.tw/RemoteControl/7tail)
8. 點一下Remote Control，選擇你決定的名字
9. `pip install -r requirements.txt`
10. 執行main.py或exe，點一下Dummy Device，選擇7tail_game
