import time

tones = {
    "0":0,
    'C0':16,'C#0':17,'D0':18,'D#0':19,'E0':21,'F0':22,'F#0':23,'G0':24,'G#0':26,'A0':28,'A#0':29,'B0':31,
    'C1':33,'C#1':35,'D1':37,'D#1':39,'E1':41,'F1':44,'F#1':46,'G1':49,'G#1':52,'A1':55,'A#1':58,'B1':62,
    'C2':65,'C#2':69,'D2':73,'D#2':78,'E2':82,'F2':87,'F#2':92,'G2':98,'G#2':104,'A2':110,'A#2':117,'B2':123,
    'C3':131,'C#3':139,'D3':147,'D#3':156,'E3':165,'F3':175,'F#3':185,'G3':196,'G#3':208,'A3':220,'A#3':233,'B3':247,
    'C4':262,'C#4':277,'D4':294,'D#4':311,'E4':330,'F4':349,'F#4':370,'G4':392,'G#4':415,'A4':440,'A#4':466,'B4':494,
    'C5':523,'C#5':554,'D5':587,'D#5':622,'E5':659,'F5':698,'F#5':740,'G5':784,'G#5':831,'A5':880,'A#5':932,'B5':988,
    'C6':1047,'C#6':1109,'D6':1175,'D#6':1245,'E6':1319,'F6':1397,'F#6':1480,'G6':1568,'G#6':1661,'A6':1760,'A#6':1865,'B6':1976,
    'C7':2093,'C#7':2217,'D7':2349,'D#7':2489,'E7':2637,'F7':2794,'F#7':2960,'G7':3136,'G#7':3322,'A7':3520,'A#7':3729,'B7':3951,
    'C8':4186,'C#8':4435,'D8':4699,'D#8':4978,'E8':5274,'F8':5588,'F#8':5920,'G8':6272,'G#8':6645,'A8':7040,'A#8':7459,'B8':7902,
    'C9':8372,'C#9':8870,'D9':9397,'D#9':9956,'E9':10548,'F9':11175,'F#9':11840,'G9':12544,'G#9':13290,'A9':14080,'A#9':14917,'B9':15804
}
song = [
    ("E5", 2), ("G4", 2), ("D5", 1.5), ("G4", 2),
    ("C5", 1.5), ("G4", 1), ("A4", 1), ("B4", 1), ("C5", 1), ("D5", 1), ("E5", 1), ("C5", 1),
    ("F5", 2), ("A4", 2), ("E5", 1.5), ("A4", 2),
    ("D5", 1.5), ("G4", 1), ("A4", 1), ("D5", 1), ("C5", 1), ("B4", 1), ("A4", 1), ("G4", 1)
]
def buzz_intro(ref):
    print("buzz")
    buzz_on = ref["buzzer"]["on"]
    buzz_off = ref["buzzer"]["off"]
    time_step = 1/4
    for note, steps in song:
        buzz_on(tones[note])
        time.sleep(time_step * steps)
    buzz_off()
    
### EYE SONG ###########################################################################
song_eye = [
  "B4", "FS5", "E5", "D5", "0",
  "B4", "F5", "E5", "D5", "0",
  "B4", "F5", "E5", "D5", "0",
  "AS4", "B4", "CS5", "D5", "CS5", "B4", "AS4"
]
    
steps_eye = [
  4, 4, 4, 4 + 4*3, 4,
  4, 4, 4, 4 + 4*3, 4,
  4, 4, 4, 4 + 4*3, 4,
  4, 4, 4, 4, 4, 4, 4*3
]
    
def buzz_eye(ref):
    print("buzz")
    buzz_on = ref["buzzer"]["on"]
    buzz_off = ref["buzzer"]["off"]
    time_step = 0.070 #1/4
    for index in range(len(song_eye)):
        note, steps = song_eye[index], steps_eye[index]
        if note == "0":buzz_off()
        else:
            buzz_on(tones[note.replace("S", "#")])
        time.sleep(time_step * steps)
    buzz_off()

