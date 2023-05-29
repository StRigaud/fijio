import numpy as np
from tifffile import tifffile
from matplotlib.colors import LinearSegmentedColormap


class WriteTiff:
    _color_dict = {
        "red": (1, 0, 0),
        "green": (0, 1, 0),
        "blue": (0, 0, 1),
        "gray": (1, 1, 1),
        "yellow": (1, 1, 0),
        "cyan": (0, 1, 1),
        "magenta": (1, 0, 1),
    }

    def __init__(
        self,
        fname: str,
        data: np.ndarray,
        spacing: tuple = (1, 1, 1),
        unit: str = "pixels",
        axes: str = "TCZYX",
        color: list[tuple] = [(1, 1, 1)],
        label: list[str] = [],
    ) -> None:
        """__init__

        Init Writter object with all parameters.

        Parameters
        ----------
        fname : str
            file name, with path and extention
        data : np.ndarray
            data to write
        spacing : tuple, optional
            pixel size, by default (1, 1, 1)
        unit : str, optional
            pixel size unit, by default "pixels"
        axes : str, optional
            data dimension axes, by default "TCZYX"
        color : list[tuple], optional
            color list for channels, by default [(1, 1, 1)]
        label : list[str], optional
            label list for channels, by default []
        """
        self._color = color
        self._spacing = spacing
        self._label = label
        self._axes = axes
        self._unit = unit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("\nWriteTiff exception caught:", exc_value)
        return self

    @property
    def fname(self) -> str:
        return self._fname

    @property
    def color(self) -> list[tuple]:
        return self._color

    @property
    def spacing(self) -> tuple:
        return self._spacing

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def axes(self) -> str:
        return self._axes

    @property
    def label(self) -> list[str]:
        return self._label

    @property
    def data(self) -> np.ndarray:
        return self._data

    @fname.setter
    def fname(self, fname: str) -> None:
        self._fname = fname

    @unit.setter
    def unit(self, unit: str) -> None:
        self._unit = unit

    @spacing.setter
    def spacing(self, spacing: tuple) -> None:
        self._spacing = spacing

    @axes.setter
    def axes(self, axes: str) -> None:
        self._axes = axes

    @color.setter
    def color(self, color: list[tuple]) -> None:
        self._color = color

    @label.setter
    def label(self, label: list) -> None:
        self._label = label

    @data.setter
    def data(self, arr: np.ndarray) -> None:
        self._data = arr

    def _transpose_axes(self) -> None:
        expected_axes = "TZCYXS"
        if self.axes == expected_axes:
            self.axes = expected_axes[-(self.data.ndim + 1) : -1]
        else:
            match_axes = [c for c in expected_axes if self.axes.find(c) != -1]
            match_axes = "".join(match_axes)
            self.data = tifffile.transpose_axes(self.data, self.axes, asaxes=match_axes)
            self.axes = match_axes

    def _check_spacing(self) -> None:
        if len(self.spacing) < 3:
            tmp_spacing = list(self.spacing)
            self.spacing = tuple([0.0] * (3 - len(tmp_spacing)) + tmp_spacing)
        if len(self.spacing) > 3:
            self.spacing = self.spacing[:2]
        self.spacing = tuple(reversed(self.spacing))

    def _get_nb_channels(self) -> int:
        return self.data.shape[self.axes.find("C")] if self.axes.find("C") > -1 else 1

    def _check_color(self) -> None:
        nb_channels = self._get_nb_channels()
        if len(self.color) != nb_channels:
            self.color = self.color + [self.color[-1]] * (nb_channels - len(self.color))

    def _chek_labels(self) -> None:
        nb_channels = self._get_nb_channels()
        if len(self.label) != nb_channels:
            add_list = ["C" + str(i) for i in range(len(self.label), nb_channels)]
            self.label = self.label + add_list

    def _expand_luts(self, bin: int = 256) -> list:
        luts = []
        for c in self.color:
            if type(c) is str:
                c = self._color_dict[c]
            norm_color = LinearSegmentedColormap.from_list(
                "Custom", [(0, 0, 0), c], N=bin
            )
            norm_lut = np.ceil(norm_color(range(bin)) * (bin - 1))[:, :-1]
            luts.append(norm_lut.T.astype(np.uint8))
        return luts

    def write(
        self,
        fname: str = None,
        data: np.ndarray = None,
        spacing: tuple = None,
        unit: str = None,
        axes: str = None,
        color: list[tuple] = None,
        label: list[str] = None,
    ) -> None:
        """write

        write data to imageJ format tif file

        Parameters
        ----------
        fname : str, optional
        data : np.ndarray, optional
        spacing : tuple, optional
        unit : str, optional
        axes : str, optional
        color : list[tuple], optional
        label : list[str], optional
        """

        if fname:
            self._fname = fname
        if color:
            self._color = color
        if spacing:
            self._spacing = spacing
        if label:
            self._label = label
        if axes:
            self._axes = axes
        if unit:
            self._unit = unit
        if data:
            self._data = data

        self._transpose_axes()
        self._check_spacing()
        self._check_color()
        self._chek_labels()
        luts = self._expand_luts()

        std_meta = {
            "spacing": self.spacing[-1],
            "unit": self.unit,
            "axes": self.axes,
            "LUTs": luts,
            "Labels": self.label,
            "mode": "composite",
        }

        tifffile.imwrite(
            self.fname,
            self.data,
            imagej=True,
            resolution=(1.0 / np.asarray(self.spacing[:2])),
            metadata=std_meta,
        )
