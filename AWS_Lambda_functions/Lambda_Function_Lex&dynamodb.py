import json
import boto3
from decimal import *
from boto3.dynamodb.conditions import Key
def lambda_handler(event, context):
    response = {}
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    food_name = event['sessionState']['intent']['slots']['food']['value']['interpretedValue']
    dynamodbclient = boto3.resource('dynamodb')
    table = dynamodbclient.Table("fooditems")
    table_obj = table.query(KeyConditionExpression=Key('foodname').eq(food_name))
    #Debug print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # Debug print(table_obj)
    calorie_count = str(table_obj["Items"][0]["calorie"])
    #print(calorie_count)
    #print(event)
    if event["invocationSource"] == "DialogCodeHook":
        if event['inputTranscript'] == 'yes' and event["interpretations"][0]["intent"]["confirmationState"] == "Confirmed" and event["interpretations"][0]["intent"]["name"] == "caloriecheck":
            response = {"sessionState": {"dialogAction": {"type": "Close","state": "Fulfilled"},"intent": {'name':intent,'slots': slots}},"messages": [{"contentType": "PlainText","content": food_name+" has 40 calories in 100 grams. "}]}
        else:
            response = {"sessionState": {"dialogAction": {"type": "ConfirmIntent"},"intent": {'name':intent,'slots': slots}},"messages": [{"contentType": "PlainText","content": "Would you like to know the number of calories in "+food_name}]}
    if event["invocationSource"] == "FulfillmentCodeHook":
        response = {"sessionState": {"dialogAction": {"type": "Close"},"intent": {'name':intent,'slots': slots,"state": "Fulfilled"}},
        "messages": [{"contentType": "PlainText","content": food_name+" has "+calorie_count +" calories in 100g. "}, {"contentType": "PlainText","content": "Thank you!"}]}
    return response