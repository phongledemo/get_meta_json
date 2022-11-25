password = "WindyLe78201330@"
username = "phonghle@cisco.com"
DNAC_Shockwave_Solution = "https://wiki.cisco.com/display/EDPEIXOT/DNAC+Shockwave+Solution+Sanity+Reports"
DNAC_Guardian_Solution = "https://wiki.cisco.com/display/EDPEIXOT/DNAC+Guardian+Solution+Sanity+Reports"

#login
login_button_id = 'login-button'
trust_browser_button_id = 'trust-browser-button'
userInput_id = 'userInput'
passwordInput_id = 'passwordInput'

#Get_link
tbody_xpath = '//*[@id="main-content"]/div[2]/table/tbody'
metajson_xpath = "//a[text() = 'meta.json']"
button_download_metajson_xpath = "//button[@type='submit' and @class='btn btn-primary']"
information_metajson_xpath = "//span[@class='log-not-matched']//ancestor::div[1]"



log =  {
            "version":1,
                "root":{
                    "handlers" : ["console", "file"],
                    "level": "DEBUG"
                },
                "handlers":{
                    "console":{
                        "formatter": "console",
                        "class": "logging.StreamHandler",
                        "level": "INFO"
                    },
                    "file":{
                        "formatter":"file",
                        "class":"logging.FileHandler",
                        'encoding': 'utf8',
                        'filename': 'log/log_file.log',
                    }
                },
                "formatters":{
                    'console' : {
                        'format': '{asctime}: {levelname}:(lineno {lineno}): {message} ',
                        'style': '{',
                        'datefmt': '%Y/%m/%d %H:%M:%S'
                    },
                    'file': {
                        'format': '{asctime}: {levelname}: (lineno {lineno}): {message} ',
                        'style': '{',
                        'datefmt': 'pb_%Y_%m_%d_%H_%M_%S'
                    },
                'loggers': {
                    'custom': {
                        'handlers': ['console', 'file'],
                        'propagate': True,
                    },
                },
            }
        }