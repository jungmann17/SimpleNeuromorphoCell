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
ccl = h.IClamp(simpleCell.soma(0.8))
update_iclamp(ccl, 10, 50, -1)

# ----- Create Vectors to Record Plotting Parameters -----
t_vec = h.Vector()
ccl_vec = h.Vector()
vcl_vec = h.Vector()
v_vec = h.Vector()
i_cadyn_vec = h.Vector()
i_im_vec = h.Vector()
il_leak_vec = h.Vector()

# ----- Create Recording for Each Parameter -----
t_vec.record(h._ref_t)
ccl_vec.record(ccl._ref_i)
v_vec.record(simpleCell.soma(0.5)._ref_v)
i_cadyn_vec.record(simpleCell.soma(0.5)._ref_i_cadyn)
i_im_vec.record(simpleCell.soma(0.5)._ref_i_im)
il_leak_vec.record(simpleCell.soma(0.5)._ref_il_leak)

# ----- Run Simulation and Plot Figures -----
h.run()

# ----- Create Plots to Visualize Results -----
pyplot.figure(figsize=(8, 8))
plot_v, = pyplot.plot(t_vec, v_vec, 'b', label='simpleCell.soma.v')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('mV')
pyplot.legend(handles=[plot_v])
pyplot.title('Soma Voltage')
pyplot.figure(figsize=(8, 8))
plot_ccl, = pyplot.plot(t_vec, ccl_vec, 'r', label='ccl.i')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('nA')
pyplot.legend(handles=[plot_ccl])
pyplot.title('Current Clamp')
pyplot.figure(figsize=(8, 8))
plot_i_cadyn, = pyplot.plot(t_vec, i_cadyn_vec, 'b', label='i_cadyn')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('mV')
pyplot.legend(handles=[plot_i_cadyn])
pyplot.title('i_cadyn')
pyplot.figure(figsize=(8, 8))
plot_i_im, = pyplot.plot(t_vec, i_im_vec, 'b', label='i_im')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('mV')
pyplot.legend(handles=[plot_i_im])
pyplot.title('i_im')
pyplot.figure(figsize=(8, 8))
plot_il_leak, = pyplot.plot(t_vec, il_leak_vec, 'b', label='il_leak')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('mV')
pyplot.legend(handles=[plot_il_leak])
pyplot.title('il_leak')
pyplot.subplots_adjust(left=0.065, bottom=0.075, right=0.98, top=0.95, wspace=0.2, hspace=0.25)
pyplot.legend()
pyplot.show()
