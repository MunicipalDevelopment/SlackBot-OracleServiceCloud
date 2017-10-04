import os
import time
from slackclient import SlackClient
import requests
import json
import closeslack as slack


# starterbot's ID as an environment variable
BOT_ID = 'YOUR BOTID'

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "311"

# instantiate Slack & Twilio clients
slack_client = SlackClient('YOUR SLACK KEY')


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command followed by division name to get the total."
    


    if command.startswith('show'):
        
        d = command.split(' ')
        response = d[1]
        if d[1].startswith('traffic'):
            hold=[]
            ourl = "https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents?q=queue.id=90%20and%20statusWithType.status.id=3%20or%20queue.id=91%20and%20statusWithType.status.id=3%20or%20queue.id=92%20and%20statusWithType.status.id=3&totalResults=true"
            oresponse=requests.get(ourl,auth=('USER', 'PASSWORD')).text
            oresponseAsJSON=json.loads(oresponse)
            for x in oresponseAsJSON['items']:
                hold.append(x['lookupName'])
            response =','.join(str(e) for e in hold)
        elif d[1].startswith('csd'):
            hold=[]
            csdurl = "https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents?q=queue.id=67%20and%20statusWithType.status.id=3&totalResults=true"
            csdresponse=requests.get(csdurl,auth=('USER', 'PASSWORD')).text
            csdresponseAsJSON=json.loads(csdresponse)
            for x in csdresponseAsJSON['items']:
                hold.append(x['lookupName'])
            response =','.join(str(e) for e in hold)
        else:
            response = "You specified an incorrect division"
    


    if command.startswith('close'):
        x=command.split(' ')
        r = slack.close(x[1],' '.join(x[2:])) #this calls the function in closeslack.py

        response=r







    if command.startswith('case'):
        c = command.split(' ')
        url='https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents?q=lookupName%20like%27'+c[1]+'%27'
        response=requests.get(url,auth=('USER', 'PASSWORD')).text
        responseAsJSON=json.loads(response)

        iurl='https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents/'+str(responseAsJSON['items'][0]['id'])
        iresponse=requests.get(iurl,auth=('USER', 'PASSWORD')).text
        iresponseAsJSON=json.loads(iresponse)
        a=iresponseAsJSON['subject']
        b=iresponseAsJSON['customFields']['c']['description']
        d=iresponseAsJSON['customFields']['c']['address']

        if a is None:
            a=""
        if b is None:
            b=""
        if d is None:
            d=""

        response=a+"\n"+b+"\n"+d


    if command.startswith('divisions'):
        response = "traffic, parking, parks, streets, csd, engineering, facilities, other"


    if command.startswith('help'):
        response = "Use 311 division to get open 311s. Use divisions to get list of valid divisions. Use case 171205-000123 to get info on a specific case. Use close xxx-xxx <resolution text> to close a ticket"


    if command.startswith('311'):
        d = command.split(' ')
        response = d[1]
        if d[1].startswith('traffic'):
            ourl = "https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents?q=queue.id=90%20and%20statusWithType.status.id=3%20or%20queue.id=91%20and%20statusWithType.status.id=3%20or%20queue.id=92%20and%20statusWithType.status.id=3&totalResults=true"
            oresponse=requests.get(ourl,auth=('USER', 'PASSWORD')).text
            oresponseAsJSON=json.loads(oresponse)
            response =str(len(oresponseAsJSON['items']))+" open 311s"
        elif d[1].startswith('csd'):
            csdurl = "https://YOURDOMAIN.custhelp.com/services/rest/connect/v1.3/incidents?q=queue.id=67%20and%20statusWithType.status.id=3&totalResults=true"
            csdresponse=requests.get(csdurl,auth=('USER', 'PASSWORD')).text
            csdresponseAsJSON=json.loads(csdresponse)
            response =str(len(csdresponseAsJSON['items']))+" open 311s"
        else:
            response = "You specified an incorrect division"
    




    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