### Generic #########################################################
import asyncio
import _thread

class RTTTL:
    def __init__(self, tune):
        tune_pieces = tune.split(':')
        if len(tune_pieces) != 3:
            raise ValueError('tune should contain exactly 2 colons')
        self.tune = tune_pieces[2]
        self.tune_idx = 0
        self.parse_defaults(tune_pieces[1])

    def parse_defaults(self, defaults):
        # Example: d=4,o=5,b=140
        val = 0
        id = ' '
        for char in defaults:
            char = char.lower()
            if char.isdigit():
                val *= 10
                val += ord(char) - ord('0')
                if id == 'o':
                    self.default_octave = val
                elif id == 'd':
                    self.default_duration = val
                elif id == 'b':
                    self.bpm = val
            elif char.isalpha():
                id = char
                val = 0
        # 240000 = 60 sec/min * 4 beats/whole-note * 1000 msec/sec
        self.msec_per_whole_note = 240000.0 / self.bpm

    def next_char(self):
        if self.tune_idx < len(self.tune):
            char = self.tune[self.tune_idx]
            self.tune_idx += 1
            if char == ',':
                char = ' '
            return char
        return '|'

    def notes(self):
        """Generator which generates notes. Each note is a tuple where the
           first element is the note & octave and the second element is
           the duration (in milliseconds).
        """
        while True:
            # Skip blank characters and commas
            char = self.next_char()
            while char == ' ':
                char = self.next_char()

            # Parse duration, if present. A duration of 1 means a whole note.
            # A duration of 8 means 1/8 note.
            duration = 0
            while char.isdigit():
                duration *= 10
                duration += ord(char) - ord('0')
                char = self.next_char()
            if duration == 0:
                duration = self.default_duration

            if char == '|': # marker for end of tune
                return

            note = char.upper()
            char = self.next_char()

            # Check for sharp note
            if char == '#':
                note += '#'
                char = self.next_char()

            # Check for duration modifier before octave
            # The spec has the dot after the octave, but some places do it
            # the other way around.
            duration_multiplier = 1.0
            if char == '.':
                duration_multiplier = 1.5
                char = self.next_char()

            # Check for octave
            if char >= '4' and char <= '7':
                octave = char
                char = self.next_char()
            else:
                octave = str(self.default_octave)

            # Check for duration modifier after octave
            if char == '.':
                duration_multiplier = 1.5
                char = self.next_char()

            if note == 'P':
                identifier = "REST"
            else:
                identifier = note + octave

            msec = (self.msec_per_whole_note / duration) * duration_multiplier

            yield identifier, msec


