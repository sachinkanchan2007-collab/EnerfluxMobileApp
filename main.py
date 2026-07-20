from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

import os
os.environ['KIVY_CAMERA'] = 'opencv'

import time
import base64
from io import BytesIO
from datetime import datetime

# Kivy core camera setup
from kivy.core.camera import CameraBase
if not hasattr(CameraBase, 'fps'):
    CameraBase.fps = 30

# Kivy UI Components
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.image import Image  
from kivy.uix.camera import Camera  
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp

from kivy.core.audio import SoundLoader

# serial library (For Android/PC)
try:
    import serial
except ImportError:
    serial = None

# फाईलचे नाव बदलून 'serial_setting_done.txt' केले आहे
DATABASE_FILE = "serial_setting_done.txt"

BASE64_LOGO = "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"

COMMAND_CHART = {
    "RTC_SET": "285347492D572D5254432D31343331303429",
    "SH_CAL": "285347492D572D53482D43414C29",
    "CT_CAL": "285347492D572D43542D43414C29",
    "DATA_CLEAR": "285347492D572D414C2D44523129",
    "METER_CLR": "285347492D572D434C5229",
    "RESP_SUCCESS": "5375636573730D0A"
}

CURRENT_BAUD = 9600
COLOR_LIGHT_GREEN = (0.55, 0.85, 0.55, 1)   
COLOR_LITE_ORANGE = (1, 0.6, 0.2, 1)        
COLOR_STOP = (1, 0.3, 0.3, 1)               
COLOR_BACK = (0.6, 0.6, 0.6, 1)              

def play_alert_sound(sound_type="success"):
    try:
        sound = None
        if sound_type == "success":
            sound = SoundLoader.load('success.wav')
        elif sound_type == "alert":
            sound = SoundLoader.load('alert.wav')
        elif sound_type == "not_scan":
            sound = SoundLoader.load('not_scan.mp3')
        elif sound_type == "next_meter":
            sound = SoundLoader.load('next_meter.mp3')
        if sound: sound.play()
    except Exception as e:
        print("Sound playback failed:", e)

