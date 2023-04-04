import os
from apis.utils.custom_storage import MediaStorage


class S3BucketService:

    def upload_file(self, file, file_path, file_name):
        file_path_within_bucket = os.path.join(file_path, file_name)
        media_storage = MediaStorage()
        media_storage.save(file_path_within_bucket, file)
        file_url = media_storage.url(file_path_within_bucket)
        return file_url
