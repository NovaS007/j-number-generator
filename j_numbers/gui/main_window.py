from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

try:
    from ..core import calculations as gjn
    from ..io.csv_writer import writeCSV
except ImportError:
    from j_numbers.core import calculations as gjn
    from j_numbers.io.csv_writer import writeCSV


class JNumGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("J-Number Generator")
        self.geometry("900x650")
        self.minsize(800, 560)

        # Core inputs
        self.base_var = tk.StringVar(value="10")
        self.k_var = tk.StringVar(value="15")
        self.show_results_var = tk.BooleanVar(value=True)

        # Optional seed digit inputs (blank = wildcard)
        self.a_var = tk.StringVar(value="")
        self.b_var = tk.StringVar(value="")
        self.c_var = tk.StringVar(value="")

        self._configure_style()
        self._build_ui()

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#f4f7fb")
        style.configure("Header.TFrame", background="#1f4e79")
        style.configure("HeaderTitle.TLabel", background="#1f4e79", foreground="white",
                        font=("Helvetica", 20, "bold"))
        style.configure("HeaderSub.TLabel", background="#1f4e79", foreground="#dbe9f6",
                        font=("Helvetica", 10))
        style.configure("Section.TLabelframe", background="#f4f7fb", padding=(12, 10))
        style.configure("Section.TLabelframe.Label", font=("Helvetica", 11, "bold"))
        style.configure("TLabel", background="#f4f7fb", font=("Helvetica", 10))
        style.configure("TCheckbutton", background="#f4f7fb", font=("Helvetica", 10))
        style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), padding=(12, 8))
        style.configure("Secondary.TButton", font=("Helvetica", 10), padding=(10, 7))

    def _build_ui(self):
        self.configure(background="#f4f7fb")

        # Header
        header = ttk.Frame(self, style="Header.TFrame", padding=(18, 16))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="J-Number Generator",
            style="HeaderTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Generate unique J-numbers, inspect factors, and export to CSV.",
            style="HeaderSub.TLabel"
        ).pack(anchor="w", pady=(4, 0))

        # Main content
        main = ttk.Frame(self, style="App.TFrame", padding=16)
        main.pack(fill="both", expand=True)

        # Input section
        input_frame = ttk.Labelframe(main, text="Settings", style="Section.TLabelframe")
        input_frame.pack(fill="x", pady=(0, 12))

        input_grid = ttk.Frame(input_frame)
        input_grid.pack(fill="x")

        ttk.Label(input_grid, text="Base").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.base_entry = ttk.Entry(input_grid, textvariable=self.base_var, width=18)
        self.base_entry.grid(row=1, column=0, sticky="ew", padx=(0, 12))

        ttk.Label(input_grid, text="k (max c repeats)").grid(row=0, column=1, sticky="w", pady=(0, 4))
        self.k_entry = ttk.Entry(input_grid, textvariable=self.k_var, width=18)
        self.k_entry.grid(row=1, column=1, sticky="ew", padx=(0, 12))

        self.show_results_check = ttk.Checkbutton(
            input_grid,
            text="Show results in window",
            variable=self.show_results_var
        )
        self.show_results_check.grid(row=1, column=2, sticky="w")

        # Optional seed digits (a, b, c)
        ttk.Label(input_grid, text="Seed a (optional)").grid(row=2, column=0, sticky="w", pady=(8, 4))
        self.a_entry = ttk.Entry(input_grid, textvariable=self.a_var, width=18)
        self.a_entry.grid(row=3, column=0, sticky="ew", padx=(0, 12))

        ttk.Label(input_grid, text="Seed b (optional)").grid(row=2, column=1, sticky="w", pady=(8, 4))
        self.b_entry = ttk.Entry(input_grid, textvariable=self.b_var, width=18)
        self.b_entry.grid(row=3, column=1, sticky="ew", padx=(0, 12))

        ttk.Label(input_grid, text="Seed c (optional)").grid(row=2, column=2, sticky="w", pady=(8, 4))
        self.c_entry = ttk.Entry(input_grid, textvariable=self.c_var, width=18)
        self.c_entry.grid(row=3, column=2, sticky="ew", padx=(0, 12))

        input_grid.columnconfigure(0, weight=1)
        input_grid.columnconfigure(1, weight=1)
        input_grid.columnconfigure(2, weight=1)

        # Buttons
        button_frame = ttk.Frame(main, style="App.TFrame")
        button_frame.pack(fill="x", pady=(0, 12))

        ttk.Button(
            button_frame,
            text="Generate and Save CSV",
            style="Primary.TButton",
            command=self.generate_and_save
        ).pack(side="left")

        ttk.Button(
            button_frame,
            text="Clear Output",
            style="Secondary.TButton",
            command=self.clear_output
        ).pack(side="left", padx=(10, 0))

        ttk.Button(
            button_frame,
            text="Export to Excel",
            style="Secondary.TButton",
            command=lambda: self._on_export_excel_clicked()
        ).pack(side="left", padx=(10, 0))

        # Results section
        results_frame = ttk.Labelframe(main, text="Results", style="Section.TLabelframe")
        results_frame.pack(fill="both", expand=True)

        text_container = ttk.Frame(results_frame)
        text_container.pack(fill="both", expand=True)

        self.output = tk.Text(
            text_container,
            wrap="none",
            bg="white",
            fg="#1f2937",
            insertbackground="#1f2937",
            font=("Menlo", 11),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            state="disabled",
            takefocus=0
        )

        self.output.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(text_container, orient="vertical", command=self.output.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=y_scroll.set)

        x_scroll = ttk.Scrollbar(text_container, orient="horizontal", command=self.output.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        self.output.configure(xscrollcommand=x_scroll.set)

        text_container.rowconfigure(0, weight=1)
        text_container.columnconfigure(0, weight=1)

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(
            self,
            textvariable=self.status_var,
            anchor="w",
            padding=(12, 6)
        )
        status.pack(fill="x", side="bottom")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")
        self.status_var.set("Output cleared.")

    def log(self, text):
        # Temporarily enable, insert, then disable to keep the widget read-only
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")
        # Keep console logging as well for debugging
        print(text)


    def _get_inputs(self):
        base_text = self.base_var.get().strip()
        k_text = self.k_var.get().strip()

        try:
            base = int(base_text)
            k = int(k_text)
        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Base and k must both be integers.\n\n"
                "Examples:\n"
                "  Base = 10\n"
                "  k = 15"
            )
            return None

        if base < 2:
            messagebox.showwarning(
                "Invalid Base",
                "Base must be at least 2."
            )
            return None

        if k < 0:
            messagebox.showwarning(
                "Invalid k",
                "k must be 0 or greater."
            )
            return None

        return base, k

    def _get_seed_inputs(self, base):
        """
        Parse optional a,b,c inputs. Returns a tuple (a, b, c) where each is either
        an int or None (None means wildcard / not provided). Raises ValueError when invalid.
        """
        def parse_single(s, name):
            s = s.strip()
            if s == "":
                return None
            try:
                v = int(s)
            except ValueError:
                raise ValueError(f"'{name}' must be an integer in [0, {base-1}] or left blank.")
            if v < 0 or v >= base:
                raise ValueError(f"'{name}' must be between 0 and {base-1} for base {base}.")
            return v

        a = parse_single(self.a_var.get(), "a")
        b = parse_single(self.b_var.get(), "b")
        c = parse_single(self.c_var.get(), "c")
        return a, b, c

    def _results_to_dataframe(self, results):
        """
        Convert results dict -> pandas DataFrame.
        Columns: j_num, a, b, c, k, prime_factors (list), is_prime
        Also add prime_factors_str for simple export.
        """
        # results is {j_num: info}
        rows = []
        for j_num, info in results.items():
            rows.append({
                "j_num": j_num,
                "a": info.get("a"),
                "b": info.get("b"),
                "c": info.get("c"),
                "k": info.get("k"),
                "prime_factors": info.get("prime_factors", []),
                "is_prime": info.get("is_prime")
            })
        df = pd.DataFrame(rows)
        # ensure consistent types
        if df.empty:
            return df
        df = df.sort_values(["j_num"]).reset_index(drop=True)
        df["prime_factors_str"] = df["prime_factors"].apply(lambda lst: ";".join(map(str, lst)) if lst else "")
        df["num_prime_factors"] = df["prime_factors"].apply(len)
        return df

    def _on_export_excel_clicked(self):
        try:
            results = getattr(self, "last_results", None)
            if results is None:
                messagebox.showinfo("No data", "No generated results in memory. Generate first, or re-open a saved CSV.")
                return
            self.export_to_excel(results)
        except Exception as e:
            messagebox.showwarning("Error", str(e))

    def export_to_excel(self, results, path=None):
        """
        Export results to an Excel .xlsx file. Split prime_factors into separate columns.
        If path is None, ask user for save location.
        """
        df = self._results_to_dataframe(results)
        if df.empty:
            messagebox.showinfo("Export", "No data to export.")
            return

        # Expand prime_factors list into columns pf_0, pf_1, ...
        pf_df = pd.DataFrame(df["prime_factors"].tolist())
        if not pf_df.empty:
            pf_df = pf_df.fillna("")  # empty cells as blank
            pf_df = pf_df.rename(columns=lambda i: f"pf_{i}")
            out_df = pd.concat([df.drop(columns=["prime_factors"]), pf_df], axis=1)
        else:
            out_df = df.drop(columns=["prime_factors"])

        # Ask for path if not provided
        if path is None:
            desktop = Path.home() / "Desktop"
            initial_dir = str(desktop if desktop.exists() else Path.home())
            default_name = "jnums_export.xlsx"
            path = filedialog.asksaveasfilename(
                title="Save Excel As",
                initialdir=initial_dir,
                initialfile=default_name,
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if not path:
                self.log("Excel export cancelled.")
                return

        try:
            out_df.to_excel(path, index=False, engine="openpyxl")
        except Exception as e:
            messagebox.showwarning("Export failed", f"Could not save Excel file:\n{e}")
            return

        messagebox.showinfo("Export complete", f"Exported {len(out_df)} rows to:\n{path}")

    def generate_and_save(self):
        self.output.delete("1.0", tk.END)

        inputs = self._get_inputs()
        if inputs is None:
            return

        base, k = inputs
        self.status_var.set("Generating J-numbers...")

        # Parse and validate optional seed inputs first (fast-path decision)
        try:
            a_seed, b_seed, c_seed = self._get_seed_inputs(base)
        except ValueError as e:
            messagebox.showwarning("Invalid seed input", str(e))
            self.status_var.set("Invalid seed input.")
            return

        try:
            # Choose best generation strategy:
            # - If user provided a,b,c -> compute only that seed
            # - If user provided a and b -> compute for that a,b and all c (faster than full enumeration)
            # - Otherwise compute everything and filter
            if a_seed is not None and b_seed is not None and c_seed is not None:
                results = gjn.getJNumsForSeed(a_seed, b_seed, c_seed, k, base)
            elif a_seed is not None and b_seed is not None and c_seed is None:
                results = gjn.getJNumsForAB(a_seed, b_seed, k, base)
            else:
                results = gjn.getAllJNums(k, base)
        except Exception as e:
            messagebox.showwarning(
                "Generation Error",
                f"Something went wrong while generating results:\n\n{e}"
            )
            self.status_var.set("Generation failed.")
            return

        # Filter results (None means wildcard)
        filtered = {}
        for j_num, info in results.items():
            if a_seed is not None and info.get("a") != a_seed:
                continue
            if b_seed is not None and info.get("b") != b_seed:
                continue
            if c_seed is not None and info.get("c") != c_seed:
                continue
            filtered[j_num] = info

        if not filtered:
            messagebox.showinfo(
                "No results",
                "No J-numbers were found that match the provided seed digits (a, b, c)."
            )
            self.status_var.set("No results found.")
            return

        self.last_results = filtered


        # Ask user where to save (default to Desktop)
        desktop = Path.home() / "Desktop"
        initial_dir = str(desktop if desktop.exists() else Path.home())
        default_name = f"jnums_base{base}_k{k}.csv"

        save_path = filedialog.asksaveasfilename(
            title="Save CSV As",
            initialdir=initial_dir,
            initialfile=default_name,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not save_path:
            self.log("Save cancelled.")
            self.status_var.set("Save cancelled.")
            return

        try:
            writeCSV(save_path, filtered)
        except Exception as e:
            messagebox.showwarning(
                "Save Error",
                f"Could not save the CSV:\n\n{e}"
            )
            self.status_var.set("Save failed.")
            return

        self.log(f"Generated {len(filtered)} unique J-numbers (after seed filter).")
        self.log(f"Saved CSV to: {save_path}")
        self.log("")

        if self.show_results_var.get():
            self.log("j_num | a b c k | prime_factors | is_prime")
            self.log("-" * 80)
            for j_num, info in sorted(filtered.items()):
                self.log(
                    f"{j_num} | "
                    f"a={info['a']} b={info['b']} c={info['c']} k={info['k']} | "
                    f"{info['prime_factors']} | "
                    f"{info['is_prime']}"
                )

        self.status_var.set(f"Done. Saved {len(filtered)} rows.")
        messagebox.showinfo("Done", f"Saved {len(filtered)} rows to:\n{save_path}")


if __name__ == "__main__":
    app = JNumGUI()
    app.mainloop()
