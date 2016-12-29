import os
import httplib2

import apiclient
from apiclient import discovery
import oauth2client

__all__ = ('InternetConnectionError', 'Google')


class InternetConnectionError(IOError): pass


def request(func):
    def wrapper(self, *args, **kwargs):
        try:
            credentials = self.get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build(self.api_name, self.api_version, http=http)
        
            return func(self, *args, service, **kwargs)
        except (apiclient.errors.HttpError,
                httplib2.ServerNotFoundError):
            raise InternetConnectionError()

    return wrapper


class Google:
    def __init__(self, api_key_path, credentials_path, scopes, app_name, api_name='plus', api_version='v1'):
        self.api_key_path = api_key_path
        self.credentials_path = credentials_path
        self.scopes = scopes
        self.app_name = app_name
        self.api_name = api_name
        self.api_version = api_version


    def get_credentials(self):
        store = oauth2client.file.Storage(self.credentials_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(
                self.api_key_path,
                self.scopes,
            )
            flow.user_agent = self.app_name
            flags = oauth2client.tools.argparser.parse_args(args=[])
            credentials = oauth2client.tools.run_flow(flow, store, flags)

        return credentials


    @request
    def get_current_user_mail(self, service):
        person = service.people().get(userId='me').execute()
        return person["emails"][0]["value"]
