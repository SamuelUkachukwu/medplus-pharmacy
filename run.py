import gspread
from google.oauth2.service_account import Credentials
import datetime
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
    request input validation
    Calls for new account creation
    """
    while True:
        print("Please enter the last three digits of the Patient ID")
        print("Patient ID eg: 000\n")
        patient_id = input("Patient ID:")
        if validate_patient_id(patient_id):
            patients_list = SHEET.worksheet('patients').col_values(1)
            if str(f"MP{patient_id}") in patients_list:
                print('Patient account found\n')
                patient_drug_history(f"MP{patient_id}")
            else:
                print(f"No account found for the provided ID:{patient_id}")
                new_patient = input("Create a new account? Y/N :").lower()
                if new_patient == 'y':
                    create_new_patient()
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
    except ValueError:
        print("Invalid Patient ID, Please Try Again")
        return False
    return True


def create_new_patient():
    """
    Creates a new patient account by calling the listed functions
    """
    patient_id = create_new_patient_id()
    print("\nCreating New Account…\n")
    create_new_patient_account(patient_id)


def create_new_patient_id():
    """
    generates new id
    verify id generated is not already in the patient list
    """
    patients_list = SHEET.worksheet('patients').col_values(1)
    while True:
        for new_num in range(1, 199):
            if str(f"MP{new_num:03}") in patients_list:
                continue
            else:
                patient_id = str(f"{new_num:03}")
                return patient_id
        break


def create_new_patient_account(data):
    """
    Create new patient account writes to worksheet 'patient'
    Create new worksheet for new account created
    """
    new_patient = []
    new_sheet_header = [
        'Date', 'Medication',
        'Prescribed for', 'Dosage',
        'Dosing Frequency', 'Special Notes'
        ]
    new_patient_id = f"MP{data}"
    new_patient.append(new_patient_id)
    fname = input("Enter Your First Name\n").capitalize()
    new_patient.append(fname)
    lname = input("Enter Your Last Name:\n").capitalize()
    new_patient.append(lname)
    SHEET.worksheet('patients').append_row(new_patient)
    SHEET.add_worksheet(title=f"{new_patient_id}", rows=100, cols=20)
    SHEET.worksheet(f"{new_patient_id}").append_row(new_sheet_header)
    print("\nNew Account Created\n")
    patient_drug_history(new_patient_id)


def patient_drug_history(data):
    """
    patient drug history data retrived from worksheet
    """
    print("Retrieving Patient's Drug History...")
    print('Patient Drug History Retrieved\n')
    patients_list = SHEET.worksheet('patients').col_values(1)
    index = patients_list.index(data)
    patient = SHEET.worksheet("patients").row_values(int(index)+1)
    print(f" Name: {patient[1]} {patient[2]}\n Patient ID: {patient[0]}")
    history = SHEET.worksheet(f"{patient[0]}").get_all_values()

    if history[0] == history[-1]:
        print("\nPatient has no recorded history")
    else:
        print(f"\nDate: {history[-1][0]}")
        print(f"Medication: {history[-1][1]}")
        print(f"Prescribed for: {history[-1][2]}")
        print(f"Dosage: {history[-1][3]}")
        print(f"Dosing frequency: {history[-1][4]}")
        print(f"Notes: {history[-1][5]}\n")
    while True:
        request = input("Enter new details? Y/N :").lower()
        if request == 'y':
            enter_drug_history(f"{patient[0]}")
            break
        elif request == 'n':
            print('ok')
            break


def enter_drug_history(data):
    """
    new drug information is added to patients worksheet
    """
    new_med = []
    date = datetime.datetime.now()
    date1 = date.strftime("%x")
    medication = input("Medication: ").capitalize()
    reason = input("Prescribed For: ")
    dosage = input("Dosage: ")
    dose_frq = input("Dose Frequency: ")
    notes = input("Special Notes: ")
    new_med.extend([date1, medication, reason, dosage, dose_frq, notes])
    SHEET.worksheet(data).append_row(new_med)


print('Welcome To Medplus Pharmacy "Your health, Our care"\n')
collect_user_input()
