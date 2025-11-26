import customtkinter as ctk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil
import time # ডেমো প্রোগ্রেস দেখানোর জন্য

# --- Configuration and Initial Settings ---
ctk.set_appearance_mode("Dark") # Dark mode is set (ডার্ক মোড সেট করা হলো)
ctk.set_default_color_theme("blue")

class FileCompressorApp(ctk.CTk):
    """Main Application Class (প্রধান অ্যাপ্লিকেশন ক্লাস)"""
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("📁 Advanced File Compressor & Extractor")
        self.geometry("650x500") # Height slightly increased for the progress bar (উচ্চতা সামান্য বাড়ানো হয়েছে প্রোগ্রেস বারের জন্য)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Frame layout configuration
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Title ---
        self.title_label = ctk.CTkLabel(self.main_frame, text="File Compressor & Extractor", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # --- Tab View (Compress and Extract) ---
        self.tab_view = ctk.CTkTabview(self.main_frame, width=600)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Create tabs (ট্যাব তৈরি করা)
        self.compress_tab = self.tab_view.add("Compress (Create ZIP)")
        self.extract_tab = self.tab_view.add("Extract (Unzip)")

        # --- Setup Compress Tab ---
        self.setup_compress_tab()

        # --- Setup Extract Tab ---
        self.setup_extract_tab()
        
        # --- Theme Switch Button ---
        self.theme_switch = ctk.CTkSwitch(self.main_frame, text="Light Mode", command=self.change_theme)
        self.theme_switch.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="w")
        
        self.theme_switch.select() # Set switch for Default Dark Mode (ডিফল্ট ডার্ক মোডের জন্য সুইচ সেট করা)

    # --- Compress Tab Setup ---
    def setup_compress_tab(self):
        self.compress_tab.grid_columnconfigure(0, weight=1)
        
        # Input Field and Button (ইনপুট ফিল্ড ও বাটন)
        self.path_entry_c = ctk.CTkEntry(self.compress_tab, placeholder_text="Enter file or folder path...", width=450)
        self.path_entry_c.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.browse_button_c = ctk.CTkButton(self.compress_tab, text="Browse", command=self.browse_path_c)
        self.browse_button_c.grid(row=0, column=1, padx=(0, 20), pady=(20, 10))

        self.output_name_entry = ctk.CTkEntry(self.compress_tab, placeholder_text="Enter output ZIP file name (e.g., archive.zip)", width=450)
        self.output_name_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.compress_button = ctk.CTkButton(self.compress_tab, text="Compress File (ZIP)", command=self.compress_file)
        self.compress_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        # Status Label (স্ট্যাটাস লেবেল)
        self.compress_status_label = ctk.CTkLabel(self.compress_tab, text="", text_color="#10b981")
        self.compress_status_label.grid(row=3, column=0, columnspan=2, padx=20, pady=(5, 0))

        # Progress Bar (প্রোগ্রেস বার)
        self.compress_progress = ctk.CTkProgressBar(self.compress_tab, orientation="horizontal")
        self.compress_progress.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="ew")
        self.compress_progress.set(0) # Initially set to zero (প্রাথমিকভাবে জিরো সেট করা)

        
    def browse_path_c(self):
        """Select file or folder for compression (কম্প্রেস করার জন্য ফাইল বা ফোল্ডার নির্বাচন)"""
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        if path:
            self.path_entry_c.delete(0, "end")
            self.path_entry_c.insert(0, path)

    def compress_file(self):
        """Compresses the selected file or folder into a ZIP file (সিলেক্ট করা ফাইল বা ফোল্ডারকে ZIP ফাইলে কম্প্রেস করে)"""
        input_path = self.path_entry_c.get()
        zip_filename_with_ext = self.output_name_entry.get()
        
        # Reset progress bar and status (প্রোগ্রেস বার এবং স্ট্যাটাস রিসেট করা)
        self.compress_progress.set(0)
        self.compress_status_label.configure(text="Starting job...", text_color="yellow")
        self.update() # Update UI (UI আপডেট করা)
        
        if not input_path or not zip_filename_with_ext:
            self.compress_status_label.configure(text="Failed: Please provide input path or ZIP name.", text_color="red")
            messagebox.showerror("Error", "Please provide both input path and ZIP file name.")
            return

        if not zip_filename_with_ext.endswith(".zip"):
            zip_filename_with_ext += ".zip"
        
        output_dir = filedialog.askdirectory(title="Where to save the ZIP file?")
        if not output_dir:
            self.compress_status_label.configure(text="Cancelled.", text_color="gray")
            messagebox.showinfo("Cancelled", "Compression cancelled.")
            return
            
        output_path = os.path.join(output_dir, zip_filename_with_ext)

        try:
            # For simulated progress (সিমুলেটেড প্রোগ্রেস দেখানোর জন্য)
            self.compress_status_label.configure(text="Compressing...", text_color="#22c55e")
            self.compress_progress.set(0.2)
            self.update() 
            
            if os.path.isfile(input_path):
                # It is a single file (এটি একটি একক ফাইল)
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Only the file name will be inside the ZIP, not the full path (শুধু ফাইলের নাম ZIP-এর ভিতরে থাকবে, পুরো পাথ নয়)
                    zipf.write(input_path, os.path.basename(input_path))
                
            elif os.path.isdir(input_path):
                # It is a folder (shutil is better) (এটি একটি ফোল্ডার)
                base_name = zip_filename_with_ext[:-4] 
                shutil.make_archive(
                    base_name=os.path.join(output_dir, base_name), 
                    format='zip', 
                    root_dir=os.path.dirname(input_path), # Parent directory of the folder (ফোল্ডারের প্যারেন্ট ডিরেক্টরি)
                    base_dir=os.path.basename(input_path) # Folder name (ফোল্ডারের নাম)
                )

            else:
                self.compress_status_label.configure(text="Failed: Invalid Path.", text_color="red")
                messagebox.showerror("Error", "Invalid Path: File or folder not found.")
                return
            
            # On success (সফল হলে)
            self.compress_progress.set(1.0)
            self.compress_status_label.configure(text=f"Success: {zip_filename_with_ext} created!", text_color="#10b981")
            messagebox.showinfo("Success", f"Compression successful:\n{output_path}")

        except Exception as e:
            self.compress_progress.set(0)
            self.compress_status_label.configure(text="Error occurred.", text_color="red")
            messagebox.showerror("Compression Error", f"An error occurred during compression: {e}")
            
    # --- Extract Tab Setup ---
    def setup_extract_tab(self):
        self.extract_tab.grid_columnconfigure(0, weight=1)
        
        # Input Field and Button (ইনপুট ফিল্ড ও বাটন)
        self.path_entry_e = ctk.CTkEntry(self.extract_tab, placeholder_text="Enter ZIP file path...", width=450)
        self.path_entry_e.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.browse_button_e = ctk.CTkButton(self.extract_tab, text="Browse", command=self.browse_path_e)
        self.browse_button_e.grid(row=0, column=1, padx=(0, 20), pady=(20, 10))
        
        self.extract_button = ctk.CTkButton(self.extract_tab, text="Extract File", command=self.extract_file)
        self.extract_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Status Label (স্ট্যাটাস লেবেল)
        self.extract_status_label = ctk.CTkLabel(self.extract_tab, text="", text_color="#10b981")
        self.extract_status_label.grid(row=2, column=0, columnspan=2, padx=20, pady=(5, 0))

        # Progress Bar (প্রোগ্রেস বার)
        self.extract_progress = ctk.CTkProgressBar(self.extract_tab, orientation="horizontal")
        self.extract_progress.grid(row=3, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="ew")
        self.extract_progress.set(0) # Initially set to zero (প্রাথমিকভাবে জিরো সেট করা)
        
    def browse_path_e(self):
        """Select ZIP file for extraction (এক্সট্র্যাক্ট করার জন্য ZIP ফাইল নির্বাচন)"""
        path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if path:
            self.path_entry_e.delete(0, "end")
            self.path_entry_e.insert(0, path)

    def extract_file(self):
        """Extracts the ZIP file (ZIP ফাইল এক্সট্র্যাক্ট করে)"""
        input_zip_path = self.path_entry_e.get()
        
        # Reset progress bar and status (প্রোগ্রেস বার এবং স্ট্যাটাস রিসেট করা)
        self.extract_progress.set(0)
        self.extract_status_label.configure(text="Starting job...", text_color="yellow")
        self.update()
        
        if not input_zip_path or not input_zip_path.endswith(".zip"):
            self.extract_status_label.configure(text="Failed: Please select a valid ZIP file.", text_color="red")
            messagebox.showerror("Error", "Please select a valid ZIP file.")
            return
            
        extract_to_dir = filedialog.askdirectory(title="Where to extract?")
        if not extract_to_dir:
            self.extract_status_label.configure(text="Cancelled.", text_color="gray")
            messagebox.showinfo("Cancelled", "Extraction cancelled.")
            return
            
        try:
            # For simulated progress (সিমুলেটেড প্রোগ্রেস দেখানোর জন্য)
            self.extract_status_label.configure(text="Extracting...", text_color="#22c55e")
            self.extract_progress.set(0.2)
            self.update()
            
            # Use zipfile.ZipFile to extract (zipfile.ZipFile ব্যবহার করে এক্সট্র্যাক্ট করা)
            with zipfile.ZipFile(input_zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_dir)
            
            # On success (সফল হলে)
            self.extract_progress.set(1.0)
            self.extract_status_label.configure(text=f"Success: '{os.path.basename(input_zip_path)}' extracted!", text_color="#10b981")
            messagebox.showinfo("Success", f"File successfully extracted to:\n{extract_to_dir}")

        except FileNotFoundError:
            self.extract_progress.set(0)
            self.extract_status_label.configure(text="Failed: ZIP file not found.", text_color="red")
            messagebox.showerror("Error", "ZIP file not found.")
        except zipfile.BadZipFile:
            self.extract_progress.set(0)
            self.extract_status_label.configure(text="Failed: Corrupt ZIP file.", text_color="red")
            messagebox.showerror("Error", "This is a bad or corrupt ZIP file.")
        except Exception as e:
            self.extract_progress.set(0)
            self.extract_status_label.configure(text="Error occurred.", text_color="red")
            messagebox.showerror("Extraction Error", f"An error occurred during extraction: {e}")

    # --- Theme Change Function ---
    def change_theme(self):
        """Switches between Light and Dark themes (লাইট এবং ডার্ক থিমের মধ্যে পরিবর্তন করে)"""
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Light Mode")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Dark Mode")

# --- Run Application ---
if __name__ == "__main__":
    app = FileCompressorApp()
    app.mainloop()