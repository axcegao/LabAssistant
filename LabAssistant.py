import telebot
import numpy as np
import matplotlib.pyplot as plt
import os
from telebot import types

TOKEN = "my token"
bot = telebot.TeleBot(TOKEN)
stage = 0

@bot.message_handler(commands=['start'])
def start(message):
    global stage
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}👋! Я LabAssistant - программа-ассистент для помощи молодому ученому. Мой функционал можешь узнать по команде /function. Для начала работы введи команду /select_calc."
                     .format(message.from_user), reply_markup=markup)
    stage = 0 
    
@bot.message_handler(commands=['function'])
def function(message):
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id,
                     "Список моих функций:\n1.Я могу переводить частоту излучения или энергию фотонов в длину волны света и обратно.✅\n2.Я могу вычислять положения резонанса и его ширины на полувысоте по спектру в формате .txt, а также выведу график с отмеченными положениями пика и его ширины на полувысоте.✅\n3.Я могу вычислить флюенс лазерной системы по средней мощности.✅\n4.Я могу собирать обратную связь пользователей.✅\nЧтобы воспользоваться одной из функций используй команду /select_calc.",
                     reply_markup=markup)
    
@bot.message_handler(commands=['select_calc'])
def select_calc(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text="Перевод единиц", callback_data='Вариант 1')
    itembtn2 = types.InlineKeyboardButton(text="Положение резонанса", callback_data='Вариант 2')
    itembtn3 = types.InlineKeyboardButton(text="Флюенс лазерной системы", callback_data='Вариант 3')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Выбери что хочешь сделать: ", reply_markup=markup)
    
def calc(message, variant):
    global stage
    if variant == 'Вариант 1':
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton(text="Частота->Длина",
                                          callback_data='Вариант 5')
        itembtn2 = types.InlineKeyboardButton(text="Энергия->Длина",
                                          callback_data='Вариант 6')
        itembtn3 = types.InlineKeyboardButton(text="Длина->Энергия",
                                          callback_data='Вариант 7')
        itembtn4 = types.InlineKeyboardButton(text="Длина->Частота",
                                          callback_data='Вариант 8')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.send_message(message.chat.id, text="Выбери что хочешь перевести: ", reply_markup=markup)
        stage = 2
    elif variant == 'Вариант 2':
        bot.send_message(message.chat.id, text="Пожалуйста, загрузите файл со спектром в формате .txt.\nПример правильного файла: ")
        send_example_file(message.chat.id)
        stage = 11
    elif variant == 'Вариант 3':
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
        itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Ты выбрал функцию: вычисление флюенса по средней мощности, начать? ", reply_markup=markup)
        stage = 7

def calc_next(message, variant):
    global stage
    global per
    if variant == 'Вариант 5':
        per = bot.send_message(message.chat.id, "Введи частоту излучения(Гц): ")
        bot.register_next_step_handler(per, next_calc)
        stage = 3
    elif variant == 'Вариант 6':
        per1 = bot.send_message(message.chat.id, "Введи энергию фотона(Дж): ")
        bot.register_next_step_handler(per1, nexxt_calc)
        stage = 4
    elif variant == 'Вариант 7':
        per2 = bot.send_message(message.chat.id, "Введи длину волны (м): ")
        bot.register_next_step_handler(per2, nexxxt_calc)
        stage = 5
    elif variant == 'Вариант 8':
        per3 = bot.send_message(message.chat.id, "Введи длину волны (м): ")
        bot.register_next_step_handler(per3, nexxxxt_calc)
        stage = 6

def next_calc(message):
    global stage
    frequency = message.text  # Получаем текст из сообщения
    try:
        frequency = float(frequency)  # Преобразуем в число
        if frequency >= 0:
            result = 3 * 10**8 / frequency
            bot.send_message(message.chat.id, f"Длина волны: {result} м")
            bot.send_message(message.chat.id, f"Диапазон волны: {get_wave_range(result)}")
            markup = types.InlineKeyboardMarkup()
            itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
            itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Хочешь оставить отзыв о работе бота?", reply_markup=markup)
            stage = 1
        else:
            bot.send_message(message.chat.id, "Частота должна быть неотрицательной.❌\nДля новой оперии введи /select_calc.")
            stage = 0
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть коректным.❌\nВозможно, вы хотите ввести в число типа float ',' а не '.'.\nДля новой оперии введи /select_calc.")
        stage = 0

def nexxt_calc(message):
    global stage
    energy = message.text  # Получаем текст из сообщения
    try:
        energy = float(energy)  # Преобразуем в число
        if energy >= 0:
            h = 6.626e-34  # Постоянная Планка (Дж·с)
            c = 3e8  # Скорость света (м/с)
            # Используем правильную формулу для длины волны
            result = (h * c) / energy
            bot.send_message(message.chat.id, f"Длина волны: {result} м")
            bot.send_message(message.chat.id, f"Диапазон волны: {get_wave_range(result)}")
            markup = types.InlineKeyboardMarkup()
            itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
            itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Хочешь оставить отзыв о работе бота?", reply_markup=markup)
            stage = 1
        else:
            bot.send_message(message.chat.id, "Энергия должна быть неотрицательной.❌\nДля новой операции введи /select_calc.")
            stage = 0 
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть корректным.❌\nВозможно, вы хотите ввести в число типа float ',' а не '.'.\nДля новой операции введи /select_calc.")
        stage = 0

