# AUTOGENERATED! DO NOT EDIT! File to edit: XmlElementTree.ipynb (unless otherwise specified).

__all__ = ['Dict2Data', 'read_asxml', 'exclude_kpts', 'get_ispin', 'get_summary', 'get_kpts', 'get_tdos', 'get_evals',
           'get_bands_pro_set', 'get_dos_pro_set', 'get_structure', 'export_vasprun', 'load_export', 'dump_dict',
           'load_from_dump']

# Cell
import numpy
from nbdev import show_doc
class Dict2Data(dict):
    """
    - Returns a Data object with dictionary keys as attributes of Data accessible by dot notation.
    - **Parmeters**
        - dict : Python dictionary (nested as well) containing any python data types.
    - **Methods**
        - to_dict()  : Converts a Data object to dictionary if it could be made a dictionary, otherwise throws relevant error.
        - to_json()  : Converts to json str or save to file if `outfil` given. Accepts `indent` as parameter.
        - to_pickle(): Converts to bytes str or save to file if `outfile` given.
    - **Example**
        > x = Dict2Data({'A':1,'B':{'C':2}})
        > x
        > Data(
        >     A = 1
        >     B = Data(
        >         C = 2
        >         )
        >     )
        > x.B.to_dict()
        > {'C': 2}
    """
    def __init__(self,d):
        if isinstance(d,Dict2Data):
            d = d.to_dict() # if nested Dict2Dataects, must expand here.
        for a,b in d.items():
            if isinstance(b,Dict2Data):
                b = b.to_dict() # expands self instance !must here.
            if isinstance(b,(list,tuple)):
                setattr(self,a,[Dict2Data(x) if isinstance(x,dict) else x for x in b])
            else:
                setattr(self,a,Dict2Data(b) if isinstance(b,dict) else b)
    def to_dict(self):
        """
        - Converts a `Dict2Data` object (root or nested level) to a dictionary.
        """
        result = {}
        for k,v in self.__dict__.items():
            if isinstance(v,Dict2Data):
                result.update({k:Dict2Data.to_dict(v)})
            else:
                result.update({k:v})
        return result
    def to_json(self,outfile=None,indent=1):
        """
        - Dumps a `Dict2Data` object (root or nested level) to json.
        - **Parameters**
            - outfile : Default is None and returns string. If given, writes to file.
            - indent  : Json indent. Default is 1.
        """
        from .vr_parser import dump_dict
        return dump_dict(self,dump_to='json',outfile=outfile,indent=indent)

    def to_pickle(self,outfile=None):
        """
        - Dumps a `Dict2Data` object (root or nested level) to pickle.
        - **Parameters**
            - outfile : Default is None and returns string. If given, writes to file.
        """
        from .vr_parser import dump_dict
        return dump_dict(self,dump_to='pickle',outfile=outfile)

    def __repr__(self):
        items= []
        for k,v in self.__dict__.items():
            if type(v) not in (str,float,int,range) and not isinstance(v,Dict2Data):
                if isinstance(v,numpy.ndarray):
                    v = "<{}:shape={}>".format(v.__class__.__name__,numpy.shape(v))
                elif type(v) in (list,tuple):
                    v = ("<{}:len={}>".format(v.__class__.__name__,len(v)) if len(v) > 10 else v)
                else:
                    v = v.__class__
            if isinstance(v,Dict2Data):
                v = repr(v).replace("\n","\n    ")
            items.append(f"    {k} = {v}")

        return "Data(\n{}\n)".format('\n'.join(items))
    def __getstate__(self):
        pass  #This is for pickling

# Cell
def read_asxml(path=None,suppress_warning=False):
    """
    - Reads a big vasprun.xml file into memory once and then apply commands.
    If current folder contains `vasprun.xml` file, it automatically picks it.

    - **Parameters**
        - path             : Path/To/vasprun.xml
        - suppress_warning : False by defualt. Warns about memory usage for large files > 100 MB.
    - **Returns**
        - xml_data : Xml object to use in other functions
    """
    if(path==None):
        path='./vasprun.xml'
    import xml.etree.ElementTree as ET
    import os
    if not os.path.isfile(path):
        print("File: '{}'' does not exist!".format(path))
        return # This is important to stop further errors.
    elif 'vasprun.xml' not in path:
        print("File should end with 'vasprun.xml', prefixes are allowed.")
        return # This is important to stop further errors.
    else:
        if suppress_warning == False:
            from .g_utils import get_file_size,printy,printg
            fsize = get_file_size(path)
            value = float(fsize.split()[0])
            print_str = """
            File: {} is large ({}).
            It may consume a lot of memory (generally 3 times the file size).

            An alternative way is to parse vasprun.xml is by using `Vasp2Visual` module in Powershell by command
            `pivotpy.load_export('path/to/vasprun.xml'), which runs underlying powershell functions to load data whith
            efficient memory managment. It works on Windows/Linux/MacOS if you have powershell core and Vasp2Visual
            installed on it.

            Hit `Ctrl+C` if you do not get `successful!` prompt in <10 sec, then use `load_export()` instead with
            max_filled/max_empty given, default is 10/10 bands above and below VBM.
            """.format(path,fsize)
            if 'MB' in fsize and value > 100:
                printy(print_str)
            elif 'GB' in fsize and value > 1:
                printy(print_str)
                value = value*1024 # To show in MBs for later Use.

        tree = ET.parse(path)
        xml_data = tree.getroot()
        if suppress_warning == False and value > 100:
            printg('\n      successful!\n')
        return xml_data

