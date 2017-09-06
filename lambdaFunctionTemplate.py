# Alexa skill lambda function python template

from __future__ import print_function
import random
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    if (event['session']['application']['applicationId'] !=
            "---skill ID here---"): 
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        event['session']['attributes'] = {}

    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_launch():

    return Help()


def on_intent(intent_request, session):

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "intentOne":
        return intentOne(intent, session)
    elif intent_name == "intentTwo":
        return intentTwo(intent, session)       
    elif intent_name == "intentThree":
        return intentThree(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return Stop()
    elif intent_name == "AMAZON.HelpIntent":
        return Help()
    elif intent_name == 'AMAZON.StopIntent':
        return Stop()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    pass


def Stop():
    should_end_session = True
    speech_output = ""
    session_attributes = {}

    return build_response(
        session_attributes,
        build_speechlet_responseND(
            speech_output,
            should_end_session))


def Help():
    should_end_session = False
    speech_output = 'Enter help text here.'
    session_attributes = {}

    return build_response(
        session_attributes,
        build_speechlet_responseND(
            speech_output,
            should_end_session))


#------------------------------DynamoDBFunctions-------------------------------


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-west-1',
    aws_access_key_id="access key here",
    aws_secret_access_key="secret access key here")


def addItem(table, ID, playerName):
    #Add name to the table
    Table = dynamodb.Table(table)
    Table.put_item(
        Item={
            'userId': ID,
            'playerName': playerName
        }
    )


def updateItem(table, ID, playerName, item):
    #Not currently used
    Table = dynamodb.Table(table)
    Table.update_item(
        Key={
            'userId': ID,
            'playerName': playerName
        },
        UpdateExpression="set playerName = :p",
        ExpressionAttributeValues={
            ':p': item,
        },
        ReturnValues="UPDATED_NEW"
    )


def readItem(table, ID, playerName):
    #Not currently used
    Table = dynamodb.Table(table)
    try:
        response = Table.get_item(
            Key={
                'userId': ID,
                'playerName': playerName
            }
        )
    except ClientError as e:
        return "Error"
    else:
        item = response['Item']
        return item


def deleteItem(table, ID, playerName):
    #Remove name from the table
    Table = dynamodb.Table(table)
    try:
        response = Table.delete_item(
            Key={
                'userId': ID,
                'playerName': playerName
            },
        )
    except ClientError as e:
        return "Error"
    else:
        return "Succeeded"

def deleteAll(table, ID):
    #Remove everything under one ID
    Table = dynamodb.Table(table)
    players = Table.query(KeyConditionExpression=Key('userId').eq(ID))
    for i in players['Items']:
        Name = i['playerName']
        response = Table.delete_item(
            Key={
                'userId': ID,
                'playerName': Name
            },
        )



# -------------------------------Intent handlers-------------------------------


def intentOne(intent, session):

    should_end_session = True
    session_attributes = {}
    speech_output = 'speech output here'

    return build_response(
        session_attributes,
        build_speechlet_responseND(
            speech_output,
            should_end_session))


def intentTwo(intent, session):

    should_end_session = True
    session_attributes = {}
    speech_output = 'speech output here'

    return build_response(
        session_attributes,
        build_speechlet_responseND(
            speech_output,
            should_end_session))


def intentThree(intent, session):

    should_end_session = True
    session_attributes = {}
    speech_output = 'speech output here'

    return build_response(
        session_attributes,
        build_speechlet_responseND(
            speech_output,
            should_end_session))





# ----------------- Helpers that build all of the responses -------------------


def build_speechlet_responseND(output, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "shouldEndSession": should_end_session
    }


def build_speechlet_response(output, should_end_session, S2E, reprompt=""):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt
            }
        },
        "directives": [
            {
                "type": "Dialog.ElicitSlot",
                "slotToElicit": S2E
            }
        ],
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
