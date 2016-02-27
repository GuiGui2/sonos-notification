#!/usr/bin/env python
from soco import SoCo
import gi
gi.require_version('Notify', '0.7') 
from gi.repository import Notify,GdkPixbuf
import requests
import tempfile

if __name__ == '__main__':
    sonos = SoCo('192.168.22.236')
    track = sonos.get_current_track_info()
    r = requests.get(track['album_art'])
    fp = tempfile.NamedTemporaryFile()
    cover_image = fp.write(r.content)
    # Use GdkPixbuf to create the proper image type
    image = GdkPixbuf.Pixbuf.new_from_file(fp.name)
    Notify.init("Sonos_Track")
    Sonos_Track=Notify.Notification.new("Title: {0}\nArtist: {1}".format(track['title'],track['artist']))
    Sonos_Track.set_image_from_pixbuf(image)
    Sonos_Track.show()
