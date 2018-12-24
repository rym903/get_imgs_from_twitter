# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from dotenv import load_dotenv

import datetime
import os

# from flask import current_app
from google.cloud import storage
import six
# from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest

load_dotenv()
project_id = os.getenv("PROJECT_ID")
storage_name = os.getenv("CLOUD_STORAGE_BUCKET")
allowed_extensions = os.getenv("ALLOWED_EXTENTIONS").split(" ")

def _get_storage_client():
    return storage.Client(project=project_id)


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
#    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


# [START upload_file]
def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    _check_extension(filename, allowed_extensions)
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(storage_name)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
# [END upload_file]

# [START upload_image_file]
def upload_image_file(file, filename):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = upload_file(
        file.read(),
        filename,
        file.headers.get_content_type()
    )

#    current_app.logger.info(
#        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
# [END upload_image_file]
