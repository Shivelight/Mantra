# -*- coding: utf-8 -*-
import requests
import time


__author__ = "Arkie"
__email__ = "cwkfr@protonmail.com"
__status__ = "Development"


def ms():
    return int(round(time.time() * 1000))


class RegService(object):

    def __init__(self):
        self.sessionId = None
        self.region = None
        self.phone = None
        self.normalizedPhone = None
        self.password = None
        self.authToken = None
        self.certificate = None
        self.mid = None
        self.displayName = None
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "X-Line-Application": "CHROMEOS\t2.1.0\tChrome_OS\t1"
        }

    def register(self, phone, region):
        self.phone = phone
        self.region = region
        reg = self._startVerification()

        if "error" in reg:
            raise Exception(reg['message'])

        self.sessionId = reg['result']['sessionId']
        self.normalizedPhone = reg['result']['normalizedPhone']

        while True:
            try:
                pin = input(("Enter the verification code you "
                             "received via text message."
                             "If you didn't receive a verification code, "
                             "please try the following: [R]esend Code. "
                             "Verification Code: "))
            except EOFError:
                continue
            if pin in {"R", "r"}:
                self._resend()
                print("Verification code has been sent.")
                continue

            ver = self._verifyPhoneNumber(pin)
            if ver['verificationResult'] == "FAILED":
                print("Invalid verification code. Please try again.")
                continue
            break

        if ver['verificationResult'] == "OK_REGISTERED_WITH_ANOTHER_DEVICE":
            while True:
                try:
                    deleteAcc = input(("Phone number found on database, "
                                       "this will delete everything from that account. "
                                       "Are you sure want to continue? [Y/n]"))
                except EOFError:
                    continue
                if deleteAcc == "Y":
                    break
                elif deleteAcc == "n":
                    return
                else:
                    continue

        while True:
            try:
                password = input("Please enter your password (6-20): ")
                if 6 <= len(password) <= 20:
                    self.password = password
                    break
            except EOFError:
                continue

        while True:
            try:
                name = input("Please enter your display name (1-20): ")
                if 1 <= len(name) <= 20:
                    self.displayName = name
                    break
            except EOFError:
                continue

        rsakey = self._getRSAKey()

        createdAcc = self._create(rsakey)
        self.authToken = createdAcc['result']['authToken']
        self.certificate = createdAcc['result']['certificate']

        self._headers['X-Line-Access'] = self.authToken

        profile = self._getProfile()
        self.mid = profile['result']['mid']
        self.encryptedPhone = profile['result']['phone']
        self._setProfile()

        while True:
            try:
                email = input("Do you want to register an email? [Y/n]")
                if email in {"Y", "n"}:
                    break
            except EOFError:
                continue

        if email == "Y":
            while True:
                pass

    def _startVerification(self):
        data = {
            "deviceInfo": {
                "applicationType": self._headers['X-Line-Application'].split("\t")[0],
                "deviceName": "",
                "model": "Parallels",
                "systemName": "",
                "systemVersion": ""
            },
            "locale": "en",
            "phoneNumber": self.phone,
            "region": self.region
        }
        result = requests.post("https://w.line.me/lrs/v1/reg?t=" + ms,
                               json=data,
                               headers=self._headers)
        return result.json()

    def _resend(self):
        requests.get("https://w.line.me/lrs/v1/reg/" + self.sessionId + "/resend?t=" + ms)

    def _verifyPhoneNumber(self, pinCode):
        data = {
            "pinCode": pinCode
        }
        result = requests.post("https://w.line.me/lrs/v1/reg/" + self.sessionId + "/verify?t="+ ms,
                               json=data,
                               headers=self._headers)
        return result.json()

    def _getRSAKey(self):
        result = requests.get("https://w.line.me/lrs/v1/reg/rsaKey?_={}?t={}".format(ms),
                              headers=self._headers)
        return result.json()

    def _encryptPassword(self, rsakey):
        phone = self.normalizedPhone.replace("-", "").replace(" ", "")
        message = (chr(len(rsakey.sessionKey)) + rsakey.sessionKey
                  + chr(len(phone)) + phone
                  + chr(len(password)) + password).encode('utf-8')
        publicKey = rsa.PublicKey(int(rsakey.nvalue, 16), int(rsakey.evalue, 16))
        crypto = rsa.encrypt(message, publicKey).hex()
        return crypto

    def _create(self, rsakey):
        data = {
            "encryptedPassword": self._encryptPassword(rsakey),
            "keynm": rsakey['keynm']
        }
        result = requests.post("https://w.line.me/lrs/v1/reg/" + self.sessionId + "/create?t=" + ms,
                               json=data,
                               headers=self._headers)
        return result.json()

    def _getProfile(self):
        result = requests.get("https://w.line.me/lrs/v1/post/reg/profile?t=" + ms,
                              headers=self._headers)
        return result.json()

    def _setProfile(self):
        data = {
            "profile": {
                "mid": self.mid,
                "userid": None,
                "regionCode": "ID",
                "phone": self.encryptedPhone,
                "email": None,
                "displayName": self.displayName,
                "phoneticName": None,
                "pictureStatus": self.mid,
                "thumbnailUrl": None,
                "statusMessage": None,
                "allowSearchByUserid": True,
                "allowSearchByEmail": True,
                "picturePath": "",
                "musicProfile": None,
                "setMid": True,
                "setUserid": False,
                "setRegionCode": True,
                "setPhone": True,
                "setEmail": False,
                "setDisplayName": True,
                "setPhoneticName": False,
                "setPictureStatus": False,
                "setThumbnailUrl": False,
                "setStatusMessage": False,
                "setAllowSearchByUserid": True,
                "setAllowSearchByEmail": True,
                "setPicturePath": True,
                "setMusicProfile": False
            }
        }
        requests.put("https://w.line.me/lrs/v1/post/reg/profile?t=" + ms,
                     json=data,
                     headers=self._headers)

    def _getSettings(self):
        result = requests.get('https://w.line.me/lrs/v1/post/reg/settings?t=' + ms,
                              headers=self._headers)
        return result.json()

    def _setSettings(self):
        data = {
            "attrSet": ["PRIVACY_SEARCH_BY_PHONE_NUMBER", "PRIVACY_SEARCH_BY_USERID"],
            "settings": {
                "notificationEnable": True,
                "notificationMuteExpiration": -1,
                "notificationNewMessage": True,
                "notificationGroupInvitation": True,
                "notificationShowMessage": True,
                "notificationIncomingCall": True,
                "notificationSoundMessage": None,
                "notificationSoundGroup": None,
                "notificationDisabledWithSub": True,
                "notificationPayment": True,
                "privacySyncContacts": False,
                "privacySearchByPhoneNumber": False,
                "privacySearchByUserid": False,
                "privacySearchByEmail": False,
                "privacyAllowSecondaryDeviceLogin": True,
                "privacyProfileImagePostToMyhome": False,
                "privacyProfileMusicPostToMyhome": False,
                "privacyReceiveMessagesFromNotFriend": True,
                "privacyAgreeUseLineCoinToPaidCall": False,
                "privacyAgreeUsePaidCall": False,
                "privacyAllowFriendRequest": True,
                "privacyAllowNearby": False,
                "contactMyTicket": None,
                "identityProvider": "LINE_PHONE",
                "identityIdentifier": None,
                "snsAccounts": {},
                "phoneRegistration": True,
                "emailConfirmationStatus": "NOT_SPECIFIED",
                "accountMigrationPincodeType": "NOT_APPLICABLE",
                "enforcedInputAccountMigrationPincode": False,
                "securityCenterSettingsType": "NOT_APPLICABLE",
                "preferenceLocale": "en",
                "customModes": {},
                "e2eeEnable": False,
                "hitokotoBackupRequested": False,
                "agreementNearbyTime": -1,
                "setNotificationEnable": True,
                "setNotificationMuteExpiration": True,
                "setNotificationNewMessage": True,
                "setNotificationGroupInvitation": True,
                "setNotificationShowMessage": True,
                "setNotificationIncomingCall": True,
                "setNotificationSoundMessage": False,
                "setNotificationSoundGroup": False,
                "setNotificationDisabledWithSub": True,
                "setNotificationPayment": True,
                "setPrivacySyncContacts": True,
                "setPrivacySearchByPhoneNumber": True,
                "setPrivacySearchByUserid": True,
                "setPrivacySearchByEmail": True,
                "setPrivacyAllowSecondaryDeviceLogin": True,
                "setPrivacyProfileImagePostToMyhome": True,
                "setPrivacyProfileMusicPostToMyhome": True,
                "setPrivacyReceiveMessagesFromNotFriend": True,
                "setPrivacyAgreeUseLineCoinToPaidCall": True,
                "setPrivacyAgreeUsePaidCall": True,
                "setPrivacyAllowFriendRequest": True,
                "setPrivacyAllowNearby": True,
                "setContactMyTicket": False,
                "setIdentityProvider": True,
                "setIdentityIdentifier": False,
                "snsAccountsSize": 0,
                "setSnsAccounts": True,
                "setPhoneRegistration": True,
                "setEmailConfirmationStatus": True,
                "setAccountMigrationPincodeType": True,
                "setEnforcedInputAccountMigrationPincode": True,
                "setSecurityCenterSettingsType": True,
                "setPreferenceLocale": True,
                "customModesSize": 0,
                "setCustomModes": True,
                "setE2eeEnable": True,
                "setHitokotoBackupRequested": True,
                "setAgreementNearbyTime": True
            }
        }
        requests.put("https://w.line.me/lrs/v1/post/reg/settings/attr?t=" + ms,
                     json=data,
                     headers=self._headers)