class RoundedButton(Button):
    def __init__(self, bg_color=COLOR_LIGHT_GREEN, radius=8, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.custom_bg_color = bg_color
        self.radius = radius
        self.halign = 'center'
        self.valign = 'middle'
        self.font_size = '11sp'  # मोबाईल स्क्रीनसाठी योग्य फॉन्ट साईज
        self.bind(size=self._update_text_size)
        with self.canvas.before:
            self.color_obj = Color(*self.custom_bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_canvas, size=self._update_canvas)
    def _update_text_size(self, instance, value):
        self.text_size = (instance.width - dp(10), None)
        
    #def _update_canvas(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_custom_color(self, new_color):
        self.custom_bg_color = new_color
        self.color_obj.rgba = new_color

# ==========================================
# Base Screen Structure
# ==========================================
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_process = None
        
       self.ser = init_serial()

        self.main_layout = BoxLayout(orientation='vertical')
        
        self.header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        with self.header.canvas.before:
            Color(0.5, 0.85, 0.5, 1)
            self.rect = Rectangle(size=self.header.size, pos=self.header.pos)
        self.header.bind(size=self._update_rect, pos=self._update_rect)
        
        self.lbl_title = Label(text=" ENERFLUX", color=(0,0,0,1), bold=True, font_size='18sp', halign='left', size_hint_x=0.4)
        self.lbl_status = Label(text="Connected", color=(0,0,0,1), font_size='13sp', halign='right', size_hint_x=0.5)
        
        self.led_indicator = Label(size_hint_x=0.1)
        with self.led_indicator.canvas.before:
            self.led_color = Color(0, 1, 0, 1)
            self.led_rect = Rectangle(size=(dp(15), dp(15)), pos=self.led_indicator.pos)
        self.led_indicator.bind(size=self._update_led, pos=self._update_led)
        
        self.header.add_widget(self.lbl_title)
        self.header.add_widget(self.lbl_status)
        self.header.add_widget(self.led_indicator)
        self.main_layout.add_widget(self.header)
        
        self.time_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), padding=[dp(10), 0, dp(10), 0])
        with self.time_bar.canvas.before:
            Color(0.6, 0.9, 0.6, 0.6)
            self.time_rect = Rectangle(size=self.time_bar.size, pos=self.time_bar.pos)
        self.time_bar.bind(size=self._update_time_rect, pos=self._update_time_rect)
        
        self.lbl_time = Label(text="", color=(0,0,0,1), font_size='12sp', bold=True, halign='left', valign='middle', size_hint_x=0.55)
        self.lbl_time.bind(size=self.lbl_time.setter('text_size'))
        
        # २. बटनचा फॉन्ट 12sp करा आणि रुंदी 0.45 करा
        self.btn_top_settings = RoundedButton(
            text=f"Settings ({CURRENT_BAUD})", 
            bg_color=COLOR_LIGHT_GREEN, 
            bold=True, 
            font_size='12sp',  # फॉन्ट १२ केला
            size_hint_x=0.45,  # रुंदी वाढवली
            size_hint_y=0.8, 
            pos_hint={'center_y': 0.5}
        )
        self.btn_top_settings.bind(on_press=lambda x: setattr(self.manager, 'current', 'settings'))
        
        self.time_bar.add_widget(self.lbl_time)
        self.time_bar.add_widget(self.btn_top_settings)
        self.main_layout.add_widget(self.time_bar)
        
        self.logo_area = BoxLayout(size_hint_y=None, height=dp(100), orientation='vertical', padding=[0, dp(5), 0, dp(5)])
        with self.logo_area.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.logo_bg_rect = Rectangle(size=self.logo_area.size, pos=self.logo_area.pos)
        self.logo_area.bind(size=self._update_logo_bg, pos=self._update_logo_bg)

        try:
            binary_data = base64.b64decode(BASE64_LOGO)
            data = BytesIO(binary_data)
            core_image = CoreImage(data, ext="png")
            self.logo_image = Image(texture=core_image.texture, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            self.logo_area.add_widget(self.logo_image)
        except Exception:
            self.logo_image = Label(text="ENERFLUX LOGO", color=(0,0,0,1))
            self.logo_area.add_widget(self.logo_image)

        self.main_layout.add_widget(self.logo_area)
        
        self.content_area = BoxLayout(orientation='vertical', size_hint_y=0.68)
        self.main_layout.add_widget(self.content_area)
        self.add_widget(self.main_layout)
        
        Clock.schedule_interval(self.update_header, 1.0)
        self.last_stop_press_time = 0

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_time_rect(self, instance, value):
        self.time_rect.pos = instance.pos
        self.time_rect.size = instance.size
        
    def _update_led(self, instance, value):
        self.led_rect.pos = (instance.pos[0] + dp(5), instance.pos[1] + instance.size[1]/3)

    def _update_logo_bg(self, instance, value):
        self.logo_bg_rect.pos = instance.pos
        self.logo_bg_rect.size = instance.size

    def update_header(self, dt):
        self.lbl_time.text = datetime.now().strftime("Date: %d/%m/%Y | Time: %H:%M:%S")

    def change_btn_color(self, btn, status):
        if hasattr(btn, 'set_custom_color'):
            if status == "ON":
                btn.set_custom_color(COLOR_LITE_ORANGE)
            else:
                btn.set_custom_color(COLOR_LIGHT_GREEN)

    def handle_stop_press(self, stop_callback_func):
        current_time = time.time()
        if stop_callback_func: stop_callback_func()
        if current_time - self.last_stop_press_time < 2.0:
            self.manager.current = 'main'
        self.last_stop_press_time = current_time
    def on_pre_enter(self, *args):
        if hasattr(self, 'btn_top_settings'):
            self.btn_top_settings.font_size = '12sp'
            self.btn_top_settings.text = f"Settings ({CURRENT_BAUD})"


# ==========================================
# MainWindow & Screens (Settings/Calibration)
# ==========================================
class MainWindow(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display_msg = Label(text="Welcome to Enerflux App", size_hint_y=0.08, font_size='16sp', bold=True)
        self.content_area.add_widget(self.display_msg)
        
        grid = GridLayout(cols=1, spacing=dp(8), padding=[dp(25), dp(5), dp(25), dp(10)], size_hint_y=0.92)
        
        self.btn_rtc = RoundedButton(text="RTC Setting", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(46))
        self.btn_rtc.bind(on_press=self.process_rtc)
        
        btn_clear_data = RoundedButton(text="Meter All Data Clear", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(46))
        btn_clear_data.bind(on_press=self.ask_password_data_clear)
        
        btn_calibration = RoundedButton(text="Meter Calibration", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(46))
        btn_calibration.bind(on_press=lambda x: setattr(self.manager, 'current', 'calibration'))
        
        btn_serial = RoundedButton(text="Meter Serial Setting", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(46))
        btn_serial.bind(on_press=lambda x: setattr(self.manager, 'current', 'serial_setting'))
        
        self.btn_meter_clear = RoundedButton(text="Meter Clear", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(46))
        self.btn_meter_clear.bind(on_press=self.process_meter_clear)
        
        btn_stop = RoundedButton(text="STOP", bg_color=COLOR_STOP, bold=True, size_hint_y=None, height=dp(46))
        btn_stop.bind(on_press=self.process_stop)
        
        grid.add_widget(self.btn_rtc)
        grid.add_widget(btn_clear_data)
        grid.add_widget(btn_calibration)
        grid.add_widget(btn_serial)
        grid.add_widget(self.btn_meter_clear)
        grid.add_widget(btn_stop)
        self.content_area.add_widget(grid)

    def process_rtc(self, instance):
        self.stop_all_processes()
        self.active_process = "rtc"
        self.rtc_button_ref = instance
        instance.background_color = [1, 0.6, 0.2, 1]
        self.display_msg.text = "RTC Setting Start..."
        self.rtc_event = Clock.schedule_interval(self.send_rtc_command, 2.0)

    def send_rtc_command(self, dt):
        if self.ser and self.ser.is_open:
            try: self.ser.write(bytes.fromhex(COMMAND_CHART.get("RTC_SET")))
            except Exception: pass

    def ask_password_data_clear(self, instance):
        layout = GridLayout(cols=1, spacing=10, padding=[dp(20), dp(10), dp(20), dp(10)])
        self.clear_pass_input = TextInput(password=True, readonly=True, halign='center', font_size='24sp', size_hint_y=None, height=dp(50))
        layout.add_widget(self.clear_pass_input)

        num_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.7)
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Clear', '0', 'Enter']:
            btn = RoundedButton(text=i, bg_color=COLOR_LIGHT_GREEN if i not in ['Clear', 'Enter'] else COLOR_BACK)
            btn.bind(on_press=lambda x, b=i: self.handle_clear_keypad(b, instance))
            num_grid.add_widget(btn)
        layout.add_widget(num_grid)

        btn_close = RoundedButton(text="Cancel", bg_color=COLOR_STOP, size_hint_y=None, height=dp(45))
        btn_close.bind(on_press=lambda x: self.clear_popup.dismiss())
        layout.add_widget(btn_close)
        self.clear_popup = Popup(title='Enter Password to Clear Data', content=layout, size_hint=(0.85, 0.7), auto_dismiss=False)
        self.clear_popup.open()

    def handle_clear_keypad(self, button_text, original_instance):
        if button_text == 'Clear': self.clear_pass_input.text = ""
        elif button_text == 'Enter':
            if self.clear_pass_input.text == "1234":
                self.clear_popup.dismiss()
                self.process_all_data_clear(original_instance)
            else: self.clear_pass_input.text = ""
        else: self.clear_pass_input.text += button_text

    def process_all_data_clear(self, instance):
        self.stop_all_processes()
        self.active_process = "all_data_clear"
        self.data_clear_button_ref = instance
        instance.background_color = [1, 0.6, 0.2, 1]
        self.display_msg.text = "Meter All Data Clear Start..."
        self.clear_event = Clock.schedule_interval(self.send_all_data_clear_command, 2.0)

    def send_all_data_clear_command(self, dt):
        if self.ser and self.ser.is_open:
            try: self.ser.write(bytes.fromhex(COMMAND_CHART.get("DATA_CLEAR")))
            except Exception: pass

    def process_meter_clear(self, instance):
        self.stop_all_processes()
        self.active_process = "meter_clear"
        self.meter_clear_button_ref = instance
        instance.background_color = [1, 0.6, 0.2, 1]
        self.display_msg.text = "Meter Clear Start..."
        self.meter_clear_event = Clock.schedule_interval(self.send_meter_clear_command, 2.0)

    def send_meter_clear_command(self, dt):
        if self.ser and self.ser.is_open:
            try: self.ser.write(bytes.fromhex(COMMAND_CHART.get("METER_CLR")))
            except Exception: pass

    def process_stop(self, instance):
        self.stop_all_processes()
        self.display_msg.text = "All Processes Stopped."

    def stop_all_processes(self):
        if hasattr(self, 'rtc_event') and self.rtc_event: Clock.unschedule(self.rtc_event)
        if hasattr(self, 'clear_event') and self.clear_event: Clock.unschedule(self.clear_event)
        if hasattr(self, 'meter_clear_event') and self.meter_clear_event: Clock.unschedule(self.meter_clear_event)
        if hasattr(self, 'rtc_button_ref') and self.rtc_button_ref: self.rtc_button_ref.background_color = COLOR_LIGHT_GREEN
        if hasattr(self, 'data_clear_button_ref') and self.data_clear_button_ref: self.data_clear_button_ref.background_color = COLOR_LIGHT_GREEN
        if hasattr(self, 'meter_clear_button_ref') and self.meter_clear_button_ref: self.meter_clear_button_ref.background_color = COLOR_LIGHT_GREEN
        self.active_process = None

class SettingsWindow(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        grid = GridLayout(cols=1, spacing=10, padding=[dp(30), dp(10), dp(30), dp(15)])
        self.lbl_info = Label(text=f"Current Baud Rate: {CURRENT_BAUD}", font_size='16sp', size_hint_y=None, height=40)
        grid.add_widget(self.lbl_info)
        
        btn_2400 = RoundedButton(text="Set Baud Rate 2400", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(50))
        btn_2400.bind(on_press=lambda x: self.set_baud(2400))
        btn_9600 = RoundedButton(text="Set Baud Rate 9600", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(50))
        btn_9600.bind(on_press=lambda x: self.set_baud(9600))
        
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=15)
        btn_back = RoundedButton(text="Return", bg_color=COLOR_BACK, bold=True)
        btn_back.bind(on_press=lambda x: self.go_back())
        btn_stop = RoundedButton(text="STOP", bg_color=COLOR_STOP, bold=True)
        bottom_layout.add_widget(btn_back)
        bottom_layout.add_widget(btn_stop)
        
        grid.add_widget(btn_2400)
        grid.add_widget(btn_9600)
        grid.add_widget(bottom_layout)
        self.content_area.add_widget(grid)

    def set_baud(self, baud):
        global CURRENT_BAUD
        CURRENT_BAUD = baud
        self.lbl_info.text = f"Baud Rate Set to {baud}"
        if self.ser: self.ser.baudrate = baud
        
        self.btn_top_settings.font_size = '12sp'
        self.btn_top_settings.text = f"Settings ({CURRENT_BAUD})"
  

    def go_back(self): self.manager.current = 'main'

class CalibrationWindow(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lbl_msg = Label(text="Calibration Mode Idle", size_hint_y=0.15, font_size='18sp', bold=True)
        self.content_area.add_widget(self.lbl_msg)
        
        grid = GridLayout(cols=1, spacing=10, padding=[dp(30), dp(5), dp(30), dp(15)], size_hint_y=0.85)
        self.btn_shunt = RoundedButton(text="Shunt Calibration", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(50))
        self.btn_shunt.bind(on_press=self.start_shunt)
        self.btn_ct = RoundedButton(text="CT Calibration", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(50))
        self.btn_ct.bind(on_press=self.start_ct)
        
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=15)
        btn_back = RoundedButton(text="Return", bg_color=COLOR_BACK, bold=True)
        btn_back.bind(on_press=lambda x: self.go_back())
        btn_stop = RoundedButton(text="STOP", bg_color=COLOR_STOP, bold=True)
        btn_stop.bind(on_press=self.stop_logic)
        bottom_layout.add_widget(btn_back)
        bottom_layout.add_widget(btn_stop)
        
        grid.add_widget(self.btn_shunt)
        grid.add_widget(self.btn_ct)
        grid.add_widget(bottom_layout)
        self.content_area.add_widget(grid)
        self.shunt_event = None
        self.ct_event = None

    def start_shunt(self, instance):
        self.stop_logic()
        self.lbl_msg.text = "Calibration Start: Shunt Loop"
        self.shunt_event = Clock.schedule_interval(self.send_shunt_data, 1.5)

    def send_shunt_data(self, dt):
        self.change_btn_color(self.btn_shunt, "ON")
        if self.ser and self.ser.is_open: self.ser.write(bytes.fromhex(COMMAND_CHART.get("SH_CAL")))
        Clock.schedule_once(lambda dt: self.change_btn_color(self.btn_shunt, "OFF"), 0.5)

    def start_ct(self, instance):
        self.stop_logic()
        self.lbl_msg.text = "Calibration Start: CT Loop"
        self.ct_event = Clock.schedule_interval(self.send_ct_data, 1.5)

    def send_ct_data(self, dt):
        self.change_btn_color(self.btn_ct, "ON")
        if self.ser and self.ser.is_open: self.ser.write(bytes.fromhex(COMMAND_CHART.get("CT_CAL")))
        Clock.schedule_once(lambda dt: self.change_btn_color(self.btn_ct, "OFF"), 0.5)

    def stop_logic(self, instance=None):
        if self.shunt_event: Clock.unschedule(self.shunt_event); self.shunt_event = None
        if self.ct_event: Clock.unschedule(self.ct_event); self.ct_event = None
        self.change_btn_color(self.btn_shunt, "OFF")
        self.change_btn_color(self.btn_ct, "OFF")
        self.lbl_msg.text = "All Stopped Safely"

    def go_back(self): self.stop_logic(); self.manager.current = 'main'

# ==========================================
# SerialSettingWindow (स्कॅनर आणि फाईल सेव्हिंग)
# ==========================================
class SerialSettingWindow(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lbl_msg = Label(text="Next Meter Serial Scan", size_hint_y=0.1, font_size='18sp', bold=True)
        self.content_area.add_widget(self.lbl_msg)
        
        self.buttons_container = BoxLayout(orientation='vertical', size_hint_y=0.45, spacing=dp(8), padding=[dp(25), dp(5), dp(25), dp(5)])
        
        self.btn_scan = RoundedButton(text="Start Scan Simulation", bg_color=COLOR_LIGHT_GREEN, bold=True, size_hint_y=None, height=dp(48))
        self.btn_scan.bind(on_press=self.simulate_barcode_scan)
        self.buttons_container.add_widget(self.btn_scan)
        
        middle_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(48), spacing=dp(10))
        btn_back = RoundedButton(text="Return", bg_color=COLOR_BACK, bold=True)
        btn_back.bind(on_press=lambda x: self.go_back())
        
        self.btn_stop = RoundedButton(text="STOP Loop", bg_color=COLOR_STOP, bold=True)
        self.btn_stop.bind(on_press=lambda x: self.handle_stop_press(self.stop_logic))
        middle_layout.add_widget(btn_back)
        middle_layout.add_widget(self.btn_stop)
        self.buttons_container.add_widget(middle_layout)
        
        bottom_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(48), spacing=dp(10))
        
        self.btn_edit_serial = RoundedButton(text="Edit Serial Number", bg_color=COLOR_LIGHT_GREEN, bold=True)
        self.btn_edit_serial.bind(on_press=lambda x: setattr(self.manager, 'current', 'edit_serial'))
        
        self.btn_manual_protected = RoundedButton(text="Enter Manually Serial Number", bg_color=COLOR_BACK, bold=True)
        self.btn_manual_protected.bind(on_press=self.ask_manual_entry_password)
        
        bottom_buttons_layout.add_widget(self.btn_edit_serial)
        bottom_buttons_layout.add_widget(self.btn_manual_protected)
        self.buttons_container.add_widget(bottom_buttons_layout)
        
        self.content_area.add_widget(self.buttons_container)
        
        self.camera_container = BoxLayout(size_hint_y=0.45, padding=[dp(30), dp(5), dp(30), dp(5)])
        self.content_area.add_widget(self.camera_container)
        
        self.camera_widget = None
        self.scan_retry_count = 0
        self.scanned_serial_data = ""

    def simulate_barcode_scan(self, instance):
        self.stop_logic()
        self.lbl_msg.text = "Camera Opening & Scanning..."
        self.scan_retry_count = 0 
        self.btn_manual_protected.bg_color = COLOR_BACK
        if not self.camera_widget:
            self.camera_widget = Camera(play=True, index=0, resolution=(640, 480))
            self.camera_container.add_widget(self.camera_widget)
        Clock.schedule_once(self.check_barcode_scan_loop, 2.5)

    def check_barcode_scan_loop(self, dt):
        scan_successful = False 
        if scan_successful:
            self.scanned_serial_data = "12345678"  
            self.process_successful_scan()
        else:
            self.scan_retry_count += 1
            if self.scan_retry_count <= 4:
                self.lbl_msg.text = f"Scanning... {self.scan_retry_count} retry"
                Clock.schedule_once(self.check_barcode_scan_loop, 2.5)
            else:
                self.lbl_msg.text = "Scan Failed! Enter Manually Option Available."
                self.btn_manual_protected.set_custom_color(COLOR_LIGHT_GREEN)
                play_alert_sound("not_scan")
                self.close_camera()

    def ask_manual_entry_password(self, instance):
        layout = GridLayout(cols=1, spacing=10, padding=[dp(20), dp(10), dp(20), dp(10)])
        self.pass_input = TextInput(password=True, readonly=True, halign='center', font_size='22sp', size_hint_y=None, height=dp(45))
        layout.add_widget(self.pass_input)

        num_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.7)
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Clear', '0', 'Enter']:
            btn = RoundedButton(text=i, bg_color=COLOR_LIGHT_GREEN if i not in ['Clear', 'Enter'] else COLOR_BACK)
            btn.bind(on_press=self.handle_password_keypad)
            num_grid.add_widget(btn)
        layout.add_widget(num_grid)

        btn_close = RoundedButton(text="Cancel", bg_color=COLOR_STOP, size_hint_y=None, height=dp(40))
        btn_close.bind(on_press=lambda x: self.pass_popup.dismiss())
        layout.add_widget(btn_close)
        self.pass_popup = Popup(title='Enter Password (1234)', content=layout, size_hint=(0.85, 0.75), auto_dismiss=False)
        self.pass_popup.open()

    def handle_password_keypad(self, instance):
        val = instance.text
        if val == 'Clear': self.pass_input.text = ""
        elif val == 'Enter':
            if self.pass_input.text == "1234":
                self.pass_popup.dismiss()
                self.open_manual_serial_keypad()
            else:
                self.pass_input.text = ""
                play_alert_sound("alert")
        else: self.pass_input.text += val

    def open_manual_serial_keypad(self):
        layout = GridLayout(cols=1, spacing=10, padding=[dp(20), dp(10), dp(20), dp(10)])
        self.serial_input_field = TextInput(readonly=True, halign='center', font_size='22sp', size_hint_y=None, height=dp(45), hint_text="Enter Serial")
        layout.add_widget(self.serial_input_field)

        num_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.6)
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Clear', '0', 'ADD']:
            btn = RoundedButton(text=i, bg_color=COLOR_LIGHT_GREEN if i not in ['Clear', 'ADD'] else (COLOR_LITE_ORANGE if i=='ADD' else COLOR_BACK))
            btn.bind(on_press=self.handle_serial_entry_keypad)
            num_grid.add_widget(btn)
        layout.add_widget(num_grid)

        btn_close = RoundedButton(text="Cancel", bg_color=COLOR_STOP, size_hint_y=None, height=dp(40))
        btn_close.bind(on_press=lambda x: self.serial_popup.dismiss())
        layout.add_widget(btn_close)
        self.serial_popup = Popup(title='Enter Meter Serial', content=layout, size_hint=(0.85, 0.8), auto_dismiss=False)
        self.serial_popup.open()

    def handle_serial_entry_keypad(self, instance):
        val = instance.text
        if val == 'Clear': self.serial_input_field.text = ""
        elif val == 'ADD':
            if self.serial_input_field.text.strip():
                self.scanned_serial_data = self.serial_input_field.text.strip()
                self.serial_popup.dismiss()
                self.process_successful_scan()
        else: self.serial_input_field.text += val

    def process_successful_scan(self):
        self.close_camera()
        self.lbl_msg.text = f"Serial {self.scanned_serial_data} Added. Sending Serial Setting Command..."
        Clock.schedule_once(self.send_serial_setting_command, 0.5)

    def send_serial_setting_command(self, dt):
        serial_hex = "".join("{:02x}".format(ord(c)) for c in self.scanned_serial_data)
        serial_cmd = "28" + serial_hex + "29" 
        
        response_received = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.flushInput()
                self.ser.write(bytes.fromhex(serial_cmd))
                time.sleep(0.6)
                read_data = self.ser.read(self.ser.in_waiting or 20).hex().upper()
                if COMMAND_CHART["RESP_SUCCESS"].upper() in read_data:
                    response_received = True
            except Exception as e: print("Transmission error:", e)
        else: response_received = True 

        if response_received:
            self.lbl_msg.text = "Serial Success! Sending Meter Clear Command..."
            play_alert_sound("success")
            Clock.schedule_once(self.send_meter_clear_after_response, 1.0)
        else:
            self.lbl_msg.text = "Serial Setting Failed (No Success Response)"
            play_alert_sound("alert")

    def send_meter_clear_after_response(self, dt):
        clear_cmd = COMMAND_CHART.get("METER_CLR")
        clear_response = False
        if self.ser and self.ser.is_open:
            try:
                self.ser.flushInput()
                self.ser.write(bytes.fromhex(clear_cmd))
                time.sleep(0.6)
                read_data = self.ser.read(self.ser.in_waiting or 20).hex().upper()
                if COMMAND_CHART["RESP_SUCCESS"].upper() in read_data:
                    clear_response = True
            except Exception as e: print("Clear error:", e)
        else: clear_response = True

        if clear_response:
            # फिक्स: दोन्ही प्रोसेस यशस्वीरित्या पूर्ण झाल्यावर डेटा 'serial_setting_done.txt' मध्ये सेव्ह होतो
            try:
                with open(DATABASE_FILE, "a") as f:
                    f.write(f"{self.scanned_serial_data}\n")
            except Exception as e:
                print("File writing error:", e)

            self.lbl_msg.text = "Next Meter Serial Scan"
            play_alert_sound("next_meter")
        else:
            self.lbl_msg.text = "Meter Clear Failed (No Success Response)"
            play_alert_sound("alert")

    def close_camera(self):
        if self.camera_widget:
            self.camera_widget.play = False
            self.camera_container.remove_widget(self.camera_widget)
            self.camera_widget = None

    def stop_logic(self):
        self.close_camera()
        self.change_btn_color(self.btn_scan, "OFF")
        self.lbl_msg.text = "Next Meter Serial Scan"

    def go_back(self):
        self.stop_logic()
        self.manager.current = 'main'

