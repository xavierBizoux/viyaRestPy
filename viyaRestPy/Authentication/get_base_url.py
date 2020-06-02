import sys
import os
import json


def get_base_url():
    config_file = os.path.join(os.path.expanduser('~'), '.sas', 'config.json')
    try:
        with open(config_file) as json_file:
            if os.stat(configFile).st_size == 0:
                raise EOFError
            else:
                data = json.load(json_file)
    except OSError as err:
        print(err)
        sys.exit()
    except EOFError:
        print("File {0:s} is empty.".format(config_file))
        sys.exit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit()
        # check that information is in profile
    current_profile = os.environ.get("SAS_CLI_PROFILE", "Default")
    if current_profile in data:
        base_url = data[current_profile]['sas-endpoint']
        return base_url
    else:
        print(
            "ERROR: profile {0:s} does not exist. Recreate profile with sas-admin profile init.".format(current_profile))
        sys.exit()
