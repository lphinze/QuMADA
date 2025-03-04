# %%
# Copyright (c) 2023 JARA Institute for Quantum Information
#
# This file is part of QuMADA.
#
# QuMADA is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# QuMADA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# QuMADA. If not, see <https://www.gnu.org/licenses/>.
#
# Contributors:
# - Hendrik Bluhm
# - Lennart Hinze

# Ignore flake8 and mypy, as these file is going to be redone either way.
# TODO: Remove these comments then
# flake8: noqa
# type: ignore

# Example measurement for the DecaDAC featuring an interface locking process. Derived from parallel_acquisition_example.

from qcodes.station import Station

from qcodes.dataset import (
    #Measurement,
    #experiments,
    initialise_or_create_database_at,
    #load_by_run_spec,
    load_or_create_experiment,
)

from qumada.measurement.scripts import (
    Generic_1D_Sweep,
    Generic_1D_Sweep_buffered
)

from qumada.instrument.buffers.buffer import (
    #load_trigger_mapping,
    map_triggers,
    #save_trigger_mapping,
)

from qumada.instrument.mapping import (
    #DUMMY_DMM_MAPPING,
    add_mapping_to_instrument,
    map_terminals_gui,
)

#from qumada.instrument.custom_drivers.Dummies.dummy_dac import DummyDac, DummyDac_Channel 
from qumada.instrument.custom_drivers.Harvard.DecadacLock import DecadacLock
from qumada.instrument.custom_drivers.Harvard.Decadac import Decadac

from qumada.instrument.mapping.Harvard.Decadac import DecadacMapping
from qumada.instrument.mapping.base import map_gates_to_instruments

import threading
from pathlib import Path
import numpy as np

import pyvisa

#from qtools_metadata.metadata import create_metadata, save_metadata_object_to_db

#db.api_url = "http://134.61.7.48:9124"
#metadata = create_metadata()

# List visa resources
rm=pyvisa.ResourceManager()
print(rm.list_resources())

# %%
trigger = threading.Event()

station = Station()
dac = DecadacLock(name = "decadac", address = "COM5", min_val = -10, max_val = 10, terminator="\n")
#add_mapping_to_instrument(dac, mapping = DecadacMapping())

station.add_component(dac)

initialise_or_create_database_at(Path.home() / "test_db_DecaDAC.db")

# %% Measurement Setup
parameters = {
    "ohmic": {
        #"voltage": {"type": "gettable"},
        #"current": {"type": "gettable"},
    },
    "gate1": {"voltage": {"type": "dynamic", "setpoints": np.linspace(0, 0.5, 100), "value": 0.5, "delay": 0.01}},
    "gate2": {"voltage": {"type": "dynamic", "setpoints": np.linspace(0, 0.5, 100), "value": 0.5, "delay": 0.01}},
}
# %%

#script = Generic_1D_Sweep_buffered()
script = Generic_1D_Sweep()

script.setup(
    parameters,
    metadata=None,
    ramp_rate=0.5,
    #buffer_settings=buffer_settings,
    #trigger_type="manual",
    #trigger_type="hardware",
    #trigger_start=trigger.set,
    #trigger_reset=trigger.clear,
)

map_terminals_gui(station.components, script.gate_parameters)
#map_triggers(station.components) # fails if useing Generic_1D_Sweep()

load_or_create_experiment("test_exp", sample_name="no_sample")
# %% Run measurement
script.run()

# %%
