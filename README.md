pydropboxer
===========

Scripts to upload large files to drobpox using its python SDK

The script uploader_noprogress.py makes use of Dropbox's python SDK's inbuilt function "upload_chunked()" to upload files which doesnt give upload progess.

The upload progess can be get by making chunks of files and then uploading the chunks and then commiting them on the dropbox server.
Uploading the first chunk generates an uploadId and rest of chunks should be uploaded with that uploadId. After all the chunks are uploaded, compose the file using the upload Id. 
