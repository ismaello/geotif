import argparse
import logging
from src.image import GRDImage


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process and save GRD images. This script reads a GRD image file, normalizes, calibrates, downsamples it, and saves it as a PNG.",
        epilog="Example usage: python geotif.py data/input/image.tif 0-1 256 256 data/output/image.png",
    )
    parser.add_argument("file_path", help="Path to the GRD file.")
    parser.add_argument(
        "normalization_format", help="Normalization format('0-1', '-1-1', '0-255')."
    )
    parser.add_argument(
        "max_size",
        type=int,
        nargs=2,
        help="Maximum size of the downsampled image (width height).",
    )
    parser.add_argument(
        "output_filename",
        default="data/output/normalized.png",
        help="Directory to save the output image.",
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        file_path = args.file_path
        normalization_format = args.normalization_format
        max_size = tuple(args.max_size)
        output_path = args.output_filename

        image = GRDImage(file_path)
        image.normalize(normalization_format)
        image.calibrate()
        image.downsample(max_size)
        image.save_as_png(output_path)
        logger.info(f"Image ID: {image.image_id}, Timestamp: {image.timestamp}")

    except Exception as e:
        logger.error(f"Error in execution: {e}")
        raise


if __name__ == "__main__":
    main()
