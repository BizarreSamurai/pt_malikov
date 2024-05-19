import logging
import re
import paramiko

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import os
from dotenv import load_dotenv
from pathlib import Path

import psycopg2
from psycopg2 import Error

dotenv_path = Path.cwd() / Path('.env')
load_dotenv(dotenv_path=dotenv_path)

host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')

host_db = os.getenv('HOST_DB')
username_db = os.getenv('USER_DB')

port_db = os.getenv('PORT_DB')
password_db = os.getenv('PASSWORD_DB')
database = os.getenv('DATABASE')

TOKEN = os.getenv('TOKEN')

# Подключаем логирование
logging.basicConfig(
    filename='telegram_bot_log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def get_emailsCommand(update: Update, context):
    connection = None
    data = ''
    try:
        connection = psycopg2.connect(user=username_db, password=password_db, host=host_db, port=port_db, database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM e_table;")
        select = cursor.fetchall()
        for row in select:
            data += f'{row}\n'
        logging.info("Команда select успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе select в PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    update.message.reply_text(data)


def get_phone_numbersCommand(update: Update, context):
    connection = None
    data = ''
    try:
        connection = psycopg2.connect(user=username_db, password=password_db, host=host_db, port=port_db, database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pn_table;")
        select = cursor.fetchall()
        for row in select:
            data += f'{row}\n'
        logging.info("Команда select успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе select в PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    update.message.reply_text(data)


def get_repl_logsCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('docker logs devops_bot-db-1 | grep replication')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data, 'utf-8').replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_releaseCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_unameCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_uptimeCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_dfCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_freeCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_mpstatCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_wCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(' w ')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_authsCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_criticalCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -p crit -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_psCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_ssCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss -tulpn')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def get_apt_listCommand(update: Update, context):
    update.message.reply_text('Введите название пакета или all для вывода всех пакетов: ')

    return 'get_apt_list'


def get_apt_list(update: Update, context):
    
    data = str()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    user_input = update.message.text
    if re.search(r'all', user_input):
        stdin, stdout, stderr = client.exec_command('apt list --installed | head -n 50')
        data = stdout.read() + stderr.read()
    else:
        stdin, stdout, stderr = client.exec_command('apt list --installed '+user_input)
        data = stdout.read() + stderr.read()
    
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END


def get_servicesCommand(update: Update, context):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('systemctl list-units --type=service --state=running')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'


def findPhoneNumbers (update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(?:\+7|8)[-\s(]{,2}\d{3}[-)\s]{,2}\d{3}[-\s]{,1}\d{2}[-\s]{,1}\d{2}') # регулярка для номеров

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END # Завершаем выполнение функции
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
        
    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю

    # Спрашиваем пользователя, нужно ли записывать телефоны в базу данных
    update.message.reply_text("Хотите записать найденные телефоны в базу данных? (да/нет)")

    # Сохраняем список найденных телефонов в контексте, чтобы использовать его в следующем обработчике
    context.user_data['phone_list'] = phoneNumberList

    return 'confirm_phone_write'


def confirm_phone_write(update: Update, context):
    user_response = update.message.text.lower()  # Получаем ответ пользователя
    phoneNumberList = context.user_data['phone_list']  # Получаем список телефонов из контекста

    if user_response == 'да':
        connection = None
        try:
            # Устанавливаем соединение с базой данных
            connection = psycopg2.connect(user=username_db, password=password_db, host=host_db, port=port_db, database=database)
            cursor = connection.cursor()

            for phone_number in phoneNumberList:
                cursor.execute("INSERT INTO pn_table (phone_number) VALUES (%s)", (phone_number,))

            connection.commit()
            logging.info("Команда insert успешно выполнена")
            update.message.reply_text("Данные успешно записаны в базу данных")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе select в PostgreSQL: %s", error)
            update.message.reply_text("Ошибка при записи данных в базу данных: {}".format(error))
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")

    else:
        update.message.reply_text("Операция отменена. Телефоны не будут записаны в базу данных")

    return ConversationHandler.END  # Завершаем обработку диалога


def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска для поиска электронной почты: ')

    return 'findEmail'


def  findEmail(update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) электронные адресса

    emailRegex = re.compile(r'[A-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[A-Z]{2,4}',re.I) # регулярка для поиска email

    emailList = emailRegex.findall(user_input) # Ищем email

    if not emailList: # Обрабатываем случай, когда email нет
        update.message.reply_text('Электронные почты не найдены')
        return ConversationHandler.END # Завершаем выполнение функции
    
    email = '' # Создаем строку, в которую будем записывать email
    for i in range(len(emailList)):
        email += f'{i+1}. {emailList[i]}\n' # Записываем очередной email
        
    update.message.reply_text(email) # Отправляем сообщение пользователю

    # Спрашиваем пользователя, нужно ли записывать email-адреса в базу данных
    update.message.reply_text("Хотите записать найденные email-адреса в базу данных? (да/нет)")

    # Сохраняем список найденных email-адресов в контексте, чтобы использовать его в следующем обработчике
    context.user_data['email_list'] = emailList

    return 'confirm_email_write'


def confirm_email_write(update: Update, context):
    user_response = update.message.text.lower()  # Получаем ответ пользователя
    emailList = context.user_data['email_list']  # Получаем список email-адресов из контекста

    if user_response == 'да':
        connection = None
        try:
            # Устанавливаем соединение с базой данных
            connection = psycopg2.connect(user=username_db, password=password_db, host=host_db, port=port_db, database=database)
            cursor = connection.cursor()

            for email in emailList:
                cursor.execute("INSERT INTO e_table (email) VALUES (%s)", (email,))

            connection.commit()
            logging.info("Команда insert успешно выполнена")
            update.message.reply_text("Данные успешно записаны в базу данных")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе select в PostgreSQL: %s", error)
            update.message.reply_text("Ошибка при записи данных в базу данных: {}".format(error))
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")

    else:
        update.message.reply_text("Операция отменена. Email-адреса не будут записаны в базу данных")

    return ConversationHandler.END  # Завершаем обработку диалога


def verify_passwordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки: ')

    return 'verify_password'


def  verify_password(update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий пароль

    if (len(user_input) < 8) or not (                   # Пароль должен содержать не менее восьми символов
        re.search(r'[A-Z]', user_input)                 # Пароль должен включать хотя бы одну заглавную букву (A–Z)
        and re.search(r'[a-z]', user_input)             # Пароль должен включать хотя бы одну строчную букву (a–z)
        and re.search(r'\d', user_input)                # Пароль должен включать хотя бы одну цифру (0–9)
        and re.search(r'[!@#$%^&*()]', user_input)      # Пароль должен включать хотя бы один специальный символ, такой как !@#$%^&*()
        ):
        update.message.reply_text('Пароль простой')     # Отправляем сообщение пользователю
        return                                          # Завершаем выполнение функции

    update.message.reply_text('Пароль сложный') # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога


def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога номеров
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('findPhoneNumbers', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'confirm_phone_write': [MessageHandler(Filters.text & ~Filters.command, confirm_phone_write)],
        },
        fallbacks=[]
    )

    # Обработчик диалога email
    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('findEmail', findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
            'confirm_email_write': [MessageHandler(Filters.text & ~Filters.command, confirm_email_write)],
        },
        fallbacks=[]
    )

    # Обработчик диалога с паролем
    convHandlerVerify_password = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_passwordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )

    # Обработчик диалога /get_apt_list
    convHandlerGet_apt_list = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_listCommand)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )
		
	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerVerify_password)
    dp.add_handler(CommandHandler("get_release", get_releaseCommand))
    dp.add_handler(CommandHandler("get_uname", get_unameCommand))
    dp.add_handler(CommandHandler("get_uptime", get_uptimeCommand))
    dp.add_handler(CommandHandler("get_df", get_dfCommand))
    dp.add_handler(CommandHandler("get_free", get_freeCommand))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstatCommand))
    dp.add_handler(CommandHandler("get_w", get_wCommand))
    dp.add_handler(CommandHandler("get_auths", get_authsCommand))
    dp.add_handler(CommandHandler("get_critical", get_criticalCommand))
    dp.add_handler(CommandHandler("get_ps", get_psCommand))
    dp.add_handler(CommandHandler("get_ss", get_ssCommand))
    dp.add_handler(convHandlerGet_apt_list)
    dp.add_handler(CommandHandler("get_services", get_servicesCommand))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logsCommand))
    dp.add_handler(CommandHandler("get_emails", get_emailsCommand))
    dp.add_handler(CommandHandler("get_phone_numbers", get_phone_numbersCommand))

	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
