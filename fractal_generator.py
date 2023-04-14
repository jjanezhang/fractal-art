from mandelbrot import MandelbrotSet
from viewport import Viewport
from PIL import Image, ImageDraw, ImageFont
from weather_params import get_weather_params
from cities import get_city_lat_lon
import numpy as np
import warnings
import sys
warnings.filterwarnings('ignore', category=DeprecationWarning)

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

def get_fractal(loc):
    location, temp, humidity, precipitation = get_weather_params(loc)
    #print(loc, location, temp, humidity, precipitation)
    max_iterations = get_max_iterations(humidity, precipitation)
    mandelbrot_set = MandelbrotSet(max_iterations=max_iterations, escape_radius=1000)
    image = Image.new(mode="RGB", size=(250, 250))
    viewport = Viewport(image, center=-0.75, width=3.5)
    palette = get_palette(temp)
    paint(mandelbrot_set, viewport, palette, smooth=True)
    add_label(image, location)
    image.show()
    return image

def add_label(image, text):
    width, height = 250, 250
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/Applications/fonts/Lato/Lato-Black.ttf', 14)

    text_width, text_height = draw.textsize(text, font=font)
    x = (width - text_width) / 2
    y = height - text_height - 15

    # Check the average brightness of the image to determine the text color
    brightness = sum(image.convert('L').getdata()) / (width * height)
    if brightness < 128:
        text_color = (255, 255, 255, 255) # Use white text on dark background
    else:
        text_color = (0, 0, 0, 255) # Use black text on light background

    # Draw the text label on the image
    draw.text((x, y), text, font=font, fill=text_color)

def get_max_iterations(humidity, precipitation):
    #range 10-500
    min_value, max_value = 10, 160
    if precipitation:
        min_value = 100
    
    humidity_factor = 1 - (humidity/100)
    value_range = max_value - min_value
    return round(min_value + (humidity_factor * value_range)) 

def generate_multicolor_gradient(num_colors, control_points):
    control_points.sort(key=lambda x: x[0])

    # Create a list of colors and positions
    colors = [c[1] for c in control_points]
    positions = [c[0] for c in control_points]

    # Create a linear interpolation function for each color channel
    r_interp = np.interp(np.linspace(0, 1, num_colors), positions, [c[0] for c in colors])
    g_interp = np.interp(np.linspace(0, 1, num_colors), positions, [c[1] for c in colors])
    b_interp = np.interp(np.linspace(0, 1, num_colors), positions, [c[2] for c in colors])

    # Create a list of RGB tuples
    gradient = [(int(r), int(g), int(b)) for r, g, b in zip(r_interp, g_interp, b_interp)]

    return gradient

def get_palette(temp):
    control_points = [(0 + i * 0.05, color) for i, color in enumerate([(255,255,255), 
                                                                      (228,240,255), 
                                                                      (147, 177, 215),
                                                                      (111,157,218), 
                                                                      (29,109,212),
                            (30,79,139), 
                            (19,112,152), 
                            (55,142,137), 
                            (33,159,155),
                            (34,159,105),
                            (70,171,55),
                            (240,235,80),
                            (194, 171, 118),
                            (213,163,45),
                            (189, 113, 80), 
                            (199, 98, 54),
                            (159, 41, 76), 
                            (110,20,49), 
                            (64,0,21), (0,0,0)])]

    gradient = generate_multicolor_gradient(50, control_points)
    temp_range = 140   # range of possible temperatures
    temp_offset = (max(0, temp)) / temp_range   # offset between 0 and 1 based on temperature
    color_offset = int(temp_offset * 50)   # index of color in gradient list

    # Shift the color gradient to the correct starting position
    palette = gradient[color_offset:color_offset+5]
    print(palette)
    return palette

def format_city(city):
    city = city.lower().replace(" ", "_")
    return city

def get_fractal_set():
    cities = get_city_lat_lon()
    image_list = []
    for _, lat, lon in cities:
        fractal = get_fractal(f"{lat},{lon}")
        image_list.append(fractal)
    
    new_image = Image.new('RGB', (2000, 2000), (255, 255, 255))

    for i in range(8):
        for j in range(8):
            x = j * 250
            y = i * 250
            index = i * 8 + j
            if index < len(image_list):
                new_image.paste(image_list[index], (x, y))

    new_image.save('final.png')

n = sys.argv[1]
print(get_fractal(n))
#print(get_fractal_set())