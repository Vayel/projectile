import os

from projectile.uploader import DriveDocumentUploader


def create(drive, path):
    return DriveDocumentUploader(
        'Test DriveDocumentUploader',
        'validated',
        drive,
        path,
    )


def test_init(document_folder, drive):
    create(drive, document_folder)


def test_create_folder(document_folder, drive):
    u = create(drive, document_folder)

    open(u.get_document_path('file1'), 'w').close()
    open(u.get_document_path('file2'), 'w').close()

    u.create_folder()


def test_share_folder(document_folder, drive):
    u = create(drive, document_folder)
    u.create_folder()
    u.share_folder(os.environ['TEST_DRIVE_SHARED_TO_MAIL'])
