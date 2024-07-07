import os,csv, sys, time, threading, abc, glob,re
import time
import random
import json
import requests
import concurrent.futures
from datetime import datetime
from optparse import OptionParser

article_view_count=0
total_count=0
ok_count=0
false_count=0
max_time=0
min_time=1000000
sum_time=0

# -------------------------------------------------------------------------
def load_request(worker_no):

    BASE_URL="http://localhost:8080/transactions/transfer"
    HEADERS = {'Content-Type': 'application/json'}

    global article_view_count
    global total_count
    global ok_count
    global false_count
    global max_time
    global min_time
    global sum_time

    while True:
        if article_view_count > 1000 :
            break;
        start_time = datetime.now()
        response=requests.post(BASE_URL, headers=HEADERS)
        end_time = datetime.now()
        elapsed_time = end_time - start_time

        if response.status_code == 200:
            ok_count = ok_count + 1
        else :
            false_count = false_count + 1

        sum_time = sum_time + int( elapsed_time.total_seconds() * 1000 )
        total_count = total_count + 1

        if max_time <= int( elapsed_time.total_seconds() * 1000 ):
            max_time = int( elapsed_time.total_seconds() * 1000 )

        if min_time >= int( elapsed_time.total_seconds() * 1000 ):
            min_time = int( elapsed_time.total_seconds() * 1000 )

        article_view_count=article_view_count+1
        print("Worker: ", worker_no,
            " POST response :",response.status_code, 
            "article_view_count :", article_view_count,
            "elapsed time : ",int( elapsed_time.total_seconds() * 1000 )
        )
        time.sleep(1)

    return True

# -------------------------------------------------------------------------
def parse_options():
    parser = OptionParser()
    parser.add_option("-w", action="store", type="int", dest="max_workers", default=1, help="Max Thread Workers")
    (options, args) = parser.parse_args()
    return options

def main():
    options = parse_options()    

    #print("Worker Count :",options.max_workers)

    global article_view_count
    global total_count
    global ok_count
    global false_count
    global max_time
    global min_time
    global sum_time

    with concurrent.futures.ThreadPoolExecutor(max_workers=options.max_workers) as executor: 
        future_load_data = {executor.submit(load_request,worker_no): worker_no for worker_no in range(0,options.max_workers)}
        for future in concurrent.futures.as_completed(future_load_data):
            results = future_load_data[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (results, exc))
            else:
                print(str(data), ' Done!')

    print(
        "===============================================",
        "\ntotal_count\t: ",total_count,
        "\nok_count\t: ",ok_count,
        "\nfalse_count\t: ",false_count,
        "\nmin_time\t: ",min_time,
        "\nmax_time\t: ",max_time,
        "\nsum_time\t: ",sum_time,
        "\navg_time\t: ",(sum_time/total_count),
        "\n==============================================="
    )

if __name__ == '__main__':
   main()

