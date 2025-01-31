from PIL import Image
from pathlib import Path
import ncempy.io as nio
import numpy as np
import pandas as pd
from scipy import fft
from matplotlib import pyplot as plt
from . import tem_helper

__all__ = ['transfer_scalebar_metadata', 'get_spacing']

def transfer_scalebar_metadata(ser_file: Path, tiff_file=None, scalebar_units='n'):
    """
    Transfers the scalebar metadata found in the ser file to the given tiff file
    to be read by software like ImageJ.
    If tiff file is None, then creates new file based on ser file and saves
    it in the same directory as the ser file.

    ser_file - file to read metadata from.
    tiff_file - file to put metadata into. If None, then creates new file in same directory.
    scalebar_units - one of ['M', 'K', '', 'c', 'm', 'u', 'n', 'p'] (SI prefixes)
    """
    ser_data = nio.read(ser_file)
    pixelsize = ser_data['pixelSize'][0]
    pixelUnit = ser_data['pixelUnit'][0]
    givenunits = pixelUnit.rsplit('m', 1)[0]
    multiplier = tem_helper.unit_multiplier(givenunits, scalebar_units)
    resolution = 1 / (pixelsize * multiplier)

    imageDescription = (270, f'ImageJ=1.54m\nunit={scalebar_units}m\n')
    newSubfileType = (254, 0)
    resolutionUnit = (296, 1)
    samplesPerPixel = (277, 1)
    xResolution = (282, resolution)
    yResolution = (283, resolution)

    metadatalist = [
        imageDescription,
        newSubfileType,
        resolutionUnit,
        samplesPerPixel,
        xResolution,
        yResolution
    ]

    metadata = { meta[0] : (meta[1],) for meta in metadatalist }

    tiff_img: Image.Image|None = None

    if tiff_file is None:
        filename = str(ser_file.name)[:-3] + 'tif'
        tiff_file = ser_file.parent / filename
        imgdata = ser_data['data']
        tiff_img = Image.fromarray(imgdata)
    else:
        with Image.open(tiff_file) as img:
            tiff_img = Image.fromarray(np.asarray(img))

    tiff_img.save(tiff_file, tiffinfo=metadata)
    return


def get_spacing(file: Path,
                wavelen_estimate,
                colnames=['Distance_(nm)', 'Gray_Value'],
                plot=False):
    """ 
    Performs FFT on given data file.
    file - a csv file containing the intensity information
    wavelen_estimate - guess where the wavelength is to remove harmonics.
    should choose a number slightly higher than the expected wavelength
    colnames - column names in the given file.
    plot - whether we should plot the data via pyplot.
    """
    dataframe = pd.read_csv(file)
    distance, intensity = colnames
    xdata = dataframe[distance].values
    ydata = dataframe[intensity].values

    spectrum = np.abs(np.array(fft.fft(ydata)))
    frq = fft.fftfreq(len(spectrum))
    delta = xdata[1]-xdata[0]
    with np.errstate(divide='ignore'):
        wavelens = delta / frq

    plotrange = np.abs(wavelens) < wavelen_estimate

    cut_wavelens = wavelens[plotrange]
    cut_spectrum = spectrum[plotrange]
    idx_max = np.argmax(cut_spectrum)
    characteristic_wavelen = np.abs(cut_wavelens[idx_max])

    if plot:
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(file.name[:-4] + f' ({characteristic_wavelen:.4}nm)')
        ax[0].plot(xdata, ydata)
        ax[0].set_xlabel('Distance (nm)')
        ax[0].set_title('Intensity Profile')
        ax[1].plot(cut_wavelens, cut_spectrum)
        ax[1].set_title('Fourier Transform')
        ax[1].set_xlabel('Wavelength (nm)')

    return characteristic_wavelen
