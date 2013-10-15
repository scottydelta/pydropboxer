#!/usr/bin/env python
import dropbox
from StringIO import StringIO
# Get your app key and secret from the Dropbox developer website
client = dropbox.client.DropboxClient("bMYLQowOQj8AAAAAAAAAAaqrTJzf8CGrGcDpf-OSZSfWnyX-cKlaSm3JadceWfD9")
file_obj = open('../tumblr_ltxqyu54r41qk5i64o1.mp3', 'r+')
offset = 0
upload_id = None
chunk_size = 1024*1024
first_block = file_obj.read(chunk_size)
while True:
  if first_block:
    try:
      offset, upload_id = client.upload_chunk( StringIO(first_block), chunk_size, offset, upload_id )
      print offset, upload_id
      first_block = file_obj.read(chunk_size)
    except Exception as e:
      print e
  else:
    print "upload complete"
    break
