"""
    Animal TV Add-on
    Developed by mhancoc7
    https://patreon.m7kodi.dev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import xbmcplugin
import resources.lib.modules.common as common

mode = common.AnimalTV().plugin_queries['mode']

if mode == "main":
    common.patreon_notify()
    common.stream_list()

else:
    common.play_stream(mode)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
