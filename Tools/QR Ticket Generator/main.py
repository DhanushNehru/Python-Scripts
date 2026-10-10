import qrcode
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
from fpdf import FPDF
# gmail auth
gmail_user = 'Event.vitb@gmail.com'
gmail_password = 'jydbwqtbfvwwrdpv'

FILEPATH = "InsertDataHERE.xlsx"


def send_ticket(email, full_name, registration_number, event_name, pdf_dir):
    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = email
        msg['Subject'] = 'Event Ticket'
        # Add text to the email body
        text = MIMEText(f"Hey {full_name},"
                        f"\n PFA of your event {event_name} Ticket"
                        f"\n We hope you enjoy the event!")
        msg.attach(text)
        # # Add an image attachment to the email
        # with open('image.jpg', 'rb') as f:
        #     img = MIMEImage(f.read())
        #     msg.attach(img)
        # Add a pdf attachment to the email
        fileName = pdf_dir
        with open(fileName, 'rb') as f:
            pdf = MIMEApplication(f.read(), _subtype='pdf')
        pdf.add_header('content-disposition', 'attachment', filename=os.path.basename(fileName))
        msg.attach(pdf)
        # Create the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()

    except:
        print(f"{registration_number}-{full_name} Failed to send mail")


def make_qr(full_name: str, registration_number: str, unique_id: str, event_name: str):
    try:

        print(f"{registration_number}-{full_name} QR successfully generated")

        # Making QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(unique_id)
        qr.make(fit=True)

        # Saving QR in respective directory
        img = qr.make_image(fill_color="black", back_color="white")
        qrcode_dir = f"{registration_number}.png"
        img.save(qrcode_dir)

        print(f"{registration_number}-{full_name} QR Code saved here:- {qrcode_dir}")

        return qrcode_dir
    except:
        print(f"{registration_number}-{full_name} Failed to generate QR for ")


class PDF(FPDF):
    def __init__(self):
        super().__init__(format='A5', orientation='L')

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Entry Pass')
        # Line break
        self.ln(20)

    def heading(self, EVENT_NAME):
        self.cell(80)
        # Font
        self.set_font("Arial", 'B', 40)
        # Event name
        self.cell(30, 30, EVENT_NAME, 0, 0, 'C')

    def date_time_venue(self, DATE_TIME_EVENT, VENUE_EVENT):
        self.cell(40)
        # Font
        self.set_font("Arial", 'B', 10)
        # DATE_TIME_VENUE
        self.cell(-110, 76, DATE_TIME_EVENT, 0, 0, 'C')
        self.cell(110, 88, VENUE_EVENT, 0, 0, 'C')

    def attendee_name(self, PER_NAME):
        self.set_y(70)
        self.set_font("Arial", 'B', 25)
        # ATTENDEE NAME
        self.cell(60, 50, PER_NAME, 0, 0, 'L')
        # self.cell(65, 58, ROLE, 0, 0, 'C')

    def role_in_event(self, ROLE):
        self.set_y(76)
        self.set_font("Arial", 'I', 10)
        # Role in Event
        self.cell(60, 52, f"ROLE: {ROLE}", 0, 0, 'L')

    def payment_status(self, PAYMENT):
        self.set_y(-37)
        self.set_font("Arial", '', 10)
        # Payment Status
        self.cell(0, 10, PAYMENT, 0, 0, 'L')

    def order_number(self, order_no):
        self.set_x(-75)
        self.set_font("Arial", '', 10)
        # Order Number
        self.cell(0, 10, f"Order Number: {order_no}", 0, 0, 'L')

    def get_qr_code(self, file_path: str):
        self.image(name=file_path, x=155, y=85, w=25, h=25)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def generate_pdf(event_name: str, full_name: str, role: str, payment_status: str,
                 unique_id: str, qrcode_dir: str, registration_number: str,
                 date_time_event='28 February 2023, 4PM to 7PM', venue_event='location_hehe'):
    try:

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.heading(EVENT_NAME=event_name)
        pdf.date_time_venue(DATE_TIME_EVENT=date_time_event, VENUE_EVENT=venue_event)
        pdf.attendee_name(PER_NAME=full_name)
        pdf.role_in_event(ROLE=role)
        pdf.payment_status(PAYMENT=payment_status)
        pdf.order_number(order_no=unique_id)
        pdf.get_qr_code(qrcode_dir)

        pdf_dir = f"{registration_number}.pdf"

        pdf.output(pdf_dir)

        print(f"{registration_number}-{full_name} PDF saved here:- {pdf_dir}")
        os.remove(f"{registration_number}.png")
        return pdf_dir

    except Exception as e:
        print(e)


def start_entry_process():
    # collection = connectToDatabase()
    df = pd.read_excel(FILEPATH)
    confirm_payment_df = df[df['payment status'] == 'captured']
    failed_payment_df = df[df['payment status'] == 'failed']

    for index in range(0, len(confirm_payment_df)):
        # try:

        registration_number = confirm_payment_df['registration_number'].iloc[index].upper()
        unique_id = confirm_payment_df['order_id'].iloc[index]
        event_name = confirm_payment_df['payment button title'].iloc[index]
        email = confirm_payment_df['email'].iloc[index]
        full_name = confirm_payment_df['full_name'].iloc[index].upper()
        gender = confirm_payment_df['gender'].iloc[index].upper()
        role = "ATTENDEE"
        payment_status = "PAID"
        document = {
            "registration_number": registration_number,
            "full_name": full_name,
            "unique_id": unique_id,
            "event_name": event_name,
            "email": email,
            "gender": gender,
            "role": role,
            "payment_status": payment_status,
            "isInside": False
        }
        try:

            qrcode_dir = make_qr(full_name, registration_number, unique_id, event_name)
            pdf_dir = generate_pdf(event_name, full_name, role, payment_status,
                                   unique_id, qrcode_dir, registration_number)

            send_ticket(email, full_name, registration_number, event_name, pdf_dir)

        except Exception as e:
            print(e)
            print(f"{registration_number}-{full_name} Already in database")


if __name__ == '__main__':
    start_entry_process()
