class question:
    def __init__(self, question:list, answer:str, type, reward:int=0, choice=[]):
        self.question = question
        self.answer = answer 
        self.type = type # 0: 選擇題(無正確答案) answer請填None 1: 選擇題(有正確答案) answer為長度為3的list 2: 填空題
        self.reward = reward # 0: 有正確答案，答對加答錯減 1: 史萊姆數量乘上答案 2: 史萊姆數量加上答案 3: 史萊姆數量減去答案 4: 史萊姆數量除以答案
class choice:
    def __init__(self, choice:str, choice_num:str):
        self.choice = choice #題目數字
        self.choice_num = choice_num #答案數字
choose_question_mutiple_choice_list = [ choice('cos0°','1'), #只有數字
                                        choice('cos90°','0'), 
                                        choice('sin90°','1'),
                                        choice('tan45°','1'),
                                        choice('tan0°','0'),
                                        choice('1','1'),
                                        choice('2','2'),
                                        choice('3','3'),
                                        choice('4','4'),
                                        choice('5','5'),
                                        choice('6','6'),
                                        choice('7','7'),
                                        choice('8','8'),
                                        choice('9','9'),
                                        choice('10','10'),
                                        choice('e','2.71828')]
question_list = [question(["史萊姆們感受到隱藏在身體裡的潛力","將自己複製成____倍"],None,0,1),
                 question(["路過的忍者讓史萊姆們領悟了分身術","將自己複製成____倍"],None,0,1),
                 question(["史萊姆們呼喚了隱藏在森林的同伴","吸引了____隻史萊姆"],None,0,2),
                 question(["史萊姆們的春天到了❤","史萊姆們啪啪啪生出了____隻史萊姆"],None,0,2),
                 question(["有冒險者小隊來討伐史萊姆了!","有____隻史萊姆被殺死了"],None,0,3),
                 question(["性愛用品企業來補充史萊姆黏液的庫存了!","有____隻史萊姆被抓走了"],None,0,3),
                 question(["野生的訓練家出現了!訓練家對史萊姆們使用了精靈球!","萊姆萊姆!有____隻史萊姆被Get daze了!"],None,0,3),
                 question(["地板忽然裂開冒出了岩漿!","只有____分之一倍的史萊姆沒被燒死了"],None,0,4),
                 question(["因為附近強者間的決鬥 空間被打到裂開了!","只有____分之一倍的史萊姆沒被吸入次元的裂縫"],None,0,4),
                 question(["\"你才是挑戰者喔\"史萊姆們路過附近強者間的決鬥","和說這句話的高等冒險者一起被砍成____分之一倍了"],None,0,4)]
