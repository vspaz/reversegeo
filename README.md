# reversegeo

 reversegeo is a cli utility that does reverse geocoding using Google API geo data.
 
 ## How-to
 
 ### Configuration
 reverse geocoding utility is configurable via config. 
 
 ```
 {
    "api": {
        "url": "https://maps.googleapis.com/maps/api/geocode/json",
        "key": "",
        "result_type": "locality"
    },
    "http": {
        "timeout": 2,
        "retries": 3,
        "delay": 0.1
    },
    "logging": {
        "log_file_name": "",
        "logdir": ""
    }
}
 ```
 
 **required params**:
 
 *api*
 
  - api.url  - google api endpoint https://maps.googleapis.com/maps/api/geocode/json
  - api.key  - key to authenticate reversegeo with google api
  - api.result_type - filter for Google API geo data
  
 **optional params**
 
 *http*
 
 - http.timeout - request timeout in seconds. default is 0.5 sec.
 - http.retries - number of requests retries if request fails default is 3.
 - http.delay - time between retries default 0.1 sec.
 
 *logging*
- logging.log_file_name - logfile where to write log messages; default stderr.
- logging.logdir - directory with log files

### Command line options


```
./reversegeo.py -h
usage: reversegeo -c cfg.json -s [source] -d [dump] -f [files]

utility to retrieve reverse geocoding data from google API.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        absolute path to config.json
  -s SOURCE [SOURCE ...], --source SOURCE [SOURCE ...]
                        absolute path to source directories
  -d DUMP, --dump DUMP  absolute path to dump directory
  -f FILES, --files FILES
                        filter csv files with a regular expression

```

**required params**

- -c, --config
```
./reversegeo.py -c reversegeo.json
``` 

**optional params**  
  
 - -v, --version - display current version and exit.
 - -s, --source - one or several directories with csv files. 
    default is reversegeo/data. utility filters all files and finds csv files.
    you can choose which files to filter by submitting a regex or file name via
    -f option. see below.
 - -f, --files, regex or exact file name. used together with -s option. default value is '*.csv'.  
 - -d, --dump - folder to dump files split by countries. default reversegeo/dump
 
 ### Installation & Use
 
 Currently it's not packaged and can be used as a command line utility only.
 it doesn't have too many external dependencies, so installation is pretty simple.
 
 pip3 install -r reversegeo/requirements/prod.txt
 tested with python3.5, but other python3 versions should work as well.
 
 **NOTE**
 You might probably wish to use some sort of virtualenv, Docker etc. for that!
 
 ### How to run
 
 ```
 ./reversegeo -c reversegeo.json
 ```
 
 the examples of data source files and dumped files can be found in data and 
 source folders respectively. 