# ==================================================
# EditSerialWindow (सर्च आणि डिलीट फिक्स)
# ==================================================
class EditSerialWindow(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lbl_msg = Label(text="Enter Password to Access", size_hint_y=0.1, font_size='16sp', bold=True)
        self.content_area.add_widget(self.lbl_msg)

        self.main_grid = GridLayout(cols=1, spacing=10, padding=[dp(30), dp(5), dp(30), dp(15)])
        self.content_area.add_widget(self.main_grid)
        self.show_password_pad()

    def show_password_pad(self):
        self.main_grid.clear_widgets()
        self.password_input = TextInput(password=True, readonly=True, halign='center', font_size='24sp', size_hint_y=None, height=dp(50))
        self.main_grid.add_widget(self.password_input)

        num_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.6)
        for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Clear', '0', 'Enter']:
            btn = RoundedButton(text=i, bg_color=COLOR_LIGHT_GREEN if i not in ['Clear', 'Enter'] else COLOR_BACK)
            btn.bind(on_press=self.handle_keypad)
            num_grid.add_widget(btn)
        self.main_grid.add_widget(num_grid)

        btn_back = RoundedButton(text="Return", bg_color=COLOR_BACK, size_hint_y=None, height=dp(50))
        btn_back.bind(on_press=lambda x: self.go_to_main())
        self.main_grid.add_widget(btn_back)

    def handle_keypad(self, instance):
        text = instance.text
        if text == 'Clear': self.password_input.text = ""
        elif text == 'Enter':
            if self.password_input.text == "1234":
                self.lbl_msg.text = "Access Granted"
                self.show_search_interface()
                play_alert_sound("success")
            else:
                self.lbl_msg.text = "Wrong Password! Try Again."
                self.password_input.text = ""
                play_alert_sound("alert")
        else: self.password_input.text += text

    def show_search_interface(self):
        self.main_grid.clear_widgets()
        self.search_input = TextInput(hint_text="Enter Meter Serial Manually", halign='center', font_size='20sp', size_hint_y=None, height=dp(50))
        self.main_grid.add_widget(self.search_input)

        btn_search = RoundedButton(text="Search Serial Number", bg_color=COLOR_LIGHT_GREEN, size_hint_y=None, height=dp(50))
        btn_search.bind(on_press=self.search_meter_in_file)
        self.main_grid.add_widget(btn_search)

        self.lbl_result = Label(text="", font_size='18sp', bold=True, size_hint_y=0.2)
        self.main_grid.add_widget(self.lbl_result)

        self.btn_delete = RoundedButton(text="DELETE METER", bg_color=COLOR_STOP, size_hint_y=None, height=dp(50))
        self.btn_delete.bind(on_press=self.delete_meter_from_file)
        
        btn_back = RoundedButton(text="Return", bg_color=COLOR_BACK, size_hint_y=None, height=dp(50))
        btn_back.bind(on_press=lambda x: self.go_to_main())
        self.main_grid.add_widget(btn_back)

    def search_meter_in_file(self, instance):
        serial_no = self.search_input.text.strip()
        if not serial_no: return

        # 'serial_setting_done.txt' फाईल मधून शोधणे
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "r") as f:
                meters = f.read().splitlines()

            if serial_no in meters:
                self.lbl_result.text = f"Meter {serial_no} is present in File"
                self.lbl_result.color = (0, 1, 0, 1)
                play_alert_sound("success")
                if self.btn_delete not in self.main_grid.children:
                    self.main_grid.add_widget(self.btn_delete, index=1)
            else: self.show_not_found(serial_no)
        else: self.show_not_found(serial_no)

    def show_not_found(self, serial_no):
        self.lbl_result.text = f"Meter {serial_no} NOT Found!"
        self.lbl_result.color = (1, 0, 0, 1)
        play_alert_sound("alert")
        if self.btn_delete in self.main_grid.children:
            self.main_grid.remove_widget(self.btn_delete)

    def delete_meter_from_file(self, instance):
        serial_no = self.search_input.text.strip()
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, "r") as f:
                meters = f.read().splitlines()
            
            if serial_no in meters:
                meters.remove(serial_no)
                with open(DATABASE_FILE, "w") as f:
                    for m in meters: f.write(f"{m}\n")
                
                self.lbl_result.text = f"Deleted Successfully from File!"
                self.lbl_result.color = (1, 0.5, 0, 1)
                self.search_input.text = ""
                if self.btn_delete in self.main_grid.children:
                    self.main_grid.remove_widget(self.btn_delete)
                play_alert_sound("success")

    def go_to_main(self):
        self.lbl_msg.text = "Enter Password to Access"
        self.show_password_pad()
        self.manager.current = 'main'