# Cell
def exclude_kpts(xml_data=None):
    """
    - Returns number of kpoints to exclude used from IBZKPT.
    - **Parameters**
        - xml_data : From `read_asxml` function
    - **Returns**
        - int      : Number of kpoints to exclude.
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    for kpts in xml_data.iter('varray'):
        if(kpts.attrib=={'name': 'weights'}):
            weights=[float(arr.text.strip()) for arr in kpts.iter('v')]
    exclude=[]
    [exclude.append(item) for item in weights if item!=weights[-1]];
    skipk=len(exclude) #that much to skip
    return skipk

# Cell
def get_ispin(xml_data=None):
    """
    - Returns value of ISPIN.
    - **Parameters**
        - xml_data : From `read_asxml` function
    - **Returns**
        - int      : Value of ISPIN.
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    for item in xml_data.iter('i'):
        if(item.attrib=={'type': 'int', 'name': 'ISPIN'}):
            return int(item.text)

# Cell
def get_summary(xml_data=None):
    """
    - Returns overview of system parameters.
    - **Parameters**
        - xml_data : From `read_asxml` function
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes accessible via dot notation.
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    for i_car in xml_data.iter('incar'):
        incar={car.attrib['name']:car.text.strip() for car in i_car}
    n_ions=[int(atom.text) for atom in xml_data.iter('atoms')][0]
    type_ions=[int(atom_types.text) for atom_types in xml_data.iter('types')][0]
    elem=[info[0].text.strip() for info in xml_data.iter('rc')]
    elem_name=[]; #collect IONS names
    [elem_name.append(item) for item in elem[:-type_ions] if item not in elem_name]
    elem_index=[0]; #start index
    [elem_index.append((int(entry)+elem_index[-1])) for entry in elem[-type_ions:]];
    ISPIN=get_ispin(xml_data=xml_data)
    # Fields
    try:
        for pro in xml_data.iter('partial'):
            dos_fields=[field.text.strip() for field in pro.iter('field')]
            dos_fields = [field for field in dos_fields if 'energy' not in field]
    except:
        dos_fields = []
    for i in xml_data.iter('i'): #efermi for condition required.
        if(i.attrib=={'name': 'efermi'}):
            efermi=float(i.text)
    #Writing information to a dictionary
    info_dic={'SYSTEM':incar['SYSTEM'],'NION':n_ions,'TypeION':type_ions,'ElemName':elem_name,'ElemIndex':elem_index,\
        'E_Fermi': efermi,'ISPIN':ISPIN,'fields':dos_fields,'incar':incar}
    return Dict2Data(info_dic)

# Cell
def get_kpts(xml_data=None,skipk=0,joinPathAt=[]):
    """
    - Returns kpoints and calculated kpath.
    - **Parameters**
        - xml_data   : From `read_asxml` function
        - skipk      : Number of initil kpoints to skip
        - joinPathAt : List of indices of kpoints where path is broken
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes `kpath` and `kpoints`
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    import numpy as np
    for kpts in xml_data.iter('varray'):
        if(kpts.attrib=={'name': 'kpointlist'}):
            kpoints=[[float(item) for item in arr.text.split()] for arr in kpts.iter('v')]
    kpoints=np.array(kpoints[skipk:])
    #KPath solved.
    kpath=[0];pts=kpoints
    [kpath.append(np.round(np.sqrt(np.sum((pt1-pt2)**2))+kpath[-1],6)) for pt1,pt2 in zip(pts[:-1],pts[1:])]
    # If broken path, then join points.
    try:
        joinPathAt
    except NameError:
        joinPathAt = []
    if(joinPathAt):
        for pt in joinPathAt:
            kpath[pt:]=kpath[pt:]-kpath[pt]+kpath[pt-1]

    return Dict2Data({'NKPTS':len(kpoints),'kpoints':kpoints,'kpath':kpath})

