# Program to Read in a HOC Cell Template and Convert it to a Python Cell Template for Use with NetPyNe and Python


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


# Define list variables
python_file_string = "from neuron import h\n\n\n# Define a Class for Cell\nclass Cell(object):\n    # Create an " \
                     "initialization function that runs when a cell is created\n    # Create sections of the cell, " \
                     "connect cell sections, and create functions to initialize each section\n    def __init__(self):\n"
section_names = []
sec_list_names = []
functionList = []
sec_param_string = []
sec_param_num = []

# Define string variables
init_sec_function = ""
shape_string = ""
subset_string_array = []
geo_string = ""
geom_nseg_string = ""
biophysics_string = ""
tab = "    "
variable = ""

# Define flag variables
basic_shape_flag = -1
subset_flag = -1
geo_flag = -1
geom_nseg_flag = -1
biophysics_flag = -1
section_names_flag = -1
insert_flag = 0
count = 0
sec_confirmed = 0

# Open HOC Template
hoc_temp = open('CellTemplate.hoc', 'r')

# Create and Open New Python Template File
python_temp = open('CellTemplate.py', 'w')

# Read HOC template line by line looking for information that we need to convert to Python
for line in hoc_temp:
    split_line = line.split()
    if split_line:
        # If I find a line starting with create I split, strip, and append the line in proper format to the python
        # template string
        if split_line[0] == "}" and subset_flag > -1:
            # print "exiting subset statement...\n"
            subset_flag = -1
        if split_line[0] == "create":
            #print "Create\n"
            for i in range(1, len(split_line)):
                s = split_line[i].strip(',')
                split_line[i] = s
                section_names.append(split_line[i])
                create_string = "{1}{1}self.{0} = {0} = h.Section(name='{0}', cell=self)\n".format(split_line[i], tab)
                python_file_string += create_string
        # If I find a line starting with connect I split it and append the line in proper format to the python
        # template string
        elif split_line[0] == "connect":
            for i in range(1, len(split_line)):
                s = split_line[i].strip(',')
                split_line[i] = s
                first_pareth = split_line[i].find("(")
                sec_pareth = split_line[i].find(")")
                if i == 1:
                    if first_pareth + 1 == sec_pareth - 1:
                        first_conn_loc = split_line[i][first_pareth + 1]
                    else:
                        first_conn_loc = split_line[i][first_pareth + 1:sec_pareth - 1]
                elif i == 2:
                    if first_pareth + 1 == sec_pareth - 1:
                        sec_conn_loc = split_line[i][first_pareth + 1]
                    else:
                        sec_conn_loc = split_line[i][first_pareth + 1:sec_pareth - 1]
                split_line[i] = split_line[i][0:first_pareth]
            connect_string = "{4}{4}self.{0}.connect(self.{1}({2}), {3})\n".format(split_line[1][0:], split_line[2],
                                                                                   sec_conn_loc, first_conn_loc, tab)
            python_file_string += connect_string
        elif -1 < basic_shape_flag < len(section_names):
            # print "Basic Shape: " + str(section_names_flag)
            section_names_flag += 1
            sec_confirmed = 0
            shape_string = ""
            for i in range(0, len(split_line)):
                variable = ""
                if split_line[i] == section_names[section_names_flag]:
                    # print section_names[section_names_flag]
                    sec_confirmed = 1
                elif sec_confirmed:
                    s = split_line[i].strip('{},()')
                    split_line[i] = s
                    s = split_line[i].strip('{,()')
                    split_line[i] = s
                    # print "Start: " + split_line[i] + "\n"
                    # print "Last Letter: " + split_line[i][-1] + "\n"
                    # print not split_line[i][-1].isalpha()
                    # print split_line[i][-1] != "("
                    while len(split_line[i]) > 0 and not split_line[i][-1].isalpha():
                        if split_line[i][-1] != "(":
                            variable = split_line[i][-1] + variable
                        split_line[i] = split_line[i][:-1]
                    # print "Variable: " + variable
                    # print "End: " + split_line[i] + "\n"
                    if split_line[i] == "pt3dclear":
                        shape_string += "{2}{2}h.{0}(sec={1})\n".format(split_line[i], section_names
                        [section_names_flag], tab)
                    elif split_line[i] == "pt3dadd":
                        shape_string += "{2}{2}h.{0}({1}, ".format(split_line[i], variable, tab)
                    else:
                        if count == 2:
                            shape_string += "{0}, sec={1})\n".format(variable, section_names[section_names_flag])
                            count = 0
                        else:
                            shape_string += "{0}, ".format(variable)
                            count += 1
            basic_shape_flag += 1
            sec_param_string.append(shape_string)
            sec_param_num.append(section_names_flag)
        elif -1 < subset_flag:
            # print split_line
            if subset_flag == 0:
                for i in range(0, len(split_line)):
                    s = split_line[i].strip(',')
                    split_line[i] = s
                    if split_line[i] != "objref":
                        sec_list_names.append(split_line[i])
                        subset_string_array.append("{0}{0}self.{1} = h.SectionList()\n".format(tab, split_line[i]))
            elif subset_flag > 0 and len(split_line) == 2:
                for j in range(0, len(section_names)):
                    if split_line[0] == section_names[j]:
                        for k in range(0, len(sec_list_names)):
                            if split_line[1] == "{0}.append()".format(sec_list_names[k]):
                                s = split_line[1].strip(')')
                                split_line[1] = s
                                subset_string_array.append("{0}{0}self.{1}sec=self.{2})\n".format(tab, split_line[1],
                                                                                                  split_line[0]))
            elif subset_flag > 0 and len(split_line) > 2:
                if split_line[0] == "for":
                    loop_lower = split_line[1].strip(',')
                    loop_lower = loop_lower[-1:]
                    s = split_line[4].strip(')')
                    split_line[4] = s
                    # print loop_lower
                    subset_string_array.append("{0}{0}for i in range({1}, {2}):\n{0}{0}{0}self.{4}sec=self.{3})\n".format(
                        tab, loop_lower, split_line[2], split_line[3], split_line[4]))
            # print subset_string
            subset_flag += 1
        elif -1 < geo_flag < len(section_names):
            # print "Geometry: " + str(section_names_flag)
            section_names_flag += 1
            for i in range(1, len(split_line)):
                if not (split_line[i] == "{" or split_line[i] == "}" or split_line[i] == "="):
                    if is_number(split_line[i]):
                        geo_string += "= {0}\n".format(split_line[i])
                        sec_param_string.append(geo_string)
                        sec_param_num.append(section_names_flag)
                    else:
                        geo_string = "{2}{2}{0}.{1} ".format(section_names[geo_flag], split_line[i], tab)
            geo_flag += 1
        elif -1 < geom_nseg_flag < len(section_names):
            # print "Geom Nseg: " + str(section_names_flag)
            section_names_flag += 1
            for i in range(1, len(split_line)):
                if not (split_line[i] == "{" or split_line[i] == "}" or split_line[i] == "="):
                    if is_number(split_line[i]):
                        geom_nseg_string += "= {0}\n".format(split_line[i])
                        sec_param_string.append(geom_nseg_string)
                        sec_param_num.append(section_names_flag)
                    else:
                        geom_nseg_string = "{2}{2}{0}.{1} ".format(section_names[geom_nseg_flag], split_line[i], tab)
            geom_nseg_flag += 1
        elif -1 < biophysics_flag < len(section_names):
            # print "Biophysics: " + str(section_names_flag)
            for i in range(0, len(split_line)):
                if split_line[i] == "}":
                    biophysics_flag += 1
                    sec_confirmed = 0
                elif sec_confirmed:
                    if not split_line[i] == "=":
                        if is_number(split_line[i]):
                            biophysics_string += " = {0}\n".format(split_line[i])
                            sec_param_string.append(biophysics_string)
                            sec_param_num.append(section_names_flag)
                        elif insert_flag == 1:
                            biophysics_string = "{2}{2}{0}.insert('{1}')\n".format(section_names[biophysics_flag],
                                                                                   split_line[i], tab)
                            sec_param_string.append(biophysics_string)
                            sec_param_num.append(section_names_flag)
                            insert_flag = 0
                        else:
                            if split_line[i] == "insert":
                                insert_flag = 1
                            else:
                                biophysics_string = "{2}{2}{0}.{1}".format(section_names[biophysics_flag], split_line[i]
                                                                           , tab)
                elif split_line[i] == section_names[biophysics_flag]:
                    sec_confirmed = 1
                    section_names_flag += 1
        elif split_line[0] == "proc":
            if split_line[1] == "basic_shape()":
                # print "Basic Shape\n"
                section_names_flag = -1
                basic_shape_flag = 0
                count = 0
            elif split_line[1] == "subsets()":
                # print "Subsets\n"
                section_names_flag = -1
                subset_flag = 0
            elif split_line[1] == "geom_nseg()":
                # print "Geometry Number of Segs\n"
                section_names_flag = -1
                geom_nseg_flag = 0
            elif split_line[1] == "geom()":
                # print "Geometry\n"
                section_names_flag = -1
                geo_flag = 0
            elif split_line[1] == "biophys()":
                # print "Biophysics\n"
                section_names_flag = -1
                biophysics_flag = 0
                sec_confirmed = 0

