# API

## This will be the server application.

### Functions:
-   login   :
    -   Will server as the authentication component of the server
    -   A person will not be able to use the API without authentication
    -   Allowed methods : "POST"
-   get_list    :
    -   Will return a list of all commands saved in a json file
    -   Allowed methods : "GET"
-   add_command :
    -   Will add a pair of an alias and a command to the json file
    -   Allowed methods : "POST"
-   remove_command
    -   Will remove a pair of an alias and a command from the json file
    -   Allowed methods : "PUT"
-   modify_command  :
    -   Will modify the alias or the command in the json file
    -   Allowed methods : "PUT"
-   execute_costume_command :
    -   Will execute a shell command given by the user
    -   Allowed methods : "POST"
-   execute_command_by_alias    :
    -   Will execute a command already saved in the json file
    -   Allowed methods : "POST"


### Code info:
All libraries are written in the "requirements.txt" file. This script uses flask to host a HTTP server. JWT cookies for authentication. And subprocesses to execute the shell commands.

#### Security concerns and other notable information:
1.  This will be vulnerable to a MITM type attack. Solution: Use HTTPS
