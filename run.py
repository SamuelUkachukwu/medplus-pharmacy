import gspread
from google.oauth2.service_account import Credentials
# from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('medplus_pharmacy')


def collect_user_input():
    """
    Captures user input of Patients ID
    """
    while True:
        print(f"Please enter the last three digits of the Patient ID")
        print(f"Patient ID eg: 000\n")
        patient_id = input("Patient ID:")
        if validate_patient_id(patient_id):
            patients_list = SHEET.worksheet('patients').col_values(1)
            if str(f"MP{patient_id}") in patients_list:
                print('Patient account found')
                print('Retriving Drug History...')
                patient_drug_history()
            else:
                print(f"An account could not be found for the provided Patient ID: {patient_id}")
                new_patient = input("Do You want to create a new account? Y/N :").lower()
                if new_patient == 'y':
                    create_new_patient_account()
                elif new_patient == 'n':
                    collect_user_input()
                else:
                    print('Invalid Answer')
                    collect_user_input()
            break


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



def create_new_patient_account():
    """
    function to create new patient account
    """
    print('we are here now')


def patient_drug_history():
    """
    patient drug history data retrived from worksheet
    """
    print('this is the drug history')



print('Welcome To Medplus Pharmacy "Serving with care"\n')
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
