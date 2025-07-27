import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import json
from datetime import datetime, timedelta

# --- Mehrsprachige Texte ---
texts = {
    "de": {
        "title": "🔑 Lizenzschlüssel Generator",
        "prefix": "Lizenz-Präfix (optional):",
        "count": "Anzahl der Lizenzen:",
        "valid": "Gültigkeit in Tagen (leer = unendlich):",
        "block_length": "Blocklänge (Zeichen pro Block):",
        "blocks_count": "Anzahl der Blöcke:",
        "generate": "🔄 Lizenzen generieren",
        "result": "Erzeugte Lizenzschlüssel:",
        "save": "💾 Lizenzen speichern",
        "copy": "📋 In Zwischenablage kopieren",
        "theme_dark": "🌙 Dunkelmodus",
        "theme_light": "☀️ Hellmodus",
        "error_value": "Bitte gültige Werte eingeben!",
        "saved": "Lizenzen wurden gespeichert.",
        "copied": "Lizenzen wurden in die Zwischenablage kopiert!",
        "nothing_to_copy": "Bitte erst Lizenzen generieren.",
        "savefile": "Textdatei",
        "jsonfile": "JSON Datei",
        "license_note": "\n\n---\nDiese Lizenz wurde mit dem Lizenzgenerator erstellt.",
    },
    "en": {
        "title": "🔑 License Key Generator",
        "prefix": "License Prefix (optional):",
        "count": "Number of Licenses:",
        "valid": "Validity in Days (empty = unlimited):",
        "block_length": "Block Length (chars per block):",
        "blocks_count": "Number of Blocks:",
        "generate": "🔄 Generate Licenses",
        "result": "Generated License Keys:",
        "save": "💾 Save Licenses",
        "copy": "📋 Copy to Clipboard",
        "theme_dark": "🌙 Dark Mode",
        "theme_light": "☀️ Light Mode",
        "error_value": "Please enter valid values!",
        "saved": "Licenses saved.",
        "copied": "Licenses copied to clipboard!",
        "nothing_to_copy": "Please generate licenses first.",
        "savefile": "Text File",
        "jsonfile": "JSON File",
        "license_note": "\n\n---\nThis license was generated with the license key generator.",
    },
    "ru": {
        "title": "🔑 Генератор лицензионных ключей",
        "prefix": "Префикс лицензии (необязательно):",
        "count": "Количество лицензий:",
        "valid": "Срок действия в днях (пусто = неограниченно):",
        "block_length": "Длина блока (символов в блоке):",
        "blocks_count": "Количество блоков:",
        "generate": "🔄 Сгенерировать лицензии",
        "result": "Сгенерированные лицензионные ключи:",
        "save": "💾 Сохранить лицензии",
        "copy": "📋 Скопировать в буфер обмена",
        "theme_dark": "🌙 Темная тема",
        "theme_light": "☀️ Светлая тема",
        "error_value": "Пожалуйста, введите корректные значения!",
        "saved": "Лицензии сохранены.",
        "copied": "Лицензии скопированы в буфер обмена!",
        "nothing_to_copy": "Пожалуйста, сначала сгенерируйте лицензии.",
        "savefile": "Текстовый файл",
        "jsonfile": "JSON файл",
        "license_note": "\n\n---\nЭта лицензия была создана с помощью генератора лицензионных ключей.",
    }
}

current_lang = "de"

def tr(key):
    return texts[current_lang].get(key, key)

def generate_license_key(prefix, block_length=5, blocks_count=5):
    chars = string.ascii_uppercase + string.digits
    blocks = [''.join(secrets.choice(chars) for _ in range(block_length)) for _ in range(blocks_count)]
    key = '-'.join(blocks)
    return f"{prefix}-{key}" if prefix else key

