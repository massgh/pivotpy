# AUTOGENERATED! DO NOT EDIT! File to edit: Utilities.ipynb (unless otherwise specified).

__all__ = ['get_file_size', 'interpolate_data', 'ps_to_py', 'ps_to_std', 'select_dirs', 'select_files',
           'get_child_items', 'invert_color', 'printr', 'printg', 'printb', 'printy', 'printm', 'printc',
           'EncodeFromNumpy', 'DecodeToNumpy', 'Vasprun', 'link_to_class', 'nav_links', 'export_potential',
           'LOCPOT_CHG']

# Cell
def get_file_size(path):
    import os
    if os.path.isfile(path):
        size = os.stat(path).st_size
        for unit in ['Bytes','KB','MB','GB','TB']:
            if size < 1024.0:
                return "%3.2f %s" % (size,unit)
            size /= 1024.0
    else:
        return ''

# Cell
def interpolate_data(x,y,n=10,k=3):
    """
    - Returns interpolated xnew,ynew. If two points are same, it will add 0.1*min(dx>0) to compensate it.
    - **Parameters**
        - x: 1D array of size p,
        - y: ndarray of size p*q*r,....
        - n: Number of points to add between two given points.
        - k: Polynomial order to interpolate.

    - Only axis 0 will be interpolated. If you want general interploation, use `from scipy.interpolate import make_interp_spline, BSpline`

    - **General Usage**: K(p),E(p,q) input from bandstructure.
        - `Knew,Enew= interpolate_data(K,E,n=10,k=3)`. cubic interploation
    """
    import numpy as np
    #Add very small values at simliar points to make interpolation work.
    ind=[i for i in range(0,len(x)) if x[i-1]==x[i]] #Duplicate indices
    xa=np.unique(x)
    dx=0.1*np.min(xa[1:]-xa[:-1])
    if(ind):
        for pt in ind:
            x[pt:]=x[pt:]-x[pt]+x[pt-1]+dx
    # Now Apply interpolation
    from scipy.interpolate import make_interp_spline, BSpline
    xnew=[np.linspace(x[i],x[i+1],n) for i in range(len(x)-1)]
    xnew=np.reshape(xnew,(-1))
    spl = make_interp_spline(x, y, k=k) #BSpline object
    ynew = spl(xnew)
    return xnew,ynew

# Cell
def ps_to_py(ps_command='Get-ChildItem', exec_type='-Command', path_to_ps='powershell.exe'):
    """
    - Captures powershell output in python.
    - **Parameters**
        - ps_command: enclose ps_command in ' ' or " ".
        - exec_type : type of execution, default '-Command', could be '-File'.
        - path_to_ps: path to powerhell.exe if not added to PATH variables.
    """
    from subprocess import Popen, PIPE
    try: # Works on Linux and Windows if PS version > 5.
        cmd = ['pwsh', '-ExecutionPolicy', 'Bypass', exec_type, ps_command]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    except FileNotFoundError:
        try: # Works only on Windows.
            cmd = ['powershell', '-ExecutionPolicy', 'Bypass', exec_type, ps_command]
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        except FileNotFoundError:
            # Works in case nothing above works and you know where is executable.
            cmd = [path_to_ps, '-ExecutionPolicy', 'Bypass', exec_type, ps_command]
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE)

    out=[]; #save to out.
    while True:
        line = proc.stdout.readline()
        if line!=b'':
            line=line.strip()
            u_line=line.decode("utf-8")
            out.append(u_line)
        else:
            break
    out=[item for item in out if item!=''] #filter out empty lines
    return out

# Cell
def ps_to_std(ps_command='Get-ChildItem', exec_type='-Command', path_to_ps='powershell.exe'):
    """
    - Prints powershell output in python std.
    - **Parameters**
        - ps_command: enclose ps_command in ' ' or " ".
        - exec_type: type of execution, default '-Command', could be '-File'.
        - path_to_ps: path to powerhell.exe if not added to PATH variables.
    """
    out=ps_to_py(path_to_ps=path_to_ps,exec_type=exec_type,ps_command=ps_command)
    for item in out:
        print(item)
    return None

