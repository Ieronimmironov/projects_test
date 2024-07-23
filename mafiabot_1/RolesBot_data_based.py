import telebot
from telebot import types
import random
import sqlite3 as sl

u = ''

contain_chat = [0, ["mafia", "avalon"], [["mafia", "civilian", "doctor", "commisioner", "maniac", "leader"], ["Minion of Mordred", "Loyal Servant of Arthur", "Assassin", "Merlin", "Mordred", "Oberon", "Morgana", "Percival"]], True]
contain_group = [0, [], [], []]
group = {}
chat = {}

games = ['', '', '']

bot = telebot.TeleBot('6765293063:AAEQb52ZBWsug9gugYFHJAO0P92tjx6SKUY')

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

connection = sl.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Templates (
id INTEGER PRIMARY KEY,
user_id TEXT NOT NULL,
info TEXT NOT NULL
)
''')
connection.commit()
connection.close()

def is_empty(id):
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Games WHERE group_id = ?', (id,))
    game = cursor.fetchall()
    b_is = False
    if(len(game) == 0):
        b_is = True
    connection.commit()
    connection.close()
    return b_is
def add(group_id: str, users_id: str, users: str, info: str):
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Games (group_id, users_id, users, info) VALUES (?, ?, ?, ?)', (group_id, users_id, users, info))
    connection.commit()
    connection.close()
def update_group(group_id: str, users_id: str, users: str, info: str):
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
def load(id: str):
    global chat
    text = ''
    for i in range(len(chat[id][1])):
        text = text + '; ' + chat[id][1][i]
        for c in chat[id][2][i]:
            text = text + ', ' + c
    #is empty
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Templates WHERE user_id = ?', (id,))
    game = cursor.fetchall()
    connection.commit()
    connection.close()
    print(text)
    #update or add
    if(len(game) == 0):
        #add
        connection = sl.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Templates (user_id, info) VALUES (?, ?)', (id, text))
        connection.commit()
        connection.close()
    else:
        connection = sl.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE Templates SET info = ?  WHERE user_id = ?', (text, id))
        connection.commit()
        connection.close()
def download(id: str) -> list:
    #is empty
    connection = sl.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT info FROM Templates WHERE user_id = ?', (id,))
    game = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    print(game)
    temp = game.split("; ")[1:]
    templates = []
    for t in temp:
        templates.append(t.split(", "))
    print(templates)
    return templates     
def insert(id: str):
    global chat
    temp = download(id)
    chat[id][1] = []
    chat[id][2] = []
    for templates in temp:
        chat[id][1].append(templates[0])
        chat[id][2].append(templates[1:])

@bot.message_handler(commands=['start'])
def start(message):
    global group
    global chat
    global games
    global u
    games = ['', '', '']
    id = str(message.chat.id)
    user_id = str(message.from_user.id)
    u = user_id
    if(user_id == id):
        if(id not in chat):
            #download(id)
            chat[id] = [0, ["mafia", "avalon"], [["mafia", "civilian", "doctor", "commisioner", "maniac", "leader"], ["Minion of Mordred", "Loyal Servant of Arthur", "Assassin", "Merlin", "Mordred", "Oberon", "Morgana", "Percival"]], True]
        if(not chat[id][3]):
            chat[id][1] = chat[id][1][0:-1]
            chat[id][2] = chat[id][2][0:-1]
        chat[id][0] = 0
        start_button = types.InlineKeyboardMarkup(row_width=1)
        creat_a_new_template = types.InlineKeyboardButton("create a new template", callback_data="create_a_new_template")
        delete_the_saved_template = types.InlineKeyboardButton("delete the saved template", callback_data="delete_the_saved_template")
        start_button.add(creat_a_new_template, delete_the_saved_template)
        bot.send_message(id, "create a new template, or delete the saved template", reply_markup=start_button)
    else:
        if(id not in group):
            group[id] = [0, [], [], []]
        if(user_id not in chat):
            chat[user_id] = [0, ["mafia", "avalon"], [["mafia", "civilian", "doctor", "commisioner", "maniac", "leader"], ["Minion of Mordred", "Loyal Servant of Arthur", "Assassin", "Merlin", "Mordred", "Oberon", "Morgana", "Percival"]], True]
        group[id][0] = 0
        group[id][1] = []
        group[id][2] = []
        start_group_button = types.InlineKeyboardMarkup(row_width=1)
        creat_a_new_game = types.InlineKeyboardButton("create a new game", callback_data="create_a_new_game")
        open_the_saved_template = types.InlineKeyboardButton("open the saved template", callback_data="open_the_saved_template")
        if(not group[id][3] == []):
            start_group_button.row(types.InlineKeyboardButton("last game", callback_data="last_game"))
        start_group_button.add(creat_a_new_game, open_the_saved_template)
        bot.send_message(id, "create a new game, or open the saved template", reply_markup=start_group_button)
@bot.message_handler(commands=['mafia'])
def mafia_send(message):
    global games
    id = str(message.chat.id)
    if(group[id][0] == 3):
        if(not is_empty(id)):
            update_group(id, games[0], games[1], games[2])
        else:
            add(id, games[0], games[1], games[2])
        bot.send_message(message.chat.id, 'ok', parse_mode='Markdown')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global memory
    id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if(id == user_id):
        if(chat[id][0] == 1):#create_a_new_template
            chat[id][0] = 3
            chat[id][1].append(message.text)
            chat[id][2].append([])
            chat[id][3] == False
            ok_button = types.InlineKeyboardMarkup(row_width=1)
            ok_button.add(types.InlineKeyboardButton("ok", callback_data="ok_button"))
            bot.send_message(id, "click the button to complete the template creation", reply_markup=ok_button)
            bot.send_message(id, "write the names of the roles")
        elif(chat[id][0] == 2):#delete_the_saved_template
            name_of_template = message.text
            if(name_of_template in chat[id][1]):
                list_of_template = chat[id][2][chat[id][1].index(name_of_template)]
                chat[id][1].remove(name_of_template)
                chat[id][2].remove(list_of_template)
                bot.send_message(id, "ok, the template '" + name_of_template + "' has been deleted")
                chat[id][0] = 0
                load(id)
        elif(chat[id][0] == 3):
            chat[id][2][-1].append(message.text)
    else:
        if(group[id][0] == 1):#create_a_new_game
            group[id][1].append(message.text)
            group[id][3] = list(group[id][1])
        elif(group[id][0] == 2):#open_the_saved_template
            name_of_template = message.text
            list_of_template = chat[user_id][2][chat[user_id][1].index(name_of_template)]
            choose_role = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for role in list_of_template:
                choose_role.row(types.KeyboardButton(role))
            bot.send_message(id, "choose role", parse_mode='html', reply_markup=choose_role)
            group[id][0] = 1
            ok_button1 = types.InlineKeyboardMarkup(row_width=1)
            ok_button1.add(types.InlineKeyboardButton("ok", callback_data="ok_button1"))
            bot.send_message(id, "Then click the button to start the game", reply_markup=ok_button1)
@bot.callback_query_handler(func=lambda call: call.data == "create_a_new_template")
def creaet_a_new_template_pressed(call: types.CallbackQuery):
    global chat
    id = str(call.message.chat.id)
    if(chat[id][0] == 0):
        bot.send_message(chat_id=call.message.chat.id, text="choose name of your new template")
        chat[id][0] = 1
@bot.callback_query_handler(func=lambda call: call.data == "delete_the_saved_template")
def delete_the_saved_template_pressed(call: types.CallbackQuery):
    global chat
    id = str(call.message.chat.id)
    if(chat[id][0] == 0):
        chat[id][0] = 2
        choose_template = types.ReplyKeyboardMarkup(resize_keyboard=True)
        insert(id)
        templates = chat[id][1]
        for temp in templates:
            choose_template.row(types.KeyboardButton(temp))
        bot.send_message(id, "choose one of this templates", parse_mode='html', reply_markup=choose_template)        
@bot.callback_query_handler(func=lambda call: call.data == "create_a_new_game")
def create_a_new_game_pressed(call: types.CallbackQuery):
    global group
    id = str(call.message.chat.id)
    if(group[id][0] == 0):
        group[id][0] = 1
        ok_button1 = types.InlineKeyboardMarkup(row_width=1)
        ok_button1.add(types.InlineKeyboardButton("ok", callback_data="ok_button1"))
        bot.send_message(id, "write roles, then click the button to start the game", reply_markup=ok_button1)
@bot.callback_query_handler(func=lambda call: call.data == "open_the_saved_template")
def open_the_saved_template_pressed(call: types.CallbackQuery):
    global chat
    id = str(call.message.chat.id)
    user_id = str(call.from_user.id)
    if(group[id][0] == 0):
        if(user_id not in chat):
            chat[user_id] = list(contain_chat.copy())
        insert(user_id)
        group[id][0] = 2
        choose_template = types.ReplyKeyboardMarkup(resize_keyboard=True)
        templates = chat[user_id][1]
        for temp in templates:
            choose_template.row(types.KeyboardButton(temp))
        bot.send_message(id, "choose one of this templates", parse_mode='html', reply_markup=choose_template)
@bot.callback_query_handler(func=lambda call: call.data == "ok_button")
def ok_button(call: types.CallbackQuery):
    global chat
    id = str(call.from_user.id)
    if(chat[id][0] == 3):
        bot.send_message(call.message.chat.id, "ok, the new template has been created")
        chat[id][0] = 0
        chat[id][3] = True
        load(id)
@bot.callback_query_handler(func=lambda call: call.data == "ok_button1")
def ok_button1(call: types.CallbackQuery):
    global group
    id = str(call.message.chat.id)
    if(group[id][0] == 1):
        get_role = types.InlineKeyboardMarkup(row_width=1)
        get_role.add(types.InlineKeyboardButton("get", callback_data="get_role"))
        bot.send_message(id, "ok, click the button to get role", reply_markup=get_role)
        group[id][0] = 3
        choose_template = types.ReplyKeyboardMarkup(resize_keyboard=True)
        st = types.KeyboardButton('/start')
        mf = types.KeyboardButton('/mafia')
        choose_template.row(st, mf)
        bot.send_message(id, "Next?", parse_mode='html', reply_markup=choose_template)
@bot.callback_query_handler(func=lambda call: call.data == "get_role")
def get_role(call: types.CallbackQuery):
    global group
    global games
    id = str(call.message.chat.id)
    user_id = str(call.from_user.id)
    if((user_id not in group[id][2]) and (len(group[id][1]) > 0) and (group[id][0] == 3)):
        rand = random.randint(0, len(group[id][1]) - 1)
        role = group[id][1][rand]
        bot.send_message(call.from_user.id, role)
        group[id][2].append(user_id)
        group[id][1].remove(role)
        games[0] = games[0] + ', ' + str(call.from_user.id)
        games[1] = games[1] + ', ' + str(call.from_user.first_name)
        games[2] = games[2] + ', ' + role
        print(games)
        print(games[0].split(", ")[1:])
@bot.callback_query_handler(func=lambda call: call.data == "last_game")
def last_game(call: types.CallbackQuery):
    global group
    id = str(call.message.chat.id)
    if(group[id][0] == 0):
        group[id][1] = list(group[id][3].copy())
        group[id][0] = 3
        get_role = types.InlineKeyboardMarkup(row_width=1)
        get_role.add(types.InlineKeyboardButton("get", callback_data="get_role"))
        bot.send_message(id, "ok, click the button to get role", reply_markup=get_role)

bot.infinity_polling()
