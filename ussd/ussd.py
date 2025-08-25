from re import match


def get_menu (ussd_string):
    match ussd_string:
        case '*379#':
            return ' 1. Balance\n 2. Data\n 3. Offers\n 4. More'
        case  '1':
            return 'Your balance is $10'
        case  '2':
            return 'You have 1GB data left'
        case  '3':
            return 'No offers available'
        case  '4':
            return ' 1. Help\n 2. Settings'
        case  default:
            return 'Invalid option'
        


# ussd_string = '1'
# response = get_menu(ussd_string)
# print(response)
