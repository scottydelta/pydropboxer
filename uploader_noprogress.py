import dropbox
import os
import simplejson
import zipfile
import shutil
import sys
#See Dropbox Python SDK to get the access token after the user validates, put the access token in place of "access_token" in the next line
client = dropbox.client.DropboxClient("qGFBtr0aIjQAAAAAAAAAARB2AN22R-w5h26H_eeLENozaEYmaTEbZRrMbgevFr0o")

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
    bigFile = open(elem+".zip", 'rb')
    size = os.path.getsize(elem+".zip")
    uploader = client.get_chunked_uploader(bigFile, size)
    while uploader.offset < size:
      try:
        upload = uploader.upload_chunked()
        print "chunk uploaded: " + uploader.offset
      except Exception as e:
        print e
        print "prob"
    uploader.finish(elem+".zip")
    if client.metadata(elem+".zip")['bytes'] ==size:
      os.remove(elem+".zip")
    shareUrl = client.share(elem+".zip")
    print shareUrl
  else:
    try:
      bigFile = open(elem, 'rb')
    except IOError:
      print "Could not read the File"
      continue
    size = os.path.getsize(elem)
    print size
    print client.account_info()
    uploader = client.get_chunked_uploader(bigFile, size)
    while uploader.offset < size:
      try:
        upload = uploader.upload_chunked()
        print "chunk uploaded: " + uploader.offset
      except Exception as e:
        print e
        print "prob"
    uploader.finish(elem)
    if client.metadata(elem)['bytes'] ==size:
        os.remove(elem)
    shareUrl = client.share(elem)
    print shareUrl
