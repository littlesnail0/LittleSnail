from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '10544044'
API_KEY = 'BQBg3oGPnrFrAulmsDazTPpL'
SECRET_KEY = '87b82d43edaed4be69fc4bed803f0feb'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


result = client.asr(get_file_content('test.mp3'), 'wav', 8000, {
    'lan': 'zh',
})

print(result)
