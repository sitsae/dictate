import pyaudio
import wave
import sys  
import keyboard


def record(filename):
        with wave.open(f'./written/{filename}', 'wb') as wf:
            p = pyaudio.PyAudio()
            framerate = int(p.get_default_input_device_info().get("defaultSampleRate"))
            sampwidth = p.get_sample_size(pyaudio.paInt16)
            format = p.get_format_from_width(sampwidth)
            channels = 1
            wf.setparams((channels, sampwidth, framerate, 0, 'NONE', 'not compressed')) 
            stream = p.open(framerate, channels, format, input=True)
            chunk = 1024  # eller 2048, 4096 
            print('* recording... Press enter to stop recording')

            while True:
                if keyboard.is_pressed('enter'):
                    break
                # data = stream.read(framerate)
                data = stream.read(chunk)

                import numpy as np
                import os
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.linalg.norm(audio_data)
                print(f"Volume: {volume}")
                # Clear terminal (cross-platform)

                # ----------------------------------------

                wf.writeframes(data)

            stream.close()
            p.terminate()
            # is_recorded = True
            print('* done recording')


