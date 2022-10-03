import random
import re

def is_num(word: str): #num인지 파악
    num_str = ''
    comma_str = 0
    p1 = re.compile('\d{2}.\d{2}.\d{2,4}')
    p2 = re.compile('\d{2}-\d{2}-\d{2,4}')
    if p1.match(word) != None or p2.match(word) != None:
        return False, None

    for i in range(len(word)):
        if ord('0') <= ord(word[i]) <= ord('9'):
            num_str += word[i]
        elif word[i]==',':
            comma_str += 1
        elif word[i]=='.':
            num_str += '.'

    if len(word) == 0: #문자열 없으면 None 반환
        return False, word
    if len(num_str) + comma_str == len(word):
        return True, word.replace(',', '.')
    if len(num_str) * 2 >= len(word):
        return True, word
    else:
        return False, word

def is_number_column(table_data: list, col_idx: int): #Column 중에 num이 있는지 확인
    is_number = True
    column_content = []
    for i in range(1, len(table_data)):
        isNum, cont = is_num(table_data[i][col_idx]) # T/F 반환만 원함
        if isNum is False:
            is_number = False
        column_content.append(cont)
    return is_number, column_content

class Table_template:
    def __init__(self, table_name, table):
        self.src_table = table
        self.src_Table_name = table_name

        ## To find Basic (Like name) column
        self.is_basic_found = False
        self.is_basic_name = False
        self.number_column = {} ## NAME 같은 베이직 컬럼 설정해두고 텍스트 주어로 쓰기 (ex) helen's ~~
        self.basic_column = {}
        self.not_basic_column = {}

        for index in range(len(self.src_table)):
            ans, cont = is_number_column(self.src_table, index)
            if ans:
                self.number_column[index] = cont
                self.not_basic_column[index] = cont
            else:
                if not self.is_basic_found:
                    if self.src_table[0][index] == 'name' or 'Name' or 'NAME':
                        self.is_basic_name = True
                    self.basic_column[index] = cont
                    is_basic_found = True
                else:
                    self.not_basic_column[index] = cont

    def select_random_column(self):
        select_column_index = random.choice(list(self.not_basic_column.keys()))

        return select_column_index, self.not_basic_column[select_column_index]

    def make_text_1(self, table_name, basic_col, cont_col_index, content_col): # all column _ epigraph
        cont_col_name = self.src_table[0][cont_col_index]
        text = f'In {table_name}, '

        for index, (basic, cont) in enumerate(zip(list(basic_col.values())[0], content_col)):
            if index == len(content_col) - 1:
                text += f'and {basic}\'s {cont_col_name} is {cont}.'
                break
            text += f'{basic}\'s {cont_col_name} is {cont}, '
        return text

    def make_text_2(self, table_name, basic_col, cont_col_index, content_col): ## Only num column _ total
        if cont_col_index in list(self.number_column.keys()):
            cont_col_name = self.src_table[0][cont_col_index]
            text = 'In this table, '
            total = 0
            for index, (basic, cont) in enumerate(zip(list(basic_col.values())[0], content_col)):
                text += f'{basic}\'s {cont_col_name} is {cont}, '
                total += float(cont)
            text += f'and Total of {cont_col_name} is {total}.'
            return text
        else:
            return 'No numerical'

    def make_text_3(self, table_name, basic_col, cont_col_index, content_col):  ## Only num column _ diff
        basic_col = list(basic_col.values())[0]
        if cont_col_index in list(self.number_column.keys()):
            cont_col_name = self.src_table[0][cont_col_index]
            text = f'In {table_name}, {basic_col[0]}\'s {cont_col_name} is {content_col[0]},'
            for index in range(1, len(basic_col)-1):
                text += f' {basic_col[0]} is as different as {basic_col[index]} and {abs(float(content_col[0])-float(content_col[index]))},'
            text += f'{basic_col[0]} is as different as {basic_col[-1]} and {abs(float(content_col[0])-float(content_col[-1]))}.'
            return text
        else:
            return 'No numerical'

    def make_text_4(self, table_name, basic_col, cont_col_index, content_col): ## Only num column _ avg
        if cont_col_index in list(self.number_column.keys()):
            cont_col_name = self.src_table[0][cont_col_index]
            text = ''
            total = 0
            for index, (basic, cont) in enumerate(zip(list(basic_col.values())[0], content_col)):
                text += f'{basic}\'s {cont_col_name} is {cont}, '
                total += float(cont)
            text += f'So Average of {cont_col_name} is {total/len(basic_col)} on this table.'
            return text
        else:
            return 'No numerical'

    def make_text_5(self, table_name, basic_col, cont_col_index, content_col): # all column - describe basic column
        cont_col_name = self.src_table[0][cont_col_index]
        text = 'First, There is '
        cont_col_2, cont_2, cont_col_name_2 = cont_col_index, '', ''

        while(cont_col_2 == cont_col_index):
            cont_col_2, cont_2 = self.select_random_column()

        cont_col_name_2 = self.src_table[0][cont_col_2]

        for index, (cont, cont2) in enumerate(zip(content_col, cont_2)):
            text += f'case where {cont_col_name} is {cont} and {cont_col_name_2} is {cont2}, '
            if index == len(content_col)-1:
                text += f'and lastly case that {cont_col_name} is {cont} and {cont_col_name_2} is {cont2} on this table.'
        return text

    def make_text_6(self, table_name, basic_col, cont_col_index, content_col): ## Only num column _ portion
        basic_col = list(basic_col.values())[0]
        if cont_col_index in list(self.number_column.keys()):
            cont_col_name = self.src_table[0][cont_col_index]
            text = f'In {table_name}, {basic_col[0]}\'s {cont_col_name} is {content_col[0]},'
            for index in range(1, len(basic_col) - 1):
                text += f' {basic_col[0]} is {float(content_col[0])/float(content_col[index])} times {basic_col[index]},'
            text += f'{basic_col[0]} is {float(content_col[0]) - float(content_col[-1])} times {basic_col[-1]}.'
            return text
        else:
            return 'No numerical'


