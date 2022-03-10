import time
import cv2 

class pixel:
    def __init__(self, r, g, b):
        self.r = int(r) 
        self.g = int(g)
        self.b = int(b)
    def __str__(self):
        return f'( {self.r} {self.g} {self.b} )'

    def rgb(self):
        return [self.r, self.g, self.b]

    def __add__(self, other):
        new_r = self.r + other.r
        new_g = self.g + other.g
        new_b = self.b + other.b
        return pixel(new_r, new_g, new_b)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __truediv__(self, other):
        return pixel(self.r//other, self.g//other, self.b//other)

    def __div__(self, other):
        return pixel(self.r//other, self.g//other, self.b//other)

    def __repr__(self):
        return f'{self.r} {self.g} {self.b}'

    def __rtruediv__(self, other):
        return pixel(self.r//other, self.g//other, self.b//other)

class raw_image:
    raw: list[list] = [[]]
    width: int = 0
    height: int = 0
    name = 'FILE'

    def __init__(self, arr: list, width, height, name):
        self.raw = arr
        self.width = width
        self.height = height
        self.name = name

    def make_img(self, user_input):
        header = f'P3\n{self.width} {self.height}\n255\n'
        with open(f'{user_input}_final.ppm', 'w') as f:
            f.write(header)
            for i in range(self.height):
                for j in range(self.width):
                    f.write(
                        f'{self.raw[i][j].r} {self.raw[i][j].g} {self.raw[i][j].b}')
                    f.write('\n')

def get_files(image: str) -> list:
    '''
    Gets a list of all file paths
    '''
    files = []
    for i in range(1, 11):
        filePath = f'raw_images/{image}/{image}_{i}.ppm'
        files.append(filePath)
    return files

def comp_average(images: list[raw_image], height, width, name) -> raw_image:
    '''
    Takes the raw image data, and averages the values out
    '''
    # TODO: make compute average faster
    new_image = [[pixel] * width for _ in range(height)]
    for image in images:
        for i in range(height):
            for j in range(width):
                new_pixel = pixel(0, 0, 0)
                red = image.raw[i][j].r
                green = image.raw[i][j].g
                blue = image.raw[i][j].b
                new_pixel = pixel(red, green, blue)
                new_image[i][j] += new_pixel
                del new_pixel
    
    for i in range(height):
        for j in range(width):
            new_image[i][j] = new_image[i][j] / 10

    return raw_image(new_image, width, height, name)

def get_raw_data(line: str) -> pixel:
    rgb = str(line).split()
    return pixel(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def test(file):
    print(file)
    data = open(file, 'rb').read().decode('ascii').split('\n')
    print(data[1])                                                       

def get_pixels(files: list[str]) -> list[raw_image]:
    '''
    Gets the pixel data from the list of files
    '''
    # TODO: this is really slow. Going to figure out how to make it faster
    all_pixels = []
    width = 591
    height = 600
    for file in files:
        data = open(file, 'rb').read().decode('ascii').split('\n')
        #curr_file = open(file, 'r').read().split('\n')
        width = int(str(data[1]).split(' ')[0])
        height = int(str(data[1]).split(' ')[1])
        image = raw_image(list(map(get_raw_data, data[3:-1])), width, height, file)
        # sets the images array to the list of pixels
        image.raw = to_matrix(image.raw, width)
        # adds each image object to the master list
        all_pixels.append(image)
        del image
    return all_pixels

def to_matrix(l, width) -> list[list]:
    '''
    Convert a 1d array to a 2d matrix
    '''
    return [l[i:i+width] for i in range(0, len(l), width)]

def main():
    spaceDict = {
        1: 'cone_nebula',
        2: 'n44f',
        3: 'orion',
        4: 'wfc3_uvis',
    }
    print('''Which photo do you want to denoise:
    1) Cone Nebula
    2) n44f
    3) orion
    4) wfc3_uvis
    ''')

    tTotal0 = time.time()
    user_input = int(input('Input: '))

    if user_input in spaceDict: 
        user_input = spaceDict[user_input]
    else: 
        return 

    tGetFiles0 = time.time()
    files = get_files(user_input)
    tGetFiles1 = time.time()
    print(f'Get file time: {tGetFiles1 - tGetFiles0} seconds')

    tGetRaw0 = time.time()
    images = get_pixels(files)
    tGetRaw1 = time.time()
    print(f'Get raw data time: {tGetRaw1 - tGetRaw0} seconds')
    tAve0 = time.time()
    denoised = comp_average(images, images[0].height, images[0].width, user_input)
    tAve1 = time.time()
    print(f'Get compute average Time: {tAve1 - tAve0} seconds')
    tMakeImg0 = time.time()
    denoised.make_img(user_input)
    tMakeImg1 = time.time()
    print(f'Get compute average time: {tMakeImg1 - tMakeImg0} seconds')
    tTotal1 = time.time()
    print(f'Total time taken: {tTotal1-tTotal0} seconds')
    i = cv2.imread(f'{user_input}_final.ppm')
    cv2.imwrite(f'{user_input}_final.jpg', i)
    
if __name__ == '__main__':
    main()
