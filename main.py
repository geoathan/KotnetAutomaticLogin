import re                               ## Basislib voor regular expressions
import mechanize                        ## Emulates a browser



username='r0448466' # insert your r number
password='*********' # insert your password

#try:
browser = mechanize.Browser()
browser.addheaders = [{'User-agent','Mozilla/5.0'}]
browser.set_handle_robots(False);
response = browser.open('https://netlogin.kuleuven.be/')

## passing first loging screen (where we check for language and press 'Ga verder')
forms = mechanize.ParseResponse(response, backwards_compat=False)
form=forms[0]
#print form
browser.select_form(nr=1)
browser.submit()

## Second login screen that asks for credentials
browser.select_form(nr=1)
browser.form["uid"] = username

password_name = browser.form.find_control(type="password").name # password name dynamically changes in each login so we capture that name for the specific login
browser.form[password_name]=password #give password
browser.submit() #submit form
#print browser.geturl() 

print '---------------'    
html = browser.response()
html = html.read().lower()
html = unicode(html,errors='ignore')
#print html

login_check_pattern = re.compile('error:<rc=202 (.*?) <kotnet-verify-password')
login_check = re.findall(login_check_pattern,html)

try:
    if login_check[0] == 'invalid password':
        print 'login unsuccesful, check username/password combination'
        print '---------------'
    else:
        print 'unknown error'
        print '---------------'
        
except :
    print 'login succesful for ' + username
    print '---------------'

## Scrape details from 'login succesful' page    
    percent_pattern = re.compile (r'mbytes<br>((.*?))</td>')
    percent = re.findall(percent_pattern,html)

    megabytes_pattern = re.compile(r'<td width="30%">(.*?)<br>')
    megabytes = re.findall(megabytes_pattern,html)

    ip_pattern = re.compile(r'ip-addr = (.*?)<br>')
    ip = re.findall(ip_pattern,html)

    usr_id_pattern = re.compile('intranet userid = kuleuven/(.*?)</br>')
    usr_id = re.findall(usr_id_pattern,html)

    email_pattern = re.compile('email = (.*?)<br>' )
    email = re.findall(email_pattern,html)
                            
    print 'download: ' + percent[0][0] +' '+ megabytes[0]
    print 'upload: ' + percent[1][0] +' '+ megabytes[1]
    print 'your ip is: ' + ip[0]
    print 'your email is : ' + email[0]
    print 'your user id is : ' + usr_id[0]