# Cell
import os
import glob
#Selection of required project directories.
def select_dirs(path = os.getcwd(),include=[],exclude=[]):
    """
    - Returns selected directories recursively from a parent directory.
    - **Parameters**
        - path    : path to a parent directory, default is `"."`
        - include : list of keywords to include directories, avoid wildcards.
        - exclude : list of keywords to exclude directories, avoid wildcards.
    - **Returns**
        - Tuple of two elements, list of selcted directories and given path.
    """
    print('Use command `get_child_items()` instead for more flexibility.')
    list_dirs=[]; req_dirs=[];
    for filename in glob.iglob(path + '**/**', recursive=True):
        if os.path.isdir(filename):
            list_dirs.append(filename)
    for item in list_dirs:
        for check in include:
            if(check in item):
                if(path != os.getcwd()):
                    req_dirs.append(item.replace("\\","/"))
                if(path == os.getcwd()):
                    req_dirs.append('.'+(item.split(os.getcwd())[-1]).replace("\\","/"))
    for item in req_dirs.copy():
        for ex in exclude:
            if ex in item:
                req_dirs.remove(item)
    return (req_dirs,path.replace("\\","/"))
#Selction of files in selected directories.
def select_files(path=os.getcwd(),include=[],exclude=[]):
    """
    - Returns selected files from a given directory.
    - **Parameters**
        - path    : path to a parent directory, default is `"."`
        - include : list of keywords to include files, avoid wildcards.
        - exclude : list of keywords to exclude files, avoid wildcards.
    - **Returns**
        - Tuple of two elements, list of selcted files and given path.
    """
    print('Use command `get_child_items()` instead for more flexibility.')
    req_files=[]
    all_files=os.listdir(path)
    for file in all_files:
        for check in include:
                    if(check in file):
                        req_files.append(file)
    for item in req_files.copy():
        for ex in exclude:
            if ex in item:
                req_files.remove(item)
    return (req_files,path.replace("\\","/"))

# Cell
def get_child_items(path = os.getcwd(),depth=None,recursive=True,include=[],exclude=[],filesOnly=False,dirsOnly= False):
    """
    - Returns selected directories/files recursively from a parent directory.
    - **Parameters**
        - path    : path to a parent directory, default is `"."`
        - depth   : int, subdirectories depth to get recursively, default is None to list all down.
        - recursive : If False, only list current directory items, if True,list all items recursively down the file system.
        - include : list or str of keywords to include directories/files, avoid wildcards.
        - exclude : list or str of keywords to exclude directories/files, avoid wildcards.
        - filesOnly : Boolean, if True, returns only files.
        - dirsOnly  : Boolean, if True, returns only directories.
    - **Returns**
        - GLOB : Tuple (children,parent), children is list of selected directories/files and parent is given path. Access by index of by `get_child_items().{children,path}`.
    """
    import os
    import glob
    import numpy as np
    from collections import namedtuple
    if include != None and type(include) == str:
        include = [include,]
    if exclude != None and type(exclude) == str:
        exclude = [exclude,]
    path = os.path.abspath(path) # important
    pattern = path + '**/**' # Default pattern
    if depth != None and type(depth) == int:
        pattern = path + '/'.join(['*' for i in range(depth+1)])
        if glob.glob(pattern) == []: #If given depth is more, fall back.
            pattern = path + '**/**' # Fallback to default pattern if more depth to cover all.
    glob_files = glob.iglob(pattern, recursive=recursive)
    if dirsOnly == True:
        glob_files = filter(lambda f: os.path.isdir(f),glob_files)
    if filesOnly == True:
        glob_files = filter(lambda f: os.path.isfile(f),glob_files)
    list_dirs=[]
    for g_f in glob_files:
        list_dirs.append(os.path.relpath(g_f,path))
    # Include check
    req_dirs=[]
    if include != []:
        for check in include:
            req_dirs.extend(list(filter(lambda f: check in f ,list_dirs)))
    elif include == []:
        req_dirs = list_dirs
    # Exclude check
    to_exclude = []
    if exclude != []:
        for ex in exclude:
            to_exclude.extend(list(filter(lambda f: ex in f ,req_dirs)))
        req_dirs = [r_d for r_d in req_dirs if r_d not in to_exclude]
    # Keep only unique
    req_dirs = list(np.unique(req_dirs))
    out_files = namedtuple('GLOB',['children','parent'])
    return out_files(req_dirs,os.path.abspath(path))

