class question:
    def __init__(self, question:list, answer:str, type, reward:int=0):
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
                 question(["史萊姆們呼喚了隱藏在森林的同伴","吸引了____隻史萊姆"],None,0,2)]
