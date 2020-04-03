from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import argparse


def mail_to_list(email_list, info_list, gmail, password, subject):
    """Send an email to everyone in the provided csv."""

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail, password)

    # Count how many emails have been sent
    i = 0

    num_users = len(info)
    for email, info in zip(email_list, info_list):
        body = """PUT TEXT OF YOUR EMAIL HERE AND USE .format(info) to insert
                  email-specific information into the email."""
        msg = MIMEMultipart()
        msg['From'] = gmail
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.sendmail(gmail, email, text)
        print('Sent email %s out of %s' % ((i + 1), num_users))
        i += 1

    # Notify user that emails have finished sending
    print('Done sending emails.')


def parse_args():
    """Standard command-line argument parser."""
    # Create command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("gmail", help="Your gmail username, including "
                                      "@gmail.com", type=str)
    parser.add_argument("gmail_PW", help="Your gmail password.", type=str)
    parser.add_argument("subject", help="Email subject.", type=str)
    parser.add_argument("-f", "--file", help="Read from Excel file",
                        required=False, default=None)

    # Parse arguments
    results = vars(parser.parse_args())

    # Display
    print("Your email management selections: \n {}".format(results))

    # Get variables
    gmail = results["gmail"]
    pw = results["gmail_PW"]
    subject = results["subject"]
    file = results["file"]

    return gmail, pw, subject, file


def main():
    # Parse args and read in data, if we have
    gmail, pw, subject, file = parse_args()
    df = pd.read_excel(file)  # Read as excel file

    # Default form: Spreadsheet headers are 'email' and 'info' (where info can be more than one column)
    email_list = df['email']  # Email column
    info_list = df['info']    # Info column(s)
    mail_to_list(email_list, info_list, gmail, pw, subject)


if __name__ == "__main__":
    main()
