class Imageprocessing:
    def __init__(self, img, mask, treshhold, name):
        self.name = name
        self.img = img.tolist()
        self.mask = mask.tolist()
        self.treshhold = treshhold

    def to_grayscale(self, bolean=True): # False to apply to mask
        img = self.mask
        if bolean:
            img = self.img
        grayscale = []
        for x_axis in img:
            axis = []
            for pixel in x_axis:
                grayscale_pixel = ((pixel[0] + pixel[1] + pixel[2]) / 3)
                axis.append(int(grayscale_pixel))
            grayscale.append(axis)
        return grayscale

    def get_global_brightness(self):
        img = self.to_grayscale()
        iteration = 0
        brighness_scale = 0
        for y_axis in img:
            for pixel in y_axis:
                brighness_scale += pixel
                iteration += 1
        brighness_scale = (brighness_scale / iteration) / 128
        print('Average brightness :' + str(brighness_scale))
        return brighness_scale


    def apply_mask(self):
        img = self.to_grayscale()
        mask = self.to_grayscale(False)
        result = []
        y_position = 0
        x_position = 0
        for y_axis in img:
            axis = []
            for pixel in y_axis:
                if mask[y_position][x_position] == 0:
                    axis.append(0)
                else:
                    axis.append(pixel)
                x_position += 1
            result.append(axis)
            x_position = 0
            y_position += 1
        return result

    def calculate_contrast(self):
        masked = self.apply_mask()
        contrast = 0
        y_position = 0
        x_position = 0
        for y_axis in masked:
            for pixel in y_axis:
                try:
                    top = masked[y_position - 1][x_position]
                    bottom = masked[y_position + 1][x_position]
                    left = masked[y_position][x_position - 1]
                    right = masked[y_position - 1][x_position + 1]
                    if 0 not in [pixel, top, bottom, left, right]:
                        contrast += self.neighboor_contrast(pixel, top, bottom, left, right)
                except:
                    pass
                x_position += 1
            x_position = 0
            y_position += 1
        print("Contrast/Threshold for %s : %s/%s " % (self.name, contrast, self.treshhold))
        return contrast

    def neighboor_contrast(self, reference, top, bottom, left, right):
        result = 0
        top = (reference - top)**2
        bottom = (reference - bottom)**2
        left = (reference - left)**2
        right = (reference - right)**2
        if top > 20:
            result += top
        if bottom > 20:
            result += bottom
        if left > 20:
            result += left
        if right > 20:
            result += right
        return result

    def is_available(self):
        if self.calculate_contrast() > self.treshhold:
            print("Véhicule présent")
            return False
        else:
            print("Véhicule non présent")
            return True
