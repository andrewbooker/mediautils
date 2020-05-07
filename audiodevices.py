import sounddevice as sd

def UsbAudioDevices():
    usable = {}

    devs = sd.query_devices()
    for d in range(len(devs)):
        dev = devs[d]
        if "USB" in dev["name"] and dev["default_samplerate"] == 44100:
            usable[d] = dev["name"]

    return usable

