import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



columns = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
			'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH']


def cell(x, y):
	return columns[y] + str(x)

def make_range(c1, c2, list_name):
	return list_name + '!' + ':'.join([c1, c2])


class Sheet:

	SPREADSHEET_ID = '1Bb9N6LI77tTF7s2WINnpwDxSiLRrcPLuXNQVg_pkTiA'
	token_path = 'token_marks.pickle'
	value_input_option = 'RAW'

	# col, row
	first_cell = (3, 3)


	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	service = None
	def __init__(self, logger, token_path='token.pickle'):

		self.logger = logger
		logger.info('Sheet initializing...')
		creds = None
		if os.path.exists(token_path):
			with open(token_path, 'rb') as token:
				creds = pickle.load(token)

		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', self.SCOPES)
				creds = flow.run_local_server()

			with open(token_path, 'wb') as token:
				pickle.dump(creds, token)

		self.service = build('sheets', 'v4', credentials=creds)
		self.logger.info('Sheet initialized')

	def write(self, values, _range):
		body = {
		    'values': values
		}
		result = self.service.spreadsheets().values().update(
		    spreadsheetId=self.SPREADSHEET_ID, range=_range,
		    valueInputOption=self.value_input_option, body=body).execute()
		print('{0} cells updated.'.format(result.get('updatedCells')))

	# def set_color(self, color, _range):


	# def refresh(self, state, pair, marks=None, _from=None):
	# 	col, row = pair
	# 	col = (col - 1) * 2 + self.first_cell[0]
	# 	row = (row - 1) * 2 + self.first_cell[1]
	# 	_range = ':'.join([self.columns[col] + str(row), self.columns[col + 1] + str(row + 1)])
	# 	if state == 'start':
	# 		pass
	# 	if state == 'end':
	# 		self.write(marks, _range)

	def update(self, state, pair, circle, marks=None, _from=None):
		x, y = pair
		if state == 'write':
			b = 1 if _from == 'male' else 2
			
			_range = make_range(cell(2*x + b, 2*y + 1), cell(2*x + b, 2*y + 2), 'marks_{}'.format(circle))
			self.write([marks], _range)
		else:
			_range = make_range(cell(2*x + 1, 2*y + 1), cell(2*x + 2, 2*y + 2), 'marks_{}'.format(circle))
			if state == 'start':
				c = '?'
			elif state == 'end':
				c = '!'
			marks = [[c, c], [c, c]]
			self.write(marks, _range)

	def get_user_list(self):
		code2user = {}
		girls = self.service.spreadsheets().values().get(
			spreadsheetId=self.SPREADSHEET_ID,
			range='girls!A2:F'
			).execute().get('values', [])
		boys = self.service.spreadsheets().values().get(
			spreadsheetId=self.SPREADSHEET_ID,
			range='boys!A2:F'
			).execute().get('values', [])
		for user in girls:
			code2user[user[3]] = {
				'sex':'female',
				'name':user[1],
				'from':user[2],
				'order':int(user[0])
			}
		for user in boys:
			code2user[user[3]] = {
				'sex':'male',
				'name':user[1],
				'from':user[2],
				'order':int(user[0])
			}
		return code2user





