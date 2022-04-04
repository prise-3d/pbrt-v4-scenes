import OpenEXR, Imath
import numpy as np

class EXR():

    def __init__(self, data, spp):

        self.data = data
        self.shape = data.shape
        self.spp = spp


    def save(self, filename):
        
        h, w, c = self.data.shape

        dataR = []
        dataG = []
        dataB = []

        for j in range(h):
            for i in range(w):
                dataR.append(self.data[j][i][0])
                dataG.append(self.data[j][i][1])
                dataB.append(self.data[j][i][2])

        dataR_array = np.array(dataR, np.float16).tobytes()
        dataG_array = np.array(dataG, np.float16).tobytes()
        dataB_array = np.array(dataB, np.float16).tobytes()
        
        # add number of spp
        header = OpenEXR.Header(w, h)
        header['samplesPerPixel'] = self.spp
        
        # specify HALF floating point
        header['channels'] = { 'R' : Imath.Channel(Imath.PixelType(OpenEXR.HALF)),
                       'G' : Imath.Channel(Imath.PixelType(OpenEXR.HALF)),
                       'B' : Imath.Channel(Imath.PixelType(OpenEXR.HALF))}

        exr = OpenEXR.OutputFile(filename, header)
        
        exr.writePixels({'R': dataR_array, 'G': dataG_array, 'B': dataB_array})

    @staticmethod
    def fromfile(filename):

        # read EXR file and create 
        exr_img = OpenEXR.InputFile(filename)
        exr_data = exr_img.header()

        # extract header metadata
        h, w = (exr_data['dataWindow'].max.y, exr_data['dataWindow'].max.x)
        img_size = (h + 1, w + 1)
        spp = exr_data['samplesPerPixel']
        
        # extract RGB data
        data_r = exr_img.channel('R')
        data_g = exr_img.channel('G')
        data_b = exr_img.channel('B')

        # convert into numpy array
        r = np.frombuffer(data_r, 'half').reshape(img_size)
        g = np.frombuffer(data_g, 'half').reshape(img_size)
        b = np.frombuffer(data_b, 'half').reshape(img_size)

        # store into current attribute
        data = np.dstack((r, g, b))

        return EXR(data, spp)

    @staticmethod
    def fusion(exr_list):

        spp_sum = sum([ exr.spp for exr in exr_list])
        data = np.sum([ exr.data * (exr.spp / float(spp_sum)) for exr in exr_list ], axis=0)

        return EXR(data, spp_sum)
        

    def __str__(self) -> str:
        return f'(shape: {self.size}, spp: {self.spp})'