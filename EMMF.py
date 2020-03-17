import sys, imaplib, smtplib, email, email.policy

user = 'yourEmailHere@gmail.com'
password = 'asdfasdfasdfasdf' # For Gmail visit https://myaccount.google.com/apppasswords ,  select App (E-Mail) and Device (whatever u wanna call it) ,  select generate  and   paste the generated code between the single quotation marks
imap_url = 'imap.gmail.com'
smtp_url = 'smtp.gmail.com'
smtp_port = '587'

mailbox = 'School' # The Name of your Mailbox you wat to query

# All the E-Mail adresses, you want the unread mails to be forwarded to. 
#   Enclosed in single quotation marks,  seperated by comma and space  and   enclosed in square brackets.
recipients = ['idk@ab.cd','idk@ef.gh']


## Functions definition

# sets up the imap auth
def auth_imap(user,password,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user,password)
    return con

# sets up the smtp auth
def auth_smtp(user,password,smtp_url,smtp_port):
    con = smtplib.SMTP(smtp_url,smtp_port)
    con.ehlo()
    con.starttls()
    con.ehlo()
    con.login(user,password)
    return con

# get mails as email.message.Message objects
def get_mails(con,search):
    mlist = str(str(search)[1:].replace("'",''))
    mlist = mlist.split()
    mails = []
    for mnbr in mlist:
        stat, data = con.fetch( mnbr ,'(RFC822)')
        if not stat == 'OK' : raise Warning(UserWarning('Could not download mails "'+ mlist +'" from mailbox "'+ mailbox +'", returned stat "'+ stat +'", data "'+ data +'"'))

        mails.append(email.message_from_bytes(data[0][1], policy=email.policy.default))

    return mails
  

def quit():
    print('Close SMTP connection ...')
    smtpcon.quit()
    print('Close IMAP connection ...')
    con.close()
    con.logout()
    print('Finally done ...')
    print()
    input("To quit the programm, press ENTER.")
    sys.exit(0)
    

## Actual execution chain
print ('Connecting with E-Mail mailbox "'+ mailbox +'" by "' + user + '" using the IMAP server "'+ imap_url +' and the SMTP server "'+ smtp_url +':'+ smtp_port +'" ...')

con = auth_imap(user, password, imap_url) #Connect IMAP 
smtpcon = auth_smtp(user,password,smtp_url,smtp_port) #Connect SMTP
stat, data = con.select(mailbox = mailbox) #Check mailbox

if not stat == 'OK' : raise Warning(UserWarning('Could not select mailbox "'+ mailbox +'", returned stat "'+stat+'", data "'+data+'"'))

print()

cm = str(data[0])[2:len(str(data [0]))-1]
if not cm.isdigit() or ( cm.isdigit() and int(cm) < 1) : raise Warning(UserWarning('No messages in mailbox "'+ mailbox +'", returned stat "'+stat+'", data "'+data+'"'))

stat, data = con.search(None,'Unseen')

if not stat == 'OK' : raise Warning(UserWarning('Could not search mailbox "'+ mailbox +'", returned stat "'+stat+'", data "'+data+'"'))

print( str( len( data[0].decode("utf-8").split() ) ) + ' unread E-Mails: '+ data[0].decode("utf-8"))
print()

if  len( data[0].decode("utf-8").split() ) == 0: quit()

print('Donwload E-Mails '+ data[0].decode("utf-8"))
mails = get_mails(con,data[0])
print()
counter = 1
for msg in mails: 
    print(str(counter) +'th E-Mail on its way to everybody!')
    smtpcon.send_message(msg,None,recipients)
    counter = counter + 1
print ()
print ('Done!')
print()
quit()