# Cell
def get_tdos(xml_data=None,spin_set=1,elim=[]):
    """
    - Returns total dos for a spin_set (default 1) and energy limit. If spin-polarized calculations, gives SpinUp and SpinDown keys as well.
    - **Parameters**
        - xml_data : From `read_asxml` function
        - spin_set : int, default is 1.and
        - elim     : List [min,max] of energy, default empty.
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes E_Fermi, ISPIN,tdos.
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    import numpy as np #Mandatory to avoid errors.
    tdos=[]; #assign for safely exit if wrong spin set entered.
    ISPIN=get_ispin(xml_data=xml_data)
    for neighbor in xml_data.iter('dos'):
        for item in neighbor[1].iter('set'):
            if(ISPIN==1 and spin_set==1):
                if(item.attrib=={'comment': 'spin 1'}):
                    tdos=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
            if(ISPIN==2 and spin_set==1):
                if(item.attrib=={'comment': 'spin 1'}):
                    tdos_1=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
                if(item.attrib=={'comment': 'spin 2'}):
                    tdos_2=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
                    tdos = {'SpinUp':tdos_1,'SpinDown':tdos_2}
            if(spin_set!=1): #can get any
                if(item.attrib=={'comment': 'spin {}'.format(spin_set)}):
                    tdos=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
    for i in xml_data.iter('i'): #efermi for condition required.
        if(i.attrib=={'name': 'efermi'}):
            efermi=float(i.text)
    dos_dic= {'E_Fermi':efermi,'ISPIN':ISPIN,'tdos':tdos}
    #Filtering in energy range.
    if elim: #check if elim not empty
        if(ISPIN==1 and spin_set==1):
            up_ind=np.max(np.where(tdos[:,0]-efermi<=np.max(elim)))+1
            lo_ind=np.min(np.where(tdos[:,0]-efermi>=np.min(elim)))
            tdos=tdos[lo_ind:up_ind,:]
        if(ISPIN==2 and spin_set==1):
            up_ind=np.max(np.where(tdos['SpinUp'][:,0]-efermi<=np.max(elim)))+1
            lo_ind=np.min(np.where(tdos['SpinUp'][:,0]-efermi>=np.min(elim)))
            tdos = {'SpinUp':tdos_1[lo_ind:up_ind,:],'SpinDown':tdos_2[lo_ind:up_ind,:]}
        if(spin_set!=1):
            up_ind=np.max(np.where(tdos[:,0]-efermi<=np.max(elim)))+1
            lo_ind=np.min(np.where(tdos[:,0]-efermi>=np.min(elim)))
            tdos=tdos[lo_ind:up_ind,:]
        dos_dic= {'E_Fermi':efermi,'ISPIN':ISPIN,'grid_range':range(lo_ind,up_ind),'tdos':tdos}
    return Dict2Data(dos_dic)

# Cell
def get_evals(xml_data=None,skipk=None,elim=[]):
    """
    - Returns eigenvalues as numpy array. If spin-polarized calculations, gives SpinUp and SpinDown keys as well.
    - **Parameters**
        - xml_data : From `read_asxml` function
        - skipk    : Number of initil kpoints to skip.
        - elim     : List [min,max] of energy, default empty.
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes evals and related parameters.
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    import numpy as np #Mandatory to avoid errors.
    evals=[]; #assign for safely exit if wrong spin set entered.
    ISPIN=get_ispin(xml_data=xml_data)
    if skipk!=None:
        skipk=skipk
    else:
        skipk=exclude_kpts(xml_data=xml_data) #that much to skip by default
    for neighbor in xml_data.iter('eigenvalues'):
            for item in neighbor[0].iter('set'):
                if(ISPIN==1):
                    if(item.attrib=={'comment': 'spin 1'}):
                        evals=np.array([[float(th.text.split()[0]) for th in thing] for thing in item])[skipk:]
                        NBANDS=len(evals[0])
                if(ISPIN==2):
                    if(item.attrib=={'comment': 'spin 1'}):
                        eval_1=np.array([[float(th.text.split()[0]) for th in thing] for thing in item])[skipk:]
                    if(item.attrib=={'comment': 'spin 2'}):
                        eval_2=np.array([[float(th.text.split()[0]) for th in thing] for thing in item])[skipk:]
                        evals={'SpinUp':eval_1,'SpinDown':eval_2}
                        NBANDS=len(eval_1[0])

    for i in xml_data.iter('i'): #efermi for condition required.
        if(i.attrib=={'name': 'efermi'}):
            efermi=float(i.text)
    evals_dic={'E_Fermi':efermi,'ISPIN':ISPIN,'NBANDS':NBANDS,'evals':evals}
    if elim: #check if elim not empty
        if(ISPIN==1):
            up_ind=np.max(np.where(evals[:,:]-efermi<=np.max(elim))[1])+1
            lo_ind=np.min(np.where(evals[:,:]-efermi>=np.min(elim))[1])
            evals=evals[:,lo_ind:up_ind]
        if(ISPIN==2):
            up_ind=np.max(np.where(eval_1[:,:]-efermi<=np.max(elim))[1])+1
            lo_ind=np.min(np.where(eval_1[:,:]-efermi>=np.min(elim))[1])
            evals={'SpinUp':eval_1[:,lo_ind:up_ind],'SpinDown':eval_2[:,lo_ind:up_ind]}
        NBANDS=up_ind-lo_ind #update Bands
        evals_dic={'E_Fermi':efermi,'ISPIN':ISPIN,'NBANDS': int(NBANDS),'bands_range':range(lo_ind,up_ind),'evals':evals}
    return Dict2Data(evals_dic)

