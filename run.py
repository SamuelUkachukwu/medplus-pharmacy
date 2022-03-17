import gspread
from google.oauth2.service_account import Credentials
import random
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
                print("Retrieving Patient's Drug History...")
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
    except ValueError as error:
        print(f"invalid patient Id {error}, please try again")
        return False
    return True


def create_new_patient_account():
    """
    function to create new patient account
    """
    new_patient = []
    new_sheet_header = ['Date', 'Medication', 'Brand Name', 'Prescribed for', 'Dosage', 'Dosing Frequency',	'Special Notes']
    new_patient_id = create_new_patient_id()
    new_patient.append(new_patient_id)
    fname = input("Enter Your First Name\n")
    new_patient.append(fname)
    lname = input("Enter Your Last Name:\n")
    new_patient.append(lname)
    SHEET.worksheet('patients').append_row(new_patient)
    print(new_patient)
    SHEET.add_worksheet(title=f"{new_patient_id}", rows=100, cols=20)
    SHEET.worksheet(f"{new_patient_id}").append_row(new_sheet_header)

# worksheet = SHEET.add_worksheet(title="007", rows=100, cols=20)

#     patients_list = SHEET.worksheet('patients').col_values(1)
#     new_patient = list(patients_list[-1][-3:])
#     print(new_patient[2])


def create_new_patient_id():
    """
    function to create new patient id
    """
    patients_list = SHEET.worksheet('patients').col_values(1)
    while True:
        for new_num in range(1, 200):
            if str(f"MP{new_num:03}") in patients_list:
                continue
            else:
                patient_id = str(f"MP{new_num:03}")
                return patient_id
        break


# create_new_patient_id()
# patients_list = SHEET.worksheet('patients').col_values(1)
# patients_list.append('MP004')
# print((patients_list))
# new = [1,2,2,2,3,4]
# SHEET.worksheet('patients').append_row(patients_list)
# SHEET.worksheet('patients').append_row(new)

# print(new)
def patient_drug_history():
    """
    patient drug history data retrived from worksheet
    """
    print('this is the drug history')


print('Welcome To Medplus Pharmacy "Your health, Our care"\n')
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
