# python imports
import sys, getopt, time, os.path, queue

# API querying functions import
from csv_io import *
from uber_aggregation import uber_query
from lyft_aggregation import lyft_query
from weather_aggregation import weather_query

UBER_REQUEST_LIMIT = 2000

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
        
    dst_file = "out.csv"
    
    print "I: " + src_file
    print "O: " + dst_file
    print "S: " + str(sandbox)
    print "P: " + str(privileged)
    
    # Set the distance (in mi) of Uber trip for the run
    trip_distance = 10
    
    # Get lat, long, and location identifier from CSV
    location_data = get_location_data(src_file)
    
    # Set CSV output location for results
    if not os.path.isfile(dst_file):
        make_CSV(dst_file)
    else:
        CSV = open(dst_file, "a")
        CSV.write("\n\n")
        CSV.close()
        
    count, run, total_locations, total_hr_req = 0, 0, 0, 0
    print location_data
    num_locations = len(location_data)
    num_uber_reqs = 2
    start_time = time.time()
    
    while 1:
        elapsed_time = time.time() - start_time
        
        for location in location_data:
            if total_hr_req < UBER_REQUEST_LIMIT - 1 and elapsed_time < 3590:
                
                # Run routine from Uber and Lyft
                try:
                    data = [location, trip_distance, uber_query(privileged, sandbox, location, trip_distance),
                            lyft_query(location, trip_distance), weather_query(location)]
                except IndexError:
                    while False:
                        data = [location, trip_distance, uber_query(privileged, sandbox, location, trip_distance),
                                lyft_query(location, trip_distance), weather_query(location)]
                                
                count+= 1
                total_locations += 1
                total_hr_req += num_uber_reqs
                
                if count < num_locations:
                    CSV_write(dst_file, data, False)
                else:
                    CSV_write(dst_file, data, True)
                    count = 0
                    run += 1
                    
                elapsed_time = time.time() - start_time
            else:
                while elapsed_time < 3600:
                    elapsed_time = time.time() - start_time

                count = 0
                run = 0
                total_locations = 0
                total_hr_requests = 0
                start_time = time.time()

if __name__ == "__main__":
    main()