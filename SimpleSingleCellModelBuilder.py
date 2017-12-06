# Python Script for Simple Single Cell Model
# Developer: Brenyn Jungmann
# Date: 10/23/2017
# Version: 0.1
# Purpose is to get the users input, build the code necessary, and run the model

# What inputs do we need from the user?
# 1. Simulation Parameters
#   a. h.init
#   b. h.tstop
#   c. h.dt
#   d. h.steps_per_ms
# 2. Stimulation (Current Clamp) Parameters
#   a. amp
#   b. delay
#   c. duration
# 3. Record Plotting Parameters
#   a. Vectors needed - h.Vector()
#   b. What currents/voltages they want to plot

# Imports
import CellTemplate
import os
from neuron import h

# Run Hoc_To_Python.py converter first
os.system('HOC_To_Python.py')

print "\nConverted CellTemplate.hoc properly."

h.load_file("stdgui.hoc")

# All variables needed to get user information and create model_file_string
initVoltage = -60
runTime = 100
integrationInterval = 0.001
stepsPerMs = integrationInterval * 1000000
cc_section = ''
cc_location = -1
i_amp = 0
i_delay = 0
i_dur = 0
v_section = ''
v_location = -1
v_delay = 0
v_dur = 0
v_amp = 0
recording_list = ''
suffix = []
rec_array = []
rec_vec_array = []
rec_vec_string = ''
# plotting_string = ''

# All strings needed to generate new model file
model_file_string = ''
func_def_string = 'def update_iclamp(iclamp, delay, dur, amp):\n    iclamp.delay = float(delay)  # in ms\n' \
                  '    iclamp.dur = float(dur)  # in ms\n    iclamp.amp = float(amp)  # in nA\n\n\n' \
                  'def update_vclamp(vclamp, dur, amp):\n    vclamp.dur[0] = float(dur)  # in ms\n    ' \
                  'vclamp.amp[0] = float(amp)  # in mV\n\n'
header_string = '# Import neuron, pyplot, CellTemplate for access to cell, and the NEURON standard GUI\nfrom neuron ' \
                'import h\nfrom matplotlib import pyplot\nimport CellTemplate\nh.load_file("stdgui.hoc")\n\n\n'
simulation_string = '\n# ----- Simulation Parameters -----\n'
stimulation_string = '\n# ----- Stimulation Parameters -----\n'
vec_creation_string = '\n# ----- Create Vectors to Record Plotting Parameters -----\nt_vec = h.Vector()\nccl_vec = ' \
                      'h.Vector()\nvcl_vec = h.Vector()\n'
cell_creation_string = '\n# ----- Create Single Cell -----\nsimpleCell = CellTemplate.Cell()\n'
rec_creation_string = '\n# ----- Create Recording for Each Parameter -----\nt_vec.record(h._ref_t)\n' \
                      'ccl_vec.record(h._ref_i)\nvcl_vec.record(h._ref_v)\n'
run_sim_string = '\n# ----- Run Simulation and Plot Figures -----\nh.run()\n'

readMeString = '\nSimple Single Cell Model Creator.\nYou will be asked a series of questions to create your ' \
               'model.\nEnter the parameters you would like your model to run with, if you don\'t know what values ' \
               'to use you can type in "default" or "d" and use the default values we have set.\n\nDefault values ' \
               'are as follows:\nInitial Voltage (h.init) = -60 mV\nSimulation Runtime = 100 ms\nIntegration Interval' \
               ' = 0.001\n\nEnter Simulation Parameters\n--------------------------------------- '
simDictionary = {'h.init': initVoltage, 'h.tstop': runTime, 'h.dt': integrationInterval, 'h.steps_per_ms': stepsPerMs,
                 'i_amp': i_amp, 'i_delay': i_delay, 'i_dur': i_dur, 'cc_section': cc_section, 'cc_location':
                     cc_location, 'v_amp': v_amp, 'v_section': v_section, 'v_location': v_location, 'v_delay': v_delay,
                 'v_dur': v_dur}
mod_file_list = []


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def check_input(user_input, dict_name, type_flag):
    if is_number(user_input):
        if type_flag == 0:
            simDictionary[dict_name] = user_input
            return True
        elif type_flag == 1:
            if float(user_input) < 0 or float(user_input) > 1:
                return False
            else:
                simDictionary[dict_name] = user_input
                return True
    else:
        if user_input == "default" or user_input == "Default" or user_input == 'd':
            return True
        else:
            return False


