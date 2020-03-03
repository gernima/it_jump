import telebot
from telebot import types
import DIARY
import pickle
import test


print('start')
bot = telebot.TeleBot('1016001810:AAGPWnpJYQFGMnjxRSfROW8ALMxBygo0I7Q')
message_lesson_id = []
message_food_id = list()
stop = True
FOOD = {}
food_who_id = set()
people = 0
message_lesson = []
stolovka_all = '❌'
stolovka_food = '❌'
stolovka_who = '❌'
lessons = open('lessons', 'rb')
LESSONS = pickle.load(lessons)
lessons.close()
m = types.InlineKeyboardMarkup(row_width=3)
item_1 = types.InlineKeyboardButton(text='🗽Английский', callback_data='0')
item_2 = types.InlineKeyboardButton(text='🌌Астрономия', callback_data='1')
item_3 = types.InlineKeyboardButton(text='🦠Биология', callback_data='2')
item_4 = types.InlineKeyboardButton(text='🌍География', callback_data='3')
item_5 = types.InlineKeyboardButton(text='🖥Информатика', callback_data='4')
item_6 = types.InlineKeyboardButton(text='🏛История', callback_data='5')
item_7 = types.InlineKeyboardButton(text='📖Литература', callback_data='6')
item_8 = types.InlineKeyboardButton(text='📈Математика', callback_data='7')
item_9 = types.InlineKeyboardButton(text='💬Обществознание', callback_data='8')
item_10 = types.InlineKeyboardButton(text='⛑ОБЖ', callback_data='9')
item_11 = types.InlineKeyboardButton(text='🎭Родная литература', callback_data='10')
item_12 = types.InlineKeyboardButton(text='🎮Родной язык', callback_data='11')
item_13 = types.InlineKeyboardButton(text='📝Русский язык', callback_data='12')
item_14 = types.InlineKeyboardButton(text='🛠Технология', callback_data='13')
item_15 = types.InlineKeyboardButton(text='💡Физика', callback_data='14')
item_16 = types.InlineKeyboardButton(text='⚽️Физ - ра', callback_data='15')
item_17 = types.InlineKeyboardButton(text='🧪Химия', callback_data='16')
m.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8, item_9, item_10,
      item_11, item_12, item_13, item_14, item_15, item_16, item_17)
keyboard_edu = telebot.types.ReplyKeyboardMarkup(True)
keyboard_edu.row("Табель")
keyboard_edu.row("Авторизация")
keyboard_edu.row("Назад")

murkup = types.ReplyKeyboardMarkup(True, row_width=3)
item_1 = types.KeyboardButton('Записать Д/З')
item_2 = types.KeyboardButton('Что задали')
item_3 = types.InlineKeyboardButton('Столовая')
item_4 = types.InlineKeyboardButton('Табель успеваемости')
murkup.add(item_1, item_2, item_3, item_4)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.text == '/start':
        laste_name = message.from_user.last_name
        if not laste_name:
            laste_name = ''
        bot.send_message(message.chat.id,
                         'Привет, ' + message.from_user.first_name + ' ' + laste_name +
                         '\n\nПропиши /help, если что-то не понятно', reply_markup=murkup)
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'В разработке, выкручивайся сам'
                                          '\nКак вариант, жми на все кнопки подряд)')


def get_dz(message):
    try:
        test.click_hm(message, bot, keyboard_edu)
    except:
        bot.send_message(message.chat.id,
                         'Проверьте логин и пароль указаный при авторизации, и при необходимости заново авторизуйтесь',
                         reply_markup=keyboard_edu)
    bot.register_next_step_handler(message, edu_tatar)


def edu_tatar(message):
    text = message.text
    if text == 'Назад':
        bot.send_message(message.chat.id, 'Хорошо', reply_markup=murkup)
        bot.register_next_step_handler(message, text)
    elif text == 'Авторизация':
        bot.send_message(message.chat.id, 'Введите логин и пароль через пробел', reply_markup=keyboard_edu)
        bot.register_next_step_handler(message, edu_tatar)
    elif text == 'Табель':
        bot.send_message(message.chat.id, 'Хорошо', reply_markup=keyboard_edu)
        bot.register_next_step_handler(message, edu_tatar)


