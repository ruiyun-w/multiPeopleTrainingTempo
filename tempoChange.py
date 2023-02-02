import os
import mido
import time
from pynput import keyboard

targetTempo = 250000
def change_tempo(filename, data_path, target_path):
    mid = mido.MidiFile(data_path + filename)
    new_mid = mido.MidiFile()
    new_mid.ticks_per_beat = mid.ticks_per_beat
    for track in mid.tracks:
        new_track = mido.MidiTrack()
        for msg in track:
            new_msg = msg.copy()
            if new_msg.type == 'set_tempo':
                new_msg.tempo = 500000
            #            if msg.type == 'note_on' or msg.type == 'note_off':
            if discretize_time:
                print(msg.time)
                new_msg.time = myround(msg.time, base=mid.ticks_per_beat / (discritezition / 4))
            #                msg.time = myround(msg.time, base=mid.ticks_per_beat/(discritezition/4) )
            if offset_time:
                #                print('first:', time)

                print((mid.ticks_per_beat / (offset / 4)))
                new_msg.time = int(msg.time + mid.ticks_per_beat / (offset))
            #                print('second:', new_time)
            #                print('diff:',time )
            #            msg.time = time
            new_track.append(new_msg)
        new_mid.tracks.append(new_track)
    new_mid.save(target_path + filename)

def inputTempo():
    targetTempo = int(input("input the target tempo:"))
    return targetTempo

def on_press(key):
    targetTempo = int(key)
    print(targetTempo)

if __name__ == '__main__':
    mid = mido.MidiFile("/Users/wang/Documents/MuseScore4/Scores/Midi_K525.mid", clip=True)
    # with keyboard.Listener(on_press=on_press) as listener:
    #     listener.join()

    for track in mid.tracks:
        for msg in track:
            if msg.type == "set_tempo":
                msg.tempo = 500000
                break;

 #  mid.save("newMidiK525.mid")

    ports = mido.get_output_names()
    print(ports)
    i = 0
    with mido.open_output(ports[0]) as outport:
        for msg in mid:
            if i < 100:
                time.sleep(msg.time)
                if not msg.is_meta:
                    print(outport, msg)
                    outport.send(msg)
            i = i + 1

    for track in mid.tracks:
        for msg in track:
            if msg.type == "set_tempo":
                msg.tempo = 250000
                break;

    with mido.open_output(ports[0]) as outport:
        for msg in mid:
            if i > 100:
                time.sleep(msg.time)
                if not msg.is_meta:
                    print(outport, msg)
                    outport.send(msg)
            i = i + 1

    for track in mid.tracks:
        for msg in track:
            if msg.type == "set_tempo":
                msg.tempo = 1000000
                break;

    with mido.open_output(ports[0]) as outport:
        for msg in mid:
            if i > 200:
                time.sleep(msg.time)
                if not msg.is_meta:
                    print(outport, msg)
                    outport.send(msg)
            i = i + 1