def check_section(user_input, dict_name):
    test_cell = CellTemplate.Cell()
    sec_names = test_cell.section_names
    for sec in sec_names:
        if sec == user_input:
            simDictionary[dict_name] = user_input
            return True
    # print "Determine way to check if section is valid.\n"
    error_string = '\nValid section names are: '
    for sec in sec_names:
        if sec != sec_names[len(sec_names)-1]:
            error_string += '{0}, '.format(sec)
        else:
            error_string += '{0}.'.format(sec)
    print error_string
    return False


def create_cclamp():
    global stimulation_string
    # Type invalid section check to print valid sections.
    check_section('invalid', 'cc_section')
    section = raw_input('\nEnter current clamp section in Cell: ')
    while not check_section(section, 'cc_section'):
        # print "Section is not valid. Please try again."
        section = raw_input('\nInvalid section, please try again: ')
    print '\nValid section, current clamp will be entered into {0}.'.format(section)
    location = raw_input('\nEnter current clamp location in Cell: ')
    while not check_input(location, 'cc_location', 1):
        # print "Invalid location. Please enter a current clamp location.\n"
        location = raw_input('\nInvalid location. Valid locations are between 0 and 1: ')

    amplitude = raw_input('\nEnter current clamp amplitude (nA): ')
    while not check_input(amplitude, 'i_amp', 0):
        # print "Invalid amplitude. Please enter an amplitude in nanoamps.\n"
        amplitude = raw_input('\nInvalid amplitude. Please try again in (nA): ')

    c_delay = raw_input('\nEnter current clamp delay (ms): ')
    while not check_input(c_delay, 'i_delay', 0):
        # print "Please enter a delay in milliseconds.\n"
        c_delay = raw_input('\nInvalid delay. Valid delays are larger than 0: ')

    duration = raw_input("\nEnter current clamp duration (ms): ")
    while not check_input(duration, 'i_dur', 0):
        # print "\nPlease enter a duration in milliseconds."
        duration = raw_input("\nInvalid duration. Valid durations are larger than 0: ")

    stimulation_string += 'ccl = h.IClamp(simpleCell.{0}({1}))\n'.format(simDictionary['cc_section'],
                                                                         simDictionary['cc_location'])
    stimulation_string += 'update_iclamp(ccl, {0}, {1}, {2})\n'.format(simDictionary['i_delay'],
                                                                         simDictionary['i_dur'],
                                                                         simDictionary['i_amp'])


def create_vclamp():
    global stimulation_string
    section = raw_input('\nEnter voltage clamp section in Cell: ')
    while not check_section(section, 'v_section'):
        # print "Section is not valid. Please try again."
        section = raw_input('\nInvalid section. Valid Sections are *, *, *: ')

    location = raw_input('\nEnter voltage clamp location in Cell: ')
    while not check_input(location, 'v_location', 1):
        location = raw_input('\nInvalid location. Valid locations are between 0 and 1: ')

    voltage = raw_input('\nEnter voltage clamp amplitude (mV): ')
    while not check_input(voltage, 'v_amp', 0):
        print "Please enter a voltage in millivolts.\n"
        voltage = raw_input('\nInvalid amplitude. Please try again in (nA): ')

    duration = raw_input("\nEnter voltage clamp duration (ms): ")
    while not check_input(duration, 'v_dur', 0):
        duration = raw_input("\nInvalid duration. Valid durations are larger than 0: ")

    stimulation_string += 'vcl = h.VClamp(simpleCell.{0}({1}))\n'.format(simDictionary['v_section'],
                                                                         simDictionary['v_location'])
    stimulation_string += 'update_vclamp(vcl, {0}, {1})\n'.format(simDictionary['v_dur'], simDictionary['v_amp'])