def nexxxt_calc(message):
    global stage
    wave_length = message.text
    try:
        wave_length = float(wave_length)
        if wave_length > 0:
            h = 6.626e-34  # Постоянная Планка (Дж·с)
            c = 3e8  # Скорость света (м/с)
            energy = (h * c) / wave_length
            bot.send_message(message.chat.id, f"Энергия: {energy} Дж")
            markup = types.InlineKeyboardMarkup()
            itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
            itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Хочешь оставить отзыв о работе бота?", reply_markup=markup)
            stage = 1
        else:
            bot.send_message(message.chat.id, "Длина волны должна быть положительной.❌\nДля новой операции введи /select_calc.")
            stage = 0
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть корректным.❌\nВозможно, вы хотите ввести в число типа float ',' а не '.'.\nДля новой операции введи /select_calc.")
        stage = 0

def nexxxxt_calc(message):
    global stage
    wave_length = message.text
    try:
        wave_length = float(wave_length)
        if wave_length > 0:
            frequency = 3e8 / wave_length  # Формула для расчета частоты
            bot.send_message(message.chat.id, f"Частота: {frequency} Гц")
            markup = types.InlineKeyboardMarkup()
            itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
            itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Хочешь оставить отзыв о работе бота?", reply_markup=markup)
            stage = 1
        else:
            bot.send_message(message.chat.id, "Длина волны должна быть положительной.❌\nДля новой операции введи /select_calc.")
            stage = 0
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть корректным.❌\nВозможно, вы хотите ввести в число типа float ',' а не '.'.\nДля новой операции введи /select_calc.")
        stage = 0

def get_wave_range(result):
        if result < 1e-11:
            return "Гамма-лучи"
        elif 1e-11 <= result < 1e-8:
            return "Рентгеновские лучи"
        elif 1e-8 <= result < 4e-7:
            return "Ультрафиолет"
        elif 4e-7 <= result < 7e-7:
            return "Видимый свет"
        elif 7e-7 <= result < 1e-3:
            return "Инфракрасное излучение"
        elif 1e-3 <= result < 1:
            return "Микроволны"
        else:
            return "Радиоволны"

def send_example_file(chat_id):
    example_data = """400 0.1
401 0.15
402 0.3
403 0.5
404 0.8
405 1.0
406 0.9
407 0.7
408 0.4
409 0.2
410 0.1"""
    
    bot.send_message(chat_id, "Вот пример правильно заполненного файла:\n\n" + example_data)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global stage
    if stage == 11:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Сохраняем файл временно
        with open('spectrum.txt', 'wb') as new_file:
            new_file.write(downloaded_file)

        # Обрабатываем файл
        try:
            peak_wavelength, fwhm = process_spectrum('spectrum.txt')
            bot.send_message(message.chat.id, f'Положение резонанса: {peak_wavelength} nm\nШирина на полувысоте: {fwhm} nm')
            
            # Отправляем график
            plot_spectrum('spectrum.txt')
            with open('spectrum_plot.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка при обработке файла: {e}')
        finally:
            os.remove('spectrum.txt')
            os.remove('spectrum_plot.png')
            markup = types.InlineKeyboardMarkup()
            itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
            itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Хочешь оставить отзыв о работе бота?", reply_markup=markup)
            stage = 1

def process_spectrum(filename):
    data = np.loadtxt(filename)
    wavelengths = data[:, 0]
    intensities = data[:, 1]

    max_intensity = np.max(intensities)
    max_index = np.argmax(intensities)
    peak_wavelength = wavelengths[max_index]

    half_max = max_intensity / 2
    indices_above_half_max = np.where(intensities >= half_max)[0]
    fwhm_start = wavelengths[indices_above_half_max[0]]
    fwhm_end = wavelengths[indices_above_half_max[-1]]
    fwhm = fwhm_end - fwhm_start

    return peak_wavelength, fwhm

def plot_spectrum(filename):
    data = np.loadtxt(filename)
    wavelengths = data[:, 0]
    intensities = data[:, 1]

    max_intensity = np.max(intensities)
    max_index = np.argmax(intensities)
    peak_wavelength = wavelengths[max_index]

    half_max = max_intensity / 2
    indices_above_half_max = np.where(intensities >= half_max)[0]
    fwhm_start = wavelengths[indices_above_half_max[0]]
    fwhm_end = wavelengths[indices_above_half_max[-1]]

    plt.figure(figsize=(10, 5))
    plt.plot(wavelengths, intensities, label='Спектр')
    plt.axvline(peak_wavelength, color='r', linestyle='--', label='Положение резонанса')
    plt.axvline(fwhm_start, color='g', linestyle='--', label='Ширина на полувысоте (начало)')
    plt.axvline(fwhm_end, color='g', linestyle='--', label='Ширина на полувысоте (конец)')
    plt.title('Спектр с резонансом и шириной на полувысоте')
    plt.xlabel('Длина волны')
    plt.ylabel('Интенсивность')
    plt.legend()
    plt.grid()
    plt.savefig('spectrum_plot.png')  # Сохранение графика

