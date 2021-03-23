"""
    Animal TV Add-on
    Developed by mhancoc7

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

import os
import sys
import time
import pickle
import xbmcvfs
import xbmcgui
import xbmcaddon
import m7lib

try:
    # Python 3
    from urllib.parse import parse_qs
except ImportError:
    # Python 2
    from urlparse import parse_qs

dlg = xbmcgui.Dialog()
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
data_path = xbmcvfs.translatePath(xbmcaddon.Addon(id=addon_id).getAddonInfo('profile'))
patreon_logo = xbmcvfs.translatePath(os.path.join(plugin_path, 'resources', 'images', 'patreon.jpg'))
icon = xbmcvfs.translatePath(os.path.join(plugin_path, 'icon.png'))
fanart = xbmcvfs.translatePath(os.path.join(plugin_path, 'icon.png'))

class AnimalTV:
    def __init__(self):
        self.plugin_queries = parse_query(sys.argv[2][1:])


def dlg_oops(heading):
    dlg.ok(heading, get_string(9005))
    exit()


def patreon_notify():
    # Display Patreon Reminder
    if len(get_setting('patreon_notify')) > 0:
        set_setting('patreon_notify', str(int(get_setting('patreon_notify')) + 1))
    else:
        set_setting('patreon_notify', "1")
    if int(get_setting('patreon_notify')) == 1:
        dlg.notification(get_string(9004), get_string(9003), patreon_logo, 5000, False)
    elif int(get_setting('patreon_notify')) == 5:
        set_setting('patreon_notify', "0")


def stream_list():
    try:
        fname = data_path + "/streams.cache"
        if os.path.exists(fname) and os.stat(fname).st_mtime > time.time() - 1200:
            with open(fname,'rb') as f:
                streams = pickle.load(f)
        else:
            streams = sorted(m7lib.Stream.get_explore_org_streams(), key=lambda x: x['title'])
            with open(fname,'wb') as f:
                pickle.dump(streams,f)

        m7lib.Common.add_streams(streams)

    except SyntaxError:
        dlg_oops(addon_name)


def play_stream(video_id):
    try:
        stream_url = m7lib.Common.get_playable_youtube_url(video_id)
        m7lib.Common.play(stream_url)
    except SyntaxError:
        dlg_oops(addon_name)


def get_setting(setting):
    return addon.getSetting(setting)


def set_setting(setting, string):
    return addon.setSetting(setting, string)


def get_string(string_id):
    return addon.getLocalizedString(string_id)

def parse_query(query, clean=True):
    queries = parse_qs(query)

    q = {}
    for key, value in queries.items():
        q[key] = value[0]
    if clean:
        q['mode'] = q.get('mode', 'main')
    return q

