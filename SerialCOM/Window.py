import sys
import threading
import tkinter
from PIL import ImageTk
import customtkinter
from PIL import Image as PILImage
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


button_color = "#4636d9"
button_hover_color = "#6054d1"
background_color = "#3d3678"
dark_button_color = "#1c1938"


class Window(customtkinter.CTk):
    def __init__(self, app):

        super().__init__()

        sys.excepthook = self.custom_excepthook

        self.app = app

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.geometry("1000x680")
        self.title("SerialCOM")

        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # add widgets to app
        self.menu = MenuFrame(self, self.app)
        self.menu.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")

        self.mid_frame = MidFrame(self, self.app)
        self.mid_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 10), sticky="nsew")

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def custom_excepthook(self, type, value, traceback):

        self.mid_frame.terminal_text_label.error_write("\nError:\n")
        self.mid_frame.terminal_text_label.error_write(value)
        print("\n")


class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=background_color)

        self.app = app

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=0)

        original_image = PILImage.open("assets/SerialCOM_logo.jpg")
        new_size = (150, 150)
        resized_image = original_image.resize(new_size)

        logo_img = ImageTk.PhotoImage(resized_image)
        self.logo_widget = tkinter.Label(self, image=logo_img, borderwidth=0)
        self.logo_widget.image = logo_img
        self.logo_widget.grid(row=0,
                              column=0,
                              padx=80,
                              pady=(20, 0),
                              sticky="we")

        self.FilesButton = customtkinter.CTkButton(self, text="Files",
                                                   fg_color=button_color,
                                                   hover_color=button_hover_color,
                                                   command=self.buttonFiles_event,
                                                   height=40)
        self.FilesButton.grid(row=1,
                              column=0,
                              padx=10,
                              pady=(20, 20),
                              sticky="nsew")

        self.ports_initial_values = [""]
        self.COM_button_var = customtkinter.StringVar(value="Choose Port...")
        self.COM_button = customtkinter.CTkOptionMenu(self, values=self.ports_initial_values,
                                                      command=self.COM_button_event,
                                                      variable=self.COM_button_var,
                                                      fg_color=dark_button_color,
                                                      button_color=button_color,
                                                      button_hover_color=button_hover_color,
                                                      height=40)
        self.COM_button.grid(row=2,
                             column=0,
                             padx=10,
                             pady=(0, 20),
                             sticky="nsew",)

        self.COM_button.bind("<ButtonRelease-1>", self.update_values)

        self.baudrate_button_var = customtkinter.StringVar(value="Choose baudrate...")
        self.baudrate_button = customtkinter.CTkOptionMenu(self, values=["600", "1800",
                                                                         "4800", "9600", "19200",
                                                                         "38400", "57600", "115200", "other..."],
                                                           command=self.baudrate_button_event,
                                                           variable=self.baudrate_button_var,
                                                           fg_color=dark_button_color,
                                                           button_color=button_color,
                                                           button_hover_color=button_hover_color,
                                                           height=40)
        self.baudrate_button.grid(row=3,
                                  column=0,
                                  padx=10,
                                  pady=(0, 20),
                                  sticky="nsew",)

        # self.timeout_button = customtkinter.CTkEntry(self, placeholder_text="timeout = 0",
        #                                              fg_color=dark_button_color,
        #                                              placeholder_text_color="white",
        #                                              height=40)
        # self.timeout_button.grid(row=4,
        #                          column=0,
        #                          padx=10,
        #                          pady=(0, 20),
        #                          sticky="nsew")

        self.ConnectButton = customtkinter.CTkButton(self, text="Connect",
                                                     fg_color=button_color,
                                                     hover_color=button_hover_color,
                                                     command=self.Connect_button_event,
                                                     height=40,
                                                     anchor="center")
        self.ConnectButton.grid(row=6,
                                column=0,
                                padx=10,
                                pady=(0, 20),
                                sticky="we")

        self.empty_label = customtkinter.CTkLabel(self, text="")
        self.empty_label.grid(row=5, column=0)

        self.COM_button.bind("<Configure>", self.update_values)

    def update_values(self, event):
        ports = self.app.get_ports()
        if ports != self.ports_initial_values:
            # print(ports)
            # print(self.ports_initial_values)
            # print("różne")
            self.ports_initial_values = ports
            self.COM_button.configure(values=self.ports_initial_values)

    def baudrate_button_event(self, choice):
        self.app.set_baudrate(choice)

    def Connect_button_event(self):
        self.app.connect()

    def COM_button_event(self, choice):
        self.app.set_COM(choice)

    def buttonFiles_event(self):
        pass


