import telebot
import constants
global img
from datetime import datetime

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
r = redis.from_url(os.environ.get("REDIS_URL"))

import telebot
import constants
global img
from datetime import datetime
bot = telebot.TeleBot(constants.token)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None

@bot.message_handler(commands=['start'])
def handle_start(message):
    menu_markup = telebot.types.ReplyKeyboardMarkup()
    menu_markup.row('📜 Меню 📜')
    menu_markup.row('🔒 Бронь столика 🔒')
    menu_markup.row('Фото','Как доехать?')
    menu_markup.row('Контакты','Помощь')
    bot.send_message(message.from_user.id, 'Добро пожаловать',  reply_markup=menu_markup)



#copy
@bot.message_handler(content_types = ['text'])
def send_welcome(message):
    if message.text == '🔒 Бронь столика 🔒':
        msg = bot.send_message(message.from_user.id,"Привет, давай забронируем столик, как тебя зовут?")
        bot.register_next_step_handler(msg, process_name_step)
    elif message.text == '📜 Меню 📜':

        info_markup = telebot.types.ReplyKeyboardMarkup()
        info_markup.row('Карта бара')
        info_markup.row('Кухня')
        info_markup.row('Назад')
        bot.send_message(message.from_user.id, 'Наше меню: ', reply_markup=info_markup)
        msg = bot.send_message(message.from_user.id, "Выберите категорию")
        bot.register_next_step_handler(msg, menu_kategorii)


        return

    elif message.text == 'Назад':
        menu_markup = telebot.types.ReplyKeyboardMarkup()
        menu_markup.row('📜 Меню 📜')
        menu_markup.row('🔒 Бронь столика 🔒')
        menu_markup.row('Фото', 'Как доехать?')
        menu_markup.row('Контакты', 'Помощь')
        bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=menu_markup)

    if message.text == 'Как доехать?':
        bot.send_message(message.from_user.id, 'Вулиця Паньківська, 20, Київ, Украина, 02000')
        bot.send_chat_action(message.from_user.id, 'find_location')
        bot.send_location(message.from_user.id, 50.4358945, 30.5050359)
    if message.text == 'Контакты':
            bot.send_message(message.from_user.id, 'https://www.instagram.com/')
            bot.send_message(message.from_user.id, 'https://www.facebook.com/')
            bot.send_message(message.from_user.id, '+380999999999' + '   ' + 'Елена (Администратор)')
            bot.send_message(message.from_user.id, '+380999999998' + '   ' + 'Александр (Администратор)')


def process_name_step(message):
        try:
            chat_id = message.chat.id
            name = message.text
            user = User(name)
            user_dict[chat_id] = user
            msg = bot.send_message(message.from_user.id, 'Хорошо, а какой у тебя номер?(Напиши в формате 0ХХХХХХХХХ)')
            bot.register_next_step_handler(msg, process_phone_step)
        except Exception as e:
            bot.reply_to(message, 'oooops')


def process_phone_step(message):
    try:
      chat_id = message.chat.id
      ph = message.text
      if len(ph) == 10:
        if not ph.isdigit():
            msg = bot.reply_to(message, 'Неверный формат, введите номер')
            bot.register_next_step_handler(msg, process_phone_step)
            return
      else:
          msg = bot.reply_to(message, 'Неверная длина, введите номер')
          bot.register_next_step_handler(msg, process_phone_step)
          return
      user = user_dict[chat_id]
      user.ph = ph
      msg = bot.send_message(message.from_user.id, 'Окей, введите дату(Например 22.04, 12.12)')
      bot.register_next_step_handler(msg, process_date_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
    return
def process_date_step(message):
            try:
                chat_id = message.chat.id
                date = message.text
                if date != datetime.strptime(date, "%d.%m").strftime('%d.%m'):

                    return
                user = user_dict[chat_id]
                user.date = date
                msg = bot.send_message(message.from_user.id, 'Окей, а какое время?(Например 04:02, 11:23')
                bot.register_next_step_handler(msg, process_time_step)
            except Exception as e:
                msg = bot.reply_to(message, 'Неверный формат, введите дату дд.мм')
                bot.register_next_step_handler(msg, process_date_step)





def process_time_step(message):
    try:
        chat_id = message.chat.id
        time = message.text

        if time != datetime.strptime(time, "%H:%M").strftime('%H:%M'):
            return
        user = user_dict[chat_id]
        user.time = time
        bot.send_message(message.from_user.id,"Итак, "+' '+ user.name +' '+"под номером"+' '+user.ph+'  '+"отправил(а) заявку на бронь "+' '+user.date+' '+"числа, в "+' '+user.time)
        bot.send_message(-218636371,user.name +'  '+"под номером"+'  '+user.ph+'  '+"отправил(а) заявку на бронь "+''+user.date+' '+"числа, в "+' '+user.time)
    except Exception as e:
        msg = bot.reply_to(message, 'Неверный формат, введите время чч:мм')
        bot.register_next_step_handler(msg, process_time_step)


def menu_kategorii(message):
        if message.text == 'Карта бара':
            user_markup = telebot.types.ReplyKeyboardMarkup()
            user_markup.row('Безалкогольные напитки')
            user_markup.row('Кофе,чай')
            user_markup.row('Алкоголь')
            user_markup.row('Назад в категории')
            send = bot.send_message(message.from_user.id, 'Наша карта бара:', reply_markup=user_markup)
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, karbar)

        elif message.text=='Кухня':
            user_markup = telebot.types.ReplyKeyboardMarkup()
            user_markup.row('Горячее блюдо')
            user_markup.row('Супы')
            user_markup.row('Салаты')
            user_markup.row('Десерты')
            user_markup.row('Пицца')
            user_markup.row('Суши')
            user_markup.row('Назад в категории')
            send = bot.send_message(message.from_user.id, 'Наше меню:', reply_markup=user_markup)
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Назад':
            menu_markup = telebot.types.ReplyKeyboardMarkup()
            menu_markup.row('📜 Меню 📜')
            menu_markup.row('🔒 Бронь столика 🔒')
            menu_markup.row('Фото', 'Как доехать?')
            menu_markup.row('Контакты', 'Помощь')
            bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=menu_markup)

