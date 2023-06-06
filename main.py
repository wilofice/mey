import os
import time
from turtle import done
import azure.cognitiveservices.speech as speechsdk

subscription='aa28914fa17a430f9b65fad0bdc2e500'
region =  'eastus'


def get_speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)
    speech_config.speech_recognition_language="en-US"
    return speech_config

def get_speech_recognizer(speech_config):

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognition_result = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    return speech_recognition_result

def useMic():
    print('Talk in mic')
    sr = get_speech_recognizer(get_speech_config())

    out = sr.recognize_once_async().get()

    message = ''
    if out.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = out.text
        message = 'Message : {}'.format(text)
    elif out.reason == speechsdk.ResultReason.NoMatch:
        message = "NoMatch. Speech could not be recognized. Reason {}".format(out.no_match_details)
    elif out.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = out.cancellation_details
        mesage = "Speech Recognition has been canceled. Reason {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            mesage += "Error message: {}".format(cancellation_details.error_details)
    else:
        message = 'An unexpected error happened. Try again'

    print(message)

speech_recognizer = get_speech_recognizer(get_speech_config())
done = False

def continousSpeechRecognition():
    done = False

def closeMic(evt):
    message = 'Stoping speech recognition by closing mic on {}'.format(evt)

    speech_recognizer.stop_continuous_recognition()
    done = True

    if evt.result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = evt.result.cancellation_details
        mesage = "Speech Recognition has been canceled. Reason {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            mesage += "Error message: {}".format(cancellation_details.error_details)

    print(message)

def getRecognizedText(evt):
    #print('RECOGNIZED: {}'.format(evt))
    text = evt.result.text
    print(text)
    if text.find('kill') != -1 or text.find('exit') != -1:
        print('received stop')
        speech_recognizer.stop_continuous_recognition()
        done = True

def default_init_speech_event():
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.recognized.connect(getRecognizedText)
    speech_recognizer.session_stopped.connect(closeMic)
    speech_recognizer.canceled.connect(closeMic)
    

def init_speech_event():
    #speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(getRecognizedText)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(closeMic)
    speech_recognizer.canceled.connect(closeMic)

#default_init_speech_event()
init_speech_event()
speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(120)

print("done is True")