class CustomPlotWidget:
    def __init__(self, master):
        self.fig = Figure()
        self.plots = []
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.master = master
        self.ax.set_facecolor("#121212")
        self.fig.set_facecolor("#121212")

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.master.configure(fg_color='#121212')
        # master.grid_columnconfigure(0, weight=1)
        # master.grid_rowconfigure(0, weight=1)
        # self.canvas.get_tk_widget().grid(row=0,
        #                                  column=0,
        #                                  padx=0,
        #                                  pady=0,
        #                                  sticky="nsew",
        #                                  )

        self.toolbar = NavigationToolbar2Tk(self.canvas, master, pack_toolbar=False)
        # self.toolbar.grid(row=0, column=0)
        self.data_x = []
        self.data_y = []

    def plot(self, x=None, y=None, z=None):
        self.data_y.append(y)
        self.data_x.append(x)
        self.ax.plot(self.data_x, self.data_y)
        self.canvas.draw()

    def clear(self):
        self.ax.clear()
        self.data_x.clear()
        self.data_y.clear()
        self.canvas.draw()

    def show(self, show):
        if show:
            self.master.grid_columnconfigure(0, weight=1)
            self.master.grid_rowconfigure(0, weight=1)
            self.master.grid_rowconfigure(1, weight=1)
            self.canvas.get_tk_widget().grid(row=0,
                                             column=0,
                                             padx=0,
                                             pady=0,
                                             sticky="nsew",
                                             )
            self.toolbar.grid(row=1, column=0, sticky="w")
        else:
            self.canvas.get_tk_widget().grid_forget()
            self.toolbar.grid_forget()


class MidFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=10)

        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.terminal = customtkinter.CTkFrame(master=self,
                                               width=300,
                                               height=200,
                                               corner_radius=10)
        self.terminal.grid(row=0,
                           column=0,
                           sticky="nsew")

        self.terminal.grid_columnconfigure(0, weight=1)
        self.terminal.grid_rowconfigure(0, weight=1)

        # self.terminal_text_label_var = customtkinter.StringVar(value="")
        self.terminal_text_label = CustomLabel(self.terminal,
                                               # text="",
                                               # textvariable=self.terminal_text_label_var,
                                               fg_color="#121212",
                                               wrap="word")

        self.terminal_text_label.grid(row=0,
                                      column=0,
                                      padx=0,
                                      pady=0,
                                      sticky="nsew")

        self.plot_widget = CustomPlotWidget(self.terminal)

        sys.stdout = self.terminal_text_label

        self.text_var = customtkinter.StringVar(value="")
        self.textbox = customtkinter.CTkEntry(self, placeholder_text="write here")
        self.textbox.grid(row=1,
                          column=0,
                          padx=10,
                          pady=(10, 10),
                          sticky="nsew")

        self.options_menu = Options(self, self.app, self)
        self.options_menu.grid(row=0,
                               column=1,
                               padx=(10, 0),
                               pady=0,
                               sticky="nsew")

        self.send_button = customtkinter.CTkButton(self,
                                                   text="SEND",
                                                   fg_color=button_color,
                                                   hover_color=button_hover_color,
                                                   command=self.send_event)
        self.send_button.grid(row=1,
                              column=1,
                              padx=(10, 10),
                              pady=10,
                              sticky="ew")
        self.textbox.bind("<Return>", self.send_event)

    def send_event(self, arg=None):
        # todo:
        if self.options_menu.state:
            data = self.textbox.get()
            self.app.send_data(data)
            print(">>", data)
            self.textbox.delete(first_index=0, last_index=len(data))