class MusicPlayer:
    # Reference:
    # https://github.com/james1236/buzzer_music
    tones = {
        'C0':16,'C#0':17,'D0':18,'D#0':19,'E0':21,'F0':22,'F#0':23,'G0':24,'G#0':26,'A0':28,'A#0':29,'B0':31,
        'C1':33,'C#1':35,'D1':37,'D#1':39,'E1':41,'F1':44,'F#1':46,'G1':49,'G#1':52,'A1':55,'A#1':58,'B1':62,
        'C2':65,'C#2':69,'D2':73,'D#2':78,'E2':82,'F2':87,'F#2':92,'G2':98,'G#2':104,'A2':110,'A#2':117,'B2':123,
        'C3':131,'C#3':139,'D3':147,'D#3':156,'E3':165,'F3':175,'F#3':185,'G3':196,'G#3':208,'A3':220,'A#3':233,'B3':247,
        'C4':262,'C#4':277,'D4':294,'D#4':311,'E4':330,'F4':349,'F#4':370,'G4':392,'G#4':415,'A4':440,'A#4':466,'B4':494,
        'C5':523,'C#5':554,'D5':587,'D#5':622,'E5':659,'F5':698,'F#5':740,'G5':784,'G#5':831,'A5':880,'A#5':932,'B5':988,
        'C6':1047,'C#6':1109,'D6':1175,'D#6':1245,'E6':1319,'F6':1397,'F#6':1480,'G6':1568,'G#6':1661,'A6':1760,'A#6':1865,'B6':1976,
        'C7':2093,'C#7':2217,'D7':2349,'D#7':2489,'E7':2637,'F7':2794,'F#7':2960,'G7':3136,'G#7':3322,'A7':3520,'A#7':3729,'B7':3951,
        'C8':4186,'C#8':4435,'D8':4699,'D#8':4978,'E8':5274,'F8':5588,'F#8':5920,'G8':6272,'G#8':6645,'A8':7040,'A#8':7459,'B8':7902,
        'C9':8372,'C#9':8870,'D9':9397,'D#9':9956,'E9':10548,'F9':11175,'F#9':11840,'G9':12544,'G#9':13290,'A9':14080,'A#9':14917,'B9':15804
    }

    def __init__(self, buzzer_on, buzzer_off, tone_duty=0.9):
        self.on = buzzer_on
        self.off = buzzer_off
        self.tone_duty = tone_duty
        self.playing = False
        self.loop = asyncio.new_event_loop()

    def play_music(self, music, speed=1):
        if self.playing == True:
            print("Music is already playing")
            return

        async def task(tune):
            self.playing = True
            for note, length in tune:
                on_time = round(length / speed * self.tone_duty)
                off_time = round(length / speed * (1-self.tone_duty))
                freq = self.tones.get(note, 0)

                self.on(freq=freq)
                await asyncio.sleep_ms(on_time)
                self.off()
                await asyncio.sleep_ms(off_time)

                if self.playing == False:
                    print("Interrupting music")
                    break
            self.playing = False
        task(music)
        def begin(music):
            self.loop.run_until_complete(task(music))
        _thread.start_new_thread(begin, (music,))

    def stop_music(self):
        self.playing = False
        self.loop.stop()

SuperMario = 'Super Mario - Main Theme:d=4,o=5,b=125:a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16f,16p,8c6,8a.,g,16c,a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16a#,16a,16g,2f,16p,8a.,8f.,8c,8a.,f,16g#,16f,16c,16p,8g#.,2g,8a.,8f.,8c,8a.,f,16g#,16f,8c,2c6'

def buzz_mp(ref, music_rtttl):
    print("buzz mp")
    buzz_on = ref["buzzer"]["on"]
    buzz_off = ref["buzzer"]["off"]
    music = RTTTL(music_rtttl).notes()
    mp = MusicPlayer(buzz_on, buzz_off)
    mp.play_music(music)
    
def buzz_mario(ref):
    buzz_mp(ref, SuperMario)

QZKago = ('QZKago:d=4,o=5,b=125:8c,8d,8d#,8g4,8f#4,16g4,8g#4,8d#,16d#,8d,8d#,' +
          '8f,8d#,8d,16d#,8d,8c,16b4,8c,8d,'+
          '8d#,8g#4,16g4,8g#4,8g4,16d#,16d,16d#,8d,8c,8b4,8a4,8b4,c'+
          '8c,8d,8d#,8g4,8f#4,16g4,8g#4,8d#,16d#,8d,8d#,' +
          '8f,8d#,8d,16d#,8d,16c,16c,4g,'+
          '8d#,8g#4,16g4,8g#4,8g4,16g4,16f#4,16g4,16.,16g,16f#,16g,16.,'+
          '16f,16d#,16d,16c,16d,16d#,16f,16b4,4c')
def buzz_qzkago(ref):
    buzz_mp(ref, QZKago)
    
############################################################
song_index = 0
song_total = 2
def buzz(ref):
    global song_index
    if song_index == 0:
        buzz_intro(ref)
    elif song_index == 1:
        buzz_eye(ref)
    song_index = (song_index + 1) % song_total