@bot.message_handler(content_types=['text'])
def text(message):
    global message_lesson
    global message_food
    global stolovka_food
    global lessons
    global people

    if message.from_user.id == people:
        people = message.text
        if str(people).isdigit() and int(people) > 0:
            bot.send_message(message.chat.id, '♻️Число людей обновлено♻')
        else:
            people = message.from_user.id
            bot.send_message(message.chat.id, '❌Вы ввели не коректное число❌\n⬇️Напишите число ниже⬇️')
            bot.register_next_step_handler(message, text)
    elif message.text == 'Записать Д/З':
        bot.send_message(message.chat.id, 'Выбирай️', reply_markup=m)
    elif message.text == 'Табель успеваемости':
        bot.send_message(message.chat.id, 'Выбирай️', reply_markup=keyboard_edu)
        bot.register_next_step_handler(message, edu_tatar)
    elif message.text == 'Что задали':  # Выбор дня
        murkup = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton('1️⃣Понедельник', callback_data='day_понедельник_0')
        item_2 = types.InlineKeyboardButton('2️⃣Вторник', callback_data='day_вторник_1')
        item_3 = types.InlineKeyboardButton('3️⃣Среда', callback_data='day_среда_2')
        item_4 = types.InlineKeyboardButton('4️⃣Четверг', callback_data='day_четверг_3')
        item_5 = types.InlineKeyboardButton('5️⃣Пятница', callback_data='day_пятница_4')
        item_6 = types.InlineKeyboardButton('6️⃣Суббота', callback_data='day_суббота_5')
        item_7 = types.InlineKeyboardButton('⬇️Вся домашка⬇️️', callback_data='day_/_all')
        murkup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7)
        bot.send_message(message.chat.id, 'Какой день', reply_markup=murkup)
    elif message.text == 'Столовая':  # столовая
        if people:
            if message.from_user.id == people:
                bot.send_message(message.chat.id, '❌Вы ввели не коректное число❌\nДавайте заного')
            else:
                choice = types.InlineKeyboardMarkup()
                item_1 = types.InlineKeyboardButton('Добавить' + stolovka_food,
                                                    callback_data='stolovka_write')
                item_2 = types.InlineKeyboardButton('Записаться' + stolovka_all,
                                                    callback_data='stolovka_add')
                item_3 = types.InlineKeyboardButton('Отметить' + stolovka_who,
                                                    callback_data='stolovka_who')
                choice.add(item_1, item_2, item_3)
                bot.send_message(message.chat.id, "Что ты хочешь сделать?",reply_markup=choice)
                message_food_id.append(message.from_user.id)
        else:
            bot.send_message(message.chat.id, 'Сколько людей в классе?\n⬇Напишите число ниже⬇')
            people = message.from_user.id
    elif message.from_user.id in message_lesson_id:  # добавление домашки
        i = message_lesson_id.index(message.from_user.id)
        LESSONS[message_lesson.pop(i)] = message.text
        del message_lesson_id[i]
        bot.send_message(message.chat.id, '♻️Домашка обновлена♻️')
        lessons = open('lessons', 'wb')
        pickle.dump(LESSONS, lessons)
        lessons.close()
    elif message.from_user.id in message_food_id:
        del message_food_id[message_food_id.index(message.from_user.id)]
        global FOOD
        stolovka_food = '✅'
        FOOD[message.text] = [0, 0]
        bot.send_message(message.chat.id, '♻️Название блюда обновлено♻️')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global FOOD
    global stolovka_food
    global stolovka_who
    global stolovka_all
    global people
    global message_food_id
    global food_who_id

    if call.data == '-':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали:  ' + \
                                   call.message.text[
                                   call.message.text.find(':') + 2: call.message.text.find(
                                       '\n')] + '\n⬇️Напишите домашку ниже⬇️')
        message_lesson_id.append(call.from_user.id)
        message_lesson.append(
            call.message.text[call.message.text.find(':') + 3: call.message.text.find('\n')])
    elif call.data == '+':
        bot.delete_message(call.message.chat.id, call.message.json['message_id'])
        bot.send_message(call.message.chat.id, 'Выбирай️', reply_markup=m)
    elif call.data[:3] == 'day':  # Вывод домашки
        if call.data.split('_')[2] == 'all':
            pass
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали\n' +
                                   call.message.json['reply_markup']['inline_keyboard'][
                                       int(call.data.split('_')[2]) // 2][
                                       int(call.data.split('_')[2]) - \
                                       int(call.data.split('_')[2]) // 2 * 2]['text'])
        print_ = []
        for lesson in DIARY.DIARY[int(call.data.split('_')[2])]:
            print_.append(lesson + ':  ' + LESSONS.get(lesson, 'Домашки нет'))
        bot.send_message(call.message.chat.id, '\n\n'.join(print_))
    elif call.data.split('_')[0] == 'stolovka':
        if FOOD:
            if call.data.split('_')[1] == 'add':
                if FOOD[''.join(list(FOOD.keys())[0])][0] + FOOD[''.join(list(FOOD.keys())[0])][1] < int(people):
                    murkup = types.InlineKeyboardMarkup()
                    item_1 = types.InlineKeyboardButton('✅' + str(list(FOOD.values())[0][0]),
                                                        callback_data='stolovka_+')
                    item_2 = types.InlineKeyboardButton('❌' + str(list(FOOD.values())[0][1]),
                                                        callback_data='stolovka_-')
                    murkup.add(item_1, item_2)
                    bot.send_message(call.message.chat.id, list(FOOD.keys())[0] + '\nТы как?)',
                                     reply_markup=murkup)
                else:
                    bot.send_message(call.message.chat.id, '♻️Все отметились♻️')
            elif call.data.split('_')[1] == 'who':
                bot.send_message(call.message.chat.id,
                                 'Получилось ' + str(list(FOOD.values())[0][0]) + ' + ' + str(
                                     list(FOOD.values())[0][1]))
                people = 0
                FOOD = {}
                stolovka_food = '❌'
                stolovka_who = '❌'
                stolovka_all = '❌'
                message_food_id = []
                food_who_id = set()
            elif call.data.split('_')[1] == '+':
                if call.from_user.id not in food_who_id:
                    food_who_id.add(call.from_user.id)
                    FOOD[''.join(list(FOOD.keys())[0])][0] += 1
                    bot.send_message(call.message.chat.id, '♻️Мы вас отметили♻️')
                else:
                    bot.send_message(call.message.chat.id, '♻️Вы уже отметились♻️')
            elif call.data.split('_')[1] == '-':
                if call.from_user.id not in food_who_id:
                    food_who_id.add(call.from_user.id)
                    FOOD[''.join(list(FOOD.keys())[0])][1] += 1
                    bot.send_message(call.message.chat.id, '♻️Мы вас отметили♻️')
                else:
                    bot.send_message(call.message.chat.id, '♻️Вы уже отметились♻️')
            if FOOD:
                if FOOD[''.join(list(FOOD.keys())[0])][0] + FOOD[''.join(list(FOOD.keys())[0])][1] == int(people):
                    stolovka_all = '✅'
                    stolovka_who = '✅'
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        else:
            if call.data.split('_')[1] == 'write':
                global message_food
                bot.send_message(call.message.chat.id, '⬇️Напишите что дают ниже⬇️')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                message_food = True
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(call.message.chat.id, 'Что дают еще не отметили')
    else:
        hod = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton('Да', callback_data='+')
        item_2 = types.InlineKeyboardButton('Нет', callback_data='-')
        hod.add(item_1, item_2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы выбрали:  ' \
                                   + call.message.json['reply_markup']['inline_keyboard'
                                   ][int(call.data) // 3][int(call.data) - int(call.data) // 3 * 3][
                                       'text'] + '\nСделать другой выбор?', reply_markup=hod)


while True:
    bot.polling(none_stop=True)