class Options(customtkinter.CTkFrame):
    def __init__(self, master, app, mid):
        super().__init__(master, fg_color="transparent")

        self.midframe = mid
        self.app = app
        self.thread = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.switch_var = customtkinter.StringVar(value="terminal")
        self.switch = customtkinter.CTkSwitch(self, text="Plotter", command=self.switch_event,
                                              variable=self.switch_var, onvalue="plotter", offvalue="terminal",
                                              switch_width=50,
                                              progress_color="#b8f76f")
        self.switch.grid(row=0,
                         column=0,
                         padx=30,
                         pady=(40, 20),
                         sticky="ew")

        self.stop_button_var = customtkinter.StringVar(value="Start")
        self.state = False
        self.stop_button = customtkinter.CTkButton(self,
                                                   text="Start",
                                                   textvariable=self.stop_button_var,
                                                   fg_color=button_color,
                                                   hover_color=button_hover_color,
                                                   command=self.stop_button_event)
        self.stop_button.grid(row=1,
                              column=0,
                              padx=(10, 10),
                              pady=20,
                              sticky="ew")

        self.clear_button = customtkinter.CTkButton(self,
                                                    text="Clear",
                                                    fg_color=button_color,
                                                    hover_color=button_hover_color,
                                                    command=self.clear_button_event)
        self.clear_button.grid(row=2,
                               column=0,
                               padx=(10, 10),
                               pady=(0, 20),
                               sticky="ew")

        self.frame = customtkinter.CTkFrame(self, fg_color=background_color)
        self.frame.grid(row=3,
                        column=0,
                        padx=(10, 10),
                        pady=(20, 20),
                        sticky="ew")

        self.label = customtkinter.CTkLabel(self.frame, text="Display Mode", anchor="center", justify="center")
        self.label.grid(row=0,
                        column=0,
                        padx=30,
                        pady=10,
                        sticky="n")

        self.auto_mode_switch_var = customtkinter.StringVar(value="auto_off")
        self.auto_mode_switch = customtkinter.CTkSwitch(self.frame, text="auto",
                                                        command=self.auto_mode_switch_event,
                                                        variable=self.auto_mode_switch_var,
                                                        onvalue="auto_on",
                                                        offvalue="auto_off",
                                                        switch_width=40,
                                                        progress_color="#b8f76f")
        self.auto_mode_switch.grid(row=1,
                                   column=0,
                                   padx=20,
                                   pady=(0, 20),
                                   sticky="ew")

        self.newline_mode_switch_var = customtkinter.StringVar(value="ln_off")
        self.newline_mode_switch = customtkinter.CTkSwitch(self.frame, text="new line",
                                                           command=self.newline_mode_switch_event,
                                                           variable=self.newline_mode_switch_var,
                                                           onvalue="ln_on",
                                                           offvalue="ln_off",
                                                           switch_width=40,
                                                           progress_color="#b8f76f")
        self.newline_mode_switch.grid(row=2,
                                      column=0,
                                      padx=20,
                                      pady=(0, 20),
                                      sticky="ew")

        self.default_mode_switch_var = customtkinter.StringVar(value="on")
        self.default_mode_switch = customtkinter.CTkSwitch(self.frame, text="default",
                                                           command=self.default_mode_switch_event,
                                                           variable=self.default_mode_switch_var,
                                                           onvalue="on",
                                                           offvalue="off",
                                                           switch_width=40,
                                                           progress_color="#b8f76f")
        self.default_mode_switch.grid(row=3,
                                      column=0,
                                      padx=20,
                                      pady=(0, 20),
                                      sticky="ew")

        self.auto_scroll_var = customtkinter.StringVar(value="on")
        self.auto_scroll_switch = customtkinter.CTkSwitch(self, text="auto scroll",
                                                          command=self.auto_scroll_switch_event,
                                                          variable=self.auto_scroll_var,
                                                          onvalue="on",
                                                          offvalue="off",
                                                          switch_width=50,
                                                          progress_color="#b8f76f")
        self.auto_scroll_switch.grid(row=4,
                                     column=0,
                                     padx=20,
                                     pady=(0, 20),
                                     sticky="ew")

    def auto_scroll_switch_event(self):
        if self.auto_scroll_var.get() == "on":
            self.midframe.terminal_text_label.set_auto_scroll(True)
        else:
            self.midframe.terminal_text_label.set_auto_scroll(False)

    def default_mode_switch_event(self):
        if self.default_mode_switch_var.get() == "on":
            self.auto_mode_switch_var.set("auto_off")
            self.newline_mode_switch_var.set("ln_off")
        else:
            if self.auto_mode_switch_var.get() == "auto_off" or self.newline_mode_switch_var.get() == "ln_off":
                self.default_mode_switch_var.set("on")

    def newline_mode_switch_event(self):
        if self.newline_mode_switch_var.get() == "ln_on":
            self.auto_mode_switch_var.set("auto_off")
            self.default_mode_switch_var.set("off")
        else:
            self.default_mode_switch_var.set("on")

    def auto_mode_switch_event(self):
        if self.auto_mode_switch_var.get() == "auto_on":
            self.default_mode_switch_var.set("off")
            self.newline_mode_switch_var.set("ln_off")
        else:
            self.default_mode_switch_var.set("on")

    # def segmented_button_event(self, value):
    #     pass

    def clear_button_event(self):
        self.midframe.terminal_text_label.text.delete(1.0, tkinter.END)
        if self.midframe.plot_widget is not None:
            self.midframe.plot_widget.clear()

    def switch_event(self):
        if self.switch_var.get() == "plotter":
            self.midframe.terminal_text_label.show(False)
            self.midframe.plot_widget.show(True)
            self.midframe.plot_widget.plot()
        else:
            self.midframe.terminal_text_label.show(True)
            self.midframe.plot_widget.show(False)

    def stop_button_event(self):
        if not self.app.stop:
            self.state = not self.state
            if self.state:
                thread = threading.Thread(target=self.app.start_read, daemon=True)
                thread.start()
                self.stop_button_var.set("Stop")
                self.stop_button.configure(fg_color="#ab3c59", hover_color="#f7638a")
            else:
                print("\n<communication stopped!>\n")
                self.app.read = False
                self.stop_button_var.set("Start")
                self.stop_button.configure(fg_color=button_color, hover_color=button_hover_color)


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x200")
        self.title("Warning!")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Warning! Stop and disconnect before exit!")
        self.label.grid(row=0, column=0,
                        padx=20, pady=20,
                        sticky="nsew")


class CustomLabel(customtkinter.CTkTextbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack()
        self.text = self._textbox
        self.text.tag_configure("color_red", foreground="red")
        self.auto_scroll = True
        # self.configure(text_color="red")

    def write(self, text):
        self.text.insert(tkinter.END, text)
        if self.auto_scroll:
            self.text.see("end")
        # self.configure(text=self.text)

    def flush(self):
        pass

    def error_write(self, text):
        self.text.insert(tkinter.END, text, "color_red")
        if self.auto_scroll:
            self.text.see("end")

    def set_auto_scroll(self, mode):
        self.auto_scroll = mode

    def show(self, show):
        if show:
            self.master.grid_columnconfigure(0, weight=1)
            self.master.grid_rowconfigure(0, weight=1)
            self.grid(row=0,
                      column=0,
                      padx=0,
                      pady=0,
                      sticky="nsew")
        else:
            self.grid_forget()