def karbar(message):
     if message.text == 'Безалкогольные напитки':
         img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/napitki/nap1.jpeg", 'rb')
         bot.send_chat_action(message.from_user.id, 'upload_photo')
         bot.send_photo(message.from_user.id, img, 'Моршинская 0,75л. Негазована. 25грн')
         img.close()

         img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/napitki/nap2.jpeg", 'rb')
         bot.send_chat_action(message.from_user.id, 'upload_photo')
         bot.send_photo(message.from_user.id, img, 'Моршинская 0,75л. Газована. 25грн')
         img.close()
         msg = bot.send_message(message.from_user.id, "Выберите категорию")
         bot.register_next_step_handler(msg, karbar)
     elif message.text == 'Кофе,чай':
         msg = bot.send_message(message.from_user.id, "типа фото кофе, нажми другое")
         bot.register_next_step_handler(msg, karbar)
     elif message.text == 'Алкоголь':
         msg = bot.send_message(message.from_user.id, "типа фото виски, нажми другое")
         bot.register_next_step_handler(msg, karbar)
     elif message.text == 'Назад в категории':
         info_markup = telebot.types.ReplyKeyboardMarkup()
         info_markup.row('Карта бара')
         info_markup.row('Кухня')
         info_markup.row('Назад')
         bot.send_message(message.from_user.id, 'Наше меню: ', reply_markup=info_markup)
         msg = bot.send_message(message.from_user.id, "Выберите категорию")
         bot.register_next_step_handler(msg, menu_kategorii)
def kuchnia(message):

        if message.text == 'Горячее блюдо':  ##################################################################

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/goryachee/gor2.jpeg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Спагетти с кальмаром и яйцом. 370 гр. Цена 100грн.')
            img.close()

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/goryachee/gor1.jpeg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Нежнейшие ножки в соевом соусе. 500 гр. Цена 300грн.')
            img.close()
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Супы':  ################################################################
            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/supi/supi1.jpg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Борщ' + ' ' + ' Украинский. Цена 50 грн.')
            img.close()

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/supi/supi2.jpeg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Суп с лапшой и говядиной. Цена 50 грн. ')
            img.close()
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Салаты':  ################################################################
            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/salat/salat2.jpg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Салат мясной. Цена 100 грн.')
            img.close()

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/salat/salat1.jpeg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Салат греческий. Цена 80 грн. ')
            img.close()
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Десерты':  ################################################################
            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/desert/des1.jpeg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Ореховый пирог. Цена 60 грн.')
            img.close()

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/desert/des2.jpeg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Тортик кремовый. Цена 50 грн. ')
            img.close()
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Пицца':  ################################################################
            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/pizza/p1.jpg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Пицца 3 сыра с оливками. Цена 80 грн.')
            img.close()

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/pizza/p2.jpg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Пицца салями. Цена 90 грн. ')
            img.close()
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Суши':  ################################################################
            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/sushi/ss1.jpg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Филадельфия с огурцом. Цена 80 грн.')
            img.close()

            img = open("C:/Users/LadikusPC/PycharmProjects/telegabot/files/MenuPhoto/sushi/ss2.jpg", 'rb')
            bot.send_chat_action(message.from_user.id, 'upload_photo')
            bot.send_photo(message.from_user.id, img, 'Набор самурай. Цена 480 грн. ')
            img.close()
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, kuchnia)
        elif message.text == 'Назад в категории':
            info_markup = telebot.types.ReplyKeyboardMarkup()
            info_markup.row('Карта бара')
            info_markup.row('Кухня')
            info_markup.row('Назад')
            bot.send_message(message.from_user.id, 'Наше меню: ', reply_markup=info_markup)
            msg = bot.send_message(message.from_user.id, "Выберите категорию")
            bot.register_next_step_handler(msg, menu_kategorii)

def location(message):

            bot.send_message(message.from_user.id, 'Вулиця Паньківська, 20, Київ, Украина, 02000')
            bot.send_chat_action(message.from_user.id, 'find_location')
            bot.send_location(message.from_user.id,50.4358945,30.5050359)
def contacts(message):
            bot.send_message(message.from_user.id, 'https://www.instagram.com/')
            bot.send_message(message.from_user.id, 'https://www.facebook.com/')
            bot.send_message(message.from_user.id, '+380999999999' + '   ' + 'Елена (Администратор)')
            bot.send_message(message.from_user.id, '+380999999998' + '   ' + 'Александр (Администратор)')


bot.polling(none_stop=True)
