import telebot
import time 
import sqlite3 as sl
from telebot import types
memory = {}
step = {}

voting = {}
result = {}
chooses = {}
vot = {}

mafia = {}
commisioner = {}
doctor = {}

bot = telebot.TeleBot('token')
connection = sl.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Games (
id INTEGER PRIMARY KEY,
group_id TEXT NOT NULL, 
users_id TEXT NOT NULL,
users TEXT NOT NULL,
info TEXT NOT NULL
)
''')

connection.commit()
connection.close()

def is_empty(id):
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Games WHERE group_id = ?', (id,))
    games = cursor.fetchall()
    if(len(games) == 0):
        return True
    connection.commit()
    connection.close()
    return False
def add(group_id: str, users_id: str, users: str, info: str):
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Games (group_id, users_id, users, info) VALUES (?, ?, ?, ?)', (group_id, users_id, users, info))
    connection.commit()
    connection.close()
def update_group_game(group_id: str, users_id: str, users: str, info: str):
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Games SET users_id = ?, users = ?, info = ?  WHERE group_id = ?', (users_id, users, info, group_id))
    connection.commit()
    connection.close()
def get_info(id):
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT users_id, users, info FROM Games WHERE group_id = ?', (id,))
    game = cursor.fetchall()
    print(game)
    connection.commit()
    connection.close()
    return game
def print_all():
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Games')
    games = cursor.fetchall()
    for game in games:
        print(game)
    connection.commit()
    connection.close()

def sort_roles(id):
    global mafia
    global commisioner
    global doctor
    global memory
    mem = [memory[id][0].copy(), memory[id][1].copy(), memory[id][2].copy()]
    mafia[id] = []
    commisioner[id] = []
    doctor[id] = []
    while('mafia' in mem[2]):
        ind = mem[2].index('mafia')
        mem[2].pop(ind)
        mafia[id].append(ind)
    while('commisioner' in mem[2]):
        ind = mem[2].index('commisioner')
        mem[2].pop(ind)
        commisioner[id].append(ind)
    while('doctor' in mem[2]):
        ind = mem[2].index('doctor')
        mem[2].pop(ind)
        doctor[id].append(ind)
    print(mafia)
def delete(id: str, ind):
    global memory
    global mafia
    global commisioner
    global doctor
    memory[id][0].pop(ind)
    memory[id][1].pop(ind)
    memory[id][2].pop(ind)
    if(ind in mafia[id]):
        mafia[id].remove(ind)
    elif(ind in commisioner[id]):
        commisioner[id].remove(ind)
    elif(ind in doctor[id]):
        doctor[id].remove(ind)
def meet(id: str):
    for ind in range(len(mafia[id])):
        for i in range(len(mafia[id])):
            if(i != ind):
                bot.send_message(memory[id][0][mafia[id][i]], memory[id][1][mafia[id][ind]])
    for ind in range(len(doctor[id])):
        for i in range(len(doctor[id])):
            if(i != ind):
                bot.send_message(memory[id][0][doctor[id][i]], memory[id][1][doctor[id][ind]])
    for ind in range(len(commisioner[id])):
        for i in range(len(commisioner[id])):
            if(i != ind):
                bot.send_message(memory[id][0][commisioner[id][i]], memory[id][1][commisioner[id][ind]])
def send_another(l: list, text, ind):
    for i in range(len(l[id])):
        if(i != ind):
            bot.send_message(l[i][0], text)
def is_win(id):
    global step
    l = 0
    if('maniac' in memory[id][2]):
        l = 1
    if(not mafia[id] and not 'maniac' in memory[id][2]):
        bot.send_message(id, "The city has won!")
    if((len(mafia[id]) + l) >= (len(voting[id]) - len(mafia[id]) - l)):
        bot.send_message(id, "The mafia has won!")
    step[id] = -1
               
def choose_voting(id: str):
    choose_voting = types.InlineKeyboardMarkup(row_width=1)
    choose_player = types.InlineKeyboardButton("voting", callback_data="choose_player")
    night = types.InlineKeyboardButton("night", callback_data="night_voting")
    choose_voting.add(choose_player, night)
    bot.send_message(id, "choose one of this voting", reply_markup=choose_voting)
@bot.message_handler(commands=['start'])
def start(message):
    id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if(id != user_id):
        step[id] = 0
        voting[id] = []
@bot.message_handler(commands=['mafia'])
def maf(message):
    global memory
    id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if(step[id] == 0 and id != user_id):
        step[id] = 1
        chooses[id] = ['', [], [], []]
        time.sleep(1.0)
        memory_id = []
        memory_id = get_info(id)
        memory[id] = []
        voting[id] = []
        if(len(memory_id) > 0):
            memory[id] = [memory_id[0][0].split(", ")[1:], memory_id[0][1].split(", ")[1:], memory_id[0][2].split(", ")[1:]]#!!!
            print(memory)
        bot.send_message(id, "Ok, I get the game", parse_mode='Markdown')
        sort_roles(id)
        print(memory)
        #<spoiler
        for i in range(len(memory[id][0])):
            bot.send_message(id, memory[id][1][i] + ' ' + memory[id][2][i], parse_mode='Markdown')
        #>
        meet(str(message.chat.id))
        choose_voting(str(message.chat.id))
    
@bot.callback_query_handler(func=lambda call: call.data == "choose_player")
def choose_player(call: types.CallbackQuery):
    global step
    global vot
    id = str(call.message.chat.id)
    user_id = str(call.from_user.id)
    if(id != user_id and step[id] == 1):
        step[id] = 3
        vot[id] = {}
        voting = types.InlineKeyboardMarkup(row_width=1)
        for i in range(len(memory[id][0])):
            voting.add(types.InlineKeyboardButton(memory[id][1][i], callback_data="voting"))
        bot.send_message(id, "choose a plyaer", reply_markup=voting)
@bot.callback_query_handler(func=lambda call: call.data == "night_voting")
def night_voting(call: types.CallbackQuery):
    global step
    id = str(call.message.chat.id)
    user_id = str(call.from_user.id)
    if(id != user_id and step[id] == 1):
        step[id] = 2
        night_voting = types.InlineKeyboardMarkup(row_width=1)
        for i in range(len(memory[id][0])):
            night_voting.add(types.InlineKeyboardButton(memory[id][1][i], callback_data="night"))
        bot.send_message(id, "choose a plyaer", reply_markup=night_voting)
@bot.callback_query_handler(func=lambda call: call.data == "night")
def night(call: types.CallbackQuery):
    global voting
    global memory
    global chooses
    id = str(call.message.chat.id)
    user_id = str(call.from_user.id)
    if(id != user_id and step == 2 and user_id in memory[id][0]):
        ind1 = memory[id][0].index(user_id)
        role1 = memory[id][2][ind1]
        text = call.message.text
        ind2 = memory[id][1].index(text)
        role2 = memory[id][2][ind2]
        if(user_id not in voting[id]):
            voting[id].append(ind1)
        if(role1 == "maniac"):
            if(ind1 != ind2):
                bot.send_massage(user_id, "Your choose: " + role2)
                chooses[id][0] = ind2
        elif(role1 == "mafia"):
            if(role2 != "mafia" and len(chooses[id][1]) != len(mafia[id])):
                bot.send_massage(user_id, "Your choose: " + role2)
                if(len(chooses[id][1]) > 0 and chooses[id][1][0] != ind2):
                    for i in chooses[id][1]:
                        voting[id].remove(i)
                    chooses[id][1] = []
                chooses[id][1].append(ind2)
                send_another(id, role1 + ' choose: ' + role2, ind1)
        elif(role1 == "commisioner"):
            if(role2 != "commisioner"):
                bot.send_massage(user_id, "Your choose: " + role2)
                if(len(chooses[id][2]) > 0 and chooses[id][2][0] != ind2):
                    for i in chooses[id][2]:
                        voting[id].remove(i)
                    chooses[id][2] = []
                chooses[id][2].append(ind2)
                send_another(id, role1 + ' choose: ' + role2, ind1)
        elif(role1 == "doctor"):
            bot.send_massage(user_id, "Your choose: " + role2)
            if(len(chooses[id][3]) > 0 and chooses[id][3][0] != ind2):
                for i in chooses[id][3]:
                    voting[id].remove(i)
                chooses[id][3] = []
            send_another(id, role1 + ' choose: ' + role2, ind1)
        else:
            bot.send_message(user_id, "Ok")
        if(len(memory[id][0]) == len(voting[id])):
            step[id] = 1
            p = ', '
            m1 = memory[id][1][chooses[id][0]]
            m2 = memory[id][1][chooses[id][1][0]]
            d = memory[id][1][chooses[id][3][0]]
            if(m1 == m2):
                m1 = ''
                p = ''
                delete(id, chooses[id][0])
            else:
                delete(id, chooses[id][0])
                delete(id, chooses[id][1][0])
            if(m1 == d):
                m1 = ''
                p = ''
            if(m2 == d):
                m2 = ''
                p = ''
            if(m1 != '' or m2 != ''):
                killed = 'Killed: ' + m1 + p + m2 + ". The doctor didn't guess right"
            else:
                killed = 'No one was killed. The doctor guessed right'
            if(chooses[id][2] in mafia[id]):
                com = 'The commisioner guessed the mafia'
            else:
                com = 'The commisioner did not guess the mafia'
            result = killed + "\n" + com
            bot.send_message(id, result)
            is_win(id)
            step[id] = 1
            choose_voting(id)
@bot.callback_query_handler(func=lambda call: call.data == "voting")
def voting(call: types.CallbackQuery):
    global vot
    global memory
    global voting
    id = str(call.message.chat.id)
    user_id = str(call.from_user.id)
    if(id != user_id and step[id] == 3 and user_id in memory[id][0]):
        text = call.message.text
        ind1 = memory[id][0].index(user_id)
        ind2 = memory[id][1].index(text)
        if(ind1 == ind2):
            return
        if(ind2 not in vot[id]):
            vot[id][ind2] = []
        vot[id][ind2].append(ind1)
        llist = ''
        voting[id].append(ind1)
        if(len(voting[id]) == len(memory[id][0])):
            m = 0
            mi = ''
            mes = ''
            for i1 in vot[id].keys():
                for i2 in vot[id][i1]:
                    llist = llist + ', ' + memory[id][1][i2]
                #bot.send_message(id, memory[id][1][i1] + ': ' + llist[2:])
                mes = mes + memory[id][1][i1] + ': ' + llist[2:] + "\n"
                if(len(voting[id][i1]) > m):
                    m = len(voting[id][i1])
                    mi = i1
            delete(id, mi)
            bot.send_message(id, mes)
            bot.send_message(id, memory[id][1][mi] + ' eliminated')
            is_win(id)
                

bot.infinity_polling()
