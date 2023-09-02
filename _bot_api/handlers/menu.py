from .check import *
from ..keyboards.reply_choice import markup_choice


@bot.message_handler(func=lambda x: False)
def menu_button(message, destination_id, count_print):
    if message.text == "Да":
        photo_flag = True
    else:
        photo_flag = False

    choice = bot.send_message(message.chat.id, "Отлично, теперь выберите из вариантов ниже:", reply_markup=markup_choice)
    bot.register_next_step_handler(choice, check_command, destination_id, count_print, photo_flag)
