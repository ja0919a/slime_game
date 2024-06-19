組長:112550165 洪誥鴻 code

組員:
112550102 羅然 上台報告+題庫
110550114 吳錦麟 投影片+報告檔
1125501056 林瀚璿 遊戲素材

遊戲簡介:有一天，史萊姆的家被巨龍燒毀，憤怒的它決定向森林進軍，尋找巨龍。在路途上，史萊姆們想辦法集結成大軍，以數量的優勢打敗巨龍。

摘要:益智遊戲，主體使用pygame模組製作，經由iottalk的Remote Control傳給Dummy Device的回饋運行。本質上會比較像youtube廣告上常看到的糞game，但我們會努力讓他的外觀不會那麼的廉價......吧，我們將一位組員分去製作遊戲素材，因為一位好的美術會是遊戲成功的關鍵之一......大概吧，畢竟本質是糞game，所以不要有太大的期望。

resource資料夾:放圖片、字體、音效
game資料夾:遊戲主體
setup.py放一些預設物件
game.py遊戲主要運作
tool.py一些自製function
question.py題目
main.py處理iotsever回傳的值和運行

運行main.py開始遊戲
remote control 上只需要toggle和keypad 都連上dummy control

教程
1. 打開https://class.iottalk.tw (如果想換一個可以在SA.py上的ServerURL更改，但exe的修改不了)
2. 進入Project
3. select project -> add a project
4. Model -> Remote Control 點選 1 keypad, 1 toggle
5. Model -> Dummy Device 點選 Dummy Control
6. 將keypad和Dummy Control連線，toggle和Dummy Control連線 (記得檢查joint的IDF的type要sample)
7. 打開https://class.iottalk.tw/RemoteControl/+你喜歡的名字 (ex : https://class.iottalk.tw/RemoteControl/7tail)
8. 點一下Remote Control，選擇你決定的名字
9. `pip install -r requirements.txt`
10. 執行main.py或exe，點一下Dummy Device，選擇7tail_game

報告連結 : https://drive.google.com/drive/folders/1CnDZVyg7fv6cCfLDOszII-4aQ6h7gNVk?usp=sharing
報告影片 : https://youtu.be/YvN7K-56q6k
