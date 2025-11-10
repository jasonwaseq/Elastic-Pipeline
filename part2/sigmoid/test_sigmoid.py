import git
import os
import sys
import git
import math

# I don't like this, but it's convenient.
_REPO_ROOT = git.Repo(search_parent_directories=True).working_tree_dir
assert (os.path.exists(_REPO_ROOT)), "REPO_ROOT path must exist"
sys.path.append(os.path.join(_REPO_ROOT, "util"))
from utilities import runner, lint, assert_resolvable
tbpath = os.path.dirname(os.path.realpath(__file__))

import pytest

import cocotb

from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.utils import get_sim_time
from cocotb.triggers import Timer, ClockCycles, RisingEdge, FallingEdge, with_timeout
from cocotb.types import LogicArray, Range
from cocotb.binary import BinaryValue

from cocotb_test.simulator import run

from cocotbext.axi import AxiLiteBus, AxiLiteMaster, AxiStreamSink, AxiStreamMonitor, AxiStreamBus

from pytest_utils.decorators import max_score, visibility, tags
   
timescale = "1ps/1ps"

tests = ['init_test',
         'sse_test'
         ]
   
@pytest.mark.parametrize("test_name", tests)
@pytest.mark.parametrize("simulator", ["verilator", "icarus"])
@max_score(0)
def test_each(test_name, simulator):
    # This line must be first
    parameters = dict(locals())
    del parameters['test_name']
    del parameters['simulator']
    runner(simulator, timescale, tbpath, parameters, testname=test_name, defs=[f'HEXPATH="{tbpath}/"'])

@pytest.mark.parametrize("simulator", ["verilator"])
@max_score(.4)
def test_lint(simulator):
    # This line must be first
    parameters = dict(locals())
    del parameters['simulator']
    lint(simulator, timescale, tbpath, parameters, defs=[f'HEXPATH="{tbpath}/"'])

@pytest.mark.parametrize("simulator", ["verilator"])
@max_score(.1)
def test_style(simulator):
    # This line must be first
    parameters = dict(locals())
    del parameters['simulator']
    lint(simulator, timescale, tbpath, parameters, compile_args=["--lint-only", "-Wwarn-style", "-Wno-lint"], defs=[f'HEXPATH="{tbpath}/"'])

@pytest.mark.parametrize("simulator", ["verilator", "icarus"])
@max_score(3)
def test_all(simulator):
    # This line must be first
    parameters = dict(locals())
    del parameters['simulator']
    runner(simulator, timescale, tbpath, parameters, defs=[f'HEXPATH="{tbpath}/"'])

@cocotb.test()
async def init_test(dut):
    """Test for Basic Connectivity"""

    x_i = dut.x_i
    x_i.value = 0

    await Timer(1, units="ns")

    assert dut.f_o.value.is_resolvable, f"Unresolvable value (x or z in some or all bits) of f_o at Time {get_sim_time(units='ns')}ns."


@cocotb.test()
async def sse_test(dut):

    x_i = dut.x_i
    f_o = dut.f_o
    x_i.value = 0

    await Timer(1, units="ns")    

    assert f_o.value.is_resolvable, f"Unresolvable value (x or z in some or all bits) of f_o at Time {get_sim_time(units='ns')}ns."

    sse = 0
    
    xs = [i for i in range(-128, 128)]
    os = [256 / (1 + math.exp(-x/32)) for x in xs]
    for (x,o) in zip(xs, os):
        x_i.value = x
        await Timer(1, units="ns")
        assert f_o.value.is_resolvable, f"Unresolvable value (x or z in some or all bits) of f_o at Time {get_sim_time(units='ns')}ns."

        err = f_o.value - o
        sse = sse + (err ** 2)

    rmse = (sse/len(xs))**.5
    assert rmse < 5, "RMSE greater than 5!"
