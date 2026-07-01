from numula.nscore import *

def expand(pattern, reps):
    phase = 'prefix'
    prefix = ''
    middle = ''
    suffix = ''
    for c in pattern:
        match c:
            case '0' | '1' | '2':
                if phase == 'prefix':
                    prefix += c
                elif phase == 'pattern':
                    middle += c
                else:
                    suffix += c
            case '[':
                if phase == 'prefix':
                    phase = 'pattern'
                else:
                    raise exception('bad pattern')
            case ']':
                if phase == 'pattern':
                    phase = 'suffix'
                else:
                    raise exception('bad pattern')
            case _:
                raise exception('bad pattern')
    out = prefix
    for i in range(reps):
        out += middle
    out += suffix
    print('prefix', prefix)
    return out

class ScoreOrnament(ScoreBasic):
    def ornament(
        self, pattern:str, pitch:list[int], reps:int, before:bool,
        orn_dur:float, total_dur:float,
        tags:list[str]
    ):
        pattern = expand(pattern, reps)
        n = len(pattern)
        note_dur = orn_dur/n
        if before:
            self.cur_time -= orn_dur
        for c in pattern:
            match c:
                case '0': p = pitch[0]
                case '1': p = pitch[1]
                case '2': p = pitch[2]
            self.append_note(
                Note(
                    self.cur_time,
                    note_dur,
                    p,
                    .5,
                    tags
                )
            )
            self.advance_time(note_dur)
        if orn_dur < total_dur - epsilon:
            self.append_note(
                Note(
                    self.cur_time,
                    total_dur - orn_dur,
                    pitch[1],
                    .5
                )
            )
            self.advance_time(total_dur - orn_dur)