# ==========================================
# App Runner
# ==========================================
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('auth_data.json')
        
        layout = GridLayout(cols=1, spacing=10, padding=[30, 50, 30, 50])
        layout.add_widget(Label(text="Enter Authorization Code to Activate App", font_size='15sp', bold=True))
        
        self.code_input = TextInput(hint_text="Enter Code Here", halign='center', font_size='15sp', size_hint_y=None, height=50, input_filter='int')
        layout.add_widget(self.code_input)
        
        btn_verify = Button(text="Verify & Install", background_color=(0.55, 0.85, 0.55, 1), bold=True, size_hint_y=None, height=50)
        btn_verify.bind(on_press=self.verify_code)
        layout.add_widget(btn_verify)
        
        self.lbl_error = Label(text="", color=(1, 0, 0, 1))
        layout.add_widget(self.lbl_error)
        
        self.add_widget(layout)

    def verify_code(self, instance):
        input_code = self.code_input.text.strip()
        
        # ऑथोरायझेशन कोड कॅल्क्युलेशन (मागचे वर्ष + चालू तास)
        now = datetime.now()
        current_hour_24 = now.hour
        last_year = now.year - 1
        
        year_digits_sum = sum(int(d) for d in str(last_year))
        total_sum = year_digits_sum + current_hour_24
        
        base_number = 8886541965
        correct_code = str(base_number * total_sum)
        
        if input_code == correct_code:
            self.store.put('auth', is_verified=True)
            self.manager.current = 'main'
        else:
            self.lbl_error.text = "Invalid Code! Please check your time or code."

