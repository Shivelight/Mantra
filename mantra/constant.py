# -*- coding: utf-8 -*-

OBS = {
    "JP": "obs-jp.line-apps.com",
    "SG": "obs-sg.line-apps.com",
}

LEGY = {
    "JP": "legy-jp.line.naver.jp",
    "SG": "gd2s.line.naver.jp",
}


MYHOME_PATH = "/mh"
TIMELINE_PATH = "/tl"
HOMEAPI_PATH = "/ma"
TIMELINE_AUTH_PATH = "/ta"
ALBUM_PATH = "/al"
NOTE_PATH = "/nt"
GROUP_NOTE_PATH = "/gn"
MUSIC_PATH = "/ms"
OBS_PATH = "/obs"
CDN_OBS_PATH = "/cobs"
CDN_STICKER_PATH = "/cstk"
CDN_PROFILE_PATH = "/cprf"
CDN_SHOP_PATH = "/cshp"
SCRAP_PATH = "/sc"
PUBLIC_LINE_CMS_PATH = "/plc"
PUBLIC_LINE_MYHOME_PATH = "/plm"
SECURITY_CENTER_PATH = "/sec"
CONFERENCE_PATH = "/cf"
CDN_PRIVATE_PATH = "/pcdn"
AD_SHOWCASE_PATH = "/ad"
AD_STATS_PATH = "/as"
AD_TIMELINE_PATH = "/at"
VOIP_LOG_PATH = "/vl"
OBS_API_PATH = "/oa"
TRACKING_SDK_PATH = "/tr"
SEARCH_PATH = "/sg"
B612_PATH = "/b612"
KEEP_PATH = "/kp"
SQUARE_NOTE_PATH = "/sn"
VERIFICATION_PATH = "/Q"

SERVICE = {
    "binary": {
        "AUTH": "/RS3",
        "AUTH_REGISTRATION": "/api/v3p/rs",
        "BUDDY": "/BUDDY3",
        "CALL": "/V3",
        "CHANNEL": "/CH3",
        "E3": "/E3",
        "H3": "/H3",
        "LONG_POLLING": "/P3",
        "NORMAL": "/S3",
        "NORMAL_POLLING": "/NP3",
        "NOTIFY_SLEEP": "/F3",
        "REGISTRATION": "/api/v3/TalkService.do",
        "SHOP": "/SHOP3",
        "SNS_ADAPTER": "/SA3",
    },
    "compact": {
        "AGE_CHECK": "/ACS4",
        "AGE_CHECK_REGISTRATION": "/api/v4p/acs",
        "AUTH": "/RS4",
        "AUTH_REGISTRATION": "/api/v4p/rs",
        "BAN": "/BAN4",
        "BAN_REGISTRATION": "/api/v4p/ban",
        "BEACON": "/BEACON4",
        "BUDDY": "/BUDDY4",
        "CALL": "/V4",
        "CANCEL_LONGPOLLING": "/CP4",
        "CHANNEL": "/CH4",
        "CHAT_APP": "/CAPP1",
        "COIN": "/COIN4",
        "COMPACT_MESSAGE": "/C5",
        "CONN_INFO": "/R2",
        "E4": "/E4",
        "EXTERNAL_INTERLOCK": "/EIS4",
        "EXTERNAL_PROXY": "",
        "H4": "/H4",
        "HTTP_PROXY": "",
        "LIFF": "/LIFF1",
        "LONG_POLLING": "/P4",
        "NORMAL": "/S4",
        "NORMAL_POLLING": "/NP4",
        "NOTIFY_BACKGROUND": "/B",
        "NOTIFY_SLEEP": "/F4",
        "PAY": "/PY4",
        "PERSONA": "/PS4",
        "POINT": "/POINT4",
        "REGISTRATION": "/api/v4/TalkService.do",
        "SEARCH": "/search/v1",
        "SHOP": "/SHOP4",
        "SNS_ADAPTER": "/SA4",
        "SNS_ADAPTER_REGISTRATION": "/api/v4p/sa",
        "SPOT": "/SP4",
        "SQUARE": "/SQS1",
        "SQUARE_BOT": "/BP1",
        "STICON": "/SC4",
        "TYPING": "/TS",
        "UNIFIED_SHOP": "/TSHOP4",
        "USER_BEHAVIOR_LOG": "/L1",
        "USER_INPUT": "",
        "WALLET": "/WALLET4"
    },
    "json": {
        "AUTH": "/JRS4",
        "AUTH_REGISTRATION": "/api/v4jp/rs",
        "BUDDY": "/JBUDDY4",
        "CHANNEL": "/JCH4",
        "LONG_POLLING": "/JP4",
        "NORMAL": "/JS4",
        "NOTIFY_SLEEP": "/JF4",
        "REGISTRATION": "/api/v4j/TalkService.do",
        "SHOP": "/JSHOP4"
    }
}

