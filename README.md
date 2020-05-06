# webmonitoring
script that periodically checks urls and validates checks.

The following pre-requisites must be in place in order to successfully run the script:
1. python version 3
   How to Install python 3:
   Windows: Download installation package from https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe and follow wizard. 
            Ensure that "Add Python to environment variables" is selected.
   Linux: https://docs.aws.amazon.com/cli/latest/userguide/install-linux-python.html has details on how to install on Linux.
   MAC: https://wsvincent.com/install-python3-mac/ link has very good instructions.

2. Install the following 2 packages:
    pip install requests
    pip install schedule

How to run the script?:

1. Unzip WebMonitoring.zip file.
2. "python WebMonitoring.py -h" command will display command line arguement options. If you have both python 2 and python 3 installed
    then run the command with "python3 WebMonitoring.py -h"

3. Example run:
     python3 WebMonitoring.py -i urls.csv -o results.csv 
     Started processing urls.Check monitor log file in Logs folder

4. Script will create new results csv file for each day. The Result file will be named as "date_outputfilename.csv",
   Example: 2019-02-24_results4.csv
5. Script will also generate logging for each day. Logs are stored in Logs folder. It automatically keeps last 30 days logs.
   Logging configuration is found in logs.conf file.
6. Scheduling: by default script runs every 1 minute. It is possible to override this by passing --period or -p parameter. Example:
   python3 WebMonitoring.py -i urls.csv -o results4.csv -p 2 #now script will run every 2 minutes.
7. Sample urls.csv contains example on what kind of columns the script expects from the file. 
   Socket timeout is used in order to time out in scenarios where server is taking more time to respond. It would avoid script to get stuck with one url.
8. In case of Exceptions, there is no response time reported as response time would not be relevant in those cases.
9. Status:  Status=OK if no exceptions and validation check passed
            Status =NOT OK, if there is validation check
            Status=Connection timeout, if connection times out
            Status=HTTP error, for any http error such as HTTP 404 etc..
