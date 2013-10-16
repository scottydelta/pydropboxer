#!/usr/bin/env python
import dropbox
import os
import simplejson
import zipfile
import shutil
import sys
from StringIO import StringIO
from fractions import Fraction
# Get your app key and secret from the Dropbox developer website
client = dropbox.client.DropboxClient("bMYLQowOQj8AAAAAAAAAAaqrTJzf8CGrGcDpf-OSZSfWnyX-cKlaSm3JadceWfD9")

uploadlist=[]
for i in range (1,len(sys.argv)):
  uploadlist.append(sys.argv[i])
for elem in uploadlist:
  if os.path.isdir(elem):
    zip = zipfile.ZipFile(elem+".zip", 'w')
    for root, dirs, files in os.walk(elem):
      for file in files:
        zip.write(os.path.join(root, file))
    zip.close()
    shutil.rmtree(elem)
    size = os.path.getsize(elem+'.zip')
    file_obj = open(elem+'.zip', 'r+')
    offset = 0
    upload_id = None
    chunk_size = 1024*100
    first_block = file_obj.read(chunk_size)
    current_block = first_block
    while True:
      if current_block:
        try:
          offset, upload_id = client.upload_chunk( StringIO(current_block), chunk_size, offset, upload_id )
          upload_percent = 100 * float(offset)/float(size)
          #upload_percent = int(float(Fraction(offset,size))*100)
          print str(int(upload_percent)) + "% uploaded"  
          current_block = file_obj.read(chunk_size)
        except Exception as e:
          print e
      else:
       path = "/commit_chunked_upload/%s%s" % ( client.session.root, '/'+ elem.split('/')[-1]+'.zip' )
       params = dict( overwrite = False, upload_id = upload_id )
       url, params, headers = client.request( path, params, content_server=True )
       print client.rest_client.POST( url, params, headers )
       print "upload complete"
       break

