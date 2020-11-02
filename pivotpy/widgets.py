# AUTOGENERATED! DO NOT EDIT! File to edit: Widgets.ipynb (unless otherwise specified).

__all__ = ['light_style', 'dark_style', 'get_files_gui', 'get_input_gui', 'read_data', 'click_data', 'tabulate_data',
           'show_app']

# Cell
import plotly.graph_objects as go
import numpy as np
import shutil
from IPython.display import display,HTML
from ipywidgets import interact, Layout,Label,Button, Box,HBox,VBox
import ipywidgets as ipw
import os,json,pickle
from datetime import datetime
import pivotpy as pp

# Cell
light_style = """<style>
               .widget-text input {
                   background-color:white !important;
                   border-radius:20px !important;
                   padding: 0px 10px 0px 10px !important;
                   border: 1px solid #e0e8e8 !important;
                   color: gray !important;
                   }
               .widget-text input:focus {
                   border: 1px solid skyblue !important;
                   }
               .widget-text input:hover {
                   border: 1px solid skyblue !important;
                   }
               .widget-dropdown > select {
                   background-color: transparent !important;
                   border:none !important;
                   border-bottom: 1px solid skyblue !important;
                   box-shadow: inset 0 -20px 10px -20px skyblue;
               }
               .widget-dropdown > select:hover {
                   background-color: white !important;
               }
               .widget-dropdown > select > option {
                   color: gray !important;
                   background-color: #eaf0f0 !important;
               }
               .widget-dropdown > select > option:focus {
                   background-color: red !important;
               }
               .widget-box {
                   background-color:#eaf0f0 !important;
                   border-radius:5px !important;
                   padding:1px !important;
                   border: 1px solid whitesmoke !important;
                   box-shadow: 1px 1px 1px 1px gray !important;
                }
                .p-Collapse {
                    display: flex;
                    flex-direction: row;
                    align-items: stretch;

                }
                .p-Accordion .p-Collapse + .p-Collapse {
                    margin-top: 0px;
                }
                .borderless {
                border: 1px solid transparent !important;
                box-shadow: none !important;
                border-radius: 0px !important;
                margin:4px !important;
                }
                .marginless {
                    margin: 0px !important;
                    border-radius: 0px !important;
                }
                .widget-tab {
                   background-color:#eaf0f0 !important;
                   border: 1px solid whitesmoke !important;
                   box-shadow: 1px 1px 1px 1px gray !important;
                   padding: 0px 2px 2px 2px !important;

                }
                .widget-tab-contents, .widget-tab > .widget-tab-contents {
                width: 100%;
                box-sizing: border-box;
                margin: 0px !important;
                padding: 0px !important;
                flex-grow: 1;
                overflow: auto;
                background-color:#eaf0f0 !important;
                border: none !important;
                }
                .widget-tab > .p-TabBar .p-TabBar-tab {
                background-color:#eaf0f0 !important;
                border: none !important;
                color: #00aaff !important;
                font-weight: bold !important;
                font-size: 16px !important;
                font-family: "Times","serif" !important;
                text-align: center !important;
                }
                .widget-html, .widget-html-content {
                    margin: 0 !important;
                    padding: 2px !important;
                }
            </style>"""

dark_style = """<style>
               .widget-text input {
                   background-color:black !important;
                   border-radius:20px !important;
                   padding: 0px 10px 0px 10px !important;
                   border: 1px solid #404040 !important;
                   color: #abb2bf !important;
                   }
               .widget-text input:focus {
                   border: 1px solid skyblue !important;
                   }
               .widget-text input:hover {
                   border: 1px solid skyblue !important;
                   }
               .widget-dropdown > select {
                   background-color: transparent !important;
                   border:none !important;
                   border-bottom: 1px solid skyblue !important;
                   box-shadow: inset 0 -20px 10px -20px skyblue;
                   color: white !important;
               }
               .widget-dropdown > select:hover {
                   background-color: black !important;
               }
               .widget-dropdown > select > option {
                   color: whitesmoke !important;
                   background-color: black !important;
               }
               .widget-dropdown > select > option:focus {
                   background-color: red !important;
               }
               .widget-label {
                   color: white !important;
               }
               .widget-html {
                   color: white !important;
               }
               .widget-box {
                   background-color:#282c34 !important;
                   border-radius:5px !important;
                   padding:1px !important;
                   border: 1px solid black !important;
                   box-shadow: 1px 1px 1px 1px black !important;
                }
                .borderless {
                border: 1px solid transparent !important;
                box-shadow: none !important;
                border-radius: 4px !important;
                margin:4px !important;
                }
                .marginless {
                    margin: 0px !important;
                    border-radius: 0px !important;
                }
                .widget-tab {
                   background-color:black !important;
                   border: none !important;
                   box-shadow: 1px 1px 1px 1px gray !important;
                   padding: 0px 2px 2px 2px !important;

                }
                .widget-tab-contents, .widget-tab > .widget-tab-contents {
                width: 100%;
                box-sizing: border-box;
                margin: 0px !important;
                padding: 0px !important;
                flex-grow: 1;
                overflow: auto;
                border: none !important;
                background-color:black !important;
                }
                .widget-tab > .p-TabBar .p-TabBar-tab {
                background-color:black !important;
                border: none !important;
                color: #00aaff !important;
                font-weight: bold !important;
                font-size: 16px !important;
                font-family: "Times","serif" !important;
                text-align: center !important;
                }
            </style>"""

