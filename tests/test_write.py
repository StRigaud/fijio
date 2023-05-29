import numpy as np

from fijio import write


def test_minimal_write_tiff():
    random_image = np.random.random((32, 128, 256))
    with write.WriteTiff("random_image.tif", random_image) as writer:
        writer.write()


def test_write_multichannel_tiff():
    random_image = np.random.random((3, 32, 128, 256))
    with write.WriteTiff("random_image.tif", random_image) as writer:
        writer.write(color=["red", "green", "blue"])
