import json,sys,httplib,urllib,smtplib
import argparse
from email.mime.text import MIMEText
import pymysql.cursors



#=====================================================================================
#SUMMARY
#=====================================================================================
# Currently the script starts with opening a json file then in the myMain function it goes through a conditional trying to catch the alert by detail(alert name).
# If its caught myMain will take the FI number, and send it to the proper type of report to be parsed (only 4 right now). Once it arrives there the data is molded into objects
# and feeds the FI number,alertType, and data that needs to be parsed to dbPull. dbPull will keep that information but add the FIs listed email address and then pass that along to the mailer.
# the mailing function (when not hardcoded) will make the sender the corresponding email address and choose what template based on the alerttype its fed, then it pushes the email.
#=====================================================================================




#=====================================================================================
#MAIL FUNCTION
#=====================================================================================
#Matches the FIs number in our database and pulls out the first contact associated with it.

# Then this function invokes the mailing fuction and sends the folrmatted data to the proper address.

# Takes in email address, the alert type, and data.
#It is hard coded right now but emailaddr will be fed into reciever when in production
# There is an If Else statement which catches the alert type based on alertType variable and it triggers the specific template for that alert and sends it
def mailSender(emailaddr,alertType,data):

    sender = ''
    receiver = ''
    # this is me splitting the data so it can be fed into html
    parsedData = data.split('*')
    if alertType == 'user-lockout':
        #msg = """ Alert with said data """ +str(alertType)+ " "+str(emailaddr)+" "+str(data)+"\n"
        msg = MIMEText(""" 
        
        <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body  bgcolor="#d1d1e0" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<table bgcolor=#t60000" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
    <tr height="100">
        <td valign="center" >
            <table  border="0" cellpadding="20" cellspacing="0"  id="emailContainer">
                <tr>
                    <td valign="top"><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailHeader">
                        <tr>
                            <td align="left" valign="top">
                                <p class="sa" style="color:#000000; font-family: Arial; margin: 0;"><b>RSA NetWitness Suite</b></p>
                                <h1 style="color:#000000; font-family: Arial; font-weight: normal; margin: 0;"><b>ESA Notification """ +parsedData[0]+"""</b></h1></td>
                        </tr>
                    </table></td>
                </tr>
            </table></td>
    </tr>
    <tr>

        <td valign="top" bgcolor="#ffffff"><table border="0" cellpadding="20" cellspacing="0" width="100%" id="emailContainer2">
            <tr>

                <td><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailBody">
                    <tr>
                    <td><span style="color: #757575; font-family: Arial; font-size: .9em;">FI #</span>
                        <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[1]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Src User</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[2]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Dst User</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[3]+"""</p></td>
                    </tr>
                    <tr>
                        <td><hr style="border-color: #cccccc; border-width: 1px 0 0 0; border-style:solid;"></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Time</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[4]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Domain</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[5]+"""</p></td>

                    </tr>
                    <tr>
                        <td><p style="color: #757575; font-family: Arial; font-size: .9em;">Event computer</p>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[6]+"""</p></td>
                            <table cellpadding="0" cellspacing="0">
                                <tbody>
                                <tr>
                                    <td>
                                           <table border="0" cellpadding="0" cellspacing="0">
                                                <tbody>
                                                <tr>
                                                    <td>
                                                        <table id="events" border="0" cellpadding="0" cellspacing="0">
                                                            <thead>
                                                            <tr>
                                                                <th scope="col" width="300px" align="left"><span style="color: #757575; font-family: Arial; font-size: .9em; font-weight: normal;">Outcome</span></th>
                                                                <th scope="col" align="left"><span style="color: #757575; font-family: Arial; font-size: .9em; font-weight: normal;">Category</span></th>
                                                            </tr>
                                                            </thead>
                                                              <tbody>
                                                                <tr>
                                                                    <td><span style="color: #363636; font-family: Arial; font-size: 1.1em;">"""+parsedData[8]+"""</span></td>
                                                                    <td><span style="color: #363636; font-family: Arial; font-size: 1.1em;">"""+parsedData[7]+"""</span></td>
                                                                </tr>
                                                                </tbody>
</#list>                                                        </table>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>
</#list>                                    </td>
                                </tr>
                                </tbody>
                            </table>
</#if>                        </td>
                    </tr>
                </table></td>
            </tr>

        </table></td>
    </tr>

</table>

</body>
</html>
        
        
        """,'html')


        msg['Subject'] = alertType
        msg['From'] = sender
        msg['To'] = receiver

        try:
            smtpObj = smtplib.SMTP('')
            smtpObj.sendmail(sender, receiver, str(msg))
            smtpObj.quit()

            print('Step 4: sending email\n')
        except smtplib.SMTPException:
            print('Error sending email')


    elif alertType == 'executable download outside of baseline':
        msg = MIMEText("""
        <html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<style>
		td { font-family: Arial; font-size: 1em; padding-right: 5px;}
		th { font-family: Arial; text-align: left; }
	</style>
</head>
<body bgcolor="#b4b4b4" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
    <tr height="100">
        <td valign="center" bgcolor="#FFB200">
            <table border="0" cellpadding="20" cellspacing="0" id="emailContainer">
                <tr>
                    <td valign="top"><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailHeader">
                        <tr>
                            <td align="left" valign="top">
                                <p class="sa" style="color:#ffffff; font-family: Arial; margin: 0;"> <b>SOC</b> powered by <b>RSA</b> Netwitness</p>
                                <h1 style="color:#ffffff; font-family: Arial; font-weight: normal; margin: 0;">"""+str(parsedData[0])+"""</h1></td>
                        </tr>
                    </table></td>
                </tr>
            </table></td>
    </tr>
    <tr>
        <td valign="top" bgcolor="#ffffff"><table border="0" cellpadding="20" cellspacing="0" width="100%" id="emailContainer2">
            <tr>
                <td><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailBody">
					<tr>
                        <td><hr style="border-color: #cccccc; border-width: 1px 0 0 0; border-style:solid;"></td>
                    </tr>
					<tr>
                        <td>
							<p> A user has attempted to download an executable file.</p>
							<p style="color: #363636; font-family: Arial; font-size: 1.2em; margin: 4px 0; text-decoration: underline">Summary</p><br>
							<table>
								<tr>
									<td><b>Time:</b></td><td>"""+str(parsedData[1])+"""</td>
								</tr>
								<tr>
									<td><b>Proxy: </b></td><td>"""+str(parsedData[2])+"""</td>
								</tr>
								<tr>
									<td><b>Source IP: </b></td><td>"""+str(parsedData[3])+"""</td>
								</tr>
								<tr>
									<td><b>Website: </b></td><td>"""+str(parsedData[4])+"""</td>
								</tr>
								<tr>
									<td><b>File: </b></td><td>"""+str(parsedData[5])+"""</td>
								</tr>
								<tr>
									<td><b>Status: </b></td><td>"""+str(parsedData[6])+"""</td>
								</tr>
								<tr>
									<td><b>Category: </b></td><td>"""+str(parsedData[7])+"""</td>
								</tr>


								<tr>
									<td><b>Country: </b></td><td>"""+str(parsedData[8])+"""</td>
								</tr>
								<tr>
									<td><b>Organization: </b></td><td>"""+str(parsedData[9])+"""</td>
								</tr>
							</table>
							<p> This alert was generated.... </p>
						</td>

                    </tr>
                </table></td>
            </tr>
        </table></td>
		</tr>
</table>
</body>
</html>

            
            
        """,'html')


        msg['Subject'] = alertType
        msg['From'] = sender
        msg['To'] = receiver

        try:
            smtpObj = smtplib.SMTP('#')
            smtpObj.sendmail(sender, receiver, str(msg))
            smtpObj.quit()

            print('Step 4: sending email\n')
        except smtplib.SMTPException:
            print('Error sending email')


    elif alertType == 'user-unlocks':
        msg = MIMEText("""
        
           <html>
         <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body  bgcolor="#d1d1e0" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<table bgcolor=#t60000" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
    <tr height="100">
        <td valign="center" >
            <table  border="0" cellpadding="20" cellspacing="0"  id="emailContainer">
                <tr>
                    <td valign="top"><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailHeader">
                        <tr>
                            <td align="left" valign="top">
                                <p class="sa" style="color:#000000; font-family: Arial; margin: 0;"><b>RSA NetWitness Suite</b></p>
                                <h1 style="color:#000000; font-family: Arial; font-weight: normal; margin: 0;"><b>ESA Notification """ +parsedData[0]+"""</b></h1></td>
                        </tr>
                    </table></td>
                </tr>
            </table></td>
    </tr>
    <tr>

        <td valign="top" bgcolor="#ffffff"><table border="0" cellpadding="20" cellspacing="0" width="100%" id="emailContainer2">
            <tr>

                <td><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailBody">
                    <tr>
                    <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Alert ID</span>
                        <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[1]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Event Computer</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[2]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">User Source</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[3]+"""</p></td>
                    </tr>
                    <tr>
                        <td><hr style="border-color: #cccccc; border-width: 1px 0 0 0; border-style:solid;"></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">User Dest</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[4]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Domain</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[5]+"""</p></td>

                    </tr>
                    <tr>
                        <td><p style="color: #757575; font-family: Arial; font-size: .9em;">Reference ID</p>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[6]+"""</p></td>

</#if>                        </td>
                    </tr>
                </table></td>
            </tr>

        </table></td>
    </tr>

</table>

</body>
</html>
            
        
        """,'html')


        msg['Subject'] = alertType
        msg['From'] = sender
        msg['To'] = receiver

        try:
            smtpObj = smtplib.SMTP('#')
            smtpObj.sendmail(sender, receiver, str(msg))
            smtpObj.quit()

            print('Step 4: sending email\n')
        except smtplib.SMTPException:
            print('Error sending email')

    elif alertType == 'login-to-multiple-devices--0':
        msg = MIMEText("""
        
                   <html>
         <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body  bgcolor="#d1d1e0" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">

<table bgcolor=#t60000" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
    <tr height="100">
        <td valign="center" >
            <table  border="0" cellpadding="20" cellspacing="0"  id="emailContainer">
                <tr>
                    <td valign="top"><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailHeader">
                        <tr>
                            <td align="left" valign="top">
                                <p class="sa" style="color:#000000; font-family: Arial; margin: 0;"><b>RSA NetWitness Suite</b></p>
                                <h1 style="color:#000000; font-family: Arial; font-weight: normal; margin: 0;"><b>ESA Notification """ +parsedData[0]+"""</b></h1></td>
                        </tr>
                    </table></td>
                </tr>
            </table></td>
    </tr>
    <tr>

        <td valign="top" bgcolor="#ffffff"><table border="0" cellpadding="20" cellspacing="0" width="100%" id="emailContainer2">
            <tr>

                <td><table border="0" cellpadding="8" cellspacing="0" width="100%" id="emailBody">
                    <tr>
                    <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Ec Activity</span>
                        <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[1]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Header ID</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[2]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Reference ID</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[3]+"""</p></td>
                    </tr>
                    <tr>
                        <td><hr style="border-color: #cccccc; border-width: 1px 0 0 0; border-style:solid;"></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">User dest</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[4]+"""</p></td>
                    </tr>
                    <tr>
                        <td><span style="color: #757575; font-family: Arial; font-size: .9em;">Event Computer</span>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[5]+"""</p></td>

                    </tr>
                    <tr>
                        <td><p style="color: #757575; font-family: Arial; font-size: .9em;">Process</p>
                            <p style="color: #363636; font-family: Arial; font-size: 1.1em; margin: 4px 0;">"""+parsedData[6]+"""</p></td>

</#if>                        </td>
                    </tr>
                </table></td>
            </tr>

        </table></td>
    </tr>

</table>

</body>
</html>
        
        
        """, 'html')

        msg['Subject'] = alertType
        msg['From'] = sender
        msg['To'] = receiver

        try:
            smtpObj = smtplib.SMTP('#')
            smtpObj.sendmail(sender, receiver, str(msg))
            smtpObj.quit()

            print('Step 4: sending email\n')
        except smtplib.SMTPException:
            print('Error sending email')
    else:
        print(" Could not find properly tagged alert")