def get_recording_params():
    possible_record_list = []
    mod_list = []
    range_flag = 0
    count = 0
    record_types = []
    suffix_array = []
    mod_list += [each for each in os.listdir(".") if each.endswith('.mod')]
    for each_file in mod_list:
        file_pointer = open(each_file, 'r')
        for line in file_pointer:
            split_line = line.split()
            if split_line:
                if range_flag > 1 and split_line[0] == "}":
                    break
                if split_line[0] == "SUFFIX":
                    suffix = split_line[1]
                    suffix_array.append(suffix)
                elif split_line[0] == "RANGE":
                    range_flag += 1
                    for i in range(1, len(split_line)):
                        count += 1
                        s = split_line[i].strip(',')
                        split_line[i] = s
                        possible_record_list.append('{0}_{1}'.format(split_line[i], suffix))
        if count != 0:
            record_types.append(count)
            count = 0
    if stimulation_param == 'i':
        possible_record_list.append('ccl_i')
        possible_record_list.append('v')
    elif stimulation_param == 'v':
        possible_record_list.append('vcl_i')
        possible_record_list.append('v')
    elif stimulation_param == 'both':
        possible_record_list.append('ccl_i')
        possible_record_list.append('v')
        possible_record_list.append('vcl_i')
    elif stimulation_param == "none":
        possible_record_list.append('v')
    return possible_record_list, record_types, suffix_array


def print_possible_recording_params(possible_list, num_types, suf_array):
    count = 0
    range_1 = 0
    range_2 = 0
    last_element = 0
    print '\nPossible recording traces can be placed on these currents, voltages, channels, and cell parameters\n' \
          'Cell: v'
    if stimulation_param == 'i':
        print 'Current Clamp: ccl_i'
    elif stimulation_param == 'v':
        print 'Voltage Clamp: vcl_i'
    elif stimulation_param == 'both':
        print 'Current Clamp: ccl_i'
        print 'Voltage Clamp: vcl_i'
    for num in num_types:
        list_string = ''
        if num == num_types[len(num_types) - 1]:
            range_1 = last_element
            range_2 = num
            last_element = num
        elif count == 0:
            range_1 = 0
            range_2 = num
            last_element += num
        elif count > 0:
            range_1 = last_element
            range_2 += num
            last_element += num
        for i in range(range_1, range_2):
            if possible_list[i] != 'ccl_i' or possible_list[i] != 'vcl_i' or possible_list[i] != 'v':
                if possible_list[i] != possible_list[last_element - 1]:
                    list_string += '{0}, '.format(possible_list[i])
                else:
                    list_string += '{0}'.format(possible_list[i])
        print str(suf_array[count]) + ': ' + list_string
        count += 1
    print ''


def check_recording(params):
    count = 0
    valid_array = []
    global rec_array
    rec_array = []
    rec = params.split()
    for param in rec:
        p = param.strip(',')
        param = p
        rec_array.append(param)
        for var in recording_list:
            if param == var:
                valid_array.append(param)
                count += 1
    if count != len(rec_array):
        return False
    else:
        return True


def create_recordings():
    # Fix ccl_i, v, and vcl_i vectors and recording creations
    rec_string = ''
    global rec_creation_string
    rec_params = raw_input('Enter all current, voltage, channel, and cell parameters that you would like to record\n'
                           'divided by a comma. Example: (glbar_leak, gkdrbar_kdr): ')
    while not check_recording(rec_params):
        rec_params = raw_input('Invalid parameter. Please try again: ')

    for vector in rec_array:
        rec_string += '{0}_vec = h.Vector()\n'.format(vector)
        rec_vec_array.append('{0}_vec'.format(vector))

    for i in range(0, len(rec_vec_array)):
        if rec_array[i] != "ccl_i" or rec_array[i] != "vcl_i":
            rec_creation_string += '{0}.record(simpleCell.soma(0.5)._ref_{1})\n'.format(rec_vec_array[i], rec_array[i])
    return rec_string


def print_parameters():
    print("\nParameters that you chose are as follows:\n")
    print("Initial Voltage: " + str(simDictionary['h.init']) + "\n")
    print("Simulation Runtime: " + str(simDictionary['h.tstop']) + "\n")
    print("Integration Interval: " + str(simDictionary['h.dt']) + "\n")


