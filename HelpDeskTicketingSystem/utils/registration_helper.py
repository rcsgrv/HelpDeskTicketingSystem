def validate_registration_form(forename, surname, email, password, password_confirm, account_type, user):
    if not forename or len(forename.strip()) < 1:
        return 'Forename cannot be blank.'
    if not surname or len(surname.strip()) < 1:
        return 'Surname cannot be blank.'
    if not email or len(email.strip()) < 1:
        return 'Email cannot be blank.'
    if '@' not in email or '.' not in email.split('@')[-1]:
        return 'Please enter a valid email address.'
    if user is not None:
        return 'The email you have provided is already associated with an account.'
    if not password or len(password) < 8:
        return 'Password must be at least 8 characters long.'
    if password != password_confirm:
        return 'Your passwords do not match.'
    if not account_type:
        return 'You must select an account type.'
    return None