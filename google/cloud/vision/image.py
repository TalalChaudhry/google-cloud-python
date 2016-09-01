# Copyright 2016 Google Inc. All rights reserved.
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

"""Image represented by either a URI or byte stream."""


from base64 import b64encode

from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode
from google.cloud.vision.face import Face
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes


class Image(object):
    """Image representation containing information to be annotate.

    :type image_source: str
    :param image_source: A string which can a Google Cloud Storage URI, or
                         a byte stream of the image.

    :type client: :class:`Client`
    :param client: Instance of Vision client.
    """

    def __init__(self, image_source, client):
        self.client = client
        self._content = None
        self._source = None

        if _bytes_to_unicode(image_source).startswith('gs://'):
            self._source = image_source
        else:
            self._content = b64encode(_to_bytes(image_source))

    def as_dict(self):
        """Generate dictionary structure for request.

        :rtype: dict
        :returns: Dictionary with source information for image.
        """
        if self.content:
            return {
                'content': self.content
            }
        else:
            return {
                'source': {
                    'gcs_image_uri': self.source
                }
            }

    @property
    def content(self):
        """Base64 encoded image content.

        :rtype: str
        :returns: Base64 encoded image bytes.
        """
        return self._content

    @property
    def source(self):
        """Google Cloud Storage URI.

        :rtype: str
        :returns: String of Google Cloud Storage URI.
        """
        return self._source

    def detect_faces(self, limit=10):
        """Detect faces in image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of :class:`gcloud.vision.face.Face`.
        """
        faces = []
        face_detection_feature = Feature(FeatureTypes.FACE_DETECTION, limit)
        result = self.client.annotate(self, [face_detection_feature])
        for face_response in result['faceAnnotations']:
            face = Face.from_api_repr(face_response)
            faces.append(face)

        return faces
