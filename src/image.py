import numpy as np
from PIL import Image
import re
from datetime import datetime
import rasterio
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GRDImage:
    def __init__(self, file_path: str):
        """
        Initialize the GRDImage with a specified file.

        :param file_path: Path to the GRD file.
        """
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path
        self.logger.info(f"Initializing GRDImage with the file: {file_path}")

        self.data = self.read_grd()
        self.image_id, self.timestamp = self.extract_info_from_filename()
        self.calibration_factor

    def read_grd(self) -> np.ndarray:
        """
        Reads GRD data from the file path.

        :return: Numpy array containing GRD data.
        """
        try:
            with rasterio.open(self.file_path) as src:
                grd_data = src.read(1)
                tags = src.tags()
                self.calibration_factor = float(tags.get("CALIBRATION_FACTOR", 1.0))
                self.logger.info(f"Calibration factor: {self.calibration_factor}")
                self.logger.info(f"GRD data successfully read from {self.file_path}")
                return grd_data
        except Exception as e:
            self.logger.error(f"Error reading GRD data: {e}")
            raise

    def normalize(self, output_format: str):
        """
        Normalize the data according to the specified format.

        :param output_format: Format for normalization ('0-1', '-1-1', or '0-255').
        """
        self.logger.info(f"Normalizing data in format: {output_format}")
        try:
            grd_data = self.data
            if output_format == "0-1":
                normalized_data = (grd_data - np.min(grd_data)) / (
                    np.max(grd_data) - np.min(grd_data)
                )
            elif output_format == "-1-1":
                normalized_data = (
                    2
                    * (grd_data - np.min(grd_data))
                    / (np.max(grd_data) - np.min(grd_data))
                    - 1
                )
            elif output_format == "0-255":
                normalized_data = (
                    255
                    * (grd_data - np.min(grd_data))
                    / (np.max(grd_data) - np.min(grd_data))
                )
            else:
                raise ValueError(
                    'Invalid output format. Choose from "0-1", "-1-1", or "0-255".'
                )
            self.data = normalized_data.astype(np.float32)
            self.logger.info("Normalization successfully completed")
        except Exception as e:
            self.logger.error(f"Normalization error: {e}")
            raise

    def calibrate(self):
        """
        Calibrate the data using the calibration factor.

        The calibration process involves adjusting the image data based on the calibration factor.
        This process includes scaling the data to a valid range and then applying a formula to
        calculate the calibrated values (sigma0_db).

        The method ensures the data is in a valid range for calibration:
        - If the data is in the range 0-255, it is scaled to 0-1.
        - If the data is in the range -1 to 1, it is adjusted to 0-1.
        - Data must be normalized in the range 0-1 before applying the calibration formula.

        The calibration formula used is: sigma0 = CF * |data|^2, where CF is the calibration factor.
        Then, sigma0_db is calculated using the formula: 10 * log10(sigma0 + small_value),
        where small_value is added to avoid the logarithm of zero.

        Raises:
            ValueError: If the data is not normalized to a valid range (0-1) before calibration.
            Exception: For any other errors that occur during the calibration process.

        Logs:
            Information about the start and completion of the calibration process.
            Any errors that occur during the process.
        """
        self.logger.info("Starting data calibration")
        try:
            # Ensure data is in a valid range for calibration
            if np.amin(self.data) < 0 or np.amax(self.data) > 1:
                raise ValueError(
                    "Data must be normalized to a valid range (0-1) before calibration"
                )

            # Adjust data ranges if necessary
            if np.amin(self.data) >= 0 and np.amax(self.data) > 1:
                self.data = self.data / 255.0
            elif np.amin(self.data) < 0:
                self.data = (self.data + 1) / 2.0

            self.logger.info(f"Calibration factor: {self.calibration_factor}")

            # Calculate sigma0 and sigma0_db
            sigma0 = self.calibration_factor * np.abs(self.data) ** 2
            sigma0_db = 10 * np.log10(sigma0 + 1e-10)

            self.data = sigma0_db
            self.logger.info("Calibration successfully completed")
        except ValueError as ve:
            self.logger.error(f"Calibration error: {ve}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during calibration: {e}")
            raise

    def downsample(self, size: tuple = (256, 256)) -> np.ndarray:
        """
        Downsample the image to the specified size.

        :param size: Tuple indicating the new size of the image.
        :return: Numpy array of the downsampled image.
        """
        self.logger.info(f"Reducing image size to {size}")
        try:
            # Make sure the data is in the range 0-255 and convert it to np.uint8
            image_data = (self.data * 255).clip(0, 255).astype(np.uint8)

            image = Image.fromarray(self.data)
            image.thumbnail(size)
            self.logger.info("Downsampling successfully completed")
            return np.array(image)
        except Exception as e:
            self.logger.error(f"Downsampling error: {e}")
            raise

    def save_as_png(self, file_path: str):
        """
        Save the image as a PNG file.

        :param file_path: Path where the PNG file will be saved.
        """
        self.logger.info(f"Saving imagen in png file {file_path}")
        try:
            # Make sure the data is in the range 0-255 and convert it to np.uint8
            image_data = (self.data * 255).clip(0, 255).astype(np.uint8)

            image = Image.fromarray(image_data, mode="L")
            image.save(file_path)
            self.logger.info("Image successfully saved")
        except Exception as e:
            self.logger.error(f"Error saving image: {e}")
            raise

    def extract_info_from_filename(self) -> tuple:
        """
        Extract the image ID and timestamp from the file name.

        :return: Tuple containing the image ID and timestamp.
        """
        self.logger.info(f"Extracting file name information {self.file_path}")
        try:
            pattern = r"ICEYE_X\d+_GRD_(SM|SL)_(\d+)_(\d{8}T\d{6})"
            match = re.search(pattern, self.file_path)
            if match:
                image_id = match.group(2)
                timestamp = datetime.strptime(
                    match.group(3), "%Y%m%dT%H%M%S"
                ).isoformat()
                self.logger.info("Information successfully extracted")
                return image_id, timestamp
            else:
                raise ValueError("Invalid file name format")
        except Exception as e:
            self.logger.error(f"Error al extraer información: {e}")
            raise
