# coding=utf-8
'''
Created on 2017年3月17日

@author: 10256603
'''
from global_list import *
global login_info


logger = logging.getLogger()
    
    
class wbs_bom_pane(Frame):
    data_thread = None
    wbses = []
    mates = []
    prj_para_header = [
        ('POSID', 'Work Breakdown Structure Element (WBS Element)'), ]

    wbs_bom = {}
    prj_info_st = {}
    prj_para_st = {}

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.createWidgets()

    def createWidgets(self):
        self.imput_group = Frame(self)
        self.imput_group.grid(row=0, column=0, rowspan=3,
                              columnspan=5, sticky=NSEW)

        self.wbs_label = Label(self.imput_group, text='WBS NO.', anchor='w')
        self.wbs_label.grid(row=0, column=0, sticky=EW)

        self.mat_label = Label(self.imput_group, text='物料号', anchor='w')
        self.mat_label.grid(row=1, column=0, sticky=EW)

        self.plant_label = Label(self.imput_group, text='工厂', anchor='w')
        self.plant_label.grid(row=2, column=0, sticky=EW)

        self.wbs_str = StringVar()
        self.wbs_entry = Entry(self.imput_group, textvariable=self.wbs_str)
        self.wbs_entry.grid(row=0, column=1, columnspan=3, sticky=EW)
        self.wbs_entry['state'] = 'readonly'

        self.mat_str = StringVar()
        self.mat_entry = Entry(self.imput_group, textvariable=self.mat_str)
        self.mat_entry.grid(row=1, column=1, columnspan=3, sticky=EW)
        self.mat_entry['state'] = 'readonly'

        self.plant_str = StringVar()
        self.plant_entry = Entry(self.imput_group, textvariable=self.plant_str)
        self.plant_entry.grid(row=2, column=1, columnspan=1, sticky=EW)
        self.plant_str.set('2101')

        self.plant_desc1 = Label(self.imput_group, text='(默认)', anchor='w')
        self.plant_desc1.grid(row=2, column=2, sticky=EW)

        self.plant_desc2 = Label(
            self.imput_group, text='中山工厂为2001', anchor='w')
        self.plant_desc2.grid(row=2, column=3, sticky=EW)

        self.wbs_button = Button(self.imput_group, text='...')
        self.wbs_button.grid(row=0, column=4, sticky=EW)
        self.wbs_button['command'] = self.get_wbs_list

        self.mat_button = Button(self.imput_group, text='...')
        self.mat_button.grid(row=1, column=4, sticky=EW)
        self.mat_button['command'] = self.get_mat_list

        self.search_button = Button(self, text='查询')
        self.search_button.grid(row=0, column=5, sticky=EW)
        self.search_button['command'] = self.start_search

        self.clear_button = Button(self, text='清空条件')
        self.clear_button.grid(row=1, column=5, sticky=EW)
        self.clear_button['command'] = self.clear_case

        self.export_result = Button(self, text='导出结果')
        self.export_result.grid(row=2, column=5, sticky=EW)
        self.export_result['command'] = self.export_res

        self.with_wbs_bom = BooleanVar()
        self.with_prj_info = BooleanVar()
        self.with_prj_para = BooleanVar()
        
        self.with_wbs_bom.set(True)
        
        check_wbs_bom = Checkbutton(self, text="显示WBS BOM", variable = self.with_wbs_bom,
                                    onvalue = True, offvalue=False)
        check_wbs_bom.grid(row=0, column=6, sticky=EW)
        
        check_prj_info = Checkbutton(self, text="显示项目信息", variable=self.with_prj_info,
                                     onvalue=True, offvalue=False)
        check_prj_info.grid(row=1, column=6, sticky=EW)

        check_prj_para = Checkbutton(self, text="显示项目参数", variable=self.with_prj_para,
                                     onvalue=True, offvalue=False)
        
        check_wbs_bom['command'] = self.with_wbs_bom_check

        check_prj_info['command'] = self.with_prj_info_check

        check_prj_para['command'] = self.with_prj_para_check

        check_prj_para.grid(row=2, column=6, sticky=EW)

        self.ntbook = ttk.Notebook(self)
        self.ntbook.rowconfigure(0, weight=1)
        self.ntbook.columnconfigure(0, weight=1)

        self.wbs_tab = Frame(self)

        style = ttk.Style()
        style.configure("Treeview", font=('TkDefaultFont', 10))
        style.configure("Treeview.Heading", font=('TkDefaultFont', 9))

        wbs_cols = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8',
                    'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15', 'col16', 'col17',
                    'col18']
        self.wbs_list = ttk.Treeview(
            self.wbs_tab, show='headings', columns=wbs_cols, selectmode='browse')
        self.wbs_list.grid(row=0, column=0, rowspan=6,
                           columnspan=10, sticky='nsew')

        for i in range(0, len(wbs_cols)):
            self.wbs_list.heading(wbs_cols[i], text=wbs_headers[i][1])

        self.wbs_list.column('col1', width=80, anchor='w')
        self.wbs_list.column('col2', width=80, anchor='w')
        self.wbs_list.column('col3', width=40, anchor='w')
        self.wbs_list.column('col4', width=40, anchor='w')
        self.wbs_list.column('col5', width=40, anchor='w')
        self.wbs_list.column('col6', width=40, anchor='w')
        self.wbs_list.column('col7', width=80, anchor='w')
        self.wbs_list.column('col8', width=150, anchor='w')
        self.wbs_list.column('col9', width=150, anchor='w')
        self.wbs_list.column('col10', width=80, anchor='w')
        self.wbs_list.column('col11', width=60, anchor='w')
        self.wbs_list.column('col12', width=80, anchor='w')
        self.wbs_list.column('col13', width=60, anchor='w')
        self.wbs_list.column('col14', width=60, anchor='w')
        self.wbs_list.column('col15', width=40, anchor='w')
        self.wbs_list.column('col16', width=40, anchor='w')
        self.wbs_list.column('col17', width=200, anchor='w')
        self.wbs_list.column('col18', width=200, anchor='w')

        wbs_ysb = ttk.Scrollbar(self.wbs_tab, orient='vertical',
                                command=self.wbs_list.yview)
        wbs_xsb = ttk.Scrollbar(self.wbs_tab, orient='horizontal',
                                command=self.wbs_list.xview)
        wbs_ysb.grid(row=0, column=10, rowspan=6, sticky='ns')
        wbs_xsb.grid(row=6, column=0, columnspan=10, sticky='ew')

        self.wbs_list.configure(yscroll=wbs_ysb.set, xscroll=wbs_xsb.set)

        self.wbs_tab.rowconfigure(1, weight=1)
        self.wbs_tab.columnconfigure(1, weight=1)

        self.ntbook.add(self.wbs_tab, text='WBS BOM', sticky=NSEW)
        self.ntbook.grid(row=3, column=0, rowspan=12,
                         columnspan=10, sticky='nsew') 
                      
        self.prj_info_tab = Frame(self)

        i_range = len(prj_info_header)
        prj_info_cols = ['col' + str(i) for i in range(i_range)]

        self.prj_info_list = ttk.Treeview(
            self.prj_info_tab, show='headings', columns=prj_info_cols, selectmode='browse')

        self.prj_info_list.grid(row=0, column=0, rowspan=6,
                                columnspan=10, sticky='nsew')

        for i in range(0, i_range):
            self.prj_info_list.heading(
                prj_info_cols[i], text=prj_info_header[i][1])

        for i in range(0, i_range):
            self.prj_info_list.column(prj_info_cols[i], width=100, anchor='w')

        prj_info_ysb = ttk.Scrollbar(self.prj_info_tab, orient='vertical',
                                     command=self.prj_info_list.yview)
        prj_info_xsb = ttk.Scrollbar(self.prj_info_tab, orient='horizontal',
                                     command=self.prj_info_list.xview)
        prj_info_ysb.grid(row=0, column=10, rowspan=6, sticky='ns')
        prj_info_xsb.grid(row=6, column=0, columnspan=10, sticky='ew')

        self.prj_info_list.configure(
            yscroll=prj_info_ysb.set, xscroll=prj_info_xsb.set)

        self.prj_info_tab.rowconfigure(1, weight=1)
        self.prj_info_tab.columnconfigure(1, weight=1)

        self.ntbook.add(self.prj_info_tab, text='项目信息', sticky=NSEW)

        if not self.with_prj_info.get():
            self.ntbook.hide(self.prj_info_tab)

        self.get_prj_para_headers()
        self.prj_para_tab = Frame(self)

        i_range = len(self.prj_para_header)
        prj_para_cols = ['col' + str(i) for i in range(i_range)]

        self.prj_para_list = ttk.Treeview(
            self.prj_para_tab, show='headings', columns=prj_para_cols, selectmode='browse')

        self.prj_para_list.grid(row=0, column=0, rowspan=6,
                                columnspan=10, sticky='nsew')

        for i in range(0, i_range):
            self.prj_para_list.heading(
                prj_para_cols[i], text=self.prj_para_header[i][1])

        for i in range(0, i_range):
            self.prj_para_list.column(prj_para_cols[i], width=100, anchor='w')

        prj_para_ysb = ttk.Scrollbar(self.prj_para_tab, orient='vertical',
                                     command=self.prj_para_list.yview)
        prj_para_xsb = ttk.Scrollbar(self.prj_para_tab, orient='horizontal',
                                     command=self.prj_para_list.xview)
        prj_para_ysb.grid(row=0, column=10, rowspan=6, sticky='ns')
        prj_para_xsb.grid(row=6, column=0, columnspan=10, sticky='ew')

        self.prj_para_list.configure(
            yscroll=prj_para_ysb.set, xscroll=prj_para_xsb.set)

        self.prj_para_tab.rowconfigure(1, weight=1)
        self.prj_para_tab.columnconfigure(1, weight=1)

        self.ntbook.add(self.prj_para_tab, text='项目参数', sticky=NSEW)

        if not self.with_prj_para.get():
            self.ntbook.hide(self.prj_para_tab)

        log_pane = Frame(self)

        self.log_label = Label(log_pane)
        self.log_label["text"] = "操作记录"
        self.log_label.grid(row=0, column=0, sticky=W)

        self.log_text = scrolledtext.ScrolledText(log_pane, state='disabled',height=10)
        self.log_text.config(font=('TkFixedFont', 10, 'normal'))
        self.log_text.grid(row=1, column=0, columnspan=2, sticky=EW)
        log_pane.rowconfigure(1, weight=1)
        log_pane.columnconfigure(1, weight=1)

        log_pane.grid(row=15, column=0, rowspan=2, columnspan=10, sticky=NSEW)

        # Create textLogger
        text_handler = TextHandler(self.log_text)
        # Add the handler to logger

        logger.addHandler(text_handler)
        logger.setLevel(logging.INFO)

        self.rowconfigure(6, weight=1)
        self.columnconfigure(9, weight=1)

    def get_wbs_list(self):
        d = ask_list("WBS NO输入", 3)
        if not d:
            return

        self.wbses = d
        self.wbs_str.set(self.wbses[0])

    def get_mat_list(self):
        d = ask_list("物料输入", 2)
        if not d:
            return

        self.mates = d
        self.mat_str.set(self.mates[0])

    def start_search(self):
        if self.data_thread is not None and self.data_thread.is_alive():
            messagebox.showinfo('提示', '表单刷新线程正在后台刷新列表，请等待完成后再点击!')
            return

        self.__refresh_tree()

    def clear_case(self):
        self.mat_str.set('')
        self.wbs_str.set('')
        self.wbses = []
        self.mates = []
        self.wbs_bom = {}
        self.prj_info_st = {}
        self.prj_para_st = {}
        self.plant_str.set('2101')

        self.clear_list()

    def clear_list(self):
        logger.info("正在清空列表...")
        if self.with_wbs_bom.get():
            for row in self.wbs_list.get_children():
                self.wbs_list.delete(row)

        if self.with_prj_info.get():
            for row in self.prj_info_list.get_children():
                self.prj_info_list.delete(row)

        if self.with_prj_para.get():
            for row in self.prj_para_list.get_children():
                self.prj_para_list.delete(row)

    def export_res(self):
        if len(self.wbs_bom)==0 and len(self.prj_info_st)==0 and len(self.prj_para_st)==0:
            logger.info("查询结果为空，无法导出清单")
            return
        
        file_str = filedialog.asksaveasfilename(
            title="导出文件", filetypes=[('excel file', '.xlsx')])
        if not file_str:
            return

        if not file_str.endswith(".xlsx"):
            file_str += ".xlsx"

        wb = Workbook()
        ws = wb.worksheets[0]
        
        if self.with_wbs_bom.get():
            ws.title = 'WBS BOM清单'
            col_size = len(wbs_headers)
            for i in range(0, col_size):
                ws.cell(row=1, column=i + 1).value = wbs_headers[i][1]

            i_wbs_bom = len(self.wbs_bom)

            for i in range(1, i_wbs_bom + 1):
                for j in range(0, col_size):
                    ws.cell(row=i + 1, column=j + 1).value = self.wbs_bom[i][j]
        else:
            wb.remove(ws)
                
        if self.with_prj_info.get():
            ws1=wb.create_sheet("项目基本信息")
            
            for i in range(0, len(prj_info_header)):
                ws1.cell(row=1, column=i + 1).value = prj_info_header[i][1]
                
            i_prj_info = len(self.prj_info_st)
            for i in range(1, i_prj_info+1):
                for j in range(0, len(prj_info_header)):
                    ws1.cell(row=i + 1, column=j + 1).value = self.prj_info_st[i][j]
                    
        if self.with_prj_para.get():
            ws2 = wb.create_sheet("项目参数信息")
            for i in range(0, len(self.prj_para_header)):
                ws2.cell(row=1, column=i+1).value = self.prj_para_header[i][1]
                
            i_prj_para = len(self.prj_para_st)
            for i in range(1, i_prj_para+1):
                for j in range(0, len(self.prj_para_header)):
                    ws2.cell(row=i + 1, column=j + 1).value = self.prj_para_st[i][j]                   
            
        if excel_xlsx.save_workbook(workbook=wb, filename=file_str):
            messagebox.showinfo("输出", "成功输出!")

    def with_prj_info_check(self):
        b_prj_info = self.with_prj_info.get()
        
        if b_prj_info:
            self.ntbook.add(self.prj_info_tab)
            self.ntbook.select(self.prj_info_tab)
        else:
            self.ntbook.hide(self.prj_info_tab)
    
    def with_wbs_bom_check(self):
        b_wbs_bom = self.with_wbs_bom.get()
        
        if b_wbs_bom:
            self.ntbook.add(self.wbs_tab)
            self.ntbook.select(self.wbs_tab)
        else:
            self.ntbook.hide(self.wbs_tab)

    def with_prj_para_check(self):
        b_prj_para = self.with_prj_para.get()

        if b_prj_para:
            self.ntbook.add(self.prj_para_tab)
            self.ntbook.select(self.prj_para_tab)
        else:
            self.ntbook.hide(self.prj_para_tab)

    def get_prj_para_headers(self):
        re = SParameterFields.select().order_by(SParameterFields.field_name.asc())

        if not re:
            self.with_prj_para.set(False)
            return

        for r in re:
            li_1 = r.field_name
            li_2 = r.field_desc
            li = (li_1, li_2)
            self.prj_para_header.append(li)

    def refresh(self):
        self.wbs_bom = {}
        self.prj_info_st = {}
        self.prj_para_st = {}
        wbs=None

        if self.with_wbs_bom.get()==False and self.with_prj_info.get()==False and self.with_prj_para.get()==False:
            logger.warning("请至少选择一项功能")
            return 0           
            
        self.clear_list()

        logger.info("正在登陆SAP...")
        config = ConfigParser()
        config.read('sapnwrfc.cfg')
        para_conn = config._sections['connection']
        para_conn['user'] = base64.b64decode(para_conn['user']).decode()
        para_conn['passwd'] = base64.b64decode(para_conn['passwd']).decode()


        try:
            logger.info("正在连接SAP...")
            conn = pyrfc.Connection(**para_conn)

            if self.with_wbs_bom.get():
                wbs = self.refresh_wbs_bom(conn)
            else:
                wbs = self.wbses

            if wbs is None:
                logger.warning('请输入WBS list')
                return 0

            self.refresh_prj(conn, wbs)

            self.update_tree()

        except pyrfc.CommunicationError:
            logger.error("无法连接服务器")
            return -1
        except pyrfc.LogonError:
            logger.error("无法登陆，帐户密码错误！")
            return -1
        except (pyrfc.ABAPApplicationError, pyrfc.ABAPRuntimeError):
            logger.error("函数执行错误。")
            return -1

        conn.close()

        return 1

    def refresh_wbs_bom(self, conn):
        imp = []

        l_wbs = len(self.wbses)
        l_mat = len(self.mates)

        if l_wbs > 0 and l_mat > 0:
            for w in self.wbses:
                for m in self.mates:
                    line = dict(POSID=w, MATNR=m)
                    imp.append(line)
        elif l_wbs == 0 and l_mat > 0:
            for m in self.mates:
                line = dict(MATNR=m)
                imp.append(line)
        elif l_wbs > 0 and l_mat == 0:
            for w in self.wbses:
                line = dict(POSID=w)
                imp.append(line)

        else:
            return None

        logger.info("正在调用RFC函数(ZAP_PS_WBSBOM_INFO)...")
        result = conn.call('ZAP_PS_WBSBOM_INFO',
                           IT_CE_WBSBOM=imp, CE_WERKS=self.plant_str.get())

        i = 0
        wbs_s = []
        logger.info("正在分析并获取WBS BOM清单...")
        for re in result['OT_WBSBOM']:
            i += 1
            r_line = []
            wbs = re['POSID']
            if wbs not in wbs_s:
                wbs_s.append(wbs)
            for w in wbs_headers:
                if w[0] =='PSPEL':
                    r_line.append(act_to_wbs_element(wbs, re['VORNR']))
                else:
                    r_line.append(re[w[0]])
            self.wbs_bom[i] = r_line
        
        logger.info("wbs bom清单获取完成。")
        return wbs_s

    def dict_to_list(self, dict_para):
        i = 0
        i_len = len(self.prj_para_header)
        for key in dict_para.keys():
            i += 1
            s_line = dict_para[key]
            a_line = []
            a_line.append(key)

            for j in range(1, i_len):
                if dict_has_key(s_line, self.prj_para_header[j][0]):
                    a_line.append(s_line[self.prj_para_header[j][0]])
                else:
                    a_line.append('')

            self.prj_para_st[i] = a_line            

    def refresh_prj(self, conn, wbs_s):
        imp = []

        l_wbs = len(wbs_s)

        if l_wbs > 0:
            for w in wbs_s:
                line = dict(POSID=w)
                imp.append(line)
        elif l_wbs == 0:
            return

        b_prj_info = self.with_prj_info.get()
        b_prj_para = self.with_prj_info.get()

        if b_prj_info or b_prj_para:
            logger.info("正在调用RFC函数(ZAP_PS_PROJECT_INFO)...")
            result = conn.call('ZAP_PS_PROJECT_INFO',
                               IT_CE_POSID=imp, CE_WERKS=self.plant_str.get())

            if b_prj_info:
                logger.info("正在分析并获取项目基本信息...")

                i = 0
                for re in result['OT_PROJ']:
                    i += 1
                    r_line = []
                                    
                    for w in prj_info_header:
                        if w[0] == 'POSID':
                            r_line.append(format_wbs_no(re[w[0]]))
                        else:
                            r_line.append(re[w[0]])

                    self.prj_info_st[i] = r_line
                logger.info("项目基本信息获取完成")

            if b_prj_para:
                logger.info("正在分析并获取项目参数信息...")

                prj_para_s = {}
                
                for re in result['OT_CONF']:
                    
                    if dict_has_key(prj_para_s, format_wbs_no(re['POSID'])):
                        if not dict_has_key(prj_para_s[format_wbs_no(re['POSID'])], re['ATNAM']):
                            prj_para_s[format_wbs_no(re['POSID'])][re['ATNAM']] = re['ATWTB']
                    else:
                        prj_para_s[format_wbs_no(re['POSID'])] = {}
                        prj_para_s[format_wbs_no(re['POSID'])][re['ATNAM']] = re['ATWTB']

                if len(prj_para_s) != 0:
                    self.dict_to_list(prj_para_s)
                    
                logger.info("项目参数信息获取完成。")

    def __refresh_tree(self):
        self.data_thread = refresh_thread(self)
        self.data_thread.setDaemon(True)
        self.data_thread.start()

    def update_tree(self):
        b_prj_info = self.with_prj_info.get()
        b_prj_para = self.with_prj_info.get()
        b_wbs_bom = self.with_wbs_bom.get()

        l_wbs = len(self.wbs_bom)
        
        if b_wbs_bom:
            logger.info("正在更新WBS BOM列表...")
            for i in range(1, l_wbs + 1):
                self.wbs_list.insert('', END, values=self.wbs_bom[i])
            logger.info("WBS BOM列表更新完成.")

        if b_prj_info:
            logger.info("正在更新项目基本信息列表...")
            l_prj_info = len(self.prj_info_st)

            for i in range(1, l_prj_info + 1):
                self.prj_info_list.insert('', END, values=self.prj_info_st[i])
            logger.info("项目基本信息列表更新完成。")

        if b_prj_para:
            logger.info("正在更新项目参数信息列表...")
            l_prj_para = len(self.prj_para_st)

            for i in range(1, l_prj_para+1):
                self.prj_para_list.insert('', END, values=self.prj_para_st[i])
            logger.info("项目参数信息列表更新完成.")
