from flask import Flask, request, render_template
from google.cloud import dialogflow
from google.oauth2 import service_account

app = Flask(__name__)


@app.route('/')
def home():
    # just render the HTML homepage
    return render_template("index.html")


@app.route('/process', methods=['POST'])
def detect_intent():
    # create a new session
    credentials = service_account.Credentials.from_service_account_file("client-secret.json")
    session_client = dialogflow.SessionsClient(credentials=credentials)

    # replace the project id, since it is fake
    # 123456 is the session id, which should not be changed within an entire conversation with a single user
    session = session_client.session_path("human-ai-project", 123456)

    # prepare a new query input with the inner text, taken from the POST request
    text_input = dialogflow.TextInput(text=request.form["message"], language_code="en-US")
    query_input = dialogflow.QueryInput(text=text_input)

    # send the request and get the response
    response = session_client.detect_intent(session=session, query_input=query_input)

    # print(response.query_result.intent.displayName)
    # print(response.query_result.parameters['geo-city'])

    # reply to the POST request: the textual response is in "fullfilment"
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    app.run()
