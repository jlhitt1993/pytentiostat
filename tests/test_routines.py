import mock
import pytest
import unittest

from pytentiostat.routines import _load_arduino, _initialize_arduino, startup_routine, Arduino
from pytentiostat.config_reader import get_rest


class Dummy_port:
    def __init__(self):
        self.description = "default"
        self.device = "com"


class Dummy_arduino:
    def __init__(self):
        self.name = None


class Pin:
    def __init__(self):
        self.pin = "default"


class Dummy_board():
    def test_dummy_board(self):
        da = Dummy_arduino
        da.name = "good_arduino"
        good_port = Dummy_port()
        good_port.description = "Arduino Uno"
        good_port.device = "good com"
        with mock.patch("pytentiostat.routines.Arduino", returnvalue=da,):
            board = _initialize_arduino("good_port")
        assert isinstance(board, Arduino)


def test_load_arduino():
    good_port = Dummy_port()
    good_port.description = "Arduino Uno"
    good_port.device = "good com"
    bad_port = Dummy_port()
    bad_port.description = "Not Arduino"
    with mock.patch(
        "pytentiostat.routines.serial.tools.list_ports.comports",
        return_value=[good_port],
    ):
        com = _load_arduino()
        assert com == "good com"
    with pytest.raises(SystemExit):
        with mock.patch(
            "pytentiostat.routines.serial.tools.list_ports.comports",
            return_value=[bad_port],
        ):
            _load_arduino()
    with pytest.raises(SystemExit):
        _load_arduino()


def test_initialize_arduino():
    da = Dummy_arduino()
    da.name = "good_arduino"

    with pytest.raises(SystemExit):
        _initialize_arduino("bad_port")
    with mock.patch(
        "pytentiostat.routines.Arduino",
        return_value=da,
    ):
        ard = _initialize_arduino("good_port")
        assert ard.name == "good_arduino"


def test_startup_routine():
    good_com = "good com"
    good_board = "good board"
    good_pin = "good_pin"
    pin_a0 = Pin()
    pin_a2 = Pin()
    pin_d9 = Pin()
    with mock.patch("pytentiostat.routines.Arduino.get_pin", returnvalue=[good_pin],):
        with mock.patch("pytentiostat.routines._initialize_arduino", returnvalue=[good_board],):
            with mock.patch("pytentiostat.routines._load_arduino", returnvalue=good_com,):
                with mock.patch("builtins.input", returnvalue=[None]):
                    com, board, pin_a0.pin, pin_a2.pin, pin_d9.pin = startup_routine()

    # with pytest.raises(SystemExit):
    #    startup_routine()
    # assert com == "good com"
    # assert board == "good board"
    # assert pin_a0.pin == "good pin"
    # assert pin_a2.pin == "good pin"
    # assert pin_d9.pin == "good pin"

if __name__ == '__main__':
    test = Dummy_board()
    board = _initialize_arduino("good port")
    print(board)
    test.test_dummy_board(board)
