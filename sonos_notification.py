#!/usr/bin/env python
from __future__ import print_function
try:
    from queue import Empty
except:  # Py2.7
    from Queue import Empty
from soco.events import event_listener
from soco import SoCo
import gi
gi.require_version('Notify', '0.7') 
from gi.repository import Notify,GdkPixbuf
import requests
from pprint import pprint
import tempfile

if __name__ == '__main__':
    sonos = SoCo('192.168.22.236')
    sub = sonos.avTransport.subscribe()
    while True:
        try:
            event = sub.events.get(timeout=0.5)
            track = sonos.get_current_track_info()
            pprint(track)
            r = requests.get(track['album_art'])
            fp = tempfile.NamedTemporaryFile()
            cover_image = fp.write(r.content)
            # Use GdkPixbuf to create the proper image type
            image = GdkPixbuf.Pixbuf.new_from_file(fp.name)
            Notify.init("Sonos_Track")
            Sonos_Track=Notify.Notification.new("Title: {0}\nArtist: {1}\nAlbum: {2}".format(track['title'],track['artist'],track['album']))
            Sonos_Track.set_image_from_pixbuf(image)
            Sonos_Track.show()
        except Empty:
            pass
        except KeyboardInterrupt:
            sub.unsubscribe()
            event_listener.stop()
            break
