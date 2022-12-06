password = ""
username = ""
DNAC_Shockwave_Solution = "https://wiki.cisco.com/display/EDPEIXOT/DNAC+Shockwave+Solution+Sanity+Reports"
DNAC_Guardian_Solution = "https://wiki.cisco.com/display/EDPEIXOT/DNAC+Guardian+Solution+Sanity+Reports"
DNAC_Ghost_Solution = "https://wiki.cisco.com/display/EDPEIXOT/DNAC+Ghost+Solution+Sanity+Reports"
DNAC_Groot_Solution = "https://wiki.cisco.com/display/EDPEIXOT/DNAC+Groot+Solution+Sanity+Reports"
Wiki_Cisco_Page = "https://wiki.cisco.com/"
try_again_loading = 2


#login
login_button_id = 'login-button'
trust_browser_button_id = 'trust-browser-button'
userInput_id = 'userInput'
passwordInput_id = 'passwordInput'

#Get_link
big_table = '//div[@id="page"]'
tbody_xpath_2 = '//*[@id="main-content"]/div[2]/table/tbody'
tbody_xpath_1 = '//div[@class="table-wrap"]/table/tbody'
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
