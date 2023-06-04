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

    if out.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = out.text
        print('Message : {}'.format(text))
    else:
        print('It failed . Try again')

useMic

