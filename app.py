from flask import Flask,request
from Helper.helper import generate_message,get_response
from Helper.twilio import send_message
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


#----------------------------------------------------------------
# Send Inital message to whatsapp business
#----------------------------------------------------------------
@app.route('/twilio/whatsapp/',methods=['POST'])
def receive_message():
    try:
        response=generate_message("Who is Dr.Gali Nageswara")
        print(response)
        # message=request.form['Body']
        # sender_id = request.form['From']
        # print(message)
        # response=generate_message(message)
        # print(response['response'])
        # if response['status']==1:
        #     send_message(sender_id,response['response'])
    except:
        pass
    return "ok",200
        
#----------------------------------------------------------------
# main page
#----------------------------------------------------------------
@app.route('/')
def main():
    response=get_response("Who is Dr.Gali Nageswara")
    print(response)
    return "Hello i am running"

if __name__ == "__main__":
    app.run(debug=True)   

    


    