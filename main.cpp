#include "MidiFile.h"
#include "Options.h"
#include <iostream>
#include <iomanip>
#include <cstdlib>
#include "RtMidi.h"
#include<Windows.h>

using namespace std;
using namespace smf;

int main(int argc, char** argv) {
    std::vector<MidiEvent *> noteOnEvent;
    MidiFile midifile("C:\\Users\\wangr\\training\\Midi_K525.mid");

    midifile.doTimeAnalysis();
    midifile.linkNotePairs();
    midifile.joinTracks();
    int tracks = midifile.getTrackCount();
    cout << "TPQ: " << midifile.getTicksPerQuarterNote() << endl;
    if (tracks > 1) cout << "TRACKS: " << tracks << endl;
    for (int track = 0; track < tracks; track++) {
        if (tracks > 1) cout << "\nTrack " << track << endl;
        cout << "Tick\tSeconds\tDur\tMessage" << endl;
        for (int event = 0; event < midifile[track].size(); event++) {
            cout << dec << midifile[track][event].tick;
            cout << '\t' << dec << midifile[track][event].seconds;
            cout << '\t';
            if (midifile[track][event].isNoteOn())
                cout << midifile[track][event].getDurationInSeconds();
            cout << '\t' << hex;
            for (int i = 0; i < midifile[track][event].size(); i++)
                cout << int(midifile[track][event][i]) << ' ';
            cout << endl;
        }
    }

    RtMidiOut* midiout = new RtMidiOut();
    // Check available ports.
    unsigned int nPorts = midiout->getPortCount();
    if (nPorts == 0) {
        std::cout << "No ports available!\n";
    }
    // Open first available port.
    midiout->openPort(0);
    // set tempo with change 500
    double tickDurationMilseconds = double(500) / double(480);
    for (int track = 0; track < tracks; track++) {
        for (int event = 0; event < midifile[track].size(); event++) {
            if (midifile[track][event].isNoteOn()) {
                noteOnEvent.push_back(&midifile[track][event]);
            }
        }
    }

    for (int event = 1; event < noteOnEvent.size(); event++) {
        midiout->sendMessage(noteOnEvent[event-1]);
        int tickDuration = noteOnEvent[event]->tick - noteOnEvent[event-1]->tick;
        //int secDuration = int(noteOnEvent[event + 1]->seconds - noteOnEvent[event]->seconds);
        if (tickDuration) {
            //Sleep(secDuration);
            Sleep(int(tickDuration * tickDurationMilseconds));
        }
    }
    delete midiout;
    return 0;
}


