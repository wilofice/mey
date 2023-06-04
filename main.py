import os
import time
from turtle import done
import azure.cognitiveservices.speech as speechsdk

subscription='aa28914fa17a430f9b65fad0bdc2e500'
region =  'eastus'


def get_speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)
    speech_config.speech_recognition_language="fr-FR"
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

    print(message)

def init_speech_event():
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(closeMic)
    speech_recognizer.canceled.connect(closeMic)

init_speech_event()
speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(60)
