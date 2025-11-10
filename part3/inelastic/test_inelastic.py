import git
import os
import sys
import git

# I don't like this, but it's convenient.
_REPO_ROOT = git.Repo(search_parent_directories=True).working_tree_dir
assert (os.path.exists(_REPO_ROOT)), "REPO_ROOT path must exist"
sys.path.append(os.path.join(_REPO_ROOT, "util"))
from utilities import runner, lint, assert_resolvable, clock_start_sequence, reset_sequence
tbpath = os.path.dirname(os.path.realpath(__file__))

import pytest

import cocotb

from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.utils import get_sim_time
from cocotb.triggers import Timer, ClockCycles, RisingEdge, FallingEdge, with_timeout
from cocotb.types import LogicArray, Range

from cocotb_test.simulator import run

from cocotbext.axi import AxiLiteBus, AxiLiteMaster, AxiStreamSink, AxiStreamMonitor, AxiStreamBus

from pytest_utils.decorators import max_score, visibility, tags
   
import random
random.seed(42)

import queue
from itertools import product

timescale = "1ps/1ps"
tests = ['reset_test',
         "nenable_test",
         "enable_test",
         ]

@pytest.mark.parametrize("width_p", [7, 1])
@pytest.mark.parametrize("datapath_reset_p", [1, 0])
@pytest.mark.parametrize("test_name", tests)
@pytest.mark.parametrize("simulator", ["verilator", "icarus"])
@max_score(0)
def test_each(test_name, simulator, width_p, datapath_reset_p):
    # This line must be first
    parameters = dict(locals())
    del parameters['test_name']
    del parameters['simulator']
    runner(simulator, timescale, tbpath, parameters, testname=test_name)

# Opposite above, run all the tests in one simulation but reset
# between tests to ensure that reset is clearing all state.
# Opposite above, run all the tests in one simulation but reset
# between tests to ensure that reset is clearing all state.
@pytest.mark.parametrize("width_p", [7, 1])
@pytest.mark.parametrize("datapath_reset_p", [1, 0])
@pytest.mark.parametrize("simulator", ["verilator", "icarus"])
@max_score(.5)
def test_all(simulator, width_p, datapath_reset_p):
    # This line must be first
    parameters = dict(locals())
    del parameters['simulator']
    runner(simulator, timescale, tbpath, parameters)

@pytest.mark.parametrize("width_p", [1])
@pytest.mark.parametrize("datapath_reset_p", [1, 0])
@pytest.mark.parametrize("simulator", ["verilator"])
@max_score(.4)
def test_lint(simulator, width_p, datapath_reset_p):
    # This line must be first
    parameters = dict(locals())
    del parameters['simulator']
    lint(simulator, timescale, tbpath, parameters)

@pytest.mark.parametrize("width_p", [1])
@pytest.mark.parametrize("datapath_reset_p", [1, 0])
@pytest.mark.parametrize("simulator", ["verilator"])
@max_score(.1)
def test_style(simulator, width_p, datapath_reset_p):
    # This line must be first
    parameters = dict(locals())
    del parameters['simulator']
    lint(simulator, timescale, tbpath, parameters, compile_args=["--lint-only", "-Wwarn-style", "-Wno-lint"])

async def wait_for_signal(dut, signal, value):
    signal = getattr(dut, signal)
    while(signal.value.is_resolvable and signal.value != value):
        await FallingEdge(dut.clk_i)

@cocotb.test()
async def reset_test(dut):
    """Test for Initialization"""

    clk_i = dut.clk_i
    reset_i = dut.reset_i
    data_i = dut.data_i
    en_i = dut.en_i
    data_o = dut.data_o
    width_p = dut.width_p.value

    await clock_start_sequence(clk_i)
    await reset_sequence(clk_i, reset_i, 10)

    if (dut.datapath_reset_p.value == 1):
        assert data_o.value.is_resolvable, f"Unresolvable value in data_o after reset (x or z in some or all bits) at Time {get_sim_time(units='ns')}ns."
        assert data_o.value == 0, f"data_o was not 0 after reset! Time {get_sim_time(units='ns')}ns."

@cocotb.test()
async def enable_test(dut):
    """Test if enable works correctly"""

    clk_i = dut.clk_i
    reset_i = dut.reset_i
    data_i = dut.data_i
    en_i = dut.en_i
    data_o = dut.data_o
    width_p = dut.width_p.value

    await clock_start_sequence(clk_i)
    await reset_sequence(clk_i, reset_i, 10)

    en_i.value = 0
    data_i.value = 0

    await FallingEdge(clk_i)

    en_i.value = 1
    data_i.value = LogicArray('1' * width_p)
    expected = LogicArray('1' * width_p).integer

    await FallingEdge(clk_i)

    assert data_o.value.is_resolvable, f"Unresolvable value (x or z in some or all bits) at Time {get_sim_time(units='ns')}ns."
    assert data_o.value == expected, f"Incorrect result read from data_o: Expected {expected}. Got: {data_o.value} at Time {get_sim_time(units='ns')}ns."

@cocotb.test()
async def nenable_test(dut):
    """Test if !enable works correctly"""

    clk_i = dut.clk_i
    reset_i = dut.reset_i
    data_i = dut.data_i
    en_i = dut.en_i
    data_o = dut.data_o
    width_p = dut.width_p.value

    await clock_start_sequence(clk_i)
    await reset_sequence(clk_i, reset_i, 10)

    en_i.value = 0
    data_i.value = 0

    await FallingEdge(clk_i)

    en_i.value = 1
    data_i.value = LogicArray('1' * width_p)
    expected = LogicArray('1' * width_p).integer

    await FallingEdge(clk_i)

    assert data_o.value.is_resolvable, f"Unresolvable value (x or z in some or all bits) at Time {get_sim_time(units='ns')}ns."
    assert data_o.value == expected, f"Incorrect result read from data_o: Expected {expected}. Got: {data_o.value} at Time {get_sim_time(units='ns')}ns."

    en_i.value = 0
    data_i.value = LogicArray('1' * width_p)
    expected = data_o.value

    await FallingEdge(clk_i)

    assert data_o.value.is_resolvable, f"Unresolvable value (x or z in some or all bits) at Time {get_sim_time(units='ns')}ns."
    assert data_o.value == expected, f"Incorrect result read from data_o: Expected {expected}. Got: {data_o.value} at Time {get_sim_time(units='ns')}ns."
