from django.core.validators import RegexValidator

def PhoneValidator():

  return RegexValidator(regex=r'(0)+[0-9]{9}', message="Phone number must be entered in the format: '09123.....'. Up to 10 digits allowed.")

def UperCaseValidator():
  
  return RegexValidator(regex=r'^[A-Z0-9]{3,}$', message="Only uppercase letters and numbers allowed.")

