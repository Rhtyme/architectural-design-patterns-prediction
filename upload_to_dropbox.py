import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def main():
    access_token = 'sl.BEPsKJFfKVUH6jqXNvNHK6l-PRMNDCJKA9Q872eKGBZI2JPe0s5up8n8HMe9c7RX6HALlIj5EeEQRdE2yt73_k4IxPrsZwTtQXv0lDTzqUG_qfhtsll8IO6nFYXm5KgxLHOqC7DT9jfb'
    transferData = TransferData(access_token)

    file_from1 = 'mvp_ck.zip'
    file_from2 = 'mvvm_ck.zip'
    file_to = '/test/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'  # The full path to upload the file to, including the file name
    file_to1 = '/test/mvp_ck.zip'
    file_to2 = '/test/mvvm_ck.zip'

    # API v2
    transferData.upload_file(file_from1, file_to1)
    transferData.upload_file(file_from2, file_to2)

if __name__ == '__main__':
    main()
