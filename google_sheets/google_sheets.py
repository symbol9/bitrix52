import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '15AsGsq0fE2zTJYh0LEp1dohyaFxH75N5fmMsQXeZ7w4'
workbook = client.open_by_key(sheet_id)

sheet = workbook.worksheet('1')
sheet.update_cell(1, 2, 'user_id')

