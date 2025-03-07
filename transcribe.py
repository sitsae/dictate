# import json
import requests
import time
from record import record 
import keyboard
import sys

# is_recorded = False
# print('Press enter to start recording')
# keyboard.wait('enter')
# print('Recording...')
# main.record(sys.argv[1], is_recorded)
# print('Recording finished')

api_key="38845894-0330-4d19-9a5b-ad87c6893b7b"

upload_url = "https://api.gladia.io/v2/upload"
transcribe_url = "https://api.gladia.io/v2/pre-recorded"

headers = {
    "x-gladia-key": api_key
}

files = {
    "audio": (f"{sys.argv[1]}", open(f"written/{sys.argv[1]}", "rb"), "audio/wav"),
}

upload_response = requests.post(upload_url, headers=headers, files=files)


response_json = upload_response.json()

audio_url = response_json["audio_url"]
audio_id = response_json["audio_metadata"]["id"]
# print (response_json)
print(audio_url)

params = {
  "audio_url": audio_url,
  "detect_language": False,
  "language": "no",
  "sentences": True,   
}

transcribe_headers = {
    "x-gladia-key": api_key,
    "Content-Type": "application/json"
}
transcribe_response = requests.post(transcribe_url, json=params, headers=transcribe_headers)
# print(transcribe_response.text)

transcribe_response_json = transcribe_response.json()
result_url = transcribe_response_json["result_url"]
print(result_url)

result_response = requests.get(result_url, headers=headers)
# print(result_response.text)
status = result_response.json()["status"]
print("transcribing...")

while status != "done":
    print("Waiting for transcription to finish...")
    time.sleep(5)

    result_response = requests.get(result_url, headers=headers)
    status = result_response.json()["status"]

    print(status)

result_response_json = result_response.json()
transcription = result_response_json["result"]["transcription"]
# print(transcription)

transcription_lst = []
for utterance in transcription["utterances"]:
    # print(utterance["text"])
    transcription_lst.append(utterance["text"])

transcription_text = " ".join(transcription_lst)
print(transcription_text)


