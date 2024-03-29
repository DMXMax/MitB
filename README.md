# Monster In the Box (MitB)

Monster in the box.  Was inspired by the generic pifacedigitialio server, but has been rewritten to take advantage of python built-in threading. Also, the web page refreshes itself if the box is busy. 

The MitB has three different shows, which are selected by the user. 

## Additional Notes

### Installing pygame and pifacedigitalio

Rasbian seems to have its own install of pygame called python3-pygame. 

`sudo apt install python3-pygame`

Pifacedigitalio is installed through pip3

`pip3 install pifacecommon pifacedigitalio`


### fixing "cannot find device error" (Issue deprecated in 2023)
Within spi.py (at my system it was at /usr/local/lib/python3.5/dist-packages/pifacecommon/spi.py) add a line speed_hz=ctypes.c_uint32(100000) to the transfer struct so that it looks as following

 # create the spi transfer struct
        transfer = spi_ioc_transfer(
            tx_buf=ctypes.addressof(wbuffer),
            rx_buf=ctypes.addressof(rbuffer),
            len=ctypes.sizeof(wbuffer),
            speed_hz=ctypes.c_uint32(100000) 
        )

### Running the Server

`cd MitB`  
`FLASK_APP=MitBServer.py nohup flask run --host=0.0.0.0 &`

This will run on port 5000 (default)

### Additional libraries (running in a venv)
Python wants to run non-universal libs in a venv. But to get libraries and such you might need to still install pygame as above.
If you run in a venv, you may need to add libraries:

libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-2.0-0

these can be retrieved via apt-get