APP = {
    "android": {
        "UserAgent": "Line/8.7.0",
        "LineApplication": "ANDROID\t8.7.0\tAndroid OS\t7.0"
    },
    "bizandroid": {
        "UserAgent": "LAA/1070002",
        "LineApplication": "BIZANDROID\t1.7.2\tAndroid OS\t7.0"
    },
    "chrome": {
        "UserAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", # noqa
        "LineApplication": "CHROMEOS\t2.1.4\tChrome_OS\t1"
        # noqa https://chrome.google.com/webstore/detail/line/ophjlpahpchlmihnnnihgmmeilfjmjjc
    },
    "clova": {
        "UserAgent": "LCA/1.5.0 SM-A310F 7.0",
        "LineApplication": "CLOVAFRIENDS\t1.5.0\tAndroid\t7.0"
        # https://play.google.com/store/apps/details?id=com.linecorp.clova
    },
    "lite": {
        "UserAgent": "LLA/2.2.0 SM-A310F 7.0",
        "LineApplication": "ANDROIDLITE\t2.2.0\tAndroid\t7.0"
        # https://play.google.com/store/apps/details?id=com.linecorp.linelite
    },
    "ipad": {
        "UserAgent": "Line/8.5.0 iPad7,4 11.2.5",
        "LineApplication": "IOSIPAD\t8.5.0\tiPhone OS\t11.2.5"
        # https://itunes.apple.com/us/app/line/id443904275
    },
    "ios": {
        "UserAgent": "Line/8.6.1 iPhone8 11.2.5",
        "LineApplication": "IOS\t8.6.1\tiPhone OS\t11.2.5"
        # https://itunes.apple.com/us/app/line/id443904275
    },
    "mac": {
        "UserAgent": "DESKTOP:MAC:10.13.3-HIGHSIERA-x64(5.7.0)",
        "LineApplication": "DESKTOPMAC\t5.7.0\tMAC\t10.13.3-HIGHSIERA-x64"
        # https://itunes.apple.com/us/app/line/id539883307
    },
    "s40": {
        "UserAgent": "S40/2.0.11 NokiaX3-02",
        "LineApplication": "S40\t2.0.11\tS40\tNokiaX3-02"
        # https://line.me/nokia/en/
    },
    "tizen": {
        "UserAgent": "Line/1.0.3 SM-Z400F 3.0",
        "LineApplication": "TIZEN\t1.0.3\tTizen\t3.0"
        # http://www.tizenstore.com/main/getDetail.as?Id=RxyJZEqc8U
    },
    "win10": {
        "UserAgent": "DESKTOP:WIN:10.0.1709-WIN10-x64(5.5.3)",
        "LineApplication": "WIN10\t5.5.5\tWINDOWS\t10.0.1709-WIN10-x64"
        # https://www.microsoft.com/en-us/store/p/line/9wzdncrfj2g6
    },
    "windows": {
        "UserAgent": "DESKTOP:WIN:10.0.1709-WIN10-x64(5.6.0.1625)",
        "LineApplication": "DESKTOPWIN\t5.6.0.1625\tWINDOWS\t10.0.1709-WIN10-x64"
        # https://line.en.softonic.com/
    }
}

CHANNEL = {
    "LINEAT": "1417913499",
    "LINEAT_CMS": "1418234097",
}
