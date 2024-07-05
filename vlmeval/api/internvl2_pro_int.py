from vlmeval.smp import *
from vlmeval.api.base import BaseAPI
import warnings


class InternVL2ProInt(BaseAPI):

    def __init__(self,
                 model: str = 'InternVL2-Pro',
                 retry: int = 10,
                 wait: int = 3,
                 key: str = None,
                 temperature: float = 0,
                 api_base: str = 'http://101.132.98.120:11005/chat/',
                 max_tokens: int = 1024,
                 verbose: bool = True,
                 system_prompt: str = None,
                 **kwargs):

        self.model = model
        self.api_base = api_base
        if key is not None:
            self.key = key
        else:
            self.key = os.environ.get('INTERNVL2_PRO_API_KEY', '')

        warnings.warn('InternVL2-Pro API currently does not accept `temperature` and `max_tokens` paraemters. ')

        super().__init__(retry=retry, wait=wait, verbose=verbose, system_prompt=system_prompt, **kwargs)

    def generate_inner(self, inputs, **kwargs) -> str:

        image_files = [x['value'] for x in inputs if x['type'] == 'image']
        texts = [x['value'] for x in inputs if x['type'] == 'text']

        text = texts[0] if len(texts) == 1 else '\n'.join(texts)

        files = [('files', open(file_path, 'rb')) for file_path in image_files]
        data = {
            'question': text,
            'api_key': api_key
        }
        try:
            response = requests.post(url, files=files, data=data)
            ret_code = response.status_code
            ret_code = 0 if (200 <= int(ret_code) < 300) else ret_code

            if ret_code == 0:
                return ret_code, response.json().get('response', 'No response key found in the JSON.'), response
            else:
                print('Error:', response.status_code, response.text)
                return ret_code, None, response

        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            return -1, None, None
