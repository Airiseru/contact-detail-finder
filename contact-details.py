"""
This program will use regular expressions (Regex) to find the contact details {email and phone number} from a set of text (e.g. job listing)

1. Get text off the clipboard (pyperclip.paste())
2. Find all phone numbers and email addresses in the text (findall() method)
3. Paste them onto the clipboard (pyperclip.copy())

Sample Numbers:
0917-432-3103
+63 432 3103
(+632) 8523 8481
8-2498310
(632) 8 834-3000
(+63) 919-056-2255
924-6101

Sample Contact Details Sites:
https://www.unionbankph.com/contact-us/directory
https://customs.gov.ph/contact-us/

NOTE: Not all numbers may work due to the various variations of the Philippines contact numbers
"""

import pyperclip, re

# Store the clipboard contents into a variable
clipboard = str(pyperclip.paste())


# Create a Regex for Phone Numbers
phone_regex = re.compile(r'''
    ([0][9]\d{2}|\([+]?\s?[6][3]\s?\d{,2}?\)|\(?[+]?[6][3]\)?)?         # country calling code
    (\s|-|\.)?                                                          # separator
    (\d{,3})?                                                           # area code
    (\s|-|\.)?                                                          # separator
    (\d{3,})                                                            # first 3 or more digits
    (\s|-|\.)?                                                          # separator
    (\d{4})                                                             # last 4 digits
    (\s*(ext|x|ext.)\s*\d{2,5})?                                        # extension
''', re.VERBOSE)


# Create a Regex for Email Addresses
email_regex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+           # username
    @                           # @ symbol
    [a-zA-Z0-9.-]+              # domain name
    \.[a-zA-Z]{2,4}             # dot something
)''', re.VERBOSE)


# Find matches in clipboard
matches = []

# For phone numbers (ensures that it will print every number with the same format)
for groups in phone_regex.findall(clipboard):
    # country calling code
    phone_num = groups[0]

    # if the area code is not empty, append it
    if groups[2] != '':
        if groups[0] != ('' or '\n') and groups[1] != ('' or '\n'):
            phone_num += "-" + groups[2]
        # in case the country calling code isn't added, it will just add the area code
        else:
            phone_num = groups[2]

    # append the rest of the numbers
    if phone_num != '':
        phone_num += "-" + "-".join([groups[4], groups[6]])
    else: # if the phone number is still empty
        phone_num = "-".join([groups[4], groups[6]])

    # if the phone number has an extension, it will be added
    if groups[7] != '':
        phone_num += ' x' + groups[7]

    matches.append(phone_num)

# For emails
for groups in email_regex.findall(clipboard):
    matches.append(groups)


# Copy the results to the clipboard
if len(matches) > 0:
    pyperclip.copy('\n'.join(matches)) # copies to the clipboard

    # prints the results to the terminal
    print("Copied to the clipboard:\n")
    print('\n'.join(matches))

else:
    print("No phone numbers or email addresses found.")
