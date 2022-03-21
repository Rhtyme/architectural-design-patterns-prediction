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
    access_token = 'sl.BEON2PvGqETOASoSOCSDXlzkWJzfGnWvFhr_Y9Q4UK1yjE76jVkfTVvzsFZ4GA0g4Nprb2Y5yecugg7h235XanUlsyUncN7hlxxhCJx8QLrEgt0aoRSzM-MgAohGgSDZ45Re6mpL18n2'
    transferData = TransferData(access_token)

    file_from = 'ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
    file_to = '/test/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'  # The full path to upload the file to, including the file name

    # API v2
    transferData.upload_file(file_from, file_to)

if __name__ == '__main__':
    main()
