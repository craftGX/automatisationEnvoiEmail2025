import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import smtplib
import csv
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_emails(server, port, username, password, subject, body, recipients, progress_bar):
    try:
        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            smtp.login(username, password)

            total = len(recipients)
            for idx, recipient in enumerate(recipients, start=1):
                msg = MIMEMultipart()
                msg['From'] = username
                msg['To'] = recipient
                msg['Subject'] = subject

                msg.attach(MIMEText(body, 'plain'))
                smtp.send_message(msg)

                progress = (idx / total) * 100
                progress_bar['value'] = progress
                root.update_idletasks()

        return True
    except Exception as e:
        print(e)
        return False

def load_recipients(filepath):
    recipients = []
    if filepath.endswith('.csv'):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                recipients.append(row[0])
    elif filepath.endswith('.json'):
        with open(filepath, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            recipients = data.get("emails", [])
    return recipients

def browse_file():
    file_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")]))

def start_sending():
    recipients = load_recipients(file_path.get())
    if not recipients:
        messagebox.showerror("Erreur", "Aucun destinataire trouvé.")
        return

    progress_bar['value'] = 0
    success = send_emails(
        "smtp-relay.brevo.com",  # Serveur SMTP de Sendinblue
        587,
        email_address.get(),
        email_password.get(),
        email_subject.get(),
        email_body.get("1.0", tk.END),
        recipients,
        progress_bar
    )

    if success:
        messagebox.showinfo("Succès", "Tous les emails ont été envoyés avec succès.")
    else:
        messagebox.showerror("Erreur", "Une erreur s'est produite pendant l'envoi des emails.")

# Interface Tkinter
root = tk.Tk()
root.title("Envoi d'Emails Automatique avec Sendinblue")
root.geometry("500x700")
root.configure(bg="#246EB9")

# Champs
file_path = tk.StringVar()
email_address = tk.StringVar()
email_password = tk.StringVar()
email_subject = tk.StringVar()

# Style personnalisé
label_style = {"bg": "#246EB9", "fg": "#FDFFFC", "font": ("Helvetica", 12)}
entry_style = {"bg": "#F5EE9E", "fg": "#F06543", "font": ("Helvetica", 12)}
button_style = {"bg": "#4CB944", "fg": "#FDFFFC", "font": ("Helvetica", 12, "bold")}

# Widgets

# Fichier
tk.Label(root, text="Fichier CSV/JSON :", **label_style).pack()
tk.Entry(root, textvariable=file_path, width=50, **entry_style).pack()
tk.Button(root, text="Parcourir", command=browse_file, **button_style).pack(pady=5)

# Email Login
tk.Label(root, text="Adresse Email Sendinblue :", **label_style).pack()
tk.Entry(root, textvariable=email_address, **entry_style).pack()

tk.Label(root, text="Mot de passe SMTP Sendinblue :", **label_style).pack()
tk.Entry(root, textvariable=email_password, show='*', **entry_style).pack()

# Message
tk.Label(root, text="Objet :", **label_style).pack()
tk.Entry(root, textvariable=email_subject, width=50, **entry_style).pack()

# Corps de l'email
tk.Label(root, text="Corps de l'email :", **label_style).pack()
email_body = tk.Text(root, height=10, width=50, bg="#F5EE9E", fg="#F06543", font=("Helvetica", 12))
email_body.pack()

# Progression
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=10)

# Envoyer
tk.Button(root, text="Envoyer Emails", command=start_sending, **button_style).pack(pady=20)

root.mainloop()

