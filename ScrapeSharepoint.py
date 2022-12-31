# https://github.com/vgrem/Office365-REST-Python-Client/blob/master/examples/sharepoint/files/list_files.py
# https://stackoverflow.com/questions/63693398/accessing-office365-sharepoint-rest-endpoints-using-python-office365-sharepoint
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
#from office365.sharepoint.listitems.listitem import ListItem
#from tests import test_client_credentials, test_team_site_url
#from office365.runtime.auth.client_credential import ClientCredential
#from configparser import BasicInterpolation, ConfigParser
#import os

def print_file(f):
    """
    :type f: File
    """
    print(f.properties['ServerRelativeUrl'])

def enum_folder(parent_folder, fn):
    """
    :type parent_folder: Folder
    :type fn: (File)-> None
    """
    parent_folder.expand(["Files", "Folders"]).get().execute_query()
    for file in parent_folder.files:  # type: File
        fn(file)
    for folder in parent_folder.folders:  # type: Folder
        enum_folder(folder, fn)

username = "cmoler@comact.com"
password = "Woophee7"
credentials = UserCredential(username, password)
test_team_site_url = 'https://comact2.sharepoint.com/sites/Project-21-1195'

ctx = ClientContext(test_team_site_url).with_credentials(credentials)
target_folder_url = "Shared Documents"
root_folder = ctx.web.get_folder_by_server_relative_path(target_folder_url)
enum_folder(root_folder, print_file)
