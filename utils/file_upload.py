from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests


def get_best_upload_server():
    response = requests.get('https://apiv2.gofile.io/getServer')
    data = response.json()
    server = data['data']['server']

    return server


def upload_file(filepath):
    server = get_best_upload_server()
    mp_encoder = MultipartEncoder(
        fields={
            'file': (filepath, open(filepath, 'rb'))
        }
    )
    r = requests.post(
        f'https://{server}.gofile.io/uploadFile',
        data=mp_encoder,
        headers={'Content-Type': mp_encoder.content_type}
    )
    print(r)
    scrap = r.json()
    Token = scrap['data']['code']

    file_url = f'https://gofile.io/?c={Token}'

    print(f'[INFO] File Uploaded : {file_url}')

    return file_url
