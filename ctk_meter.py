# ctk_meter.py
import customtkinter as ctk
import tkinter as tk
import math

class CTkMeter(ctk.CTkFrame):
    def __init__(self, master, from_=0, to=100, width=200, height=200, **kwargs):
        super().__init__(master, width=width, height=height)
        self.from_ = from_
        self.to = to
        self.width = width
        self.height = height
        self.text_font = kwargs.get("text_font", ("Arial", 16))
        self.indicator_color = kwargs.get("indicator_color", "white")
        self.indicator_bg_color = kwargs.get("indicator_bg_color", "grey25")
        self.arc_colors = kwargs.get("arc_colors", ("green", "yellow", "red"))
        self.arc_color_ranges = kwargs.get("arc_color_ranges", (50, 80))
        self.text_color = kwargs.get("text_color", "white")
        self.title_text = kwargs.get("title_text", "")
        self.title_font = kwargs.get("title_font", ("Arial", 12))
        self.title_color = kwargs.get("title_color", "white")
        self.value = from_
        self.error_text = None
        self.configure(fg_color="transparent")
        bg_color = self.master._apply_appearance_mode(self.master.cget("fg_color"))
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=bg_color, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        self.draw_meter()
        self.set(self.value)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.canvas.config(width=width, height=height)
        self.draw_meter()
        self._update_display()

    def draw_meter(self):
        self.canvas.delete("all")
        start_angle, extent_angle = 0, 180
        cx, cy, r = self.width / 2, self.height / 2, self.width / 2 - (self.width * 0.1)
        
        total_range = self.to - self.from_
        first_segment_angle = (self.arc_color_ranges[0] / total_range) * extent_angle
        second_segment_angle = (self.arc_color_ranges[1] / total_range) * extent_angle
        
        arc_width = self.width * 0.07
        
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_angle, extent=extent_angle-second_segment_angle, style='arc', outline=self.arc_colors[2], width=arc_width)
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_angle+(extent_angle-second_segment_angle), extent=second_segment_angle-first_segment_angle, style='arc', outline=self.arc_colors[1], width=arc_width)
        self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start_angle+(extent_angle-first_segment_angle), extent=first_segment_angle, style='arc', outline=self.arc_colors[0], width=arc_width)
        
        self.canvas.create_text(cx, cy + (cy*0.5), text=self.title_text, font=self.title_font, fill=self.title_color, justify='center')
        self.text_id = self.canvas.create_text(cx, cy + (cy*0.2), text="", font=self.text_font, fill=self.text_color)
        self.canvas.create_text(cx - r, cy + 5, text=str(self.from_), font=(self.text_font[0], int(self.width*0.04)), fill=self.text_color)
        self.canvas.create_text(cx + r, cy + 5, text=str(self.to), font=(self.text_font[0], int(self.width*0.04)), fill=self.text_color)
        
        self.indicator_id = self.canvas.create_line(0,0,0,0, fill=self.indicator_color, width=3)
        self.canvas.create_oval(cx-7, cy-7, cx+7, cy+7, fill=self.indicator_bg_color, outline="")

    def set(self, value):
        self.value = max(self.from_, min(self.to, value)); self.error_text = None; self._update_display()
    def show_error(self, text):
        self.error_text = text; self._update_display()
    def _update_display(self):
        cx, cy, r = self.width / 2, self.height / 2, self.width / 2 - (self.width * 0.13)
        if self.error_text:
            self.canvas.itemconfig(self.text_id, text=self.error_text)
            angle = math.radians(180)
            x0, y0 = cx, cy; x1 = cx + r * math.cos(angle); y1 = cy - r * math.sin(angle)
            self.canvas.coords(self.indicator_id, x0, y0, x1, y1)
        else:
            self.canvas.itemconfig(self.text_id, text=f"{self.value:.1f} ms")
            total_range = self.to - self.from_
            percentage = (self.value - self.from_) / total_range if total_range != 0 else 0
            angle_deg = 180 - (percentage * 180); angle_rad = math.radians(angle_deg)
            x0, y0 = cx, cy; x1 = cx + r * math.cos(angle_rad); y1 = cy - r * math.sin(angle_rad)
            self.canvas.coords(self.indicator_id, x0, y0, x1, y1)