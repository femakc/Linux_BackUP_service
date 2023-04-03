import asyncio
import datetime
import logging
import shutil
import sys
import time

import telegram
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("CHAT_ID")
SRC_PATH = os.getenv("SRC_PATH")
DST_PATH = os.getenv("DST_PATH")


async def send_message(bot, message="None message"):
    """Send message"""
    try:
        logging.info(f"start sending message: %s", message)
        await bot.sendMessage(chat_id=os.getenv("CHAT_ID"), text=message)
    except Exception as err:
        logging.exception("sending failed %s", err)


def back_up(message, path=os.getcwd()):
    logging.info("BackUP to Path: %s", path)
    message += f"BackUP to Path {path} \n"
    if os.path.exists(DST_PATH):
        try:
            shutil.rmtree(DST_PATH)
            logging.info("Delete dirs to Path: %s", DST_PATH)
            message += "Delete - OK \n"
        except Exception as err:
            logging.exception("Delete - fail %s", err)
    try:
        logging.info("Start copy")
        time_for_path = datetime.datetime.now().strftime("%H:%M")
        logging.debug("Start copy from %s to %s. Start time %s ",
                      SRC_PATH, DST_PATH,
                      time_for_path)
        shutil.copytree(
            SRC_PATH,
            DST_PATH,
            symlinks=False,
            ignore=None,
            copy_function=shutil.copy2,
            ignore_dangling_symlinks=False,
            dirs_exist_ok=False
        )
        logging.info("Copy - OK!")
        return message + "Copy - Success!"
    except Exception as err:
        logging.exception(err)
        return message + err


def check_tokens() -> bool:
    """Check env variables"""
    logging.info('Начинаем проверку переменных')
    return all((TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SRC_PATH, DST_PATH))


def main():
    if check_tokens():
        logging.info('Variables check - OK')
        while True:
            message = "Starting BackUP service \n"
            bot = telegram.Bot(token=TELEGRAM_TOKEN)
            try:
                message = back_up(message, SRC_PATH)
                asyncio.run(send_message(bot, message=message))
            except Exception as error:
                logging.exception("BackUP - fail %s", error)
                asyncio.run(send_message(bot, f'BackUp - FAIL : {error}'))
            time.sleep(20)  # 604800 - 7 суток


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s [%(levelname)s] - %(message)s'
        ),
        handlers=[
            logging.FileHandler('logfile.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    main()