def setup_run_sim():
    plot_string = '\n# ----- Create Plots to Visualize Results -----\n'
    for i in range(0, len(rec_array)):
        if rec_array[i] == 'v':
            plot_string += 'pyplot.figure(figsize=(8, 8))\nplot_v, = pyplot.plot(t_vec, v_vec, \'b\', label=' \
                           '\'simpleCell.soma.v\')\npyplot.xlim(0, h.tstop)\npyplot.ylabel(\'mV\')\npyplot.legend' \
                           '(handles=[plot_v])\npyplot.title(\'Soma Voltage\')\n'
        else:
            plot_string += 'pyplot.figure(figsize=(8, 8))\n'
            plot_string += 'plot_{1}, = pyplot.plot(t_vec, {0}, \'b\', label=\'simpleCell.soma.{1}\')\n'.format(
                rec_vec_array[i], rec_array[i])
            plot_string += 'pyplot.xlim(0, h.tstop)\npyplot.ylabel(\'mV\')\npyplot.legend' \
                           '(handles=[plot_v])\npyplot.title(\'Soma Voltage\')\n'
    plot_string += 'pyplot.subplots_adjust(left=0.065, bottom=0.075, right=0.98, top=0.95, wspace=0.2, ' \
                   'hspace=0.25)\npyplot.legend()\npyplot.show()\n'
    return plot_string


def create_model_file():
    global model_file_string
    model_file_string += header_string + func_def_string + cell_creation_string + simulation_string + \
                         stimulation_string + vec_creation_string + rec_creation_string + plotting_string
    # Open new file for model creation
    new_file = open('NewSimpleModel.py', 'w')
    new_file.write(model_file_string)
    new_file.close()


# Explain to the user what is expected of them and how to use this program
print(readMeString)

# Get simulation parameters from the user and update simulation string
initVoltage = raw_input('Enter Initial Voltage (mV) of Cell: ')
while not check_input(initVoltage, 'h.init', 0):
    print "Please enter a number in millivolts.\n"
    initVoltage = raw_input('\nEnter Initial Voltage (mV) of Cell: ')

simulation_string += 'h.v_init = {0}\n'.format(simDictionary['h.init'])

runTime = raw_input('\nEnter Simulation Runtime (ms): ')
while not check_input(runTime, 'h.tstop', 0):
    print "Please enter a number in milliseconds.\n"
    runTime = raw_input('\nEnter Simulation Runtime (ms): ')

simulation_string += 'h.tstop = {0}\n'.format(simDictionary['h.tstop'])

integrationInterval = raw_input("\nEnter Integration Interval: ")
while not check_input(integrationInterval, 'h.dt', 0):
    print "\nPlease enter a number in milliseconds."
    integrationInterval = raw_input("\nEnter Integration Interval: ")

simulation_string += 'h.dt = {0}\n'.format(simDictionary['h.dt'])
simulation_string += 'h.steps_per_ms = {0}\n'.format(simDictionary['h.steps_per_ms'])

# Get stimulation parameters from the user
print '\nEnter Stimulation Parameters\n---------------------------------------'
stimulation_param = raw_input('What kind on stimulation would you like?\nFor current clamp enter "i", for voltage '
                              'clamp enter "v", for both enter "both", and for no stimulation enter "none": ')
while not (stimulation_param == "i" or stimulation_param == "v" or stimulation_param == "both"
           or stimulation_param == "none"):
    print '\nPlease enter "i" for current clamp, "v" for voltage clamp, "both" for both current and voltage clamp, ' \
          'or "none" for no stimulation.'
    stimulation_param = raw_input('Enter "i", "v", "both", or "none": ')

if stimulation_param == "both":
    create_cclamp()
    create_vclamp()
elif stimulation_param == "i":
    create_cclamp()
elif stimulation_param == "v":
    create_vclamp()
# else:

# Get recording parameters from the user
# noinspection PyRedeclaration
recording_list, num_record_types, suffix = get_recording_params()
print_possible_recording_params(recording_list, num_record_types, suffix)
vec_creation_string += create_recordings()
plotting_string = setup_run_sim()

# Now have all information needed to create the new model file for user to run
create_model_file()

print '\nModel has been create with filename "NewSimpleModel.py". You can run it by running this command: python NewSimpleModel.py'

# run_model = raw_input('Would you like to run the model now? Enter "Yes", "y", "No", or "n": ')
# while not (run_model == "Yes" or run_model == "y" or run_model == "No" or run_model == "n"):
#    run_model = raw_input('Invalid option, please try again: ')
# if run_model == "Yes" or "y":
#    print '\nRunning model...'
# else:
#    print '\nExiting program.'