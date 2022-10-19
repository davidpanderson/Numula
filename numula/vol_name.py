# names for volume levels.
# For finer resolution, you can prepend _ (less) or append _ (more)
# In python, anything starting with _ isn't imported by
# from foo import * (which I think is a bad idea)
# That's why these are in a separate module.
#
pppp    = .01
pppp_   = .08
_ppp    = .16
ppp     = .23
ppp_    = .30
_pp     = .38
pp      = .45
pp_     = .52
_p      = .60
p       = .67
p_      = .74
_mp     = .82
mp      = .89
mp_     = .96
mm      = 1
_mf     = 1.04
mf      = 1.11
mf_     = 1.18
_f      = 1.26
f       = 1.33
f_      = 1.40
_ff     = 1.48
ff      = 1.55
ff_     = 1.62
_fff    = 1.68
fff     = 1.77
fff_    = 1.84
_ffff   = 1.92
ffff    = 1.99

__all__ = [
    'pppp', 'pppp_',
    '_ppp', 'ppp', 'ppp_',
    '_pp', 'pp', 'pp_',
    '_p', 'p', 'p_',
    '_mp', 'mp', 'mp_',
    'mm',
    '_mf', 'mf', 'mf_',
    '_f', 'f', 'f_',
    '_ff', 'ff', 'ff_',
    '_fff', 'fff', 'fff_',
    '_ffff', 'ffff'
]
