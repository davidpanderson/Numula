from numula.nscore import *

def expand(pattern, reps):
    phase = 'prefix'
    prefix = ''
    pattern = ''
    suffix = ''
    for c in pattern:
        match c:
            case '0' | '+' | '-':
                if phase == 'prefix':
                    prefix += c
                elif phase == 'pattern':
                    pattern += c
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
        out += pattern
    out += suffix
    return out

class ScoreOrnament(ScoreBasic):
    def ornament(
        self, pattern:str, pitch:list[int], reps:int, before:bool,
        tags:list[str]
    ):
        pattern = expand(pattern, reps)
