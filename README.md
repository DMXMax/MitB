# Monster In the Box (MitB)

Monster in the box.  Was inspired by the generic pifacedigitialio server, but has been rewritten to take advantage of python built-in threading. Also, the web page refreshes itself if the box is busy. 

The MitB has three different shows, which are selected by the user. 

## Additional Notes

### Installing pygame and pifacedigitalio

Rasbian seems to have its own install of pygame called python3-pygame. 

`sudo apt install python3-pygame`

Pifacedigitalio is installed through pip3

`pip3 install pifacecommon pifacedigitalio`


### fixing "cannot find device error"
Within spi.py (at my system it was at /usr/local/lib/python3.5/dist-packages/pifacecommon/spi.py) add a line speed_hz=ctypes.c_uint32(100000) to the transfer struct so that it looks as following

 # create the spi transfer struct
        transfer = spi_ioc_transfer(
            tx_buf=ctypes.addressof(wbuffer),
            rx_buf=ctypes.addressof(rbuffer),
            len=ctypes.sizeof(wbuffer),
            speed_hz=ctypes.c_uint32(100000) 
        )

### Running the Server

`env FLASK_APP=MitBServer.py --host 0.0.0.0 `