# Cell
def get_bands_pro_set(xml_data=None,spin_set=1,skipk=0,bands_range=None):
    """
    - Returns bands projection of a spin_set(default 1) as numpy array. If spin-polarized calculations, gives SpinUp and SpinDown keys as well.
    - **Parameters**
        - xml_data    : From `read_asxml` function
        - skipk       : Number of initil kpoints to skip (Default 0).
        - spin_set    : Spin set to get, default is 1.
        - bands_range : If elim used in `get_evals`,that will return bands_range to use here..
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes of bands projections and related parameters.
    """
    import numpy as np
    import pivotpy.g_utils as gu
    if(bands_range!=None):
        check_list=list(bands_range)
        if(check_list==[]):
            return gu.printr("No bands prjections found in given energy range.")
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    #Collect Projection fields
    fields=[];
    for pro in xml_data.iter('projected'):
        for arr in pro.iter('field'):
            if('eig' not in arr.text and 'occ' not in arr.text):
                fields.append(arr.text.strip())
    #Get NIONS for reshaping data
    n_ions=[int(atom.text) for atom in xml_data.iter('atoms')][0]
    #check if bands_range provided. if not get all bands in projection.
    if bands_range==None:
        NBANDS=get_evals(xml_data=xml_data,skipk=skipk).NBANDS
        bands_range=range(0,NBANDS)
    else:
        bands_range=bands_range

    bands=[];bands_range=[ind+1 for ind in bands_range];
    for i in bands_range: #Bands loop.index written from 1.
        pro=[];
        for spin in xml_data.iter('set'):
            if(spin.attrib=={'comment': 'spin{}'.format(spin_set)}):
                for band in spin.iter('set'):
                    if(band.attrib=={'comment': 'band {}'.format(i)}):
                        for r in band.iter('r'):
                            pro.append(r.text)
        bands.append(pro)
    flist=[[[float(item) for item in entry.split()] for entry in pro] for pro in bands]
    #data shape is (NION,NKPTS,NBANDS,nProjections)
    data=np.reshape(flist,(len(flist),-1,n_ions,len(fields))).transpose([2,1,0,3])
    final_data=data[:,skipk:,:,:] #skip useless kpoints
    return Dict2Data({'labels':fields,'pros':final_data})

# Cell
def get_dos_pro_set(xml_data=None,spin_set=1,dos_range=None):
    """
    - Returns dos projection of a spin_set(default 1) as numpy array. If spin-polarized calculations, gives SpinUp and SpinDown keys as well.
    - **Parameters**
        - xml_data    : From `read_asxml` function
        - spin_set    : Spin set to get, default 1.
        - dos_range   : If elim used in `get_tdos`,that will return dos_range to use here..
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes of dos projections and related parameters.
    """
    import numpy as np
    import pivotpy.g_utils as gu
    if(dos_range!=None):
        check_list=list(dos_range)
        if(check_list==[]):
            return gu.printr("No DOS prjections found in given energy range.")
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    n_ions=get_summary(xml_data=xml_data).NION
    for pro in xml_data.iter('partial'):
        dos_fields=[field.text.strip()for field in pro.iter('field')]
        #Collecting projections.
        dos_pro=[]; set_pro=[]; #set_pro=[] in case spin set does not exists
        for ion in range(n_ions):
            for node in pro.iter('set'):
                if(node.attrib=={'comment': 'ion {}'.format(ion+1)}):
                    for spin in node.iter('set'):
                        if(spin.attrib=={'comment': 'spin {}'.format(spin_set)}):
                            set_pro=[[float(entry) for entry in r.text.split()] for r in spin.iter('r')]
            dos_pro.append(set_pro)
    if dos_range==None: #full grid computed.
        dos_pro=np.array(dos_pro) #shape(NION,e_grid,pro_fields)
    else:
        dos_range=list(dos_range)
        min_ind=dos_range[0]
        max_ind=dos_range[-1]+1
        dos_pro=np.array(dos_pro)[:,min_ind:max_ind,:]
    final_data=np.array(dos_pro) #shape(NION,e_grid,pro_fields)
    return Dict2Data({'labels':dos_fields,'pros':final_data})

