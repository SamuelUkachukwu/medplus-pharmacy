import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('medplus_pharmacy')

patient = SHEET.worksheet('MP001')
data = patient.get_all_values()
print(data)
# 
# worksheet = SHEET.add_worksheet(title="007", rows=100, cols=20)
print(SHEET.worksheet('patients').get('B'))

# worksheet_list = SHEET.worksheets()
# print(worksheet_list)

# worksheet = SHEET.worksheet('007')
# SHEET.del_worksheet(worksheet)

# worksheet_list = SHEET.worksheets()
# print(worksheet_list)
patient_id_data = SHEET.worksheet('patients')
patient_list = []
for ind in range(1, 10):
    column = patient_id_data.col_values(ind)
    print(column)

def collect_user_input():
    """
    Captures user input of Patients ID
    """
    while True:
        print(f"Please enter last three digit of Patient ID")
        print(f"ID eg: 001\n")
        patient_id = input("Patient ID:")
        # patient_id = list(patient)
        # print(patient_id[-3:])
        if validate_patient_id(patient_id):
            print("Patient ID is Correct")
            print(f"Retriving file No:{patient_id}")
            break
        print(patient_id)   


def validate_patient_id(values):
    """
    converts all values to intergers. 
    Raises ValueError if string cannot be converted into intergers
    or the length of the value is not 3
    """
    try:
        [int(value) for value in values]
        if len(values) != 3:
            raise ValueError(
            f"Last three digits is required, you entered {len(values)}"
            )
    except ValueError as e:
        print(f"invalid patient Id {e}, please try again")
        return False
    return True

collect_user_input()
# class Patient():
#     """
#     Create an instance of patient
#     """
#     def __init__(self, first_name, last_name, id_num):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.id_num = f"MP{id_num}"
#     def description(self):
#         print(f" First Name: {self.first_name}\n Surname: {self.last_name}\n ID:{self.id_num}")
