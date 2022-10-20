from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

            
def main():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    def download_file_recursively( parent_id, dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

        file_list = drive.ListFile({'q': '"{}" in parents and trashed = false'.format(parent_id)}).GetList()

        for f in file_list:
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                download_file_recursively( f['id'], os.path.join(dst_dir, f['title']))
            else:
                dst_path = os.path.join(dst_dir, f['title'])
                f.GetContentFile(dst_path)
                print('Download {} to {}'.format(f['title'], dst_path))

    # download_file_recursively( 'data', '/data')
    folder_id = drive.ListFile({'q': "title = 'data'"}).GetList()[0]['id']
    download_file_recursively( folder_id, 'data')

if __name__ == '__main__':
    main()