# Cell
def invert_color(color=(1,1,1)):
    """
    - Returns opposite of given complementary color.
    - Input: Tuple (r,g,b).
    """
    r = min(color)+max(color)
    return tuple(r-c for c in color)

# Cell
def printr(s): print("\033[91m {}\033[00m" .format(s))
def printg(s): print("\033[92m {}\033[00m" .format(s))
def printb(s): print("\033[34m {}\033[00m" .format(s))
def printy(s): print("\033[93m {}\033[00m" .format(s))
def printm(s): print("\033[95m {}\033[00m" .format(s))
def printc(s): print("\033[96m {}\033[00m" .format(s))

# Cell
import json
class EncodeFromNumpy(json.JSONEncoder):
    """
    - Serializes python/Numpy objects via customizing json encoder.
    - **Usage**
        - `json.dumps(python_dict, cls=EncodeFromNumpy)` to get json string.
        - `json.dump(*args, cls=EncodeFromNumpy)` to create a file.json.
    """
    def default(self, obj):
        import numpy
        if isinstance(obj, numpy.ndarray):
            return {
                "_kind_": "ndarray",
                "_value_": obj.tolist()
            }
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj,range):
            value = list(obj)
            return {
                "_kind_" : "range",
                "_value_" : [value[0],value[-1]+1]
            }
        return super(EncodeFromNumpy, self).default(obj)



