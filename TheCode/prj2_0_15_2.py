#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import json
app = Flask(__name__) 
ACCESS_TOKEN = 'Your Access Token here'
VERIFY_TOKEN = 'VERIFY_TOKEN'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       #print(output)

       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    sen = message['sender']
                    #print(sen)
                    #print(message)
                    if  message['message'].get('nlp'):
                        sen2 = message['message'].get('nlp')

                        #dicto=json.load(sen2)
                        #print (sen2)

                        for k,v in  sen2.items():
                            #print (k)
                            for ke,va in v.items():
                                #print (ke)
                                send_message(recipient_id,'The Field')
                                send_message(recipient_id, ke)

                                for i in va:
                                    for key,val in i.items():
                                        #str=key+' : '+val
                                        str=" ";
                                        #str=str(key)+' : '+str(val);
                                        send_message(recipient_id,'Key is')
                                        send_message(recipient_id,key)
                                        send_message(recipient_id,'Corresponding value')
                                        send_message(recipient_id,val)

                    #print (sen2)
                    response_sent_text = get_message(recipient_id)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    #send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(recipient_id):
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    siv='hi '+random.choice(sample_responses)
    return siv

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
