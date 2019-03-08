import requests, time, csv, schedule, argparse, logging, logging.config, logging.handlers

# defining default values
inputFileName = "urls.csv"
outFileName = "monitoring_result.csv"
period = 1
socketTimeOut = 60

# Read log config file
logging.config.fileConfig('logs.conf')

# define the program description and arguments.
example = 'Example: python3 Monitoring_v2.py -i urls.csv -o results.csv -p 2'
parser = argparse.ArgumentParser(description=example)
parser.add_argument("--input", "-i", help="Input config file name.Default urls.csv.File should be in csv format:url,validationText,socketTimeOut")
parser.add_argument("--output", "-o", help="Output file name. File will be in csv format")
parser.add_argument("--period", "-p", help="How often script should be run in minutes. Default is every 10 mins")

args = parser.parse_args()
if args.input:
    inputFileName = args.input
if args.output:
    outFileName = args.output
if args.period:
    period = int(args.period)


# function to create result file

def writeResult(row):
    filename = time.strftime("%Y-%m-%d") + '_' + outFileName
    with open(filename, 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()


# main function to check and verify urls.

def checkRequest(url, validationCheck, socketTimeOut):
    logger = logging.getLogger('checkURL')
    status = "NOT OK"  # default status is NOT OK unless otherwise overridden.
    responseTime = "NA"
    try:
        logger.info("Started checking url " + url)
        r = requests.get(url, timeout=float(socketTimeOut))
        r.raise_for_status()
        responseTime = r.elapsed.total_seconds()
        time.sleep(5)  # ensuring that urls are checked after certain think time.
        if validationCheck.lower() in r.text.lower():
            status = "OK"
            logger.info(url + " took " + str(responseTime) + " seconds")
        else:
            logger.error("Validation check failed.")

    except requests.ConnectionError as e:
        status = "ConnectionTimeOut"
        logger.error(url + " Connection Error. Make sure you are connected to InternetT or url is wrong.\n" + str(e))

    except requests.Timeout as e:
        status = "SocketTimeOut"
        logger.warning(url + " server failed to respond within " + socketTimeOut + " seconds." + str(e))

    except requests.HTTPError as e:
        status = "HTTP error"
        logger.error(str(e))

    except KeyboardInterrupt as e:
        logger.warning("User cancelled script run."+ str(e))
        exit(1)

    except Exception as e:
        logger.error("Uncaught exception occurred." + str(e))

    finally:
        logger.info("Finished checking url " + url)
        row = [int(time.time()), url, status, responseTime]
        writeResult(row)


# function to read external file and triggering check for each urls in the file
def monitor():
    with open(inputFileName) as csv_file:
        logger = logging.getLogger('csvRead')
        csv_reader = csv.reader(csv_file, delimiter=',')
        logger.info("Started reading csv file")
        line_count = 0
        next(csv_reader) #skip first header line
        for row in csv_reader:
            checkRequest(row[0], row[1], row[2])
            line_count += 1
        logger.info("Finished reading csv file." + f'Checked {line_count} urls.')


print("Started processing urls.Check monitor log file in Logs folder")
schedule.every(period).minutes.do(monitor)

# run scheduler. https://schedule.readthedocs.io/en/stable/
while True:
    schedule.run_pending()
    time.sleep(1)
