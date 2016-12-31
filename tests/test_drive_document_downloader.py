from projectile.downloader import DriveDocumentDownloader


def create(drive, path):
    return DriveDocumentDownloader(
        drive,
        '0B40zKDFmo_14d3B3WDJDclJtcGs',
        path,
    )


def test_init(document_folder, drive):
    create(drive, document_folder) 


def test_download_documents(document_folder, drive):
    d = create(drive, document_folder) 
    d.download_documents()

    assert d.get_document_fnames()
