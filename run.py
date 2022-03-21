import datetime
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('medplus_pharmacy')


def main(value):
    """
    main function
    """
    patients_list = SHEET.worksheet('patients').col_values(1)
    if str(f"MP{value}") in patients_list:
        print('Patient account found\n')
        patient_drug_history(f"MP{value}")
    else:
        print(f"No account found for the provided ID:{value}")
        while True:
            new_patient = input("Create a new account? Y/N :\n").lower()
            if new_patient == 'y':
                create_new_patient()
                break
            elif new_patient == 'n':
                print("\nMedplus Pharmacy Your health, Our care")
                break
            else:
                print('please enter Y or N')


def validate_patient_id():
    """
    Validates user imput of patient ID
    """
    print("Please enter the last four digits of the Patient ID")
    print("To Create New Account Enter Any Four Digit Number")
    print("Patient ID eg: 0000\n")
    while True:
        try:
            acct_id = int(input("Patient ID:\n"))
            if [x for x in str(acct_id)]:
                if len(str(acct_id)) != 4:
                    print(
                        "Value requested is 4",
                        f"you entered {len(str(acct_id))}"
                        )
                    raise ValueError()
                main(acct_id)
                break
        except ValueError:
            print("Please Enter Last 4 digits of Patient ID")


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
            if str(f"MP1{new_num:03}") in patients_list:
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
        'Date', 'Medication', 'Dosage',
        'Dosing Frequency', 'Duration',
        'Quantity Dispensed(tabs)', 'Special Notes'
        ]
    new_patient_id = f"MP1{data}"
    fname = input("Enter Patients First Name\n").capitalize()
    lname = input("Enter Patients Last Name:\n").capitalize()
    while True:
        try:
            age = int(input("Enter Age: \n"))
            if len(str(age)) <= 3 and age < 110:
                break
            else:
                print("Please Enter Required Age")
        except ValueError:
            print("Values have to be integers.")
    yob = date.today().year - age
    new_patient.extend([new_patient_id, fname, lname, yob])
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
    print(f" Name: {patient[1]} {patient[2]}")
    print(f" Age: {date.today().year - int(patient[3])}")
    print(f" Patient ID: {patient[0]}\n")
    history = SHEET.worksheet(f"{patient[0]}").get_all_values()

    if history[0] == history[-1]:
        print("\nPatient has no recorded history\n")
    else:
        print(f"\nDate: {history[-1][0]}")
        print(f"Medication: {history[-1][1]}")
        print(f"Dosage: {history[-1][2]}")
        print(f"Dosing frequency: {history[-1][3]}")
        print(f"Quantity Dispensed: {history[-1][5]}")
        print(f"Notes: {history[-1][6]}\n")
        patient_next_visit(history[-1][0], history[-1][4])

    while True:
        request = input("Enter new details? Y/N :\n").lower()
        if request == 'y':
            enter_drug_history(f"{patient[0]}")
            break
        elif request == 'n':
            print("\nMedplus Pharmacy Your health, Our care")
            break


def patient_next_visit(value1, value2):
    """
    calculates patients next visit
    """
    value1 = datetime.datetime.strptime(value1, "%m/%d/%y")
    next_visit = value1 + datetime.timedelta(days=int(value2))
    print(f"Patients Next Visit is {next_visit}")


def enter_drug_history(patient_id):
    """
    new drug information is added to patients worksheet
    """
    new_med = []
    today = datetime.datetime.now()
    date1 = today.strftime("%x")
    print(f"\nDate: {date1}")
    medication = "Zidovudine (AZT)"
    print(f"Medication: {medication}")
    print("Enter Dosage as 250 or 300")
    while True:
        dosage = str(input("Dosage: \n"))
        if dosage == '300':
            break
        elif dosage == '250':
            break
        else:
            print("Enter Dosage as 250 or 300 only")
    while True:
        try:
            dose_frq = int(input("Number of Tablets per Day:\n"))
            duration = int(input("For How Many Days: \n"))
            quantity = (dose_frq * duration)
            break
        except ValueError:
            print("Both values have to be integers.")
    notes = input("Special Notes: \n").lower()
    new_med.extend([
            date1, medication, f"{dosage}mg",
            dose_frq, duration, quantity, notes
            ])
    SHEET.worksheet(patient_id).append_row(new_med)
    print("\n Updating Patients Account...\n")
    print(" Patients account Updated\n")
    print(f" Dispense {quantity} tablets of Zidovudine(AZT) {dosage}mg.\n")
    print(f" To be taken {dose_frq} times daily for {duration} days")
    print("\nMedplus Pharmacy Your health, Our care")


print('Welcome To Medplus Pharmacy "Your health, Our care"\n')
validate_patient_id()
