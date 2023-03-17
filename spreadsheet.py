from dataclasses import replace
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("Birthday Data").sheet1
sheet2 = client.open("User Data").sheet1

#adds user ID to corresponding cell 
def NewDate(day, month, userId):
    current_cell = sheet.cell(day, month).value
    if current_cell == None:
        new_cell = "'" + str(userId) + "|"
    else:
        new_cell = "'" + current_cell + str(userId) + "|"
    sheet.update_cell(day, month, new_cell)

#adds user guild ID to corresponding cell
def NewGuild(guildId):
    no_format = "'" + str(guildId)
    sheet.update_cell(1, 25, no_format)
    

#adds guild and channel Id to corresponding cell
def NewChannel(channelId):
    no_format = "'" + str(channelId)
    sheet.update_cell(1,26, no_format)

def GetGuild():
    return sheet.cell(1, 25).value

def NewUser(day, month, userId): 
    lst = [str(userId) ,day, month]
    sheet2.append_row(lst)

def FindUser(userId):
    cell = sheet2.find(str(userId))
    return cell

def ClearUser(userId):
    cell = FindUser(userId)
    if not cell:
        return False

    day = sheet2.cell(cell.row, cell.col + 1).value
    month = sheet2.cell(cell.row, cell.col + 2).value

    sheet2.update_cell(cell.row, cell.col, '')
    sheet2.update_cell(cell.row, cell.col + 1, '')
    sheet2.update_cell(cell.row, cell.col + 2, '')

    BdayString = sheet.cell(day, month).value
    NewString = BdayString.replace(str(userId) + "|", "")
    sheet.update_cell(day, month, NewString)

    return True

# returns a list containing the user id based on the day and month
def dayList(day, month):
    current_cell = sheet.cell(day,month).value
    return current_cell[:-1].split("|")