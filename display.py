
from lib.waveshare_epd import epd4in01f
from PIL import Image

epd = epd4in01f.EPD()
epd.init()
epd.Clear()

Himage = Image.open('./images/_.bmp')
epd.display(epd.getbuffer(Himage))

epd.sleep()
