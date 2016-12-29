import os
import json
import io

from apiclient.http import MediaFileUpload, MediaIoBaseDownload

from .google import Google, request

__all__ = ('DriveFilesNotFound', 'Drive',)


class DriveFilesNotFound(FileNotFoundError): pass


class Drive(Google):
    def __init__(self, api_key_path, credentials_path, scopes, app_name):
        super().__init__(api_key_path, credentials_path, scopes, app_name, api_name='drive', api_version='v3')


    @request
    def create_folder(self, name, parents, service):
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': parents,
        }
        folder = service.files().create(
            body=metadata,
            fields='id'
        ).execute()

        return folder.get('id')


    @request
    def share_file(self, file_id, mail, service, writer=True):
        user_permission = {
            'type': 'user',
            'role': 'writer' if writer else 'reader',
            'emailAddress': mail,
        }
        service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ).execute()


    @request
    def upload_file(self, folder_id, fname, path, mimetype, service):
        file_metadata = {
            'name': fname,
            'parents': [folder_id]
        }

        media = MediaFileUpload(
            path,
            mimetype=mimetype,
            resumable=True
        )

        f = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()


    @request
    def download_file(self, file_id, save_path, service):
        fh = io.BytesIO()
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()

        with open(save_path, 'wb') as f:
            f.write(fh.getvalue())


    @request
    def list_files(self, query, service):
        resp = service.files().list(
            q=query,
            fields='files(id, name, parents, modifiedTime)',
        ).execute()

        if not resp.get('files', []):
            raise DriveFilesNotFound("Aucun fichier sur le Drive.")

        return resp.get('files', [])
