
# Track: Visualization Track (Advanced Turing Machine IDE)

import customtkinter as ctk
import json

# --- PRELOADED POPULAR RULESETS ---
PRESETS = {
    "a^n b^n c^n (Context-Sensitive)": {
        "start_state": "q0",
        "accept_state": "q_accept",
        "reject_state": "q_reject",
        "alphabet": ["a", "b", "c"],
        "transitions": {
            "q0,a": ["q1", "X", "R"], "q0,Y": ["q4", "Y", "R"],
            "q1,a": ["q1", "a", "R"], "q1,Y": ["q1", "Y", "R"], "q1,b": ["q2", "Y", "R"],
            "q2,b": ["q2", "b", "R"], "q2,Z": ["q2", "Z", "R"], "q2,c": ["q3", "Z", "L"],
            "q3,a": ["q3", "a", "L"], "q3,b": ["q3", "b", "L"], "q3,Y": ["q3", "Y", "L"], "q3,Z": ["q3", "Z", "L"], "q3,X": ["q0", "X", "R"],
            "q4,Y": ["q4", "Y", "R"], "q4,Z": ["q4", "Z", "R"], "q4,_": ["q_accept", "_", "R"]
        }
    },
    "a^n b^n (Context-Free)": {
        "start_state": "q0",
        "accept_state": "q_accept",
        "reject_state": "q_reject",
        "alphabet": ["a", "b"],
        "transitions": {
            "q0,a": ["q1", "X", "R"], "q0,Y": ["q3", "Y", "R"], "q0,_": ["q_accept", "_", "R"],
            "q1,a": ["q1", "a", "R"], "q1,Y": ["q1", "Y", "R"], "q1,b": ["q2", "Y", "L"],
            "q2,a": ["q2", "a", "L"], "q2,Y": ["q2", "Y", "L"], "q2,X": ["q0", "X", "R"],
            "q3,Y": ["q3", "Y", "R"], "q3,_": ["q_accept", "_", "R"]
        }
    },
    "a^n b^2n (Cross two 'b's for one 'a')": {
        "start_state": "q0",
        "accept_state": "q_accept",
        "reject_state": "q_reject",
        "alphabet": ["a", "b"],
        "transitions": {
            "q0,a": ["q1", "X", "R"], "q0,Y": ["q4", "Y", "R"],
            "q1,a": ["q1", "a", "R"], "q1,Y": ["q1", "Y", "R"], "q1,b": ["q2", "Y", "R"],
            "q2,b": ["q3", "Y", "L"],
            "q3,a": ["q3", "a", "L"], "q3,Y": ["q3", "Y", "L"], "q3,X": ["q0", "X", "R"],
            "q4,Y": ["q4", "Y", "R"], "q4,_": ["q_accept", "_", "R"]
        }
    },
    "Binary Palindromes (e.g. 1001, 101)": {
        "start_state": "q0",
        "accept_state": "q_accept",
        "reject_state": "q_reject",
        "alphabet": ["0", "1"],
        "transitions": {
            "q0,0": ["q_scan_R_0", "_", "R"], "q0,1": ["q_scan_R_1", "_", "R"], "q0,_": ["q_accept", "_", "R"],
            "q_scan_R_0,0": ["q_scan_R_0", "0", "R"], "q_scan_R_0,1": ["q_scan_R_0", "1", "R"], "q_scan_R_0,_": ["q_check_0", "_", "L"],
            "q_scan_R_1,0": ["q_scan_R_1", "0", "R"], "q_scan_R_1,1": ["q_scan_R_1", "1", "R"], "q_scan_R_1,_": ["q_check_1", "_", "L"],
            "q_check_0,0": ["q_scan_L", "_", "L"], "q_check_0,_": ["q_accept", "_", "R"],
            "q_check_1,1": ["q_scan_L", "_", "L"], "q_check_1,_": ["q_accept", "_", "R"],
            "q_scan_L,0": ["q_scan_L", "0", "L"], "q_scan_L,1": ["q_scan_L", "1", "L"], "q_scan_L,_": ["q0", "_", "R"]
        }
    }
}

# --- DEFAULT CUSTOM JSON (Parity Checker: Even number of 'a's) ---
CUSTOM_TEMPLATE = {
    "start_state": "q_even",
    "accept_state": "q_accept",
    "reject_state": "q_reject",
    "alphabet": ["a", "b"],
    "transitions": {
        "q_even,a": ["q_odd", "a", "R"], "q_even,b": ["q_even", "b", "R"], "q_even,_": ["q_accept", "_", "R"],
        "q_odd,a": ["q_even", "a", "R"], "q_odd,b": ["q_odd", "b", "R"]
    }
}

