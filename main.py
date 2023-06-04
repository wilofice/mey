import os
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

useMic()