from usbserial4a import serial4a
def init_serial():
    if platform == 'android':
        try:
            # हे अँड्रॉइडच्या USB पोर्टला शोधेल
            serial_obj = serial4a.get_serial_port()
            serial_obj.open()
            return serial_obj
        except Exception as e:
            print("Android USB Error:", e)
            return None
    else:
        import serial
        return serial.Serial('COM3', 9600, timeout=1)
class EnerfluxSmartApp(App):
    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.RECORD_AUDIO
            ])

    def build(self):
        sm = ScreenManager()
        # स्क्रीन लिस्ट
        sm.add_widget(AuthScreen(name='auth_screen'))
        sm.add_widget(MainWindow(name='main'))
        sm.add_widget(SettingsWindow(name='settings'))
        sm.add_widget(CalibrationWindow(name='calibration'))
        sm.add_widget(SerialSettingWindow(name='serial_setting'))
        sm.add_widget(EditSerialWindow(name='edit_serial'))
        
        # आधीच पासवर्ड टाकला असेल तर डायरेक्ट मेन स्क्रीन उघडेल
        store = JsonStore('auth_data.json')
        if store.exists('auth') and store.get('auth')['is_verified']:
            sm.current = 'main'
        else:
            sm.current = 'auth_screen'
            
        return sm

if __name__ == '__main__':
    EnerfluxSmartApp().run()
# ==========================================
# इथपर्यंत (नवीन कोड संपला)
# ==========================================