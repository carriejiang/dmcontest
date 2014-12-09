import boto
import sys, os
from boto.s3.key import Key

LOCAL_PATH = './data/'
AWS_ACCESS_KEY_ID = 'AKIAJRH3ENYNNHX5LW3Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_BUCKET_NAME = 'isc.research'

# connect to the bucket
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(AWS_BUCKET_NAME)

def download():
    # go through the list of files
    bucket_list = bucket.list()
    
    for l in bucket_list:
        key_string = str(l.key)
        if 'dmcontest' not in key_string:
            continue
        
        folder, name = key_string.split("/")
        print "Checking for file: %s" % name
        if not os.path.exists(LOCAL_PATH+name):
            print "Downloading %s" % name
            l.get_contents_to_filename(LOCAL_PATH+name)
    


if __name__ == "__main__":
    download()