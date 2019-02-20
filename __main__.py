import logging 
from datetime import datetime
from bots import Bot

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', 
	datefmt='%Y-%m-%d %H:%M:%S',
	handlers=[
        logging.FileHandler("logs/{}.log".format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))),
        logging.StreamHandler()
    ])
logger = logging.getLogger("TeleBot")
logger.setLevel(level=logging.INFO)
    
    
if __name__ == '__main__':
	bot = Bot(logger)
	bot.start()