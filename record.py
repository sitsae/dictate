import pyaudio
import wave
import sys  
import keyboard


if len(sys.argv) < 2:
   print(f'Writes a wave file. Usage: {sys.argv[0]} filename.wav')
   sys.exit(-1) 


def record(filename, is_recorded):
    with wave.open(f'./written/{sys.argv[1]}', 'wb') as wf:
        p = pyaudio.PyAudio()
        framerate = int(p.get_default_input_device_info().get("defaultSampleRate"))
        sampwidth = p.get_sample_size(pyaudio.paInt16)
        format = p.get_format_from_width(sampwidth)
        channels = 1
        wf.setparams((channels, sampwidth, framerate, 0, 'NONE', 'not compressed')) 
        stream = p.open(framerate, channels, format, input=True)
        print('* recording... Press enter to stop recording')

        while True:
            if keyboard.is_pressed('enter'):
                break
            data = stream.read(framerate)
            wf.writeframes(data)

        stream.close()
        p.terminate()
        is_recorded = True
        print('* done recording')


