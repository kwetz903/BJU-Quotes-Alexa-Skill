import json
"""
Alexa Skill that Gives Quotes from people at Bob Jones University

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import os
import atexit
import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': " B.J.U. Quote",
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the B.J.U. Quotes skill. " \
                    "Who would you like me to quote?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Is there anyone you wan't me to quote specifically?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the B.J.U. Quotes skill. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def ask_for_help(intent, session):
    session_attributes = {}
    reprompt_text = "Would you like me to repeat that?"

    try:
        print("Helping . . .")
        speech_output = 'You can say tell me a B.J.U. quote, or, you can say exit... What can I help you with?'
    except Exception as e:
        print("something went wrong. " + e.message)
        print(e)
        speech_output = "I'm sorry, There was an error while proccessing your request."
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def stop(intent, session):
    session_attributes = {}
    reprompt_text = "Goodbye!"

    try:
        print("Stopping . . .")
        speech_output = 'Goodbye!'
    except Exception as e:
        print("something went wrong. " + e.message)
        print(e)
        speech_output = "I'm sorry, There was an error while proccessing your request."
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# quotes Data
data = {
    'Dr. Bob Jones Sr.': [
        "It is a sin to do less than your best.",
        "The door to the room of success swings on the hinges of opposition.",        
        'The two biggest little words in the English language are the two little words "do right."',        
        "It is one thing to know there is a God; it's another thing to know the God that is.",        
        "A man is a fool who leans on the arm of flesh when he can be supported by the arm of Omnipotence.",        
        "What you love and what you hate reveal what you are.",        
        "Jesus never taught men how to make a living; He taught men how to live.",        
        "Do not ask God to give you a light burden; ask Him to give you strong shoulders to carry a heavy burden.",        
        "It is better to die for something than to live for nothing.",        
        "A Christian does good deeds, but just doing good deeds does not make a man a Christian.",        
        "Your character is what God knows you to be; your reputation is what men think you are.",        
        "You and God make a majority in your community.",        
        "It is never right to do wrong in order to get a chance to do right.",        
        "Jesus said that He would be in the midst of two or three gathered in His name, but this does not mean that our Lord does not like to have a larger crowd.",        
        "It is no disgrace to fail; it is a disgrace to do less than your best to keep from failing.",        
        'The religions of the world say, "do and live." The religion of the Bible says, "live and do."',        
        "God will not do for you what He has given you strength to do for yourself.",        
        'Dying men have said, "I am sorry I have been an atheist, an infidel, an agnostic, a skeptic, or a sinner"; but no man ever said with his last breath, "I am sorry I have lived a Christian life."',        
        "The drunkard in the ditch has gone to the dogs. According to the Bible, the self-righteous man who thinks he doesn't need God has gone to the Devil.",    
    ],
    'Dr. Stephen Schaub': [
        'Put on your blast goggles.',
    ],
    'Dr. Jim Knicely': [
        "If it was easy, it wouldn't be so hard",
    ]
}

alternative_names = {
    'Dr. Bob Jones Sr.': ['doctor bob', 'doctor bob jones senior', 'bob jones', 'jones', 'bob'],
    'Dr. Stephen Schaub':  ['doctor schaub', 'doctor stephen schaub', 'stephen schaub', 'schaub', 'shaub', 'shab', 'shob', 'job'],
    'Dr. Jim Knicely': ['doctor knisely', 'doctor jim knisely', 'jim knisely', 'knisely', 'nicely']
}

no_names = [None, 'None', '', 'no', 'no one', 'no thanks', 'anyone', 'i do not care', "i don't care"]

def get_ran_arr_val(arr):
    index = random.randint(0, len(arr) - 1)
    return arr[index]

def get_speaker(person):
    """
    enables more name options
    indicates if we need to apologize for not finding the requested speaker
    """
    found_requested = True
    if person in no_names:
        return get_ran_arr_val(list(data.keys())), found_requested
    for key, arr in alternative_names.items():
        if person in arr:
            return key, found_requested
    found_requested = False
    return get_ran_arr_val(list(data.keys())), found_requested

def get_quote(intent, session):   # TODO change function name
    session_attributes = {}
    reprompt_text = "Would you like another quote?"
    try:
    # get quote
        person = None   # TODO how to get intent slot
        try:
            person = intent['slots']['person']['value']
        except Exception as e:
            print("no particular person requested")
        print("person: ", person)
        speaker, found_match = get_speaker(person)
        quote = get_ran_arr_val(data[speaker])
        quote_intro = f"{speaker} once said,"
        if not found_match:
            quote_intro = f"Sorry, we couldn't find a quote by {person}, but " + quote_intro
        speech_output = f"{quote_intro} '{quote}'"
        should_end_session = True
        
    except Exception as e:
        print("something went wrong. " + str(e))
        print(e)
        speech_output = "I'm sorry, There was an error while proccessing your request."
        should_end_session = False
        
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetNewQuoteIntent":
        return get_quote(intent, session)
    if intent_name == "AMAZON.HelpIntent":
        return ask_for_help(intent, session)
    if intent_name == "AMAZON.CancelIntent":
        return stop(intent, session)
    if intent_name == "AMAZON.StopIntent":
        return stop(intent, session)
    if intent_name == "AMAZON.FallbackIntent":
        return get_quote(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
