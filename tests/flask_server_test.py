import http.client
import json
import matplotlib.pyplot as plt
from numpy import array

'''
Test the flask server by atttempting to make a plot out of the data received.
To run the test: run 'python3 flask_server_test.py' in this directory. Make sure the server is running.
'''

#attemot to make a plot out of the data on the server
def makePlot( data ):
    
    # PLOTTING
    plt.close()
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    cmap = plt.get_cmap(name='rainbow')
    
    #convert data back to numpy array
    salt = array(data['salt'])
    lonp = array(data['lonp'])
    latp = array(data['latp'])

    # pcolormesh is a fast way to make pcolor plots.  By handing it lon_psi
    # and lat_psi and any rho_grid_layer[1:-1,1:-1] the coordinate arrays
    # are one bigger in size (in both dimensions) than the data array, meaning
    # they define the data corners.  The result is that the colored tiles are
    # centered exactly where they should be (at their rho-grid location).
    cs = ax.pcolormesh(lonp, latp, salt[1:-1,1:-1], vmin=20, vmax=34.5,  cmap = cmap)
    
    plt.show()
    
    
#Create a connection
conn = http.client.HTTPConnection("localhost", 5000)

#Make a request of the server
conn.request("GET", "/")

#elicit a response from the server
response = conn.getresponse()

if response.status != 200:
    raise ValueError("Did not receive a 200 ok from the server!")

#return response_message and status code
received = json.loads(response.read().decode('utf-8'))

#attempt to make a plot out of the data
makePlot(received)