# Cell
def get_files_gui(auto_fill = 'vasprun.xml',html_style=None,height=320):
    """
    - Creates a GUI interface for files/folders filtering.
    - **Parmeters**
        - auto_fill  : Default is `vasprun.xml`, any file/folder.
        - html_style : None,`dark_style` or `light_style`.
        - height     : Height of Grid box.
    - **Returns**
        - Tuple(GUI_gridbox,Files_Dropdown). Access second one by item itself.
    """
    files_w = ipw.Dropdown(continuous_update=False)
    pw = ipw.Text(value=os.getcwd())

    incldue_w = ipw.Text(value=auto_fill)

    excldue_w = ipw.Text()
    d_layout = Layout(width='30%')
    l_layout = Layout(width='19%')
    depth_w = ipw.Dropdown(options=[None,1,2,3,4,5],value=4,layout=d_layout)
    item_w = ipw.Dropdown(options=['Both','Files','Folders'],value='Files',layout=d_layout)
    item_box = ipw.HBox([ipw.Label('Depth: ',layout=l_layout),depth_w,ipw.Label('Type: ',layout=l_layout),item_w])
    item_box.add_class('borderless').add_class('marginless')

    applybtn_w = ipw.Button(description='Apply Filters')
    applybtn_w.style.button_color = 'skyblue'
    gci_output = ipw.Output(layout=Layout(height='{}px'.format(height-70)))
    label_head = ipw.HTML("<h3>Your Filtered Files List</h3>")


    def filter_gci(applybtn_w):
        applybtn_w.description = 'Applying...'
        applybtn_w.disabled = True
        if os.path.isdir(pw.value):
            path = pw.value
        else:
            with gci_output:
                print("Given path does not exists.")
                print("Falling back to PWD: {}".format(os.getcwd()))
            path = os.getcwd()
            pw.value = path
        gci = pp.Dic2Dot({'children':[],'parent':path})

        if 'Files' in item_w.value:
            file_type = dict(filesOnly=True)
        elif 'Folders' in item_w.value:
            file_type = dict(dirsOnly=True)
        else:
            file_type = {}
        try:
            gci = pp.get_child_items(path=path, **file_type,
                           include= [i for i in incldue_w.value.split(",") if i!=''],
                           exclude= [e for e in excldue_w.value.split(",") if e!=''],
                           depth=depth_w.value)
        except:
            with gci_output:
                print('Something went wrong')
        # Enable before any error occur.
        applybtn_w.disabled = False
        files_w.options = {name: os.path.join(gci.parent,name) for name in gci.children}

        applybtn_w.description = 'Successful!'
        applybtn_w.style.button_color = 'green'
        label_head.value = "<h3>From: {}</h3>".format(gci.parent)
        with gci_output:
            display(ipw.HTML("<h4>{} files found.</h4>".format(len(gci.children))))
            display(ipw.HTML("<ol>{}<ol>".format(''.join(['<li>{}</li>'.format(i) for i in gci.children]))))


        applybtn_w.description = 'Apply Filters'
        applybtn_w.style.button_color = 'skyblue'
        gci_output.clear_output(wait=True)

    applybtn_w.on_click(filter_gci)
    out_box = ipw.Box([gci_output])
    right_box = ipw.VBox([label_head,out_box])
    out_box.add_class('borderless')
    right_box.add_class('borderless')
    i_layout = Layout(width='99%')
    incldue_w.layout = i_layout
    excldue_w.layout = i_layout
    pw.layout = i_layout
    input_box = ipw.VBox([
        ipw.Label('Path to Project Folder',layout=i_layout),pw,
        ipw.Label('Items to Include (comma separated)',layout=i_layout),incldue_w,
        ipw.Label('Items to Exclude (comma separated)',layout=i_layout),excldue_w,
        item_box,
        applybtn_w],layout=Layout(width='330px'))
    if not html_style:
        html_style = ''
    full_box = ipw.HBox([ipw.HTML(html_style),input_box, right_box],
                        layout=Layout(height='{}px'.format(height)))
    full_box.add_class('borderless')
    full_box.add_class('marginless')
    return full_box, files_w