def calculate_fluence(message, variant):
    if variant == 'Да':
        global stage
        power = bot.send_message(message.chat.id, "Введите среднюю мощность (Вт): ")
        bot.register_next_step_handler(power, get_fluence_area)
        stage = 8
    else:
        bot.send_message(message.chat.id, "Операция отменена. Для новой операции введи /select_calc.")
        stage = 0

def get_fluence_area(message):
    global stage
    global power
    power = message.text
    try:
        power = float(power)
        if power > 0:
            area = bot.send_message(message.chat.id, "Введите площадь (см²): ")
            bot.register_next_step_handler(area, get_fluence_rep, power)
            stage = 9
        else:
            bot.send_message(message.chat.id, "Мощность должна быть положительной.❌\nДля новой операции введи /select_calc.")
            stage = 0
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть корректным.❌\nДля новой операции введи /select_calc.")
        stage = 0

def get_fluence_rep(message, power):
    global stage
    global area
    area = message.text
    try:
        area = float(area)
        if area > 0:
            rep = bot.send_message(message.chat.id, "Введите частоту повторений(Гц): ")
            bot.register_next_step_handler(rep, compute_fluence, power, area)
            stage = 10
        else:
            bot.send_message(message.chat.id, "Площадь должна быть положительной.❌\nДля новой операции введи /select_calc.")
            stage = 0
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть корректным.❌\nДля новой операции введи /select_calc.")
        stage = 0

def compute_fluence(message, power, area):
    global stage
    global rep
    rep = message.text
    try:
        rep = float(rep)
        if rep > 0:
            fluence = power / (area*rep)  # Флюенс = мощность / площадь*частоту
            bot.send_message(message.chat.id, f"Флюенс: {fluence} Дж/см²")
            markup = types.InlineKeyboardMarkup()
            itembtn1 = types.InlineKeyboardButton(text="Да", callback_data='Да')
            itembtn2 = types.InlineKeyboardButton(text="Нет", callback_data='Нет')
            markup.add(itembtn1, itembtn2)
            bot.send_message(message.chat.id, "Хочешь оставить отзыв о работе бота?", reply_markup=markup)
            stage = 1
        else:
            bot.send_message(message.chat.id, "Частота повторений должна быть положительной.❌\nДля новой операции введи /select_calc.")
            stage = 0
    except ValueError:
        bot.send_message(message.chat.id, "Число должно быть корректным.❌\nДля новой операции введи /select_calc.")
        stage = 0

def feedback(message, variant):
    global stage
    if variant == 'Да':
        mesg = bot.send_message(message.chat.id,
                        "Пожалуйста, напиши, насколько ты доволен опытом использования ассистента от 1 до 5?(1/2): ")
        bot.register_next_step_handler(mesg, send_feedback)
    else:
        bot.send_message(message.chat.id, "Для продолжения введи команду /select_calc.")
        stage = 0  # Возвращаемся к началу для новой команды

def send_feedback(message):
    global stage
    bot.forward_message(
    chat_id=5437366760,  # chat_id чата в которое необходимо переслать сообщение
    from_chat_id=message.chat.id,  # chat_id из которого необходимо переслать сообщение
    message_id=message.message_id  # message_id которое необходимо переслать
    )
    next_question = bot.send_message(message.chat.id, "Пожалуйста, напиши, каких функций тебе не хватило в боте?(2/2): ")
    bot.register_next_step_handler(next_question, handle_question)

def handle_question(message):
    global stage
    bot.forward_message(
        chat_id=5437366760,  # chat_id чата, в которое необходимо переслать сообщение
        from_chat_id=message.chat.id,  # chat_id из которого необходимо переслать сообщение
        message_id=message.message_id  # message_id, которое необходимо переслать
    )
    bot.send_message(message.chat.id, "Спасибо за ваши ответы! Для продолжения пользования ботом введите команду /select_calc.")
    stage = 0

@bot.callback_query_handler(func=lambda call: True)
def answering(call):
    if stage == 0:
        calc(call.message, call.data)
    elif stage == 1:
        feedback(call.message, call.data)
    elif stage == 2:
        calc_next(call.message, call.data)
    elif stage == 3:
        next_calc(call.message, call.data)
    elif stage == 4:
        nexxt_calc(call.message, call.data)
    elif stage == 5:
        nexxxt_calc(call.message, call.data)
    elif stage == 6:
        nexxxxt_calc(call.message, call.data)
    elif stage == 7:
        calculate_fluence(call.message, call.data)
    elif stage == 8:
        get_fluence_area(call.message)
    elif stage == 9:
        get_fluence_rep(call.message)
    elif stage == 10:
        compute_fluence(call.message)
    elif stage == 11:
        handle_document(call.message)

bot.infinity_polling()
