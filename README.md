# Monster In the Box (MitB)

Monster in the box.  Was inspired by the generic pifacedigitialio server, but has been rewritten to take advantage of python built-in threading. Also, the web page refreshes itself if the box is busy. 

The MitB has three different shows, which are selected by the user. 

## Additional Notes

### Installing pygame and pifacedigitalio

Rasbian seems to have its own install of pygame called python3-pygame. 
`
sudo apt install python3-pygame
`

Pifacedigitalio is installed through pip3

`pip3 install pifacecommon pifacedigitalio`

### Running the Server

`env FLASK_APP=MitBServer.py --host 0.0.0.0 `