# Cell
def get_input_gui(rgb=True,sys_info=None,html_style=None,height=400):
    """
    - Creates a GUI interface for input/selection of orbitals/ions projection.
    - **Parmeters**
        - rgb        : Default is `True` and generates input for `plotly(quick)_rgb_lines`, if `False` creates input for `quick(plotly)_dos(color)_lines`
        - html_style : None,`dark_style` or `light_style`.
        - height     : Height of Grid box.
    - **Returns**
        - Tuple(GUI_gridbox,json_in_HTML). Access second one by item.value.
    """
    from time import sleep
    if not html_style:
        html_style = ''
    if not sys_info:
        sys_info = pp.Dic2Dot({'fields':['s'],'ElemIndex':[0,1],'ElemName':['A']})
    layout = Layout(width='30%')
    orbs_w  = ipw.Dropdown(options={'s':0},value=0,layout=layout)
    orbi_w  = ipw.Text(layout=layout)
    ions_w  = ipw.Dropdown(options={'All':[0,1,1]},value=[0,1,1],layout=layout)
    ioni_w  = ipw.Text(layout=layout)
    label_w = ipw.Text(layout=layout)
    rgb_w   = ipw.Dropdown(options={'Red':0,'Green':1,'Blue':2},value=0,layout=layout)
    rgbl_w  = Label('Color: ')
    click_w= ipw.Button(layout=Layout(width='max-content'),icon='fa-hand-o-up')
    click_w.style.button_color='skyblue'
    # Uniform label widths
    l_width = Layout(width='20%')
    rgbl_w.layout=l_width

    inpro_w = ipw.HTML(layout=Layout(height='20px'))
    if not rgb:
        layout = Layout(width='32px')
        add_w = ipw.Button(description='',layout=layout,icon='fa-plus-circle')
        del_w = ipw.Button(description='',layout=layout,icon='fa-minus-circle')
        add_w.style.button_color='#5AD5D1'
        del_w.style.button_color='#5AD5D1'
        read_box = [Label(u"Line \u00B1: "),add_w,del_w,Label(),Label(),click_w]
    else:
        read_box = [click_w]

    in_w = VBox([ipw.HTML(html_style),
                ipw.HTML("<h3>Projections</h3>"),
                HBox([rgbl_w,rgb_w,Label('Label: ',layout=l_width),label_w
                    ]).add_class('borderless').add_class('marginless'),
                HBox([Label('Ions: ',layout=l_width),ions_w,Label('::>>:: ',layout=l_width),ioni_w
                    ]).add_class('borderless').add_class('marginless'),
                HBox([Label('Orbs: ',layout=l_width),orbs_w,Label('::>>:: ',layout=l_width),orbi_w
                    ]).add_class('borderless').add_class('marginless'),
                HBox(read_box).add_class('borderless').add_class('marginless')
                ],layout=Layout(height="{}px".format(height))
                ).add_class('marginless')

    orbs_w.options= {str(i)+': '+item:str(i) for i,item in enumerate(sys_info.fields)}
    ipw.dlink((orbs_w,'value'), (orbi_w,'value'))

    inds = sys_info.ElemIndex
    ions_w.options = {"{}-{}: {}".format(inds[i],inds[i+1]-1,item):"{}-{}".format(inds[i],inds[i+1]-1) for i,item                             in enumerate(sys_info.ElemName)}

    ipw.dlink((ions_w,'value'), (ioni_w,'value'))


    def read_pro(ions_w,orbi_w,label_w):
        orbs_l = []
        if orbi_w.value:
            for o in orbi_w.value.split(","):
                if '-' in o:
                    strt,stop = o.split("-")
                    [orbs_l.append(i) for i in range(int(strt),int(stop)+1)]
                else:
                    orbs_l.append(int(o))

        ions_l = []
        if ioni_w.value:
            for o in ioni_w.value.split(","):
                if '-' in o:
                    strt,stop = o.split("-")
                    [ions_l.append(i) for i in range(int(strt),int(stop)+1)]
                else:
                    ions_l.append(int(o))
        if label_w.value:
            label_l = label_w.value
        else:
            label_l = "{}:{}".format(ioni_w.value,orbi_w.value)
        return ions_l,orbs_l,label_l
    if rgb:
        elements,orbs,labels = [[],[],[]],[[],[],[]],['','','']
    else:
        rgb_w.options = {"Line 0":0}
        rgb_w.value = 0
        rgbl_w.value = 'Line: '
        elements,orbs, labels = [[],],[[],],['',] # For DOS


    def read_lines(click_w):

        # Read Now
        index=rgb_w.value
        r_p = read_pro(ions_w,orbi_w,label_w)
        # update
        try:
            elements[index] = r_p[0]
            orbs[index]     = r_p[1]
            labels[index]   = r_p[2]
        except:
            elements.append(r_p[0]) # In case new line added.
            orbs.append(r_p[1])
            labels.append(r_p[2])

        max_ind = len(rgb_w.options) # in case a line is deleted.
        _input_ = dict(elements=elements[:max_ind],orbs=orbs[:max_ind],labels=labels[:max_ind])
        inpro_w.value = json.dumps(_input_,indent=2)

        # Button feedback.
        click_w.description = "Got {}".format(rgb_w.label)
        click_w.style.button_color = 'yellow'
        click_w.icon = 'check'
        sleep(1)
        click_w.description = "Read Input"
        click_w.style.button_color = 'skyblue'
        click_w.icon = 'fa-hand-o-up'

    click_w.on_click(read_lines)

    # Observe output of a line right in box.
    def see_input(change):
        #if change:
        x = rgb_w.value
        try: #Avoid None and prior update
            ioni_w.value = ','.join([str(i) for i in elements[x]])
            orbi_w.value = ','.join([str(i) for i in orbs[x]])
            label_w.value = labels[x]
            click_w.description = "{}".format(rgb_w.label) # Triggers when line +/- as well.
            click_w.style.button_color = 'cyan'
            click_w.icon = 'fa-refresh'
        except: pass

    rgb_w.observe(see_input,'value')

    # Add and delete lines
    if not rgb:
        def add_line(add_w):
            l_opts = len(rgb_w.options)+1
            opts = {'Line {}'.format(i):i for i in range(l_opts)}
            rgb_w.options = opts
            rgb_w.value = l_opts - 1

        add_w.on_click(add_line)

        def del_line(del_w):
            l_opts = len(rgb_w.options)-1
            if l_opts > 0: # Do not delete last line. just update,otherwise issues.
                opts = {'Line {}'.format(i):i for i in range(l_opts)}
                rgb_w.options = opts
                rgb_w.value = l_opts - 1

        del_w.on_click(del_line)
    # Finally Link Line number to input button
    ipw.dlink((rgb_w,'label'),(click_w,'description')) # Link line to input buuton.
    click_w.description='Read Input' # After link is important

    return in_w, inpro_w