def generate_keys():
    try:
        prefix = entry_prefix.get().strip()
        count = int(entry_count.get())
        valid_days = entry_valid.get()
        valid_days = int(valid_days) if valid_days else None

        block_length = int(entry_block_length.get()) if entry_block_length.get() else 5
        blocks_count = int(entry_blocks_count.get()) if entry_blocks_count.get() else 5

        keys = []
        for _ in range(count):
            key = generate_license_key(prefix, block_length, blocks_count)
            data = {"key": key}
            if valid_days:
                expiry = datetime.utcnow() + timedelta(days=valid_days)
                data["valid_until"] = expiry.strftime('%Y-%m-%d')
            keys.append(data)

        result_text.configure(state='normal')
        result_text.delete(1.0, tk.END)
        for k in keys:
            result_text.insert(tk.END, f"{k['key']} | Valid until: {k.get('valid_until', '∞')}\n")
        result_text.configure(state='disabled')

        # Automatisches Setzen der Clipboard-Funktion auf Save Button (neu setzen bei jedem Generieren)
        def save_keys():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                (tr("savefile"), "*.txt"), (tr("jsonfile"), "*.json")])
            if file_path:
                if file_path.endswith(".json"):
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(keys, f, indent=4, ensure_ascii=False)
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        for k in keys:
                            f.write(f"{k['key']} | Valid until: {k.get('valid_until', '∞')}\n")
                        f.write(tr("license_note"))  # Lizenzhinweis anhängen
                messagebox.showinfo(tr("saved"), tr("saved"))

        save_button.config(command=save_keys)
        save_button.pack(pady=10)

    except ValueError:
        messagebox.showerror("Error", tr("error_value"))

def copy_to_clipboard():
    keys_text = result_text.get("1.0", tk.END).strip()
    if not keys_text:
        messagebox.showwarning("Warning", tr("nothing_to_copy"))
        return
    root.clipboard_clear()
    root.clipboard_append(keys_text)
    messagebox.showinfo("Info", tr("copied"))

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        bg_color = "#2e2e2e"
        fg_color = "#ff0000"
        entry_bg = "#3c3f41"
        text_bg = "#1e1e1e"
        text_fg = "#ffffff"
        btn_bg = "#555555"
        style.theme_use('clam')
    else:
        bg_color = "#f2f2f2"
        fg_color = "#000000"
        entry_bg = "#ffffff"
        text_bg = "#ffffff"
        text_fg = "#000000"
        btn_bg = None
        style.theme_use('default')

    root.configure(bg=bg_color)
    frame.configure(style="Custom.TFrame")
    style.configure("Custom.TFrame", background=bg_color)

    for widget in frame.winfo_children():
        cls = widget.__class__.__name__

        if cls in ('Label', 'TLabel'):
            widget.configure(background=bg_color, foreground=fg_color)
        elif cls in ('Entry', 'TEntry'):
            try:
                widget.configure(background=entry_bg, foreground=fg_color)
            except:
                pass
        elif cls == 'Text':
            widget.config(state='normal')
            widget.configure(background=text_bg, foreground=text_fg, insertbackground=text_fg,
                             highlightbackground=text_bg, highlightcolor=text_bg)
            widget.config(state='disabled')
        elif cls in ('Button', 'TButton'):
            if btn_bg:
                style.configure("Custom.TButton", background=btn_bg, foreground=fg_color)
                widget.configure(style="Custom.TButton")
            else:
                widget.configure(style="TButton")

    if btn_bg:
        style.configure("Custom.TButton", background=btn_bg, foreground=fg_color)
        save_button.configure(style="Custom.TButton")
        copy_button.configure(style="Custom.TButton")
        theme_btn.configure(style="Custom.TButton")
    else:
        save_button.configure(style="TButton")
        copy_button.configure(style="TButton")
        theme_btn.configure(style="TButton")

    theme_btn.config(text=tr("theme_light") if dark_mode else tr("theme_dark"))