# Cell
def get_structure(xml_data=None):
    """
    - Returns structure's volume,basis,positions and rec-basis.
    - **Parameters**
        - xml_data : From `read_asxml` function.
    - **Returns**
        - Data     : pivotpy.Dict2Data with attibutes volume,basis,positions and rec_basis.
    """
    if(xml_data==None):
        xml_data=read_asxml()
    if not xml_data:
        return
    import numpy as np
    for final in xml_data.iter('structure'):
        if(final.attrib=={'name': 'finalpos'}):
            for i in final.iter('i'):
                volume=float(i.text)
            for arr in final.iter('varray'):
                if(arr.attrib=={'name': 'basis'}):
                    basis=[[float(a) for a in v.text.split()] for v in arr.iter('v')]
                if(arr.attrib=={'name': 'rec_basis'}):
                    rec_basis=[[float(a) for a in v.text.split()] for v in arr.iter('v')]
                if(arr.attrib=={'name': 'positions'}):
                    positions=[[float(a) for a in v.text.split()] for v in arr.iter('v')]
    st_dic={'volume': volume,'basis': np.array(basis),'rec_basis': np.array(rec_basis),'positions': np.array(positions)}
    return Dict2Data(st_dic)

# Cell
def export_vasprun(path=None,skipk=None,elim=[],joinPathAt=[],shift_kpath=0):
    """
    - Returns a full dictionary of all objects from `vasprun.xml` file. It first try to load the data exported by powershell's `Export-VR(Vasprun)`, which is very fast for large files. It is recommended to export large files in powershell first.
    - **Parameters**
        - path       : Path to `vasprun.xml` file. Default is `'./vasprun.xml'`.
        - skipk      : Default is None. Automatically detects kpoints to skip.
        - elim       : List [min,max] of energy interval. Default is [], covers all bands.
        - joinPathAt : List of indices of kpoints where path is broken.
        - shift_kpath: Default 0. Can be used to merge multiple calculations on single axes side by side.
    - **Returns**
        - Data : Data accessible via dot notation containing nested Data objects:
            - sys_info  : System Information
            - dim_info  : Contains information about dimensions of returned objects.
            - kpoints   : numpy array of kpoints with excluded IBZKPT points
            - kpath     : 1D numpy array directly accessible for plot.
            - bands     : Data containing bands.
            - tdos      : Data containing total dos.
            - pro_bands : Data containing bands projections.
            - pro_dos   : Data containing dos projections.
            - poscar    : Data containing basis,positions, rec_basis and volume.
    """
    import numpy as np, os
    import pivotpy.vr_parser as vp

    # Try to get files if exported data in PowerShell.
    req_files = ['Bands.txt','tDOS.txt','pDOS.txt','Projection.txt','SysInfo.py']
    if path and os.path.isfile(path):
        req_files = [os.path.join(os.path.dirname(os.path.abspath(path)),f) for f in req_files]
    logic = [os.path.isfile(f) for f in req_files]
    if not False in logic:
        from IPython.display import clear_output
        print('Loading from PowerShell Exported Data...')
        clear_output(wait=True)
        return vp.load_export(path=(path if path else './vasprun.xml'))

    # Proceed if not files from PWSH
    if(path==None):
        xml_data=vp.read_asxml(path='./vasprun.xml')
    else:
        xml_data=vp.read_asxml(path=path)
    if not xml_data:
        return
    #First exclude unnecessary kpoints. Includes only same weight points
    if skipk!=None:
        skipk=skipk
    else:
        skipk=vp.exclude_kpts(xml_data=xml_data) #that much to skip by default
    info_dic=vp.get_summary(xml_data=xml_data) #Reads important information of system.
    #KPOINTS
    kpts=vp.get_kpts(xml_data=xml_data,skipk=skipk,joinPathAt=joinPathAt)
    #EIGENVALS
    eigenvals=vp.get_evals(xml_data=xml_data,skipk=skipk,elim=elim)
    #TDOS
    tot_dos=vp.get_tdos(xml_data=xml_data,spin_set=1,elim=elim)
    #Bands and DOS Projection
    if elim:
        bands_range=eigenvals.bands_range
        grid_range=tot_dos.grid_range
    else:
        bands_range=None #projection function will read itself.
        grid_range=None
    if(info_dic.ISPIN==1):
        pro_bands=vp.get_bands_pro_set(xml_data=xml_data,spin_set=1,skipk=skipk,bands_range=bands_range)
        pro_dos=vp.get_dos_pro_set(xml_data=xml_data,spin_set=1,dos_range=grid_range)
    if(info_dic.ISPIN==2):
        pro_1=vp.get_bands_pro_set(xml_data=xml_data,spin_set=1,skipk=skipk,bands_range=bands_range)
        pro_2=vp.get_bands_pro_set(xml_data=xml_data,spin_set=2,skipk=skipk,bands_range=bands_range)
        pros={'SpinUp': pro_1.pros,'SpinDown': pro_2.pros}#accessing spins in dictionary after .pro.
        pro_bands={'labels':pro_1.labels,'pros': pros}
        pdos_1=vp.get_dos_pro_set(xml_data=xml_data,spin_set=1,dos_range=grid_range)
        pdos_2=vp.get_dos_pro_set(xml_data=xml_data,spin_set=1,dos_range=grid_range)
        pdos={'SpinUp': pdos_1.pros,'SpinDown': pdos_2.pros}#accessing spins in dictionary after .pro.
        pro_dos={'labels':pdos_1.labels,'pros': pdos}

    #Structure
    poscar=vp.get_structure(xml_data=xml_data)
    #Dimensions dictionary.
    dim_dic={'⇅':'Each of SpinUp/SpinDown Arrays','kpoints':'(NKPTS,3)','kpath':'(NKPTS,1)','bands':'⇅(NKPTS,NBANDS)','dos':'⇅(grid_size,3)','pro_dos':'⇅(NION,grid_size,en+pro_fields)','pro_bands':'⇅(NION,NKPTS,NBANDS,pro_fields)'}
    #Writing everything to be accessible via dot notation
    kpath=[k+shift_kpath for k in kpts.kpath]  # shift kpath for side by side calculations.
    full_dic={'sys_info':info_dic,'dim_info':dim_dic,'kpoints':kpts.kpoints,'kpath':kpath,'bands':eigenvals,
             'tdos':tot_dos,'pro_bands':pro_bands,'pro_dos':pro_dos,'poscar': poscar}
    return vp.Dict2Data(full_dic)

