import requests
from requests_toolbelt import MultipartEncoder
import json

class Bot:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v2.6/me/messages?access_token={0}".format(access_token)

    def send_text_message(self, recipient_id, message):
        payload = {'recipient': {'id': recipient_id},
                   'message': {'text': message}
                  }
        result = requests.post(self.base_url, json=payload)
        return result.json()
 
    def send_message(self, recipient_id, message):
        payload ={'recipient': {'id': recipient_id},
                  'message': message
                 }
        return requests.post(self.base_url, json=payload).json()

    def send_generic_message(self, recipient_id, elements):
        payload = {'recipient': {'id': recipient_id},
                   'message': { "attachment": {
                                "type": "template",
                                "payload": {
                                    "template_type": "generic",
                                    "elements": elements
                                    }
                                }
                              }
                   }
        return requests.post(self.base_url, json=payload).json()

    def send_image(self, recipient_id, image_path):
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {                
                    'attachment': {
                        'type': 'image',
                        'payload': {}
                    }
                }
            ),
            'filedata': (image_path, open(image_path, 'rb'))
        }
        multipart_data = MultipartEncoder(payload)
        multipart_header = {'Content-Type': multipart_data.content_type}
        return requests.post(self.base_url, data=multipart_data, headers=multipart_header)