def change_language(event=None):
    global current_lang
    current_lang = lang_var.get()
    root.title(tr("title"))
    # Labels updaten
    label_prefix.config(text=tr("prefix"))
    label_count.config(text=tr("count"))
    label_valid.config(text=tr("valid"))
    label_block_length.config(text=tr("block_length"))
    label_blocks_count.config(text=tr("blocks_count"))
    generate_btn.config(text=tr("generate"))
    label_result.config(text=tr("result"))
    save_button.config(text=tr("save"))
    copy_button.config(text=tr("copy"))
    toggle_theme()  # Theme neu laden für Texte im Button
    # Falls Ergebnis Text schon gefüllt ist, anpassen
    if result_text.get("1.0", tk.END).strip():
        generate_keys()

# -------------------- GUI SETUP --------------------

root = tk.Tk()
root.title(tr("title"))
root.geometry("650x650")

dark_mode = False  # Muss VOR toggle_theme() gesetzt sein

style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(10, 10))
style.configure("TEntry", padding=4)

frame = ttk.Frame(root, padding=20)
frame.pack(fill=tk.BOTH, expand=True)

# Sprach-Auswahl Dropdown
lang_var = tk.StringVar(value=current_lang)
lang_select = ttk.OptionMenu(root, lang_var, current_lang, *texts.keys(), command=change_language)
lang_select.pack(pady=5)

# Eingabefelder
label_prefix = ttk.Label(frame, text=tr("prefix"))
label_prefix.grid(row=0, column=0, sticky="w")
entry_prefix = ttk.Entry(frame, width=30)
entry_prefix.insert(0, "PRO")
entry_prefix.grid(row=0, column=1, pady=5)

label_count = ttk.Label(frame, text=tr("count"))
label_count.grid(row=1, column=0, sticky="w")
entry_count = ttk.Entry(frame, width=30)
entry_count.insert(0, "5")
entry_count.grid(row=1, column=1, pady=5)

label_valid = ttk.Label(frame, text=tr("valid"))
label_valid.grid(row=2, column=0, sticky="w")
entry_valid = ttk.Entry(frame, width=30)

entry_valid.insert(0, "")
entry_valid.grid(row=2, column=1, pady=5)

label_block_length = ttk.Label(frame, text=tr("block_length"))
label_block_length.grid(row=3, column=0, sticky="w")
entry_block_length = ttk.Entry(frame, width=30)
entry_block_length.insert(0, "5")
entry_block_length.grid(row=3, column=1, pady=5)

label_blocks_count = ttk.Label(frame, text=tr("blocks_count"))
label_blocks_count.grid(row=4, column=0, sticky="w")
entry_blocks_count = ttk.Entry(frame, width=30)
entry_blocks_count.insert(0, "5")
entry_blocks_count.grid(row=4, column=1, pady=5)

generate_btn = ttk.Button(frame, text=tr("generate"), command=generate_keys)
generate_btn.grid(row=5, column=0, columnspan=2, pady=15)

label_result = ttk.Label(frame, text=tr("result"))
label_result.grid(row=6, column=0, sticky="w", pady=(10,0))

result_text = tk.Text(frame, height=12, width=65, state='disabled', wrap="none")
result_text.grid(row=7, column=0, columnspan=2)

#Scrollbars für result_text
scroll_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=result_text.yview)
scroll_y.grid(row=7, column=2, sticky="ns")
result_text.config(yscrollcommand=scroll_y.set)

scroll_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=result_text.xview)
scroll_x.grid(row=8, column=0, columnspan=2, sticky="ew")
result_text.config(xscrollcommand=scroll_x.set)

#Buttons für Speichern & Kopieren
save_button = ttk.Button(frame, text=tr("save"), state=tk.DISABLED)
copy_button = ttk.Button(frame, text=tr("copy"), command=copy_to_clipboard)
copy_button.grid(row=9, column=0, sticky="ew", pady=10)
save_button.grid(row=9, column=1, sticky="ew", pady=10)

#Theme Toggle Button
theme_btn = ttk.Button(root, text=tr("theme_dark"), command=toggle_theme)
theme_btn.pack(pady=5)

toggle_theme() # Start mit hellem Theme

root.mainloop()