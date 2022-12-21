password = ""
username = ""
Wiki_Cisco_Page = "https://wiki.cisco.com/"
try_again_loading = 2


#login
login_button_id = 'login-button'
trust_browser_button_id = 'trust-browser-button'
userInput_id = 'userInput'
passwordInput_id = 'passwordInput'
verify_code_xpath = "//div[@class='row display-flex align-flex-justify-content-center verification-code']"

#Get_link
big_table = '//*[@id="page"]'
three_tbody_xpath = '//*[@id="main-content"]/div[2]/table/tbody'
tbody_xpath = '//div[@class="table-wrap"]/table/tbody'
metajson_xpath = "//a[text() = 'meta.json']"
button_download_metajson_xpath = "//button[@type='submit' and @class='btn btn-primary']"
information_metajson_xpath = "//span[@class='log-not-matched']//ancestor::div[1]"

#Database
database = 'mongodb+srv://triton01:root@cluster00.5hulm.mongodb.net/?retryWrites=true&w=majority'



#Logger
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
                        # 'filename': 'log/log_file.log',
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
                        'datefmt': 'log_%Y_%m_%d_%H_%M_%S'
                    },
                'loggers': {
                    'custom': {
                        'handlers': ['console', 'file'],
                        'propagate': True,
                    },
                },
            }
        }



#Product
Product = {}

#Status
Process_status = ""
