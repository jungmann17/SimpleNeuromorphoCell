# Import neuron, pyplot, CellTemplate for access to cell, and the NEURON standard GUI
from neuron import h
from matplotlib import pyplot
import CellTemplate
h.load_file("stdgui.hoc")


def update_iclamp(iclamp, delay, dur, amp):
    iclamp.delay = float(delay)  # in ms
    iclamp.dur = float(dur)  # in ms
    iclamp.amp = float(amp)  # in nA


def update_vclamp(vclamp, dur, amp):
    vclamp.dur[0] = float(dur)  # in ms
    vclamp.amp[0] = float(amp)  # in mV


# ----- Create Single Cell -----
simpleCell = CellTemplate.Cell()

# ----- Simulation Parameters -----
h.v_init = -60
h.tstop = 100
h.dt = 0.001
h.steps_per_ms = 1000.0

# ----- Stimulation Parameters -----
ccl = h.IClamp(simpleCell.p_dend(0.2))
update_iclamp(ccl, 10, 10, -10)

# ----- Create Vectors to Record Plotting Parameters -----
t_vec = h.Vector()
ccl_vec = h.Vector()
vcl_vec = h.Vector()
v_vec = h.Vector()

# ----- Create Recording for Each Parameter -----
t_vec.record(h._ref_t)
ccl_vec.record(h._ref_i)
vcl_vec.record(h._ref_v)
v_vec.record(simpleCell.soma(0.5)._ref_v)

# ----- Create Plots to Visualize Results -----
pyplot.figure(figsize=(8, 8))
plot_v, = pyplot.plot(t_vec, v_vec, 'b', label='simpleCell.soma.v')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('mV')
pyplot.legend(handles=[plot_v])
pyplot.title('Soma Voltage')
pyplot.subplots_adjust(left=0.065, bottom=0.075, right=0.98, top=0.95, wspace=0.2, hspace=0.25)
pyplot.legend()
pyplot.show()
