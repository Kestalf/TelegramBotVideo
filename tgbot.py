import telebot
import os
import subprocess

# Вставьте сюда свой токен от BotFather
BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

# Папка для сохранения видео
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на видео с YouTube, и я помогу тебе его скачать.")


@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    try:
        bot.reply_to(message, "⏳ Начинаю скачивание видео, подождите...")

        # Генерация пути для скачивания
        file_path = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')

        # Команда для скачивания видео с помощью yt-dlp
        command = [
            "yt-dlp",
            "--format", "mp4",  # Указание формата
            "--output", file_path,  # Путь для сохранения
            url
        ]

        # Выполнение команды
        subprocess.run(command, check=True)

        # Поиск скачанного файла
        downloaded_file = next((f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith('.mp4')), None)
        if not downloaded_file:
            bot.reply_to(message, "❌ Ошибка: не удалось скачать видео.")
            return

        # Путь к скачанному файлу
        downloaded_file_path = os.path.join(DOWNLOAD_FOLDER, downloaded_file)

        # Отправка видео пользователю
        with open(downloaded_file_path, "rb") as video:
            bot.send_video(message.chat.id, video, caption="🎥 Вот ваше видео!")

        # Удаление файла после отправки
        os.remove(downloaded_file_path)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}. Проверьте ссылку и попробуйте снова.")


# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