class DecodeToNumpy(json.JSONDecoder):
    """
    - Deserilizes JSON object to Python/Numpy's objects.
    - **Usage**
        - `json.loads(json_string,cls=DecodeToNumpy)` from string, use `json.load()` for file.
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        import numpy
        if '_kind_' not in obj:
            return obj
        kind = obj['_kind_']
        if kind == 'ndarray':
            return numpy.array(obj['_value_'])
        elif kind == 'range':
            value = obj['_value_']
            return range(value[0],value[-1])
        return obj

# Cell
import inspect,pivotpy as pp
class Vasprun:
    """
    - All plotting functions that depend on `export_vasprun` are joined under this class and renamed.
    - **Parameters**
        - path       : str: path/to/vasprun.xml. Auto picks in CWD.
        - skipk      : int: Skip initial kpoints
        - elim       : list: Energy range e.g. [-5,5]
        - joinPathAt : list: Join broken path at given indices. Could be obtained from `SEG-INDS` if used `trace_kpath`.
        - shift_kpath: float: Shift in kpath values for side by side plotting.
    - **Attributes**
        - data : Return of `export_vasprun` which is auto-picked in plotting methods under this class.
    - **Methods**
        - sbands    : Shortcut for `quick_bplot`.
        - sdos      : Shortcut for `quick_dos_lines`.
        - srgb      : Shortcut for `quick_rgb_lines`.
        - scolor    : Shortcut for `quick_color_lines`.
        - idos      : Shortcut for `plotly_dos_lines`.
        - irgb      : Shortcut for `plotly_rgb_lines`.
        - get_kwargs: Accepts any of ['sbands','sdos','srgb','scolor','idos','irgb'] as argument and returns argument dictionary for given method that can be unpacked in plotting function argument.
    - **Example**
        > plots = Plots(path='./vasprun.xml')
        > args_ = plots.get_kwargs('sbands')
        > # Modify args_ dictionary as you want
        > plots.sbands(**args_)
    """
    def __init__(self,path=None, skipk=None, elim=[], joinPathAt=[], shift_kpath=0):
        try:
	        shell = get_ipython().__class__.__name__
	        if shell == 'ZMQInteractiveShell' or shell =='Shell':
		        from IPython.display import set_matplotlib_formats
		        set_matplotlib_formats('svg')
        except: pass
        self.data = pp.export_vasprun(path=path, skipk=skipk, elim=elim, joinPathAt=joinPathAt, shift_kpath=shift_kpath)
        # DOCS
        Vasprun.sbands.__doc__ = '\n'.join([l for l in pp.quick_bplot.__doc__.split('\n') if 'path_ev' not in l])
        Vasprun.sdos.__doc__ = '\n'.join([l for l in pp.quick_dos_lines.__doc__.split('\n') if 'path_ev' not in l])
        Vasprun.srgb.__doc__ = '\n'.join([l for l in pp.quick_rgb_lines.__doc__.split('\n') if 'path_ev' not in l])
        Vasprun.scolor.__doc__ = '\n'.join([l for l in pp.quick_color_lines.__doc__.split('\n') if 'path_ev' not in l])
        Vasprun.idos.__doc__ = '\n'.join([l for l in pp.plotly_dos_lines.__doc__.split('\n') if 'path_ev' not in l])
        Vasprun.irgb.__doc__ = '\n'.join([l for l in pp.plotly_rgb_lines.__doc__.split('\n') if 'path_ev' not in l])
    def get_kwargs(self,plot_type='srgb'):
        """
        - Returns keyword arguments dictionary for given `plot_type` that can be unpacked in function of same plot.
        """
        valid_types = ['sbands','sdos','srgb','scolor','idos','irgb']
        if plot_type not in valid_types:
            return print("'plot_type' expects one of {}, but {!r} found.".format(valid_types,plot_type))
        if 'sbands' in plot_type:
            _args = inspect.getcallargs(pp.quick_bplot)
            return {k:v for k,v in _args.items() if 'path_evr' not in k}
        elif 'sdos' in plot_type:
            _args = inspect.getcallargs(pp.quick_dos_lines)
            return {k:v for k,v in _args.items() if 'path_evr' not in k}
        elif 'scolor' in plot_type:
            _args = inspect.getcallargs(pp.quick_color_lines)
            return {k:v for k,v in _args.items() if 'path_evr' not in k}
        elif 'idos' in plot_type:
            _args = inspect.getcallargs(pp.plotly_dos_lines)
            return {k:v for k,v in _args.items() if 'path_evr' not in k}
        elif 'irgb' in plot_type:
            _args = inspect.getcallargs(pp.plotly_rgb_lines)
            return {k:v for k,v in _args.items() if 'path_evr' not in k}
        else:
            _args = inspect.getcallargs(pp.quick_rgb_lines)
            return {k:v for k,v in _args.items() if 'path_evr' not in k}
    def sbands(self,**kwargs):
        return pp.quick_bplot(self.data,**kwargs)
    def sdos(self,**kwargs):
        return pp.quick_dos_lines(self.data,**kwargs)
    def srgb(self,**kwargs):
        return pp.quick_rgb_lines(self.data,**kwargs)
    def scolor(self,**kwargs):
        return pp.quick_color_lines(self.data,**kwargs)
    def idos(self,**kwargs):
        return pp.plotly_dos_lines(self.data,**kwargs)
    def irgb(self,**kwargs):
        return pp.plotly_rgb_lines(self.data,**kwargs)

# Cell
def link_to_class(cls):
    """
    - Binds wrapper of a function to class as attribute that does exactly the same as function. Also function returned from wrapper can be used normally as well.
    - **Parameters**
        - cls : A class object to which function is attached.
    """
    from functools import wraps
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator

# Cell
def nav_links(current_index=0,
            doc_url = r"https://massgh.github.io/pivotpy/",
            items   = ["Index",
                       "XmlElementTree",
                       "StaticPlots",
                       "InteractivePlots",
                       "Utilities",
                       "StructureIO",
                       "Widgets"
                       ],
            horizontal = False,
            out_string = False):
    from IPython.display import Markdown
    links   = [doc_url+item if not 'Index' in item else doc_url for item in items]
    style = """<style>a{text-decoration: none !important;color:lightkblue;font-weight:bold;}
                a:focus,a:active,a:hover{color:hotpink !important;}</style>\n"""
    md_str = style
    for i,(link,item) in enumerate(zip(links,items)):
        if current_index == i: item = "{}●".format(item)
        if not horizontal:
            md_str += "> [&nbsp;`▶` {}&nbsp;]({})  \n".format(item,link)
        else:
            md_str += "> [&nbsp;`▶` {}&nbsp;]({})\n".format(item,link)
    if out_string:
        return md_str
    return Markdown(md_str)

# Cell
def export_potential(locpot=None,e = True,m = False):
    """
    - Returns Data from LOCPOT and similar structure files like CHG. Loads only single set out of 2/4 magnetization data to avoid performance/memory cost while can load electrostatic and one set of magnetization together.
    - **Parameters**
        - locpot: path/to/LOCPOT or similar stuructured file like CHG. LOCPOT is auto picked in CWD.
        - e     : Electric potential/charge density. Default is True.
        - m     : Magnetization density m. Default is False. If True, picks `m` for spin polarized case, and `m_x` for non-colinear case. Additionally it can take 'x','y' and 'z' in case of non-colinear calculations.
    - **Exceptions**
        - Would raise index error if magnetization density set is not present in LOCPOT/CHG in case `m` is not False.
    """
    import numpy as np,os
    from io import StringIO
    import pivotpy as pp
    from itertools import islice # File generator for faster r
    if locpot is None:
        if os.path.isfile('LOCPOT'):
            locpot = 'LOCPOT'
        else:
            return print('./LOCPOT not found.')
    else:
        if not os.path.isfile(locpot):
            return print("File {!r} does not exist!".format(locpot))
    if m not in [True,False,'x','y','z']:
        return print("m expects one of [True,False,'x','y','z'], got {}".format(e))
    # Reading File
    with open(locpot,'r') as f:
        lines = []
        f.seek(0)
        for i in range(8):
            lines.append(f.readline())
        N = sum([int(v) for v in lines[6].split()])
        f.seek(0)
        poscar = []
        for i in range(N+8):
            poscar.append(f.readline())
        f.readline() # Empty one
        Nxyz = [int(v) for v in f.readline().split()] # Grid line read
        nlines = np.ceil(np.prod(Nxyz)/5).astype(int)
        #islice is faster generator for reading potential
        if e == True:
            potential = [l for l in islice(f, nlines)] # Do not join here.
            ignore_set = 0 # Pointer already ahead.
        else:
            ignore_set = nlines # Needs to move pointer to magnetization
        #reading Magnetization if True
        ignore_n = np.ceil(N/5).astype(int)+1 #Some kind of useless data
        if m == True:
            print("m = True would pick m_x for non-colinear case, and m for ISPIN=2.\nUse m='x' for non-colinear or keep in mind that m will refer to m_x.")
            # Needs to spare lines in generator, otherwise pointer does not go ahead.
            _ = [l for l in islice(f, ignore_n+ignore_set)] # +1 for Nx Ny Nz Line
            mag_pot = [l for l in islice(f, nlines)] # Do not join here.
        elif m == 'x':
            _ = [l for l in islice(f, ignore_n+ignore_set)] # +1 for Nx Ny Nz Line
            mag_pot = [l for l in islice(f, nlines)] # Do not join here.
        elif m == 'y':
            _ = [l for l in islice(f, 2*ignore_n+nlines+ignore_set)] # +1 for Nx Ny Nz Line
            mag_pot = [l for l in islice(f, nlines)] # Do not join here.
        elif m == 'z':
            _ = [l for l in islice(f, 3*ignore_n+2*nlines+ignore_set)] # +1 for Nx Ny Nz Line
            mag_pot = [l for l in islice(f, nlines)] # Do not join here.

    # Read Info
    basis = np.loadtxt(StringIO(''.join(poscar[2:5])))*float(poscar[1].strip())
    system = poscar[0].strip()
    ElemName = poscar[5].split()
    ElemIndex = [int(v) for v in poscar[6].split()]
    ElemIndex.insert(0,0)
    ElemIndex = list(np.cumsum(ElemIndex))
    positions = np.loadtxt(StringIO(''.join(poscar[8:N+9])))

    #Reshape Potential and magnetization by this function
    def fix_v_data(lines,shape):
        first_pot = np.loadtxt(StringIO(''.join(lines[:-1])))
        last_pot = np.loadtxt(StringIO(''.join(lines[-1]))) #incomplete line to read separately
        # data written on LOCPOT is this way, x wrapped in y and then xy wrapped in z. so reshape as NGz,NGy,NGx
        N_reshape = [shape[2],shape[1],shape[0]]
        xyz_pot = np.hstack([first_pot.reshape((-1)),last_pot]).reshape(N_reshape)
        xyz_pot = np.transpose(xyz_pot,[2,1,0]) # make xyz back for logical indexing.
        return xyz_pot
    final_dict = dict(SYSTEM=system,ElemName=ElemName,ElemIndex=ElemIndex,basis=basis,positions=positions)
    if e == True:
        xyz_pot = fix_v_data(lines=potential,shape=Nxyz)
        final_dict.update({'e':xyz_pot})
    if m == True:
        xyz_pot = fix_v_data(lines=mag_pot,shape=Nxyz)
        final_dict.update({'m':xyz_pot})
    elif m == 'x':
        xyz_pot = fix_v_data(lines=mag_pot,shape=Nxyz)
        final_dict.update({'m_x':xyz_pot})
    elif m == 'y':
        xyz_pot = fix_v_data(lines=mag_pot,shape=Nxyz)
        final_dict.update({'m_y':xyz_pot})
    elif m == 'z':
        xyz_pot = fix_v_data(lines=mag_pot,shape=Nxyz)
        final_dict.update({'m_z':xyz_pot})
    return pp.Dict2Data(final_dict)

# Cell
import pivotpy as pp
class LOCPOT_CHG:
    """
    - Returns Data from LOCPOT and similar structure files like CHG. Loads only single set out of 2/4 magnetization data to avoid performance/memory cost while can load electrostatic and one set of magnetization together.
    - **Parameters**
        - path: path/to/LOCPOT or similar stuructured file like CHG. LOCPOT is auto picked in CWD.
        - e   : Electric potential/charge density. Default is True.
        - m   : Magnetization density m. Default is False. If True, picks `m` for spin polarized case, and `m_x` for non-colinear case. Additionally it can take 'x','y' and 'z' in case of non-colinear calculations.
    - **Exceptions**
        - Would raise index error if magnetization density set is not present in LOCPOT/CHG in case `m` is not False.
    """
    def __init__(self,path=None,e = True,m = False):
        try:
	        shell = get_ipython().__class__.__name__
	        if shell == 'ZMQInteractiveShell' or shell =='Shell':
		        from IPython.display import set_matplotlib_formats
		        set_matplotlib_formats('svg')
        except: pass
        self.path = path # Must be
        self.m = m # Required to put in plots.
        self.data = pp.export_potential(locpot=path, e=e,m=m)
        # DOCS
        lines = pp.plot_potential.__doc__.split('\n')
        lines = [l for l in [l for l in lines if 'basis' not in l] if 'e_or_m' not in l]
        LOCPOT_CHG.plot_e.__doc__ = '\n'.join(lines)
        LOCPOT_CHG.plot_m.__doc__ = '\n'.join(lines)

    def plot_e(self,operation='mean_z',ax=None,period=None,
                 lr_pos=(0.25,0.75),lr_widths = [0.5,0.5],
                 labels=(r'$V(z)$',r'$\langle V \rangle _{roll}(z)$',r'$\langle V \rangle $'),
                 colors = ((0,0.2,0.7),'b','r'),annotate=True):
        return pp.plot_potential(basis=self.data.basis,e_or_m=self.data.e,operation=operation,
                                    ax=ax,period=period,lr_pos=lr_pos,lr_widths=lr_widths,
                                    labels=labels,colors=colors,annotate=annotate)

    def plot_m(self,operation='mean_z',ax=None,period=None,
                lr_pos=(0.25,0.75),lr_widths = [0.5,0.5],
                labels=(r'$M(z)$',r'$\langle M \rangle _{roll}(z)$',r'$\langle M \rangle $'),
                colors = ((0,0.2,0.7),'b','r'),annotate=True):
        if self.m == True:
            e_or_m = self.data.m
        elif self.m == 'x':
            e_or_m = self.data.m_x
        elif self.m == 'y':
            e_or_m = self.data.m_y
        elif self.m == 'z':
            e_or_m = self.data.m_z
        else:
            return print("Magnetization data set does not exist in {}".format(self.path))
        return pp.plot_potential(basis=self.data.basis,e_or_m=e_or_m,operation=operation,
                                    ax=ax,period=period,lr_pos=lr_pos,lr_widths=lr_widths,
                                    labels=labels,colors=colors,annotate=annotate)
