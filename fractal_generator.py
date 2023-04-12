from mandelbrot import MandelbrotSet
from viewport import Viewport
from PIL import Image
from weather_params import get_weather_params
import matplotlib.cm

def paint(mandelbrot_set, viewport, palette, smooth):
    for pixel in viewport:
         stability = mandelbrot_set.stability(complex(pixel), smooth)
         index = int(min(stability * len(palette), len(palette) - 1))
         pixel.color = palette[index % len(palette)]
    
def denormalize(palette):
     return [
          tuple(int(channel * 255) for channel in color)
          for color in palette
     ]

def get_fractal(lat, lon):
    location, temp, humidity, precipitation = get_weather_params(lat, lon)

    mandelbrot_set = MandelbrotSet(max_iterations=20, escape_radius=1000)
    image = Image.new(mode="RGB", size=(512, 512))
    viewport = Viewport(image, center=-0.75, width=3.5)
    colormap = matplotlib.cm.get_cmap("twilight").colors
    palette = denormalize(colormap)
    paint(mandelbrot_set, viewport, palette, smooth=True)
    image.show()

def get_max_iterations(humidity, precipitation):
     
def get_paletter(temp):