# Cell
# Reading data
def read_data(tabel_w,sys_info=None):
    data_dict = json.loads(tabel_w.value)
    if sys_info:
        data_dict["V"] = np.round(sys_info.volume,5)
        a,b,c = np.round(np.linalg.norm(sys_info.basis,axis=1),5)
        data_dict["a"] = a
        data_dict["b"] = b
        data_dict["c"] = c
        tabel_w.value = json.dumps(data_dict,indent=1)
#mouse event handler
def click_data(sel_en_w,fermi_w,tabel_w,fig):

    def handle_click(trace, points, state):
        if(points.ys!=[]):
            data_dict = json.loads(tabel_w.value)
            e_fermi = (float(fermi_w.value) if fermi_w.value else 0)
            val=np.round(float(points.ys[0])+e_fermi,4)
            for key in sel_en_w.options:
                if key in sel_en_w.value and key != 'None':
                    data_dict[key] = val # Assign value back
                if 'Fermi' in sel_en_w.value:
                    fermi_w.value = str(val + e_fermi) # change
            tabel_w.value = json.dumps(data_dict,indent=1)
            #data_send(None) #send data to Table
    for i in range(len(fig.data)):
        trace=fig.data[i]
        trace.on_click(handle_click)
# Display Table
def tabulate_data(data_dict):
    ls,ds = [],[]
    for k,v in data_dict.items():
        if v and k not in ['Fermi','so_max','so_min']:
            ls.append(k)
            ds.append(v)
    if len(ls) % 2 != 0:
        ls.append('')
        ds.append('')
    tab_data = [ls[:int(len(ls)/2)],ds[:int(len(ls)/2)],ls[int(len(ls)/2):],ds[int(len(ls)/2):]]

    htm_string = """<style>table {border-collapse: collapse !important;
      min-width: 100% !important;
      border: 1px solid gray !important;
      margin: 1px 1px 1px 1px !important;
      font-size: medium !important;
      font-family: "Times New Roman", "Times", "serif" !important;}
      th, td {text-align: center !important;
      border: 1px solid gray !important;
      padding: 1px 15px 1px 15px !important;}
      tr {width: 100% !important;}
      tr:nth-child(odd) {background-color: #16BDB8 !important;
      font-weight:bold !important;}
      tr:nth-child(even) {background-color: skyblue !important;}
      </style>"""
    htm_string += "<table><tr>{}</tr></table>".format( '</tr><tr>'.join(
                   '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in tab_data) )
    return htm_string


# Cell
def show_app():
    gui1,out_w1 = get_files_gui()
    load_btn = ipw.Button(description='Load Data')
    graph_btn = ipw.Button(description='Load Graph')
    rd_btn = ipw.Dropdown(options=['Bands','DOS'],value='Bands',layout= Layout(width='80px'))

    tabel_w = ipw.HTML(json.dumps({'V':'','a':'','b':'','c':'','Fermi': None,
                                   'VBM':'','CBM':'','so_max':'','so_min':''}),indent=1)
    view_tab_w = ipw.HTML()
    def update_table(change):
        data_dict = json.loads(tabel_w.value)
        htm_string = tabulate_data(data_dict)
        view_tab_w.value = htm_string
    tabel_w.observe(update_table,'value')

    if rd_btn.value == 'DOS':
        gui2,out_w2 = get_input_gui(rgb=False,height=None)
    else:
        gui2,out_w2 = get_input_gui(height=None)
    def on_load(btn):
        load_btn.description='Loading ...'
        try:
            file = os.path.join(os.path.split(out_w1.value)[0],'sys_info.pickle')
            with open(file,'rb') as f:
                sys_info = pickle.load(f)
            f.close()
        except:
            evr = pp.export_vasprun(out_w1.value)
            sys_info = evr.sys_info
            ifile = os.path.join(os.path.split(out_w1.value)[0],'sys_info.pickle')
            vfile = os.path.join(os.path.split(out_w1.value)[0],'vasprun.pickle')
            pp.dump_dict(evr.sys_info,outfile=ifile)
            pp.dump_dict(evr,outfile=vfile)

        if rd_btn.value=='DOS':
            tmp_ui,__ = get_input_gui(rgb=False,sys_info=sys_info,height=None)
        else:
            tmp_ui,__ = get_input_gui(rgb=True,sys_info=sys_info,height=None)

        gui2.children = tmp_ui.children
        __.value = out_w2.value # keep values
        ipw.dlink((__,'value'),(out_w2,'value'))
        load_btn.description='Load Data'

    load_btn.on_click(on_load)

    fig = go.FigureWidget()
    fig.update_layout(autosize=True)

    l_out = Layout(width='20%')
    b_out = Layout(width='30%')
    style_w = ipw.Dropdown(options=["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"],layout=b_out)

    def update_style(change):
        fig.update_layout(template=style_w.value)
    style_w.observe(update_style,'value')

    # RGB extra input
    kticks_w = ipw.Text(value='',layout=b_out)
    ktickv_w = ipw.Text(value='',layout=b_out)
    kjoin_w  = ipw.Text(value='',layout=b_out)
    elim_w   = ipw.Text(value='',layout=b_out)
    sel_en_w = ipw.Dropdown(options=['Fermi','VBM','CBM','so_max','so_min','None'],value='None',layout=b_out)
    fermi_w  = ipw.Text(value='',layout=b_out)
    theme_w = ipw.Dropdown(options=['Default','Light','Dark'],value='Default',layout=b_out)
    theme_html = ipw.HTML('') # To change theme.

    points_box = HBox([Box([Label('E Type:',layout=l_out),sel_en_w,Label('E-Fermi:',layout=l_out),fermi_w
                    ]).add_class('marginless').add_class('borderless'),graph_btn
                    ],layout=Layout(width='100%')).add_class('marginless')
    in_box = VBox([gui2]).add_class('marginless').add_class('borderless')
    top_right = HBox([graph_btn,Label('Style:'),style_w,Label('Theme:'),theme_w
                    ]).add_class('marginless')
    fig_box = Box([fig],layout=Layout(height='380px')).add_class('marginless')
    right_box = VBox([
                top_right,fig_box
                ],layout=Layout(width='60%')).add_class('marginless').add_class('borderless')

    def update_theme(change):
        if 'Dark' in theme_w.value:
            style_w.value = 'plotly_dark'
            theme_html.value = dark_style
        elif 'Light' in theme_w.value:
            style_w.value = 'ggplot2'
            theme_html.value = light_style
        else:
            style_w.value = 'plotly'
            theme_html.value = ''
    theme_w.observe(update_theme,'value')

    def update_box(change):
        if rd_btn.value == 'Bands':
            childs = [gui2,VBox([
                    HBox([Label('Ticks At: ',layout=l_out),kticks_w,Label('Labels: ',layout=l_out),ktickv_w
                        ]).add_class('borderless').add_class('marginless'),
                    HBox([Label('Join At: ',layout=l_out),kjoin_w,Label('E Range: ',layout=l_out),elim_w
                        ]).add_class('marginless').add_class('borderless')
                    ]).add_class('marginless')]
            right_box.children = [top_right,fig_box,points_box,view_tab_w]
        else:
            childs = [gui2,HBox([Label('E Range:',layout=l_out),elim_w,Label('E-Fermi:',layout=l_out),fermi_w
                                    ]).add_class('marginless')]
            right_box.children = [top_right,fig_box,view_tab_w]
            sel_en_w.value = 'None' # no scatter collection in DOS.

        in_box.children = childs

    _start = update_box(0) # initialize box
    rd_btn.observe(update_box,'value')

    upper_box = VBox([
                HBox([Label('File:',layout=Layout(width='50px')),out_w1
                    ]).add_class('borderless').add_class('marginless'),
                HBox([Label('View:',layout=Layout(width='50px')),rd_btn,load_btn
                    ]).add_class('borderless').add_class('marginless')
                ]).add_class('marginless').add_class('borderless')
    left_box = VBox([upper_box,in_box],layout=Layout(width='40%')).add_class('marginless').add_class('borderless')
    # Garph

    def update_graph(btn):
        if out_w2.value:
            fig.data = []
            try:
                file = os.path.join(os.path.split(out_w1.value)[0],'vasprun.pickle')
                graph_btn.description = file
                with open(file,'rb') as f:
                    evr = pickle.load(f)
                f.close()
                graph_btn.description = 'loading pickle...'
            except:
                evr = pp.export_vasprun(out_w1.value)
                graph_btn.description = 'loading export...'
            graph_btn.description = 'Load Graph'
            # Args of Graph function
            argdict = json.loads(out_w2.value)
            argdict.update({'E_Fermi':(float(fermi_w.value) if fermi_w.value else None)})
            argdict.update({'elim':([float(v) for v in elim_w.value.split(',')] if elim_w.value else None)})
            if rd_btn.value == 'Bands':
                argdict.update({'joinPathAt':([int(v) for v in kjoin_w.value.split(',')]
                                            if kjoin_w.value else None)})
                argdict.update({'xt_indices':([int(v) for v in kticks_w.value.split(',')]
                                            if kticks_w.value else [0,-1])})
                argdict.update({'xt_labels':([v for v in ktickv_w.value.split(',')]
                                            if ktickv_w.value else ['A','B'])})
                fig_data = pp.plotly_rgb_lines(path_evr=evr,**argdict)
            else:
                fig_data = pp.plotly_dos_lines(path_evr=evr,**argdict)

            with fig.batch_animate():
                for d in fig_data.data:
                    fig.add_trace(d)
                fig.layout = fig_data.layout
                fig.update_layout(template=style_w.value) # Also here
            read_data(tabel_w,evr.poscar)
            click_data(sel_en_w,fermi_w,tabel_w,fig)
    graph_btn.on_click(update_graph)

    style_w.value='plotly' # to trigger callback and resize graph
    tab =  ipw.Tab([gui1,HBox([theme_html,left_box,right_box
                    ]).add_class('marginless').add_class('borderless')
                    ]).add_class('marginless').add_class('borderless')
    tab.set_title(0,'Home')
    tab.set_title(1,'Output')
    return tab