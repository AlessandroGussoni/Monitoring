from gcloud import storage

from service.service.connections.abstract import AbstractConnection


class GoogleBucket(AbstractConnection):

    def __init__(self, bucket_name, bucket_kwargs={}):

        self.bucket_name = bucket_name
        self.bucket_kwargs = bucket_kwargs

    def init(self):
        setattr(self, 'storage_client', storage.Client())
        try:
            setattr(self, 'bucket', self.storage_client.get_bucket(self.bucket_name))
        except:
            setattr(self, 'bucket', self.create_bucket(bucket_name=self.bucket_name, **self.bucket_kwargs))

    def create_bucket(self, bucket_name, **kwargs):

        bucket = self.storage_client.create_bucket(bucket_name, **kwargs)
        return bucket

    def connect_to_file(self, filename, *args, **kwargs):
        self.blob = self.bucket.blob(filename)

    def upload(self, text):
        self.blob.upload_from_string(text.read(), content_type="text/plain")

    def download(self):
        try:
            logs = self.blob.download_as_string()
            logs = logs.decode()
        except:
            logs = ""
        return logs
