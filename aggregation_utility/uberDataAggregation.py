# python imports
import sys, getopt, time, os.path, queue, csv

# uber API library imports
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber_rides.errors import *

# querying framework library import
# from AgentQueryFramework import *

# OAuth 2.0 credentials
UBER_SERVER_TOKEN = "0pX05LDtY4wn4I5cub9IM-rmfHdmjO45Ma3vPVRo"
UBER_CLIENT_ID = "A3nKaRh5hSyq9RprDmJzAiWbc0F7Yu9H"
UBER_CLIENT_SECRET = "f-MBa7v-km1Y1qp2-aEurMrup7mXeRSnxeqQ5Pin"
REDIRECT_URL = "https://127.0.0.1"
UBER_PERMISSION_SCOPES = ["request"]

UBER_REQUEST_LIMIT = 2000


# def uber_query(location, dist):
#     uber_session_reg = get_uber_session(NON_PRIVILEGED)
#     uber_client_reg = UberRidesClient(uber_session_reg, SANDBOX)

#     # retrieve data from the Uber API
#     eta = [get_uber_eta(uber_client_reg, location)]
#     prices = [get_uber_price_estimates(uber_client_reg, location, dist)]

#     return [eta, prices]


# def get_uber_eta(client, location):
#     eta_response = []

#     try:
#         response = client.get_pickup_time_estimates(location[1], location[2])
#         eta_response = response.json.get('times')
#     except (ClientError, ServerError, AttributeError):
#         while False:
#             response = client.get_pickup_time_estimates(location[1], location[2])
#             eta_response = response.json.get('times')

#     this_location = [location[0]]

#     for eta in eta_response:
#         ride_type = json_parse(eta, 'display_name')
#         ride_eta = clean(json_parse(eta, 'estimate'))

#         if ride_type.find("uberPOOL") > -1:
#             this_location.append(["UberPOOL", ride_eta])
#         elif ride_type.find("uberX'") > -1:
#             this_location.append(["UberX", ride_eta])
#         elif ride_type.find("UberSELECT") > -1:
#             this_location.append(["UberSELECT", ride_eta])
#         elif ride_type.find("UberBLACK") > -1:
#             this_location.append(["UberBLACK", ride_eta])
#         elif ride_type.find("uberXL") > -1:
#             this_location.append(["UberXL", ride_eta])
#         elif ride_type.find("UberSUV") > -1:
#             this_location.append(["UberSUV", ride_eta])

#     return this_location


# def get_uber_price_estimates(client, location, dist):
#     end_location = get_end_coordinates(location, dist)
#     price_response = []

#     try:
#         price_estimates = client.get_price_estimates(
#             start_latitude=location[1],
#             start_longitude=location[2],
#             end_latitude=end_location[0],
#             end_longitude=end_location[1]
#         )
#         price_response = price_estimates.json.get('prices')
#     except (ClientError, ServerError):
#         while False:
#             price_estimates = client.get_price_estimates(
#                 start_latitude=location[1],
#                 start_longitude=location[2],
#                 end_latitude=end_location[0],
#                 end_longitude=end_location[1]
#             )
#             price_response = price_estimates.json.get('prices')

#     this_location = [location[0]]

#     for price in price_response:
#         ride_type = json_parse(price, 'display_name')
#         ride_surge = clean(json_parse(price, 'surge_multiplier'))
#         ride_price = clean(json_parse(price, 'estimate'))
#         ride_price = "$" + ride_price

#         if ride_price.find('-') > -1:
#             ride_price_min = clean(json_parse(price, 'low_estimate'))
#             ride_price_max = clean(json_parse(price, 'high_estimate'))
#             ride_price_avg = (float(ride_price_min) + float(ride_price_max)) / 2
#             ride_price = "$" + str(ride_price_avg)

#         if ride_type.find("uberPOOL") > -1:
#             this_location.append(["UberPOOL", ride_price, ride_surge])
#         elif ride_type.find("uberX'") > -1:
#             this_location.append(["UberX", ride_price, ride_surge])
#         elif ride_type.find("UberSELECT") > -1:
#             this_location.append(["UberSELECT", ride_price, ride_surge])
#         elif ride_type.find("UberBLACK") > -1:
#             this_location.append(["UberBLACK", ride_price, ride_surge])
#         elif ride_type.find("uberXL") > -1:
#             this_location.append(["UberXL", ride_price, ride_surge])
#         elif ride_type.find("UberSUV") > -1:
#             this_location.append(["UberSUV", ride_price, ride_surge])

#     return this_location


# # Initiates an Uber session
# def get_uber_session(session_type):
#     session = Session(UBER_SERVER_TOKEN)

#     return session

def usage():
  print 'usage: ' + sys.argv[0] + '[option] ... [-h help | -s boolean | -p boolean | -i file | -o file ]'
  print 'Options and arguments (and corresponding environment variables):'
  print '-h \t\t: print this help message and exit (also --help)'
  print '-s boolean \t: sandbox mode; takes a boolean value to enable (True) or disable (False) sandbox mode. Default is False.'
  print '-p boolean \t: privileged mode; takes a boolean value to enable (True) or disable (False) privileged mode. Default is False.'
  print '-i file \t: changes the program\'s input directory; takes a string for file directory.'
  print '-o file \t: changes the program\'s output directory; takes a string for file directory. Default is None.'

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:s:p:i:o", ["help", "sandbox=", "privileged=", "input=", "output="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    src_file = None
    dst_file = None
    sandbox = False
    privileged = False
    
    for o, a in opts:
        
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--sandbox"):
            sandbox = a
        elif o in ("-p", "--privileged"):
            privileged = a
        elif o in ("-i", "--input"):
            src_file = a
        elif o in ("-o", "--output"):
            dst_file = a
        else:
            assert False, "unhandled option"
            
    if None in (src_file, dst_file):
        print "Source and destination files unspecified."
        usage()
        sys.exit(2)
        
    # print output
    # print "S: " + str(sandbox)
    # print "P: " + str(privileged)
    
    # Set the distance (in mi) of Uber trip for the run
    trip_distance = 10
    
    # Get lat, long, and location identifier from CSV
    location_data = get_location_data(src_file)
    
    # Set CSV output location for results
    if not os.path.isfile(dst_file):
        makeCSV()
    else:
        CSV = open(dst_file, "a")
        CSV.write("\n\n")
        CSV.close()
        
    count, run, total_locations, total_hr_req = 0, 0, 0, 0
    num_locations = len(location_data)
    num_uber_reqs = 2
    start_time = time.time()
    
    while 1:
        elapsed_time = time.time() - start_time
        
        for location in location_data:
            if total_hr_req < UBER_REQUEST_LIMIT - 1 and elapsed_time < 3590:
                
                # Run routine from Uber and Lyft
                try:
                    data = [location, trip_distance, uber_query(location, trip_distance),
                            lyft_query(location, trip_distance), weather_query(location)]
                except IndexError:
                    while False:
                        data = [location, trip_distance, uber_query(location, trip_distance),
                                lyft_query(location, trip_distance), weather_query(location)]

if __name__ == "__main__":
    main()