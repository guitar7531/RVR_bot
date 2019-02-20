from telebot import TeleBot
from users import *
from telebot.types import (
		ReplyKeyboardMarkup,
		KeyboardButton
	)
import os
from sheets import Sheet


class Bot(TeleBot):

	users_path = 'users.pckl'
	# (,1) - male; (,0) female
	order_male2name = {}
	username2id = {}
	def __init__(self, logger):
		logger.info("Initializing...")
		self.token = open('token', 'r').readline()

		TeleBot.__init__(self, self.token)

		
		self.users = {}
		for user_file in os.listdir('users/'):
			try:
				user = load('users/' + user_file)
				user.bot = self
			except:
				continue
			self.users[user.id] = user
			self.username2id[user.username] = user.id

		self.logger = logger
		self.sheet = Sheet(logger)
		self.code2user = self.sheet.get_user_list()
		for user in self.code2user.values():
			self.order_male2name[(user['order'], 1 if user['sex'] == 'male' else 0)] =  user['name'].split()[1] if len(user['name'].split()) > 1 else user['name']

		self.con = 0

		@TeleBot.message_handler(self, commands=['start'])
		def greeting(message):
			if message.from_user.id in self.users:
				self.send_message(message.from_user.id, 'Alredy logged in')
				return
			self.users[message.from_user.id] = User(message.from_user, self)

		@TeleBot.message_handler(self)
		def onNewMessage(message):
			self.logger.info('New message from %s (%s %s): %s' 
				% (message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.text))
			if not message.from_user.id in self.users:
				self.send_message(message.from_user.id, 'Type "/start" to start')
				return
			self.users[message.from_user.id].onNewMessage(message)

		self.logger.info('Bot initialized')

	def start(self):
		super().polling()

	def update(self):
		self.code2user = self.sheet.get_user_list()
		for code, user in self.users.items():
			if user.code == code:
				user.update(code2user[code])


	# def __del__(self):
	# 	print('yspex')
	# 	if len(self.users) > 0:
	# 		dump(self.users, self.users_path)
	# 		self.logger.info('Users saved')

