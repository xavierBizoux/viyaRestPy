import sys
import os
import json

def getBaseUrl():
    configFile = os.path.join(os.path.expanduser('~'), '.sas', 'config.json')
    try:
        with open(configFile) as json_file:
            if os.stat(configFile).st_size == 0:
                raise EOFError
            else:
                data = json.load(json_file)
    except OSError as err:
        print(err)
        sys.exit()
    except EOFError:
        print("File {0:s} is empty.".format(configFile))
        sys.exit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit()
        # check that information is in profile
    curProfile = os.environ.get("SAS_CLI_PROFILE", "Default")
    if curProfile in data:
        baseUrl = data[curProfile]['sas-endpoint']
        return baseUrl
    else:
        print(
            "ERROR: profile {0:s} does not exist. Recreate profile with sas-admin profile init.".format(curProfile))
        sys.exit()