# Cell
def load_export(path= './vasprun.xml',
                joinPathAt =[],
                shift_kpath = 0,
                path_to_ps='pwsh',
                skipk = None,
                max_filled = 10,
                max_empty = 10,
                keep_files = True
                ):
    """
    - Returns a full dictionary of all objects from `vasprun.xml` file exported using powershell.
    - **Parameters**
        - path       : Path to `vasprun.xml` file. Default is `'./vasprun.xml'`.
        - skipk      : Default is None. Automatically detects kpoints to skip.
        - path_to_ps : Path to `powershell.exe`. Automatically picks on Windows and Linux if added to PATH.
        - joinPathAt : List of indices of kpoints where path is broken.
        - shift_kpath: Default 0. Can be used to merge multiple calculations side by side.
        - keep_files : Could be use to clean exported text files. Default is True.
        - max_filled : Number of filled bands below and including VBM. Default is 10.
        - max_empty  : Number of empty bands above VBM. Default is 10.
    - **Returns**
        - Data : Data accessible via dot notation containing nested Data objects:
            - sys_info  : System Information
            - dim_info  : Contains information about dimensions of returned objects.
            - kpoints   : numpy array of kpoints with excluded IBZKPT points
            - kpath     : 1D numpy array directly accessible for plot.
            - bands     : Data containing bands.
            - tdos      : Data containing total dos.
            - pro_bands : Data containing bands projections.
            - pro_dos   : Data containing dos projections.
            - poscar    : Data containing basis,positions, rec_basis and volume.
    """
    import numpy as np
    import os
    import importlib as il
    import pivotpy as pp
    import pivotpy.vr_parser as vp
    this_loc = os.getcwd()
    split_path= os.path.split(os.path.abspath(path)) # abspath is important to split.
    file_name = split_path[1]
    that_loc = split_path[0]
    # Go there.
    os.chdir(that_loc)
    # Work Here
    i = 0
    required_files = ['Bands.txt','tDOS.txt','pDOS.txt','Projection.txt','SysInfo.py']
    for _file in required_files:
        if(os.path.isfile(_file)):
           i=i+1
    if(i<5):
        if (skipk != None):
            pp.ps_to_std(path_to_ps=path_to_ps,ps_command='Import-Module Vasp2Visual; Export-VR -InputFile {} -MaxFilled {} -MaxEmpty {} -SkipK {}'.format(path,max_filled,max_empty,skipk))
        else:
            pp.ps_to_std(path_to_ps=path_to_ps,ps_command='Import-Module Vasp2Visual; Export-VR -InputFile {} -MaxFilled {} -MaxEmpty {}'.format(path,max_filled,max_empty))

    # Enable reloading SysInfo.py file.

    #import SysInfo
    #_vars = il.reload(SysInfo)
    # Single Load instead
    from importlib.machinery import SourceFileLoader
    _vars = SourceFileLoader("SysInfo", "./SysInfo.py").load_module()

    SYSTEM            = _vars.SYSTEM
    NKPTS             = _vars.NKPTS
    NBANDS            = _vars.NBANDS
    NFILLED           = _vars.NFILLED
    TypeION           = _vars.TypeION
    NION              = _vars.NION
    nField_Projection = _vars.nField_Projection
    E_Fermi           = _vars.E_Fermi
    ISPIN             = _vars.ISPIN
    ElemIndex         = _vars.ElemIndex
    ElemName          = _vars.ElemName
    poscar            = {
                        'volume':_vars.volume,
                        'basis' : np.array(_vars.basis),
                        'rec_basis': np.array(_vars.rec_basis),
                        'positions': np.array(_vars.positions)
                        }
    fields            = _vars.fields
    incar             = _vars.INCAR
    # Load Data
    bands= np.loadtxt('Bands.txt').reshape((-1,NBANDS+4)) #Must be read in 2D even if one row only.
    pro_bands= np.loadtxt('Projection.txt').reshape((-1,NBANDS*nField_Projection))
    pro_dos = np.loadtxt('pDOS.txt')
    dos= np.loadtxt('tDOS.txt')

    # Keep or delete only if python generates files (i < 5 case.)
    if(keep_files==False and i==5):
        for file in required_files:
            os.remove(file)
    # Return back
    os.chdir(this_loc)

    # Work now!
    sys_info = {'SYSTEM': SYSTEM,'NION': NION,'TypeION': TypeION,'ElemName': ElemName, 'E_Fermi': E_Fermi,'fields':fields, 'incar': incar,
               'ElemIndex': ElemIndex,'ISPIN': ISPIN}
    dim_info = {'⇅':'Each of SpinUp/SpinDown Arrays','kpoints': '(NKPTS,3)','kpath': '(NKPTS,1)','bands': '⇅(NKPTS,NBANDS)',
'dos': '⇅(grid_size,3)','pro_dos': '⇅(NION,grid_size,en+pro_fields)','pro_bands': '⇅(NION,NKPTS,NBANDS,pro_fields)'}

    bands_dic,tdos_dic,pdos_dic,pro_dic,kpath={},{},{},{},[]
    if(ISPIN==1):
        kpath   = bands[:,3]
        kpoints = bands[:,:3]
        evals   = bands[:,4:]
        bands_dic = {'E_Fermi': E_Fermi, 'ISPIN': ISPIN, 'NBANDS': NBANDS, 'evals': evals}
        tdos_dic  = {'E_Fermi': E_Fermi, 'ISPIN': ISPIN,'tdos': dos}
        pdos      = pro_dos.reshape(NION,-1,nField_Projection+1)
        pdos_dic  = {'labels': fields,'pros': pdos}
        pros      = pro_bands.reshape(NION,NKPTS,NBANDS,-1)
        pro_dic   = {'labels': fields[1:],'pros': pros}
    if(ISPIN==2):
        # Bands
        kpath   = bands[:NKPTS,3]
        kpoints = bands[:NKPTS,:3]
        SpinUp  = bands[:NKPTS,4:]
        SpinDown= bands[NKPTS:,4:]
        evals   = {'SpinUp':SpinUp,'SpinDown': SpinDown}
        bands_dic = {'E_Fermi': E_Fermi, 'ISPIN': ISPIN, 'NBANDS': NBANDS, 'evals': evals}
        # tDOS
        dlen    = int(np.shape(dos)[0]/2)
        SpinUp  = dos[:dlen,:]
        SpinDown= dos[dlen:,:]
        tdos    = {'SpinUp':SpinUp,'SpinDown': SpinDown}
        tdos_dic= {'E_Fermi': E_Fermi, 'ISPIN': ISPIN,'tdos': tdos}

        # pDOS
        plen    = int(np.shape(pro_dos)[0]/2)
        SpinUp  = pro_dos[:plen,:].reshape(NION,-1,nField_Projection+1)
        SpinDown= pro_dos[plen:,:].reshape(NION,-1,nField_Projection+1)
        pdos    = {'SpinUp':SpinUp,'SpinDown': SpinDown}
        pdos_dic= {'labels': fields,'pros': pdos}

        # projections
        pblen  = int(np.shape(pro_bands)[0]/2)
        SpinUp  = pro_bands[:pblen,:].reshape(NION,NKPTS,NBANDS,-1)
        SpinDown= pro_bands[pblen:,:].reshape(NION,NKPTS,NBANDS,-1)
        pros    = {'SpinUp': SpinUp,'SpinDown': SpinDown}
        pro_dic = {'labels': fields[1:],'pros': pros}
    # If broken path, then join points.
    try:
        joinPathAt
    except NameError:
        joinPathAt = []
    if(joinPathAt):
        for pt in joinPathAt:
            kpath[pt:]=kpath[pt:]-kpath[pt]+kpath[pt-1]
    kpath=[k+shift_kpath for k in kpath.copy()] # Shift kpath
    full_dic = {'sys_info': sys_info,'dim_info': dim_info,'kpoints': kpoints,'kpath':kpath,               'bands':bands_dic,'tdos':tdos_dic,'pro_bands': pro_dic ,'pro_dos': pdos_dic,
               'poscar':poscar}
    return Dict2Data(full_dic)

