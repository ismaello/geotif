import numpy as np
import os
from src.image import GRDImage


def test_read_grd():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    assert isinstance(image.data, np.ndarray), "Data should be a numpy array"
    assert image.data.size > 0, "Data array should not be empty"


def test_normalize_0_to_1():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("0-1")
    assert np.all(
        (0 <= image.data) & (image.data <= 1)
    ), "Data should be normalized between 0 and 1"


def test_normalize_minus1_to_1():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("-1-1")
    assert np.all(
        (-1 <= image.data) & (image.data <= 1)
    ), "Data should be normalized between -1 and 1"


def test_normalize_0_to_255():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("0-255")
    assert np.all(
        (0 <= image.data) & (image.data <= 255)
    ), "Data should be normalized between 0 and 255"
    assert image.data.dtype == np.float32, "Normalized data should be of type float32"


def test_normalize_invalid_format():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    try:
        image.normalize("invalid-format")
        assert False, "Should raise ValueError for invalid format"
    except ValueError:
        assert True


def test_calibrate_0_to_1():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("0-1")
    image.calibrate()
    assert image.data is not None, "Calibration should produce data"
    assert not np.any(np.isnan(image.data)), "Calibrated data should not contain NaNs"


def test_calibrate_minus1_to_1():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("-1-1")
    image.calibrate()
    assert image.data is not None, "Calibration should produce data"
    assert not np.any(np.isnan(image.data)), "Calibrated data should not contain NaNs"


def test_calibrate_0_to_255():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("0-255")
    image.calibrate()
    assert image.data is not None, "Calibration should produce data"
    assert not np.any(np.isnan(image.data)), "Calibrated data should not contain NaNs"


def test_downsample():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("0-255")  # Asegúrate de normalizar antes de reducir tamaño
    downsampled_image = image.downsample((256, 180))
    assert downsampled_image.shape == (
        180,
        126,
    ), "Downsampled data should have the correct shape"


def test_save_as_png():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    image.normalize("0-255")
    image.calibrate()
    image.downsample((256, 256))
    output_path = "data/output/test_output.png"
    image.save_as_png(output_path)
    assert os.path.exists(output_path), "PNG file should be created"
    os.remove(output_path)  # Clean up after test


def test_extract_info_from_filename():
    image = GRDImage("data/input/ICEYE_X4_GRD_SM_9281_20190903T144946.tif")
    assert image.image_id == "9281", "Image ID should be extracted correctly"
    assert (
        image.timestamp == "2019-09-03T14:49:46"
    ), "Timestamp should be extracted correctly"
