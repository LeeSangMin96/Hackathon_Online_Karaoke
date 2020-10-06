import pyaudio # brew install portaudio, pip install pyaudio
import numpy as np
import wave, os
from datetime import datetime
from audioop import mul, add, bias
from threading import Thread


class Nore:

    def __init__(self):
        self.INPUT_INDEX = 0 # change this to microphone
        self.OUTPUT_INDEX = 3 # change this to main speaker
        self.OUTPUT_FILENAME = 'output/%s.wav' % (datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs('output', exist_ok=True)

        self.CHUNK = 512
        self.RATE = 48000
        self.SAMPLE_WIDTH = 2

        self.DELAY_INTERVAL = 15 # min : 0, max: 15 
        self.DELAY_VOLUME_DECAY = 0.6 # min:0, max:1
        self.DELAY_N = 10 # min : 0, max : 10

        self.CHECK = True
        self.thread = None

        # delay sound
        self.original_frames = []
        self.index = 0

        # main
        self.pa = pyaudio.PyAudio()

        for i in range(self.pa.get_device_count()):
            print(self.pa.get_device_info_by_index(i))

    def add_delay(self, input):

        self.original_frames.append(input)
        output = input

        if len(self.original_frames) > self.DELAY_INTERVAL:
            for n_repeat in range(self.DELAY_N):
                delay = self.original_frames[max(self.index - n_repeat * self.DELAY_INTERVAL, 0)]

                delay = mul(delay, self.SAMPLE_WIDTH, self.DELAY_VOLUME_DECAY ** (n_repeat + 1))
                output = add(output, delay, self.SAMPLE_WIDTH)

            self.index += 1

        return output

    def stop_nore(self):
        self.CHECK = False
        self.thread = None

    def start_nore(self):
        self.thread = Thread(target=self.start_stream, args=())
        self.thread.daemon = True
        self.thread.start()


    def start_stream(self):
        # open devices
        stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            frames_per_buffer=self.CHUNK,
            input=True,
            output=True,
            input_device_index=self.INPUT_INDEX,
            output_device_index=self.OUTPUT_INDEX
        )

        frames = []

        # start stream
        while stream.is_active() and self.CHECK:
            try:
                input = stream.read(self.CHUNK, exception_on_overflow=False)
                input = self.add_delay(input)

                stream.write(input)
                frames.append(input)  
            except KeyboardInterrupt:
                break
            except Exception as e:
                print('[!] Unknown error!', e)
                exit()

        # write audio as a file
        total_frames = b''.join(frames)
    
        with wave.open(self.OUTPUT_FILENAME, 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
            f.setframerate(self.RATE)
            f.writeframes(total_frames)
            
        stream.stop_stream()
        stream.close()
        self.pa.terminate()

    

# start_stream()