# Cell
def dump_dict(dict_data = None, dump_to = 'pickle',outfile = None,indent=1):
    """
    - Dump an `export_vasprun` or `load_export`'s `Data` object or any dictionary to json or pickle string/file. It convert `Dict2Data` to dictionary before serializing to json/pickle, so json/pickle.loads() of converted Data would be a simple dictionary, pass that to `Dict2Data` to again make accessible via dot notation.
    - **Parameters**
        - dict_data : Any dictionary/Dict2Data object containg numpy arrays, including `export_vasprun` or `load_export` output.
        - dump_to  : Defualt is `pickle` or `json`.
        - outfile  : Defualt is None and return string. File name does not require extension.
        - indent   : Defualt is 1. Only works for json.
    """
    if dump_to not in ['pickle','json']:
        return print("`dump_to` expects 'pickle' or 'json', got '{}'".format(dump_to))
    try: dict_obj = dict_data.to_dict() # Change Data object to dictionary
    except: dict_obj = dict_data
    if dump_to == 'pickle':
        import pickle
        if outfile == None:
            return pickle.dumps(dict_obj)
        outfile = outfile.split('.')[0] + '.pickle'
        f = open(outfile,'wb')
        pickle.dump(dict_obj,f)
        f.close()
    if dump_to == 'json':
        import json
        from .g_utils import EncodeFromNumpy
        if outfile == None:
            return json.dumps(dict_obj,cls=EncodeFromNumpy,indent=indent)
        outfile = outfile.split('.')[0] + '.json'
        f = open(outfile,'w')
        json.dump(dict_obj,f,cls=EncodeFromNumpy,indent=indent)
        f.close()
    return None

# Cell
def load_from_dump(file_or_str,keep_as_dict=False):
    """
    - Loads a json/pickle dumped file or string by auto detecting it.
    - **Parameters**
        - file_or_str : Filename of pickl/json or their string.
        - keep_as_dict: Defualt is False and return `Data` object. If True, returns dictionary.
    """
    out = {}
    import os,pickle,json,pivotpy as pp
    if not isinstance(file_or_str,bytes):
        try: #must try, else fails due to path length issue
            if os.path.isfile(file_or_str):
                if '.pickle' in file_or_str:
                    with open(file_or_str,'rb') as f:
                        out = pickle.load(f)
                    f.close()
                elif '.json' in file_or_str:
                    with open(file_or_str,'r') as f:
                        out = json.load(f,cls=pp.DecodeToNumpy)
                    f.close()
            else: out = json.loads(file_or_str,cls=pp.DecodeToNumpy)
            # json.loads required in else and except both as long str > 260 causes issue in start of try block
        except: out = json.loads(file_or_str,cls=pp.DecodeToNumpy)
    elif isinstance(file_or_str,bytes):
            out = pickle.loads(file_or_str)

    if type(out) is dict and keep_as_dict == False:
        return Dict2Data(out)
    return out