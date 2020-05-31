"""A framework to take care of authentication/authorization for CLI apps
"""
import json
import os
import time
import sys
import logging

import msal
import pyqrcode


def load_json(filename, default=None):
    """Returns the default when filename is nonexistent or malformed"""
    try:
        with open(filename) as f:
            return json.load(f)
    except (IOError, ValueError):
        return default


class Auth(object):
    # This class is meant to be used with python-file CLI framework.
    # Members and properties without a leading underscore would be exposed to CLI.
    _authority = "https://login.microsoftonline.com/common"
    _client_id = ""  # Customize your client_id in sub-class
    _scopes = []  # Customize your scopes in sub-class

    _SESSION = "session.json"  # Currently, this app supports one account at a time

    def __init__(self):
        self.__session = load_json(self._SESSION, {})
        self._logger = logging.getLogger(self.__class__.__name__)

    def _device_flow(self, app):
        flow = app.initiate_device_flow(scopes=self._scopes)
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=2))
        print(pyqrcode.create(
            "https://rayluo.github.io/ds/ms?c=%s" % flow["user_code"],
            error="L").terminal(quiet_zone=2))  # Create smallest possible QR code
        print(flow["message"])
        sys.stdout.flush()  # Some terminal needs this to ensure the message is shown
        return app.acquire_token_by_device_flow(flow)  # By default it will block

    def login(self, username=None, password=None):
        """login with your account.

        Usage:

            cli login
            cli login --username johndoe --password placeholder
        """
        if not self._client_id:
            raise ValueError("Customize your client_id in sub-class")
        app = msal.PublicClientApplication(
            self._client_id, authority=self._authority)
        result = app.acquire_token_by_username_password(
            username, password, self._scopes
            ) if username and password else self._device_flow(app)
        if "error" in result:
            sys.exit("Auth Error: {}, {}".format(
                result["error"], result.get("error_description")))
        self._logger.info(
            "Welcome %s", result.get("id_token_claims", {}).get("name", ""))
        self.__session = result
        with open(self._SESSION, "w") as f:
            json.dump(self.__session, f)

    def logout(self):
        try:
            os.unlink(self._SESSION)
        except IOError:
            pass
        self._logger.info(
            "Goodbye %s",
            self.__session.get("id_token_claims", {}).get("name", ""))
        self.__session = None  # Unnecessary when working as a CLI

    def _session(self):
        """Return current logged-in user's session data.

        By calling this method, the caller effectively enforces end user login.
        """
        if not self.__session:
            sys.exit("You need to login first")
        ## TBD
        # if time.time() > self.__session.get("id_token_claims", {}).get("exp", 0):
        #     sys.exit("Session expired")
        return self.__session

    def _user_id(self):
        return self._session().get("id_token_claims", {}).get("aud")