class TuringMachineCore:
    def __init__(self, rules):
        self.rules = rules
        self.tape = []
        self.head = 0
        self.state = rules["start_state"]
        self.halted = False

    def load_tape(self, input_string):
        self.tape = list(input_string) + ['_'] * 50
        self.head = 0
        self.state = self.rules["start_state"]
        self.halted = False

    def step(self):
        if self.halted:
            return None
        
        char_under_head = self.tape[self.head]
        key = f"{self.state},{char_under_head}"
        
        if key in self.rules["transitions"]:
            new_state, write_char, direction = self.rules["transitions"][key]
            self.tape[self.head] = write_char
            self.state = new_state
            
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head = max(0, self.head - 1)
                
            if self.state == self.rules["accept_state"] or self.state == self.rules["reject_state"]:
                self.halted = True
            
            return f"Rule Triggered: δ({key}) -> ({new_state}, {write_char}, {direction})"
        else:
            self.state = self.rules["reject_state"]
            self.halted = True
            return f"CRASH: No rule defined for δ({key})"

class CyberTMApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # UI Setup
        self.title("Turing Machine IDE // v4.0 (Pro UX Edition)")
        self.geometry("1150x680")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # Colors 
        self.bg_color = "#121212"
        self.neon_green = "#39ff14"
        self.neon_red = "#ff003c"
        self.neon_cyan = "#00f3ff"
        
        # Initialize
        self.machine = TuringMachineCore(PRESETS["a^n b^n c^n (Context-Sensitive)"])
        self.is_running = False
        
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="SYSTEM CONTROLS", font=("Courier", 18, "bold"), text_color=self.neon_cyan).pack(pady=(20, 10))
        
        # LANGUAGE SELECTOR
        ctk.CTkLabel(self.sidebar, text="Select Target Language:", font=("Courier", 12)).pack(anchor="w", padx=20)
        self.preset_options = list(PRESETS.keys()) + ["Custom (JSON)"]
        self.dropdown = ctk.CTkOptionMenu(self.sidebar, values=self.preset_options, command=self.change_language, fg_color="#333", dynamic_resizing=False)
        self.dropdown.pack(pady=(5, 5), padx=20, fill="x")
        
        # ALPHABET HINT (UX Fix)
        self.lbl_allowed_chars = ctk.CTkLabel(self.sidebar, text="Allowed Characters: a, b, c", font=("Courier", 11, "italic"), text_color="#888")
        self.lbl_allowed_chars.pack(pady=(0, 10))
        
        self.input_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Enter test string...", font=("Courier", 14))
        self.input_entry.pack(pady=5, padx=20, fill="x")
        
        self.syntax_error_label = ctk.CTkLabel(self.sidebar, text="", text_color=self.neon_red, font=("Courier", 12))
        self.syntax_error_label.pack()
        
        # BUTTON GRID (UX Fix)
        btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=5)
        
        self.btn_load = ctk.CTkButton(btn_frame, text="LOAD STRING", command=self.load_string, fg_color="#107c41", hover_color="#18a054")
        self.btn_load.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_reset = ctk.CTkButton(btn_frame, text="🔄 RESET", command=self.reset_tape, fg_color="#333", hover_color="#555")
        self.btn_reset.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        self.btn_play = ctk.CTkButton(self.sidebar, text="▶ AUTO-RUN", command=self.toggle_play)
        self.btn_play.pack(pady=5, padx=20, fill="x")
        
        self.btn_step = ctk.CTkButton(self.sidebar, text="⏭ STEP-BY-STEP", command=self.step_machine, fg_color="#333")
        self.btn_step.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(self.sidebar, text="Sim Speed (ms):", font=("Courier", 12)).pack(pady=(10, 0))
        self.speed_slider = ctk.CTkSlider(self.sidebar, from_=50, to=1000, number_of_steps=20)
        self.speed_slider.set(300) 
        self.speed_slider.pack(pady=5, padx=20)

        # ADVANCED RULESET
        ctk.CTkLabel(self.sidebar, text="ADVANCED: RULESET (JSON)", font=("Courier", 12, "bold"), text_color=self.neon_cyan).pack(pady=(20, 5))
        self.rule_editor = ctk.CTkTextbox(self.sidebar, font=("Courier", 11), height=180)
        self.rule_editor.pack(padx=10, fill="both", expand=True)
        self.rule_editor.insert("0.0", json.dumps(PRESETS["a^n b^n c^n (Context-Sensitive)"], indent=2))
        
        self.btn_apply_rules = ctk.CTkButton(self.sidebar, text="APPLY CUSTOM JSON", command=self.apply_custom_rules, fg_color="#b8860b", hover_color="#daa520")
        self.btn_apply_rules.pack(pady=10, padx=20, fill="x")

        # --- RIGHT AREA ---
        self.right_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(self.right_frame, text="TAPE INSPECTION WINDOW", font=("Courier", 16, "bold"), text_color=self.neon_cyan).pack(anchor="w")
        self.tape_canvas = ctk.CTkCanvas(self.right_frame, height=100, bg="#1a1a1a", highlightthickness=1, highlightbackground="#333")
        self.tape_canvas.pack(fill="x", pady=10)
        
        ctk.CTkLabel(self.right_frame, text="STATE DIAGNOSTICS", font=("Courier", 16, "bold"), text_color=self.neon_cyan).pack(anchor="w", pady=(20,0))
        
        self.dashboard_frame = ctk.CTkFrame(self.right_frame, fg_color="#1a1a1a")
        self.dashboard_frame.pack(fill="x", pady=10)
        
        self.state_label = ctk.CTkLabel(self.dashboard_frame, text="CURRENT STATE: None", font=("Courier", 24, "bold"), text_color="white")
        self.state_label.pack(pady=20)
        
        self.rule_log = ctk.CTkTextbox(self.right_frame, font=("Courier", 14), height=200, fg_color="#0d0d0d", text_color=self.neon_green)
        self.rule_log.pack(fill="both", expand=True, pady=10)

    # --- FUNCTIONALITY ---
    def change_language(self, choice):
        if choice in PRESETS:
            selected_rules = PRESETS[choice]
        else:
            selected_rules = CUSTOM_TEMPLATE 
            
        self.machine = TuringMachineCore(selected_rules)
        
        allowed = ", ".join(selected_rules["alphabet"])
        self.lbl_allowed_chars.configure(text=f"Allowed Characters: {allowed}")
        
        self.rule_editor.delete("0.0", "end")
        self.rule_editor.insert("0.0", json.dumps(selected_rules, indent=2))
        
        self.rule_log.delete("0.0", "end")
        self.log_msg(f"SYSTEM: Loaded predefined language '{choice}'.")
        self.syntax_error_label.configure(text="")
        self.tape_canvas.delete("all")
        self.state_label.configure(text="CURRENT STATE: None", text_color="white")

    def apply_custom_rules(self):
        try:
            raw_json = self.rule_editor.get("0.0", "end")
            new_rules = json.loads(raw_json)
            self.machine = TuringMachineCore(new_rules)
            
            allowed = ", ".join(new_rules.get("alphabet", []))
            self.lbl_allowed_chars.configure(text=f"Allowed Characters: {allowed}")
            
            self.dropdown.set("Custom (JSON)")
            self.log_msg("SYSTEM: Custom JSON ruleset compiled and applied successfully.")
        except Exception as e:
            self.log_msg(f"ERROR: Invalid JSON format. {str(e)}", error=True)

    def load_string(self):
        input_str = self.input_entry.get().strip()
        
        if not input_str:
            self.syntax_error_label.configure(text="ERROR: Tape string cannot be empty")
            return
            
        invalid_chars = [c for c in input_str if c not in self.machine.rules["alphabet"]]
        if invalid_chars:
            self.syntax_error_label.configure(text=f"SYNTAX ERROR: {','.join(set(invalid_chars))} not in alphabet")
            return
        
        self.syntax_error_label.configure(text="")
        self.machine.load_tape(input_str)
        self.is_running = False
        self.btn_play.configure(text="▶ AUTO-RUN")
        
        self.rule_log.delete("0.0", "end") 
        self.log_msg(f"SYSTEM: Tape loaded with '{input_str}'")
        self.update_visuals()

    def reset_tape(self):
        if self.input_entry.get():
            self.load_string()
            self.log_msg("SYSTEM: Tape has been reset to starting position.")

    def step_machine(self):
        if not self.machine.halted:
            log_output = self.machine.step()
            self.log_msg(log_output)
            self.update_visuals()

    def toggle_play(self):
        if not self.is_running and not self.machine.halted:
            self.is_running = True
            self.btn_play.configure(text="⏸ PAUSE")
            self.auto_run()
        else:
            self.is_running = False
            self.btn_play.configure(text="▶ AUTO-RUN")

    def auto_run(self):
        if self.is_running and not self.machine.halted:
            self.step_machine()
            speed = int(self.speed_slider.get())
            self.after(speed, self.auto_run)
        elif self.machine.halted:
            self.is_running = False
            self.btn_play.configure(text="▶ AUTO-RUN")

    def log_msg(self, msg, error=False):
        self.rule_log.insert("end", msg + "\n")
        self.rule_log.see("end")

    def update_visuals(self):
        state_color = self.neon_green if self.machine.state == self.machine.rules["accept_state"] else (self.neon_red if self.machine.state == self.machine.rules["reject_state"] else "white")
        self.state_label.configure(text=f"CURRENT STATE: {self.machine.state}", text_color=state_color)
        
        self.tape_canvas.delete("all")
        cell_width = 50
        offset_x = 350 - (self.machine.head * cell_width) 
        
        for i, char in enumerate(self.machine.tape[:100]): 
            x0 = offset_x + (i * cell_width)
            y0 = 25
            x1 = x0 + cell_width
            y1 = 75
            
            if i == self.machine.head:
                self.tape_canvas.create_rectangle(x0, y0, x1, y1, outline=self.neon_cyan, width=3, fill="#2a2a2a")
                self.tape_canvas.create_text(x0+25, y0+25, text=char, fill=self.neon_cyan, font=("Courier", 24, "bold"))
            else:
                self.tape_canvas.create_rectangle(x0, y0, x1, y1, outline="#333", width=1)
                self.tape_canvas.create_text(x0+25, y0+25, text=char, fill="#888", font=("Courier", 20))

if __name__ == "__main__":
    app = CyberTMApp()
    app.mainloop()