#This function takes in the FI number, type of alert, and data that needs to be pulled
# It will connect to the DB and search the DB for the first email address listed for that FI.
# It then grabs and stores the address and sends the address, alerttype and data to the mailer to be parsed and sent

def dbPull(fiNumber, alertType, data):
    email = []
    connection = pymysql.connect(host='#', user='', password='#', db='#',
                                 autocommit=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("Youve connected" + '\n')

    try:
        with connection.cursor() as cursor:
            sqlStatement = "SELECT recipient FROM contacts WHERE bank_id="+str(fiNumber)+""
            cursor.execute(sqlStatement)
            if 'SHOW' or 'SELECT' in sqlStatement:
                for results in cursor:
                    email.append(results)
            else:
                print('Error in DBpull')
            print('Step 3: Pull DB data\n')
            mailSender(str(email[0]['recipient']),str(alertType),str(data))
    except:
        print('Error finding FI')
    finally:
        connection.close()

#=====================================================================================
#USER LOCKOUT
#=====================================================================================

#Defines all the data needed for User Lockouts from the json file and passes the FI number, alerttype, and data on to the dbPull
def UserLockout(Client):
    alert_id = data['events'][0]['alert_id']
    category = data['events'][0]['category']
    fi =  Client
    info = data['events'][0]['info']
    device_class = data['events'][0]['device_class']
    device_disc = data['events'][0]['device_disc']
    device_disc_type = data['events'][0]['device_disc_type']
    device_group = data['events'][0]['device_group']
    device_host = data['events'][0]['device_host']
    device_type = data['events'][0]['device_type']
    did = data['events'][0]['did']
    domain = data['events'][0]['domain']
    ec_activity = data['events'][0]['ec_activity']
    ec_outcome = data['events'][0]['ec_outcome']
    ec_subject = data['events'][0]['ec_subject']
    ec_theme = data['events'][0]['ec_theme']
    esa_time = data['events'][0]['esa_time']
    event_cat_name = data['events'][0]['event_cat_name']
    event_computer = data['events'][0]['event_computer']
    event_desc = data['events'][0]['event_desc']
    event_source = data['events'][0]['event_source']
    event_source_id = data['events'][0]['event_source_id']
    event_time = data['events'][0]['event_time']
    event_type = data['events'][0]['event_type']
    feed_name = data['events'][0]['feed_name']
    forward_ip = data['events'][0]['forward_ip']
    header_id = data['events'][0]['header_id']
    host_src = data['events'][0]['host_src']
    inv_category = data['events'][0]['inv_category']
    inv_context = data['events'][0]['inv_context']
    lc_cid = data['events'][0]['lc_cid']
    medium = data['events'][0]['medium']
    msg = data['events'][0]['msg']
    msg_id = data['events'][0]['msg_id']
    reference_id = data['events'][0]['reference_id']
    rid = data['events'][0]['rid']
    sessionid = data['events'][0]['sessionid']
    size = data['events'][0]['size']
    time = data['events'][0]['time']
    user_dst = data['events'][0]['user_dst']
    user_src = data['events'][0]['user_src']
    altType = data['detail']
    print("Step 2: Push data\n")
    dbPull(fi, altType,str(altType)+'*'+str(fi)+'*'+str(user_src)+'*'+str(user_dst)+'*'+str(time)+'*'+str(domain)+'*'+str(event_computer)+'*'+str(category)+'*'+str(ec_outcome))


#=====================================================================================
#Download out of baseline
#=====================================================================================
# Defines all the data needed for outside of baseline from the json file and passes the FI number, alerttype, and data on to the dbPull

def outsideBaseline(Client):
    fi = Client
    fullmsg = str(data['events'][0]['msg']).split(',')
    time = str(fullmsg[0])+' '+str(fullmsg[1])
    proxy = data['events'][0]['ip_src']
    source_IP = data['events'][0]['device_ip']
    website = data['events'][0]['url']
    filez = data['events'][0]['host_dst']
    status = data['events'][0]['disposition']
    category = data['events'][0]['category']
    country = data['events'][0]['country_dst']
    orginization = data['events'][0]['org_dst']
    altType = data['detail']
    print("Step 2: Push data\n")
    dbPull(fi,altType,str(altType)+'*'+str(time)+'*'+str(proxy)+'*'+str(source_IP)+'*'+str(website)+'*'+str(filez)+'*'+str(status)+'*'+str(category)+'*'+str(country)+'*'+str(orginization))

#=====================================================================================
#User Unlocks
#=====================================================================================
# Defines all the data needed for user unlocks from the json file and passes the FI number, alerttype, and data on to the dbPull

def userunlocks(Client):
    fi = Client
    ec_activity = data['events'][0]['ec_activity']
    header_id = data['events'][0]['header_id']
    reference_id = data['events'][0]['reference_id']
    user_src = data['events'][0]['user_src']
    event_computer = data['events'][0]['event_computer']
    alert_id = data['events'][0]['alert_id']
    user_dst = data['events'][0]['user_dst']
    domain = data['events'][0]['domain']
    ec_outcome = data['events'][0]['ec_outcome']
    altType = data['detail']
    print("Step 2: Push data\n")
    dbPull(fi,altType,str(altType)+'*'+str(alert_id)+'*'+str(event_computer)+'*'+str(user_src)+'*'+str(user_dst)+'*'+str(domain)+'*'+str(reference_id))


# =====================================================================================
# Multiple Devices
# ====================================================================================
# Defines all the data needed for multiple devices from the json file and passes the FI number, alerttype, and data on to the dbPull

def multipleDevices(Client):
    fi = Client
    ec_activity = data['events'][0]['ec_activity']
    header_id = data['events'][0]['header_id']
    reference_id = data['events'][0]['reference_id']
    user_dst = data['events'][0]['user_dst']
    event_computer = data['events'][0]['event_computer']
    process = data['events'][0]['process']
    altType = data['detail']
    print("Step 2: Push data\n")
    dbPull(fi,altType,str(altType)+'*'+str(ec_activity)+'*'+str(header_id)+'*'+str(reference_id)+'*'+str(user_dst)+'*'+str(event_computer)+'*'+str(process))

#=====================================================================================
#Args
#=====================================================================================
#                   NOT FINISHED WITH ARGS/TEST ARGS
# def getArgs():
#     parser = argparse.ArgumentParser()
#     print('im working')
#     parser.add_argument('--verbose',
#                         action='store_true',
#                         help='verbose flag')
#     args = parser.parse_args()
#     print('still working')
#
#     if args.verbose == "--verbose":
#         print('-verbose')
#     else:
#         print('no verbose')


# =====================================================================================
# MAIN
# =====================================================================================
# Grabs the data from the json file and allocates it to the object "data"
# this is directly determined by the detail section in the json file
# For most of this script data['detail'] and alertType determine when things are caught by the If/elif statements
def myMain():
    if 'user-lockout' in data['detail']:
        #Begin User Lockout Function
        clientNumber = data['events'][0]['fi']
        print("Step 1: User Lockout\n")
        UserLockout(clientNumber)
    elif 'executable download outside of baseline' in data['detail']:
        clientNumber = data['events'][0]['fi']
        print("Step 1: download out of baseline\n")
        outsideBaseline(clientNumber)
    elif 'user-unlocks' in data['detail']:
        clientNumber = data['events'][0]['fi']
        print("Step 1: User Unlocks\n")
        userunlocks(clientNumber)
    elif 'login-to-multiple-devices--0' in data['detail']:
        clientNumber = data['events'][0]['fi']
        print("Step 1: login to multiple\n")
        multipleDevices(clientNumber)
    else:
        print('could not catch if statement on detail name')

if __name__ == '__main__':
    myMain()
