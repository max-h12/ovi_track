import info
import smtplib

carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}

def send(number, carrier, message):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = (number).format(carriers[carrier])
    auth = (info.email, info.password)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)

def main():
    print("sending")
    for phone, carrier in info.numbers.items():
        send(phone, carrier, "test asdfa")

if __name__ == "__main__":
    main()