# Write section names to template
python_file_string += "{0}{0}self.section_names = [".format(tab)
for i in range(0, len(section_names)):
    if i != len(section_names) - 1:
        python_file_string += "'{0}', ".format(section_names[i])
    else:
		python_file_string += "'{0}']\n".format(section_names[i])

# Initialize the section lists of the Cell
for i in range(0, len(sec_list_names)):
    python_file_string += "{0}".format(subset_string_array[i])
python_file_string += "{0}{0}self.init_section_list()\n".format(tab)

for i in range(0, len(section_names)):
    func_name = "{1}# Function that defines the section {0}'s geometry and biophysics\n{1}" \
                "def init_{0}(self):\n{1}{1}{0} = self.{0}\n".format(section_names[i], tab)
    functionList.append(func_name)
    init_sec_function = "{1}{1}self.init_{0}()\n".format(section_names[i], tab)
    python_file_string += init_sec_function
python_file_string += "\n"

for i in range(0, len(section_names)):
    python_file_string += functionList[i]
    for j in range(0, len(sec_param_num)):
        if sec_param_num[j] == i:
            python_file_string += sec_param_string[j]
    python_file_string += "\n"

python_file_string += "{0}# Function to define all section lists\n{0}def init_section_list(self):\n".format(tab)
for i in range(len(sec_list_names), len(subset_string_array)):
    python_file_string += "{0}".format(subset_string_array[i])
python_temp.write(python_file_string)
hoc_temp.close()
python_temp.close()

print section_names
quit()
