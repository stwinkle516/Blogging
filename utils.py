import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random

# mail_id = "twinklesingh2302@gmail.com"
# mail_pass = "mylifestyle"

mail_id = "singhvikashh003@gmail.com"
mail_pass = "qdedxnyxjddqjqbh"

def get_hased_pass(plain_pass):
    # print("Before Conversion -> ", type(plain_pass))
    plain_pass = plain_pass.encode("utf-8")
    # print("After Conversion -> ", type(plain_pass))
    hash_salt = bcrypt.gensalt(rounds=12)
    pwd = bcrypt.hashpw(plain_pass, salt=hash_salt)
    return pwd

def verify_pass(plain_pass, hashed_pass):
    plain_pass = plain_pass.encode('utf-8')
    hashed_pass = hashed_pass.encode('utf-8')
    return bcrypt.checkpw(plain_pass, hashed_pass)

def setup_smtp():
    mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
    mail_conn.ehlo()
    mail_conn.starttls()
    mail_conn.ehlo()
    mail_conn.login(mail_id, mail_pass)
    
    return mail_conn

def send_mail(to, subject, mail_body):
    msg = MIMEMultipart()
    msg['From'] = mail_id
    msg['To'] = to
    msg['Subject'] = subject
    message = mail_body
    msg.attach(MIMEText(message))  
    
    mail_conn = setup_smtp()

    mail_conn.sendmail(mail_id, to, msg.as_string()) 
    mail_conn.quit()


def reset_password(to, name):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(all_characters, k=12))
    mail_body = f"""    
                Hi {name},

                Your password has been reset, please find your new password
                Your New password is {password}

                You can change the same after login


                Team BlogU 
                """
    send_mail(to, "Password Reset - BlogU", mail_body)
    return get_hased_pass(password)
