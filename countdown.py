import tkinter as tk
from datetime import datetime

class DERoadmapTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Senior DE Roadmap - Precise Tracker")
        self.root.geometry("500x580")
        self.root.configure(bg="#0f172a")

        # --- State Management ---
        self.display_mode = "FULL" 

        # --- Current Date Section ---
        tk.Label(root, text="CURRENT SERVER TIME", font=("Arial", 9, "bold"), 
                 bg="#0f172a", fg="#94a3b8").pack(pady=(20, 0))
        self.current_time_var = tk.StringVar()
        tk.Label(root, textvariable=self.current_time_var, 
                 font=("Courier", 14), bg="#0f172a", fg="#38bdf8").pack(pady=5)

        # --- Input Section ---
        tk.Label(root, text="TARGET DATE (YYYY-MM-DD)", font=("Arial", 9, "bold"), 
                 bg="#0f172a", fg="#94a3b8").pack(pady=(20, 0))
        self.date_entry = tk.Entry(root, justify='center', font=("Arial", 14), 
                                  bg="#1e293b", fg="white", insertbackground="white", border=0)
        self.date_entry.insert(0, "2026-10-31") 
        self.date_entry.pack(pady=10, ipady=5)

        # --- Results Section ---
        self.result_var = tk.StringVar()
        self.result_label = tk.Label(root, textvariable=self.result_var, 
                                     font=("Courier", 22, "bold"), 
                                     bg="#0f172a", fg="#fbbf24", justify="center")
        self.result_label.pack(pady=40)

        # --- Control Buttons ---
        tk.Label(root, text="SWITCH VIEW MODE", font=("Arial", 8, "bold"), 
                 bg="#0f172a", fg="#475569").pack()
        
        self.btn_frame = tk.Frame(root, bg="#0f172a")
        self.btn_frame.pack(pady=10)

        self.modes = [
            ("Full Breakdown", "FULL"), 
            ("Total Days", "DAYS_ONLY"), 
            ("Mixed Focus", "MIXED")
        ]
        
        self.buttons = {}
        for text, mode in self.modes:
            btn = tk.Button(self.btn_frame, text=text, 
                            command=lambda m=mode: self.set_mode(m),
                            bg="#334155", fg="white", relief="flat", 
                            padx=15, pady=5, font=("Arial", 10))
            btn.pack(side="left", padx=5)
            self.buttons[mode] = btn

        self.refresh_ui()

    def set_mode(self, mode):
        self.display_mode = mode
        # Simple visual feedback for active button
        for m, btn in self.buttons.items():
            btn.config(bg="#1e293b" if m != mode else "#38bdf8")

    def get_remaining_logic(self, target_dt):
        now = datetime.now()
        if target_dt < now:
            return "DEADLINE REACHED\nSHIP IT!"

        # Core Delta Calculation
        diff = target_dt - now
        total_seconds = int(diff.total_seconds())
        
        # Unit breakdown
        years = target_dt.year - now.year
        months = target_dt.month - now.month
        days = target_dt.day - now.day
        hours = target_dt.hour - now.hour
        minutes = target_dt.minute - now.minute
        seconds = target_dt.second - now.second

        # Cascading Borrowing Logic
        if seconds < 0:
            seconds += 60
            minutes -= 1
        if minutes < 0:
            minutes += 60
            hours -= 1
        if hours < 0:
            hours += 24
            days -= 1
        if days < 0:
            days += 30 # Standard DE month normalization
            months -= 1
        if months < 0:
            months += 12
            years -= 1
        
        total_months = (years * 12) + months

        # Display Logic
        if self.display_mode == "FULL":
            return (f"{total_months} Months\n"
                    f"{days} Days\n"
                    f"{hours}h : {minutes}m : {seconds}s")
        
        elif self.display_mode == "DAYS_ONLY":
            total_days = total_seconds // 86400
            rem_h = (total_seconds % 86400) // 3600
            rem_m = (total_seconds % 3600) // 60
            rem_s = total_seconds % 60
            return f"{total_days} Total Days\n{rem_h}h : {rem_m}m : {rem_s}s"
        
        elif self.display_mode == "MIXED":
            # Shows Months, Hours, Minutes, and Seconds
            return (f"{total_months} Months\n"
                    f"{hours} Hours\n"
                    f"{minutes}m : {seconds}s")

    def refresh_ui(self):
        now = datetime.now()
        self.current_time_var.set(now.strftime("%Y-%m-%d | %H:%M:%S"))

        try:
            target_str = self.date_entry.get()
            target_dt = datetime.strptime(target_str, "%Y-%m-%d")
            # Countdown to start of target day
            target_dt = target_dt.replace(hour=0, minute=0, second=0)
            self.result_var.set(self.get_remaining_logic(target_dt))
        except ValueError:
            self.result_var.set("INVALID DATE\nFORMAT: YYYY-MM-DD")

        self.root.after(1000, self.refresh_ui)

if __name__ == "__main__":
    root = tk.Tk()
    app = DERoadmapTimer(root)
    root.mainloop()