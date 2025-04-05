# This file is part of Numula
# Copyright (C) 2022 David P. Anderson
#
# Numula is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Numula is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Numula.  If not, see <http://www.gnu.org/licenses/>.

import numula_path
import comp.colorednoise as cn

# 1/f noise
# see https://github.com/felixpatzelt/colorednoise

def cn_test():
    beta = 2
    samples = 100
    y = cn.powerlaw_psd_gaussian(beta, samples)
    for i in range(100):
        print(y[i])
        
cn_test()
