import wave
import struct
import os
import math

def create_jump_sound():
    # Create jump sound (a short "boing" sound)
    sampleRate = 44100
    duration = 0.1
    frequency = 440

    wavef = wave.open('assets/sounds/jump.wav', 'w')
    wavef.setnchannels(1)
    wavef.setsampwidth(2)
    wavef.setframerate(sampleRate)

    for i in range(int(duration * sampleRate)):
        value = int(32767.0 * math.sin(frequency * math.pi * float(i) / float(sampleRate)))
        data = struct.pack('<h', value)
        wavef.writeframes(data)

    wavef.close()

def create_coin_sound():
    # Create coin sound (a short "ding" sound)
    sampleRate = 44100
    duration = 0.1
    frequency = 880

    wavef = wave.open('assets/sounds/coin.wav', 'w')
    wavef.setnchannels(1)
    wavef.setsampwidth(2)
    wavef.setframerate(sampleRate)

    for i in range(int(duration * sampleRate)):
        value = int(32767.0 * math.sin(frequency * math.pi * float(i) / float(sampleRate)))
        data = struct.pack('<h', value)
        wavef.writeframes(data)

    wavef.close()

if __name__ == '__main__':
    # Create assets directory if it doesn't exist
    os.makedirs('assets/sounds', exist_ok=True)
    
    # Create sound effects
    create_jump_sound()
    create_coin_sound()
    print("Sound effects created successfully!") 