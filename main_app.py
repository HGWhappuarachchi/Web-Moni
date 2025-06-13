# main_app.py
import customtkinter as ctk
import tkinter as tk
import threading
import time
import os
import database
import pinger
import emailer
from ctk_meter import CTkMeter
from logger_setup import get_logger_for_ip

database.initialize_db()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CHECK_INTERVAL = 5
CONSECUTIVE_FAILURES_THRESHOLD = 5
WIDGET_SIZES = {"Small": 180, "Medium": 220, "Large": 280}

# --- Draggable Window Class (DEFINITIVELY CORRECTED) ---
class DraggableToplevel(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._offset_x = 0
        self._offset_y = 0
        self.bind("<Enter>", lambda e: self.wm_attributes("-alpha", 1.0))
        self.bind("<Leave>", lambda e: self.wm_attributes("-alpha", 0.9))

    def make_draggable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_press)
        widget.bind("<B1-Motion>", self.on_drag)

    def on_press(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def on_drag(self, event):
        # --- THE FINAL, CORRECTED DRAGGING LOGIC ---
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

class NetworkMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ... (rest of the code is identical to the previous version and correct)
        self.title("Network Latency Monitor"); self.geometry("1200x750")
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.ip_widgets = {}; self.failure_counters = {}; self.alert_sent_flags = {}; self.widget_windows = {}
        self.sidebar_frame = ctk.CTkFrame(self, width=180, corner_radius=0); self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew"); self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Monitor", font=ctk.CTkFont(size=20, weight="bold")); self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.dashboard_button = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard_frame); self.dashboard_button.grid(row=1, column=0, padx=20, pady=10)
        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings_frame); self.settings_button.grid(row=2, column=0, padx=20, pady=10)
        self.dashboard_frame = ctk.CTkFrame(self, corner_radius=0); self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.dashboard_frame.grid_rowconfigure(1, weight=1); self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_label = ctk.CTkLabel(self.dashboard_frame, text="Live Network Status Dashboard", font=ctk.CTkFont(size=18)); self.dashboard_label.grid(row=0, column=0, padx=20, pady=20)
        self.ip_status_frame = ctk.CTkScrollableFrame(self.dashboard_frame, label_text="Monitored Devices"); self.ip_status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.settings_label = ctk.CTkLabel(self.settings_frame, text="Application Settings", font=ctk.CTkFont(size=18)); self.settings_label.pack(padx=20, pady=20)
        self.manage_ips_button = ctk.CTkButton(self.settings_frame, text="Manage IPs to Monitor", command=self.open_ip_management_window); self.manage_ips_button.pack(pady=10)
        self.manage_users_button = ctk.CTkButton(self.settings_frame, text="Manage Alert Recipients", command=self.open_user_management_window); self.manage_users_button.pack(pady=10)
        self.email_config_button = ctk.CTkButton(self.settings_frame, text="Configure Email Account", command=self.open_email_config_window); self.email_config_button.pack(pady=10)
        self.refresh_dashboard_widgets(); self.show_dashboard_frame(); self.start_monitoring(); self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        for ip_id in list(self.widget_windows.keys()):
            self.close_widget(ip_id, save_position=True)
        self.destroy()

    def create_widget_for_ip(self, ip_id, ip_data):
        ip_id_str = str(ip_id)
        if ip_id_str in self.widget_windows: return
        widget_win = DraggableToplevel(self)
        widget_win.overrideredirect(True)
        is_on_top = bool(ip_data['widget_ontop'])
        widget_size = WIDGET_SIZES.get(ip_data['widget_size'], WIDGET_SIZES["Medium"])
        widget_win.wm_attributes("-topmost", is_on_top)
        widget_win.geometry(f"+{ip_data['widget_pos_x']}+{ip_data['widget_pos_y']}")
        magic_color = '#121212'; widget_win.config(background=magic_color); widget_win.wm_attributes("-transparentcolor", magic_color)
        frame = ctk.CTkFrame(widget_win, fg_color="#2B2B2B", corner_radius=20, border_width=2, border_color="grey20"); frame.pack(padx=1, pady=1)
        grab_bar = ctk.CTkFrame(frame, fg_color="#3D3D3D", height=20, corner_radius=0, cursor="fleur"); grab_bar.pack(fill="x", padx=0, pady=0)
        widget_win.make_draggable(grab_bar)
        meter = CTkMeter(frame, from_=0, to=200, width=widget_size, height=widget_size, title_text=f"{ip_data['address']}\n({ip_data['description']})", title_font=("Arial", int(widget_size*0.06), "bold"), text_font=("Arial", int(widget_size*0.09), "bold"), arc_color_ranges=(40, 100)); meter.pack(pady=5, padx=5)
        meter.show_error("...")
        context_menu = tk.Menu(frame, tearoff=0, background="#2B2B2B", foreground="white", activebackground="#565B5E", activeforeground="white", relief="flat", borderwidth=0)
        resize_menu = tk.Menu(context_menu, tearoff=0, background="#2B2B2B", foreground="white");
        resize_menu.add_command(label="Small", command=lambda: self.resize_widget(ip_id_str, "Small"))
        resize_menu.add_command(label="Medium", command=lambda: self.resize_widget(ip_id_str, "Medium"))
        resize_menu.add_command(label="Large", command=lambda: self.resize_widget(ip_id_str, "Large"))
        context_menu.add_cascade(label="Resize", menu=resize_menu)
        on_top_var = tk.BooleanVar(value=is_on_top)
        context_menu.add_checkbutton(label="Keep on Top", variable=on_top_var, command=lambda: self.toggle_ontop(ip_id_str, on_top_var.get()))
        context_menu.add_separator()
        context_menu.add_command(label="Close Widget", command=lambda: self.close_widget(ip_id_str))
        def show_context_menu(event): context_menu.tk_popup(event.x_root, event.y_root)
        grab_bar.bind("<Button-3>", show_context_menu)
        self.widget_windows[ip_id_str] = {'window': widget_win, 'meter': meter, 'id': ip_id, 'frame': frame}

    def close_widget(self, ip_id_str, save_position=True):
        if ip_id_str in self.widget_windows:
            win_info = self.widget_windows[ip_id_str]
            if save_position:
                database.update_ip_widget_position(win_info['id'], win_info['window'].winfo_x(), win_info['window'].winfo_y())
            win_info['window'].destroy()
            del self.widget_windows[ip_id_str]
            
    # The following methods are unchanged and correct
    def show_dashboard_frame(self):
        self.settings_frame.grid_forget(); self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    def show_settings_frame(self):
        self.dashboard_frame.grid_forget(); self.settings_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True); monitor_thread.start()
    def refresh_dashboard_widgets(self):
        db_ips = {str(ip['id']): ip for ip in database.get_all_ips()}; db_ip_ids = set(db_ips.keys()); ui_ip_ids = set(self.ip_widgets.keys())
        num_columns = 3
        for i in range(num_columns): self.ip_status_frame.grid_columnconfigure(i, weight=1)
        for ip_id in ui_ip_ids - db_ip_ids:
            self.ip_widgets[ip_id]['frame'].destroy()
            if ip_id in self.widget_windows: self.widget_windows[ip_id]['window'].destroy()
            del self.ip_widgets[ip_id]
        row, col = 0, 0
        for ip_id, ip in db_ips.items():
            if ip_id in self.ip_widgets: self.ip_widgets[ip_id]['frame'].grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            else:
                frame = ctk.CTkFrame(self.ip_status_frame); frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                meter = CTkMeter(frame, from_=0, to=200, width=220, height=220, title_text=f"{ip['address']}\n({ip['description']})", arc_color_ranges=(40, 100)); meter.pack(pady=5, padx=5); meter.show_error("PENDING")
                button_frame = ctk.CTkFrame(frame, fg_color="transparent"); button_frame.pack(fill="x", padx=5, pady=(0, 5)); button_frame.grid_columnconfigure((0,1), weight=1)
                log_button = ctk.CTkButton(button_frame, text="View Log", height=24, command=lambda addr=ip['address']: self.open_log_viewer_window(addr)); log_button.grid(row=0, column=0, padx=5, sticky="ew")
                widget_button = ctk.CTkButton(button_frame, text="Widget", height=24, command=lambda ip_id=ip_id, ip_data=ip: self.create_widget_for_ip(ip_id, ip_data)); widget_button.grid(row=0, column=1, padx=5, sticky="ew")
                self.ip_widgets[ip_id] = {'frame': frame, 'meter': meter}
            col += 1
            if col >= num_columns: col = 0; row += 1
    def _update_ui_for_ip(self, ip_id, latency):
        ip_id_str = str(ip_id)
        if ip_id_str in self.ip_widgets:
            meter = self.ip_widgets[ip_id_str]['meter']
            if latency is not None: meter.set(latency)
            else: meter.show_error("TIMEOUT")
        if ip_id_str in self.widget_windows:
            widget_meter = self.widget_windows[ip_id_str]['meter']
            if latency is not None: widget_meter.set(latency)
            else: widget_meter.show_error("TIMEOUT")
    def monitoring_loop(self):
        print("Monitoring thread started.")
        while True:
            self.after(0, self.refresh_dashboard_widgets); time.sleep(1)
            ips_to_monitor = database.get_all_ips()
            if not ips_to_monitor: time.sleep(CHECK_INTERVAL); continue
            email_settings = database.get_email_settings(); recipients = database.get_all_users()
            for ip in ips_to_monitor:
                ip_id_str = str(ip['id']); ip_address = ip['address']; logger = get_logger_for_ip(ip_address)
                if ip_id_str not in self.failure_counters: self.failure_counters[ip_id_str] = 0; self.alert_sent_flags[ip_id_str] = False
                latency = pinger.check_latency(ip_address)
                self.after(0, self._update_ui_for_ip, ip['id'], latency)
                if latency is not None:
                    log_message = f"SUCCESS: Latency is {latency:.2f} ms"; logger.info(log_message)
                    if self.failure_counters[ip_id_str] > 0: logger.info("RECOVERY: Host is reachable.")
                    self.failure_counters[ip_id_str] = 0; self.alert_sent_flags[ip_id_str] = False
                else:
                    log_message = f"FAILURE: Host is UNREACHABLE"; logger.warning(log_message)
                    self.failure_counters[ip_id_str] += 1
                    if (self.failure_counters[ip_id_str] >= CONSECUTIVE_FAILURES_THRESHOLD and not self.alert_sent_flags[ip_id_str]):
                        self.alert_sent_flags[ip_id_str] = True; logger.error(f"ALERT: Down for {self.failure_counters[ip_id_str]} checks.")
                        email_thread = threading.Thread(target=emailer.send_alert_email, args=(ip_address, self.failure_counters[ip_id_str], email_settings, recipients), daemon=True); email_thread.start()
            time.sleep(CHECK_INTERVAL)
    def resize_widget(self, ip_id_str, size_name):
        if ip_id_str in self.widget_windows:
            win_info = self.widget_windows[ip_id_str]
            new_size = WIDGET_SIZES.get(size_name)
            win_info['meter'].set_size(new_size, new_size)
            database.update_ip_widget_size(win_info['id'], size_name)
    def toggle_ontop(self, ip_id_str, on_top_status):
        if ip_id_str in self.widget_windows:
            win_info = self.widget_windows[ip_id_str]
            win_info['window'].wm_attributes("-topmost", on_top_status)
            database.update_ip_widget_ontop(win_info['id'], 1 if on_top_status else 0)
    def open_log_viewer_window(self, ip_address):
        win_log = ctk.CTkToplevel(self); win_log.title(f"Log for {ip_address}"); win_log.geometry("700x500"); win_log.transient(self); win_log.grab_set()
        textbox = ctk.CTkTextbox(win_log, wrap="none"); textbox.pack(fill="both", expand=True, padx=10, pady=10)
        log_file_path = os.path.join('logs', f'{ip_address}.log')
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f: textbox.insert("1.0", f.read())
        except FileNotFoundError: textbox.insert("1.0", f"Log file not found for {ip_address}")
        textbox.configure(state="disabled")
    def open_ip_management_window(self):
        win_ip = ctk.CTkToplevel(self); win_ip.title("Manage IPs"); win_ip.geometry("500x500"); win_ip.transient(self); win_ip.grab_set()
        add_frame = ctk.CTkFrame(win_ip); add_frame.pack(pady=10, padx=10, fill="x")
        ip_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter IP Address"); ip_entry.pack(side="left", padx=5, expand=True, fill="x")
        desc_entry = ctk.CTkEntry(add_frame, placeholder_text="Description"); desc_entry.pack(side="left", padx=5, expand=True, fill="x")
        list_frame = ctk.CTkScrollableFrame(win_ip, label_text="Current IPs"); list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        def refresh_ip_list():
            for widget in list_frame.winfo_children(): widget.destroy()
            for ip in database.get_all_ips():
                row_frame = ctk.CTkFrame(list_frame); label_text = f"{ip['address']} ({ip['description']})"
                ctk.CTkLabel(row_frame, text=label_text).pack(side="left", padx=5, pady=2)
                delete_button = ctk.CTkButton(row_frame, text="Delete", fg_color="red", hover_color="darkred", command=lambda ip_id=ip['id']: (database.delete_ip(ip_id), refresh_ip_list())); delete_button.pack(side="right", padx=5)
                row_frame.pack(fill="x", pady=2)
        def add_new_ip():
            if ip_entry.get() and desc_entry.get(): database.add_ip(ip_entry.get(), desc_entry.get()); ip_entry.delete(0, 'end'); desc_entry.delete(0, 'end'); refresh_ip_list()
        add_button = ctk.CTkButton(add_frame, text="Add IP", command=add_new_ip); add_button.pack(side="left", padx=5); refresh_ip_list()
    def open_user_management_window(self):
        win_user = ctk.CTkToplevel(self); win_user.title("Manage Alert Recipients"); win_user.geometry("500x500"); win_user.transient(self); win_user.grab_set()
        add_frame = ctk.CTkFrame(win_user); add_frame.pack(pady=10, padx=10, fill="x")
        user_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter Recipient Email"); user_entry.pack(side="left", padx=5, expand=True, fill="x")
        list_frame = ctk.CTkScrollableFrame(win_user, label_text="Current Users"); list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        def refresh_user_list():
            for widget in list_frame.winfo_children(): widget.destroy()
            for user in database.get_all_users():
                row_frame = ctk.CTkFrame(list_frame); ctk.CTkLabel(row_frame, text=user['email']).pack(side="left", padx=5, pady=2)
                delete_button = ctk.CTkButton(row_frame, text="Delete", fg_color="red", hover_color="darkred", command=lambda user_id=user['id']: (database.delete_user(user_id), refresh_user_list())); delete_button.pack(side="right", padx=5)
                row_frame.pack(fill="x", pady=2)
        def add_new_user():
            if user_entry.get(): database.add_user(user_entry.get()); user_entry.delete(0, 'end'); refresh_user_list()
        add_button = ctk.CTkButton(add_frame, text="Add User", command=add_new_user); add_button.pack(side="left", padx=5); refresh_user_list()
    def open_email_config_window(self):
        win_email = ctk.CTkToplevel(self); win_email.title("Email Account Configuration"); win_email.geometry("400x250"); win_email.transient(self); win_email.grab_set()
        ctk.CTkLabel(win_email, text="Sender Email (Office 365):").pack(padx=20, pady=(10,0)); email_entry = ctk.CTkEntry(win_email, width=300); email_entry.pack(padx=20)
        ctk.CTkLabel(win_email, text="App Password:").pack(padx=20, pady=(10,0)); password_entry = ctk.CTkEntry(win_email, show="*", width=300); password_entry.pack(padx=20)
        current_settings = database.get_email_settings();
        if current_settings: email_entry.insert(0, current_settings['sender_email'] or ""); password_entry.insert(0, current_settings['sender_password'] or "")
        def save_settings(): database.update_email_settings(email_entry.get(), password_entry.get()); win_email.destroy()
        save_button = ctk.CTkButton(win_email, text="Save Settings", command=save_settings); save_button.pack(pady=20)

if __name__ == "__main__":
    app = NetworkMonitorApp()
    app.mainloop()