import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class StockTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("550x600")
        self.root.configure(bg="#1e272e")  # Slick dark aesthetic

        # Hardcoded stock price dictionary
        self.stock_prices = {
            "AAPL": 180.00,
            "TSLA": 250.00,
            "NVDA": 850.00,
            "AMZN": 175.00,
            "MSFT": 420.00,
            "GOOGL": 150.00
        }

        # User's current portfolio storage (Stock Symbol: Quantity)
        self.portfolio = {}

        self.create_widgets()

    def create_widgets(self):
        # 1. Header Title
        title = tk.Label(
            self.root, text="📈 PORTFOLIO TRACKER", font=("Helvetica", 22, "bold"),
            fg="#0be881", bg="#1e272e"
        )
        title.pack(pady=20)

        # 2. Input Frame Container
        input_frame = tk.LabelFrame(
            self.root, text=" Add / Update Holdings ", font=("Helvetica", 11, "bold"),
            fg="#d2dae2", bg="#2f3542", padx=15, pady=15, relief="flat"
        )
        input_frame.pack(pady=10, fill="x", padx=20)

        # Stock Selection Dropdown Label
        tk.Label(input_frame, text="Select Stock:", font=("Helvetica", 10), fg="#f5f6fa", bg="#2f3542").grid(row=0, column=0, sticky="w", pady=5)
        
        # Stock Dropdown Menu
        self.selected_stock = tk.StringVar(self.root)
        self.selected_stock.set(list(self.stock_prices.keys())[0]) # Default first stock
        stock_dropdown = tk.OptionMenu(input_frame, self.selected_stock, *self.stock_prices.keys())
        stock_dropdown.config(width=10, bg="#57606f", fg="white", activebackground="#747d8c", highlightthickness=0)
        stock_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Quantity Entry Label & Input Box
        tk.Label(input_frame, text="Quantity:", font=("Helvetica", 10), fg="#f5f6fa", bg="#2f3542").grid(row=1, column=0, sticky="w", pady=5)
        self.qty_entry = tk.Entry(input_frame, font=("Helvetica", 11), width=12, bg="#57606f", fg="white", insertbackground="white", relief="flat")
        self.qty_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Add Asset Button
        add_btn = tk.Button(
            input_frame, text="Update Portfolio", font=("Helvetica", 10, "bold"),
            bg="#0fbcf9", fg="white", activebackground="#4bcffa", activeforeground="white",
            relief="flat", padx=10, pady=5, command=self.add_stock
        )
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # 3. Portfolio Table/List Display
        table_label = tk.Label(self.root, text="Current Holdings Breakdown:", font=("Helvetica", 12, "bold"), fg="#d2dae2", bg="#1e272e")
        table_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Using a read-only text box to display current positions elegantly
        self.display_box = tk.Text(self.root, height=10, width=55, font=("Courier", 11), bg="#2f3542", fg="#ffdd59", relief="flat", padx=10, pady=10)
        self.display_box.pack(padx=20, fill="x")

        # 4. Total Value Dashboard Display
        self.total_label = tk.Label(
            self.root, text="Total Investment Value: $0.00", font=("Helvetica", 16, "bold"),
            fg="#0be881", bg="#1e272e"
        )
        self.total_label.pack(pady=20)

        # 5. Export Button (File Handling)
        export_btn = tk.Button(
            self.root, text="💾 Save Statement (.txt)", font=("Helvetica", 11, "bold"),
            bg="#ff5e57", fg="white", activebackground="#ffdd59", activeforeground="#1e272e",
            relief="flat", pady=8, command=self.export_to_file
        )
        export_btn.pack(pady=5)

        # Safe Initialization call now that all variables exist
        self.refresh_display()

    def add_stock(self):
        stock = self.selected_stock.get()
        qty_str = self.qty_entry.get().strip()

        # Basic Arithmetic validation
        try:
            qty = float(qty_str)
            if qty < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive numerical quantity.")
            return

        # Update dictionary tracker
        if qty == 0:
            if stock in self.portfolio:
                del self.portfolio[stock]
        else:
            self.portfolio[stock] = qty

        self.qty_entry.delete(0, tk.END)  # Clear the input box
        self.refresh_display()

    def refresh_display(self):
        # Enable editing briefly to overwrite text
        self.display_box.config(state="normal")
        self.display_box.delete("1.0", tk.END)

        # Dynamic template builder inside our Text widget area
        header = f"{'Ticker':<10}{'Price':<12}{'Quantity':<12}{'Total Value':<12}\n"
        divider = "-" * 48 + "\n"
        self.display_box.insert(tk.END, header + divider)

        total_portfolio_value = 0.0

        for stock, qty in self.portfolio.items():
            price = self.stock_prices[stock]
            asset_value = price * qty
            total_portfolio_value += asset_value
            
            row = f"{stock:<10}${price:<11.2f}{qty:<12.2f}${asset_value:<12.2f}\n"
            self.display_box.insert(tk.END, row)

        # Make the box read-only again to protect structure
        self.display_box.config(state="disabled")
        
        # Update metric label dynamically
        self.total_label.config(text=f"Total Investment Value: ${total_portfolio_value:,.2f}")

    def export_to_file(self):
        if not self.portfolio:
            messagebox.showwarning("Empty Portfolio", "You cannot export an empty statement. Add holdings first.")
            return

        # Prompt the user to choose where to save their file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")],
            title="Save Portfolio Statement"
        )

        if file_path:
            try:
                # File Handling operations
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("=== STOCK PORTFOLIO SUMMARY EXPORT ===\n\n")
                    file.write(f"{'Ticker':<10}{'Market Price':<15}{'Owned Qty':<12}{'Total EquityValue':<15}\n")
                    file.write("-" * 55 + "\n")
                    
                    grand_total = 0.0
                    for stock, qty in self.portfolio.items():
                        price = self.stock_prices[stock]
                        val = price * qty
                        grand_total += val
                        file.write(f"{stock:<10}${price:<14.2f}{qty:<12.2f}${val:<14.2f}\n")
                    
                    file.write("-" * 55 + "\n")
                    file.write(f"GRAND TOTAL PORTFOLIO VALUE: ${grand_total:,.2f}\n")
                
                messagebox.showinfo("Success", "Portfolio statement exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockTrackerGUI(root)
    root.mainloop()