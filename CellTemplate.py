from neuron import h


# Define a Class for Cell
class Cell(object):
    # Create an initialization function that runs when a cell is created
    # Create sections of the cell, connect cell sections, and create functions to initialize each section
    def __init__(self):
        self.soma = soma = h.Section(name='soma', cell=self)
        self.atrunk = atrunk = h.Section(name='atrunk', cell=self)
        self.p_dend = p_dend = h.Section(name='p_dend', cell=self)
        self.adendL = adendL = h.Section(name='adendL', cell=self)
        self.adendR = adendR = h.Section(name='adendR', cell=self)
        self.atrunk.connect(self.soma(0), 0)
        self.p_dend.connect(self.soma(1), 0)
        self.adendL.connect(self.atrunk(1), 0)
        self.adendR.connect(self.atrunk(1), 0)
        self.section_names = ['soma', 'atrunk', 'p_dend', 'adendL', 'adendR']
        self.all = h.SectionList()
        self.init_section_list()
        self.init_soma()
        self.init_atrunk()
        self.init_p_dend()
        self.init_adendL()
        self.init_adendR()

    # Function that defines the section soma's geometry and biophysics
    def init_soma(self):
        soma = self.soma
        h.pt3dclear(sec=soma)
        h.pt3dadd(0, 0, 0, 1, sec=soma)
        h.pt3dadd(15, 0, 0, 1, sec=soma)
        soma.L = 25
        soma.diam = 24.75
        soma.nseg = 1
        soma.Ra = 200
        soma.cm = 2.4
        soma.insert('cadyn')
        soma.gcabar_cadyn = 0.00055
        soma.insert('leak')
        soma.glbar_leak = 0.031735
        soma.el_leak = -72
        soma.insert('hd')
        soma.ghdbar_hd = 1.5e-005
        soma.insert('na3')
        soma.gbar_na3 = 0.045
        soma.ar2_na3 = 1
        soma.insert('nap')
        soma.gbar_nap = 0.000575
        soma.insert('kdr')
        soma.gbar_kdr = 0.002
        soma.insert('capool')
        soma.taucas_capool = 1000
        soma.cainf_capool = 5e-005
        soma.fcas_capool = 0.05
        soma.insert('sAHP')
        soma.gsAHPbar_sAHP = 0.0012
        soma.insert('im')
        soma.gbar_im = 0.00253
        soma.insert('kap')
        soma.gkabar_kap = 0.002

    # Function that defines the section atrunk's geometry and biophysics
    def init_atrunk(self):
        atrunk = self.atrunk
        h.pt3dclear(sec=atrunk)
        h.pt3dadd(0, 0, 0, 1, sec=atrunk)
        h.pt3dadd(-59, 0, 0, 1, sec=atrunk)
        atrunk.L = 50
        atrunk.diam = 2
        atrunk.nseg = 3
        atrunk.Ra = 200
        atrunk.cm = 2.4
        atrunk.insert('cadyn')
        atrunk.gcabar_cadyn = 0.00055
        atrunk.insert('leak')
        atrunk.glbar_leak = 0.031735
        atrunk.el_leak = -72
        atrunk.insert('hd')
        atrunk.ghdbar_hd = 1.5e-005
        atrunk.insert('im')
        atrunk.gbar_im = 0.00253
        atrunk.insert('na3')
        atrunk.gbar_na3 = 0.015
        atrunk.ar2_na3 = 1
        atrunk.insert('nap')
        atrunk.gbar_nap = 0.000575
        atrunk.insert('kdr')
        atrunk.gbar_kdr = 0.002
        atrunk.insert('kap')
        atrunk.gkabar_kap = 0.002
        atrunk.insert('capool')
        atrunk.taucas_capool = 1000
        atrunk.cainf_capool = 5e-005
        atrunk.fcas_capool = 0.05
        atrunk.insert('sAHP')
        atrunk.gsAHPbar_sAHP = 0

    # Function that defines the section p_dend's geometry and biophysics
    def init_p_dend(self):
        p_dend = self.p_dend
        h.pt3dclear(sec=p_dend)
        h.pt3dadd(15, 0, 0, 1, sec=p_dend)
        h.pt3dadd(75, 0, 0, 1, sec=p_dend)
        p_dend.L = 400
        p_dend.diam = 5
        p_dend.nseg = 7
        p_dend.Ra = 200
        p_dend.cm = 2.4
        p_dend.insert('cadyn')
        p_dend.gcabar_cadyn = 0.00055
        p_dend.insert('capool')
        p_dend.taucas_capool = 1000
        p_dend.cainf_capool = 5e-005
        p_dend.fcas_capool = 0.05
        p_dend.insert('hd')
        p_dend.ghdbar_hd = 1.5e-005
        p_dend.insert('im')
        p_dend.gbar_im = 0
        p_dend.insert('kap')
        p_dend.gkabar_kap = 0
        p_dend.insert('kdr')
        p_dend.gbar_kdr = 0.002
        p_dend.insert('leak')
        p_dend.glbar_leak = 0.031735
        p_dend.el_leak = -72
        p_dend.insert('na3')
        p_dend.gbar_na3 = 0.015
        p_dend.ar2_na3 = 1
        p_dend.insert('nap')
        p_dend.gbar_nap = 0
        p_dend.insert('sAHP')
        p_dend.gsAHPbar_sAHP = 0

    # Function that defines the section adendL's geometry and biophysics
    def init_adendL(self):
        adendL = self.adendL
        h.pt3dclear(sec=adendL)
        h.pt3dadd(-59, 0, 0, 1, sec=adendL)
        h.pt3dadd(-104, 45, 0, 1, sec=adendL)
        adendL.L = 350
        adendL.diam = 1
        adendL.nseg = 5
        adendL.Ra = 200
        adendL.cm = 2.4
        adendL.insert('cadyn')
        adendL.gcabar_cadyn = 0.00055
        adendL.insert('capool')
        adendL.taucas_capool = 1000
        adendL.cainf_capool = 5e-005
        adendL.fcas_capool = 0.05
        adendL.insert('hd')
        adendL.ghdbar_hd = 1.5e-005
        adendL.insert('im')
        adendL.gbar_im = 0
        adendL.insert('kap')
        adendL.gkabar_kap = 0.002
        adendL.insert('kdr')
        adendL.gbar_kdr = 0.002
        adendL.insert('leak')
        adendL.glbar_leak = 0.031735
        adendL.el_leak = -72
        adendL.insert('na3')
        adendL.gbar_na3 = 0.015
        adendL.ar2_na3 = 1
        adendL.insert('nap')
        adendL.gbar_nap = 0
        adendL.insert('sAHP')
        adendL.gsAHPbar_sAHP = 0

    # Function that defines the section adendR's geometry and biophysics
    def init_adendR(self):
        adendR = self.adendR
        h.pt3dclear(sec=adendR)
        h.pt3dadd(-59, 0, 0, 1, sec=adendR)
        h.pt3dadd(-104, -44, 0, 1, sec=adendR)
        adendR.L = 350
        adendR.diam = 1
        adendR.nseg = 5
        adendR.Ra = 200
        adendR.cm = 2.4
        adendR.insert('sAHP')
        adendR.gsAHPbar_sAHP = 0
        adendR.insert('nap')
        adendR.gbar_nap = 0
        adendR.insert('na3')
        adendR.gbar_na3 = 0.015
        adendR.ar2_na3 = 1
        adendR.insert('leak')
        adendR.glbar_leak = 0.031735
        adendR.el_leak = -72
        adendR.insert('kdr')
        adendR.gbar_kdr = 0.002
        adendR.insert('kap')
        adendR.gkabar_kap = 0.002
        adendR.insert('im')
        adendR.gbar_im = 0
        adendR.insert('hd')
        adendR.ghdbar_hd = 1.5e-005
        adendR.insert('capool')
        adendR.taucas_capool = 1000
        adendR.cainf_capool = 5e-005
        adendR.fcas_capool = 0.05
        adendR.insert('cadyn')
        adendR.gcabar_cadyn = 0.00055

    # Function to define all section lists
    def init_section_list(self):
        self.all.append(sec=self.soma)
        self.all.append(sec=self.atrunk)
        self.all.append(sec=self.p_dend)
        self.all.append(sec=self.adendL)
        self.all.append(sec=self.adendR)
