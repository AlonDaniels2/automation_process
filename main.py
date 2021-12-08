import download_csv
import handle_csv_file
import send_email
import log_funcs
import sys

try:
    download_csv.download_csv()
except Exception as e:
    log_funcs.log_error(e)
    sys.exit()
else:
    print("Downloaded successfully.")
try:
    handle_csv_file.handle_csv_file()
except Exception as e:
    log_funcs.log_error(e)

else:
    print("File edited successfully.")
    try:
        send_email.send_email()
    except Exception as e:
        log_funcs.log_error(e)
    else:
        print("Emailed successfully.")
