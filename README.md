# viyaRestPy

- [Introduction](#introduction)
  - [The package content](#the-package-content)
  - [Authentication](#authentication)
    - [Token based](#token-based)
    - [Password based](#password-based)
    - [Token generated by sas-admin CLI](#token-generated-by-sas-admin-cli)
  - [The usage](#the-usage)
  - [The installation](#the-installation)
  - [Writing your first code](#writing-your-first-code)
  - [Take away](#take-away)

## Introduction

With CI/CD fast approaching, the need for me to access the SAS Viya REST API's through Python code to support our team's DevOps presented itself. In this process, I've been writing multiple functions and reused those functions to avoid typing the same code again and again across different projects.
I thought it would be good if others could benefit from what I wrote to ease their REST API usage from Python. This is where my project started.
The main idea is to have a wrapper function that can be generic enough to call nearly all the existing SAS Viya REST API's and still handle the authentication process and reduce the time to write other functions dedicated for more specific tasks.

### The package content

The project contains the package in folder *viyaRestPy* and examples in the *Examples* folder. The *setup.py* is there to help install the package while still in development. The other folders contain information that relates to the build of the package.

### Authentication

For authentication, the call_rest function uses 3 different authentication techniques.

- [Introduction](#introduction)
  - [The package content](#the-package-content)
  - [Authentication](#authentication)
    - [Token based](#token-based)
    - [Password based](#password-based)
    - [Token generated by sas-admin CLI](#token-generated-by-sas-admin-cli)
  - [The usage](#the-usage)
  - [The installation](#the-installation)
  - [Writing your first code](#writing-your-first-code)
  - [Take away](#take-away)

#### Token based

Token based authentication relies on a file created by the OauthTokenGenerator in the project. It will help you create a token and store it at OS level for further usage. You should secure the generated file as it gives access to the environment. You should follow the same instructions as for the authinfo file ([Client Authentication Using an Authinfo File](https://go.documentation.sas.com/?docsetId=authinfo&docsetTarget=n0xo6z7e98y63dn1fj0g9l2j7oyq.htm&docsetVersion=9.4&locale=en#n1stv9zynsyf6rn1wbr3ejga6ozf)).
With this mechanism, you should only specify the hostname of the SAS Viya environment that was defined when using the OAuthTokenGenerator to authenticate.

#### Password based

This authentication mechanism relies on an authentication information object. This object contains the following information:

```json
{
    "user": "username",
    "pw": "password",
    "server_name": "urlToViya:port",
    "app_name": "applicationName",
    "app_secret": "applicationSecret"
}
```

In this authentication information object, the application name and the application secret are the ones that have been defined when configuring SAS Viya for REST API access. You should specify all the options in order to authenticate properly.

#### Token generated by sas-admin CLI

If the previously described authentication mechanisms are failing, the authentication will be done using the authentication information that might have been generated by the sas-admin CLI. If it was not set, the authentication will fail.

### The usage

The foundation of the viyaRestPy package is the call_rest function. This function calls the SAS Viya REST API's and takes care of the wiring needed to authenticate the user and call the needed endpoint. The call_rest function returns a response in the form of a JSON object containing: headers and json objects.

```json
{
    "headers": {},
    "json": {}
}
```

The package contains what we can call "Lego" functions that can be used for specific tasks like:

- Extracting a report based on the report name and the folder location
- Deleting a report based on the report name and the folder location
- Updating report content
- ...

These "Lego" functions are in fact calling the call_rest function multiple times for different endpoints and passing information between the different calls.
As this is a work in progress, the number of "Lego" functions is small but is expanding.

The principle is that all of the "Lego" functions are to behave as the call_rest function and return the same simple object containing a header and JSON object. Tasks like displaying results or writing information to a file should be left outside of the package. The examples are demonstrating how to read parameters from the command line and how to write output files or use input files to pass information to the "Lego" functions or the call_rest function.

### The installation

As the package is not published (yet) to a Python repository, here are the steps to install the package on your environment:

1. Open the project on <https://github.com/xavierBizoux/viyaRestPy>
1. Click on **Clone** and then on the **Copy** icon.

   ![Copy clone information](images/copyCloneLink.png)

1. Within Visual Studio Code, open the **Command palette** by pressing CTRL+SHIFT+P or under **View** menu, select **Command Palette...**.
1. In the **Command Palette**, type: *git clone* and select *Git: Clone*

    ![Launch Git clone from Command palette](images/commandPaletteGitClone.png)

1. When prompted for the *Repository URL*, paste the URL you copied from GitLab.

    ![Clone Repository](images/cloneRepository.png)

1. When asked to *Select Folder*, select the location where you want to store the code and press the **Select Repository Location**.

    ![Select Repository Location](images/selectRepositoryLocation.png)

1. When the repository is cloned to your machine, you will be asked if you want to open the cloned repository. Click on **Open**.

    ![Open cloned repository](images/saveOpenRepository.png)

1. You have now cloned the repository and you can access it from Visual Studio Code. The next step is to build the package in order to use it for your developments. You should therefore click on **Terminal** and select **New Terminal**.

    ![Open Terminal](images/openTerminal.png)

1. In the Terminal, execute the following command:

    ```bash
    py -3 -m pip install -e .
    ```

    This command will build the package in development mode and display the following information in the Terminal (if you are running on Windows):

    ```bash
    py -3 -m pip install -e .
    Obtaining file:///C:/Users/student/Documents/viyarestpy
    Requirement already satisfied: requests in c:\python38\lib\site-packages (from viyaRestPy==0.1) (2.23.0)
    Requirement already satisfied: chardet<4,>=3.0.2 in c:\python38\lib\site-packages (from requests->viyaRestPy==0.1) (3.0.4)
    Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in c:\python38\lib\site-packages (from requests->viyaRestPy==0.1) (1.25.8)
    Requirement already satisfied: idna<3,>=2.5 in c:\python38\lib\site-packages (from requests->viyaRestPy==0.1) (2.9)
    Requirement already satisfied: certifi>=2017.4.17 in c:\python38\lib\site-packages (from requests->viyaRestPy==0.1) (2020.4.5.1)
    Installing collected packages: viyaRestPy
    Attempting uninstall: viyaRestPy
        Found existing installation: viyaRestPy 0.1
        Can't uninstall 'viyaRestPy'. No files were found to uninstall.
    Running setup.py develop for viyaRestPy
    Successfully installed viyaRestPy
    ```

1. You are now ready to use the package and write your own code!

### Writing your first code

As mentioned earlier the viyaRestPy package is developed to ease calls to SAS Viya REST API's. In this section, you write a code to extract some folder's information.

1. In Visual Studio Code, create a new file. Click on the **File** menu and select **New File**.
1. Change the language of the new file to Python.

    ![Change language](images/changeFileLanguage.png)

1. Enter the following code into the new Python file:

    ```python
    # Import module(s)
    from viyaRestPy.Folders import getFolder

    # Collect information needed for authentication
    auth_info = {}
    auth_info["user"] = "gatedemo003"
    auth_info['pw'] = "lnxsas"
    auth_info["server_name"] = "http://sasviya01.race.sas.com:80"
    auth_info["app_name"] = "app"
    auth_info["app_secret"] = "appsecret"

    # Call the getFolder
    folder = getFolder(path="/Users", auth=auth_info)

    # Display name and description of the extracted folder
    print(folder["json"])["name"]
    print(folder["json"])["description"]
    ```

1. Save the program using **File** menu and **Save As ...** option. As file name, give *myGetFolder.py*.
1. From within Visual Studio Code, open a Terminal.

    ![Open Terminal](images/openTerminal.png)

1. In the Terminal, navigate to the location where you saved your code for example:

    ```bash
    cd C:\Users\student\Documents\viyarestpy\Examples
    ```

1. From that location, execute the code you saved:

    ```bash
    py -3 my_get_folder
    ```

    The results should look like this on Windows:

    ```bash
    C:\Users\student\Documents\viyarestpy\Examples>py -3 my_get_folder.py
    Users
    Base Folder for all user folders.

    C:\Users\student\Documents\viyarestpy\Examples>
    ```

### Take away

You have in a few lines of code retrieved the name and the description of a folder using REST API's. Using the viyaRestPy package eases the development process by hiding the complexity of the authentication and the REST API calls.
If you want to better understand how to create your own functions using call_rest function, you can have a look at the *get_folder.py* located under *viyaRestPy > Folders* in the Visual Studio Code project.
If you want to create your own functions, feel free to contribute!
