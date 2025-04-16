from django.core.validators import RegexValidator


PHONE_NUMBER_VALIDATOR = RegexValidator(
    regex=r'^09\d{9}$',
    message="Phone number must be in 09XXXXXXXXX format.",
    code="Invalid_phone_number"
)