if "__main__" == __name__:
    Table_name = 'BG Karlsruhe'
    Table_1 = list() # 수에 단위 붙은 경우는 나중에 따로 구현해야함요,, 흑ㅎㄱ
    Table_1.append(['number', 'name', 'Position', 'Birthday', 'Size', 'Weight', 'Last Team'])
    Table_1.append(['5', 'Tom Lipke', 'Guard/ Forward', '12.04.1986', '1,96', '98', 'Bremen Roosters'])
    Table_1.append(['6', 'Muamer Taletovic', 'Guard', '02.04.1976', '1,87', '90', 'SSC Karlsruhe'])
    Table_1.append(['7', 'David Watson', 'Forward', '16.09.1988', '1,84', '100', 'Hertener Löwen'])
    Table_1.append(['8', 'Brandon Gary', 'Center', '26.01.1983', '2,03', '110', 'Aschersleben Tiger'])
    Table_1.append(['9', 'Theodis Tarver', 'Guard', '09.07.1984', '2,06', '108', 'Chemosvit Svit'])
    Table_1.append(['10', 'Muamer Taletovic', 'Forward', '25.05.1977', '1,80', '68', 'SG Bad Dürkheim/Speyer'])
    #######################################################################

    src_table_name = Table_name
    src_table = Table_1

    Table_Maker = Table_template(src_table_name, src_table)
    idx, cont = Table_Maker.select_random_column()

    ## 1
    print(Table_Maker.make_text_1(Table_Maker.src_Table_name, Table_Maker.basic_column, idx, cont))
    ## 2
    print(Table_Maker.make_text_2(Table_Maker.src_Table_name, Table_Maker.basic_column, idx, cont))
    ## 3
    print(Table_Maker.make_text_3(Table_Maker.src_Table_name, Table_Maker.basic_column, idx, cont))
    ## 4
    print(Table_Maker.make_text_4(Table_Maker.src_Table_name, Table_Maker.basic_column, idx, cont))
    ## 5
    print(Table_Maker.make_text_5(Table_Maker.src_Table_name, Table_Maker.basic_column, idx, cont))
    ## 6
    print(Table_Maker.make_text_6(Table_Maker.src_Table_name, Table_Maker.basic_column, idx, cont))