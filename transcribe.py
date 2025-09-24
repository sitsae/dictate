# import json
import requests
import time
from record import record
import keyboard
import sys
from process import process
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.environ["GLADIA_API_KEY"]

def main():
    if len(sys.argv) < 2:
            print("Usage: python transcribe.py <output_filename.wav>")
            sys.exit(1)
    print('Press enter to start recording')
    keyboard.wait('enter')
    print('Recording...')
    record(sys.argv[1])
    print('Recording finished')

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
    process(transcription_text)

if __name__ == "__main__":
    main()
