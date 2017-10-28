import sys
import traceback 
import RPi.GPIO as GPIO 
from time import sleep 
import Adafruit_DHT 
import urllib2 
import logging
import config
from datetime import datetime

myAPI = config.api_key

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=datetime.now().strftime('gabitemp_%Y_%m_%d_%H_%M.log'),
                    filemode='w')

def getSensorData(): 
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
   T = T * 9/5.0 + 32 
   return (RH, T)

def main(): 
   baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
   while True:
       try: 
           RH, T = getSensorData()
    	   logging.info("Temperature: %s, Humidity: %s" % (T,RH))
 
	   try:
           	f = urllib2.urlopen(baseURL + 
                               		"&field1=%s&field2=%s" % (T, RH))
	   except urllib2.URLError as e_URLError:
		logging.warning("URLError " + str(e_URLError))
		pass
	   except urllib2.HTTPError as e_HTTPError:
		logging.warning("HTTPError " + str(e_HTTPError))
		pass
	   except Exception as e:
		loggging.warning("Unmanaged urllib2 error " + str(e))
		pass

	   logging.info("Thingspeak return value " + f.read())
	   f.close()
           sleep(60) #uploads DHT22 sensor values every 2 minutes 

       except Exception as e: 
       	   print logging.warning("Unmanaged error, exiting " + str(e))
           pass 
# call main 
if __name__ == '__main__': 
   main()
