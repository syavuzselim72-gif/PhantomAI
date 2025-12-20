import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import json
import os
import logging
import random
import time

# Logging ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ParticleSystem:
    def __init__(self, canvas):
        self.canvas = canvas
        self.particles = []
        self.colors = ['#ff0080', '#00ffff', '#ff8000', '#8000ff', '#00ff80']

    def create_particle(self, x, y):
        particle = {
            'x': x,
            'y': y,
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-2, 2),
            'life': 100,
            'color': random.choice(self.colors),
            'size': random.randint(2, 6)
        }
        self.particles.append(particle)
        return self.canvas.create_oval(
            x - particle['size'], y - particle['size'],
            x + particle['size'], y + particle['size'],
            fill=particle['color'], outline=''
        )

    def update_particles(self):
        to_remove = []
        for i, particle in enumerate(self.particles):
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['size'] *= 0.98

            if particle['life'] <= 0 or particle['size'] < 1:
                to_remove.append(i)
                continue

            # Glow effect
            alpha = particle['life'] / 100
            color = particle['color']
            self.canvas.coords(
                particle['id'],
                particle['x'] - particle['size'], particle['y'] - particle['size'],
                particle['x'] + particle['size'], particle['y'] + particle['size']
            )
            self.canvas.itemconfig(particle['id'], fill=color)

        # Remove dead particles
        for i in reversed(to_remove):
            self.canvas.delete(self.particles[i]['id'])
            del self.particles[i]

    def animate(self):
        self.update_particles()
        self.canvas.after(16, self.animate)  # ~60 FPS

class ChatWorker(threading.Thread):
    def __init__(self, message, server_url, callback, error_callback):
        super().__init__()
        self.message = message
        self.server_url = server_url
        self.callback = callback
        self.error_callback = error_callback
        self.daemon = True

    def run(self):
        try:
            response = requests.post(
                f"{self.server_url}/chat",
                json={"message": self.message},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if 'reply' in data:
                    self.callback(data['reply'])
                else:
                    self.error_callback("Server'dan geçersiz yanıt")
            else:
                self.error_callback(f"HTTP {response.status_code}")
        except Exception as e:
            self.error_callback(f"Hata: {str(e)}")

class NeonChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title('PhantomAI - Neon Edition')
        self.root.geometry('900x700')
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)

        # Server URL - otomatik algılanacak
        self.server_url = 'http://localhost:8001'

        # Neon renk paleti
        self.neon_colors = {
            'pink': '#ff0080',
            'cyan': '#00ffff',
            'orange': '#ff8000',
            'purple': '#8000ff',
            'green': '#00ff80',
            'bg': '#0a0a0a',
            'surface': '#1a1a1a',
            'text': '#ffffff',
            'text_secondary': '#cccccc'
        }

        self.create_styles()
        self.create_widgets()
        self.setup_animations()

        # Otomatik server algılama
        self.auto_detect_server()

    def auto_detect_server(self):
        """Otomatik olarak server IP'sini algılar"""
        self.status_label.config(text="🔍 SERVER ARANIYOR...", fg=self.neon_colors['orange'])

        def detect():
            try:
                # 1. Önce localhost'u dene
                response = requests.get('http://localhost:8001/health', timeout=2)
                if response.status_code == 200:
                    self.root.after(0, lambda: self.on_server_found('http://localhost:8001', 'YEREL'))
                    return
            except:
                pass

            try:
                # 2. Yerel IP'yi al ve aynı ağdaki IP'leri dene
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()

                # Aynı subnet'teki IP'leri test et
                ip_parts = local_ip.split('.')
                base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."

                # Paralel olarak IP'leri test et
                import concurrent.futures
                import threading

                found_server = None
                found_lock = threading.Lock()

                def test_ip(ip):
                    nonlocal found_server
                    try:
                        response = requests.get(f'http://{ip}:8001/health', timeout=1)
                        if response.status_code == 200:
                            with found_lock:
                                if not found_server:
                                    found_server = f'http://{ip}:8001'
                    except:
                        pass

                # 1-254 arası IP'leri test et (ama kendi IP'mizi atla)
                test_ips = [f"{base_ip}{i}" for i in range(1, 255) if f"{base_ip}{i}" != local_ip]

                # Thread pool ile paralel test
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    futures = [executor.submit(test_ip, ip) for ip in test_ips[:50]]  # İlk 50'yi test et
                    for future in concurrent.futures.as_completed(futures):
                        if found_server:
                            break

                if found_server:
                    self.root.after(0, lambda: self.on_server_found(found_server, 'AĞ'))
                else:
                    self.root.after(0, lambda: self.on_server_not_found())

            except Exception as e:
                logger.error(f"Otomatik algılama hatası: {e}")
                self.root.after(0, lambda: self.on_server_not_found())

        threading.Thread(target=detect, daemon=True).start()

    def on_server_found(self, url, source):
        """Server bulunduğunda çağrılır"""
        self.server_url = url
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

        self.status_label.config(text=f"✅ SERVER BULUNDU ({source})", fg=self.neon_colors['green'])
        self.connect_btn.config(text="🎉 BAĞLI")

        # Başarı partikülleri
        for _ in range(30):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            particle_id = self.particle_system.create_particle(x, y)
            self.particle_system.particles[-1]['id'] = particle_id

        self.add_message(f"🎉 Server otomatik olarak bulundu: {url} ({source})", "SYSTEM")

    def on_server_not_found(self):
        """Server bulunamadığında çağrılır"""
        self.status_label.config(text="❌ SERVER BULUNAMADI", fg=self.neon_colors['pink'])
        self.connect_btn.config(text="🔄 TEKRAR DENE")

        self.add_message("❌ Otomatik server algılama başarısız. Lütfen server URL'sini manuel girin.", "SYSTEM")
        self.add_message("💡 Server'ı çalıştırmak için: python server.py", "SYSTEM")

    def create_styles(self):
        style = ttk.Style()

        # Neon button style
        style.configure('Neon.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       background=self.neon_colors['bg'],
                       foreground=self.neon_colors['cyan'],
                       borderwidth=2,
                       relief='raised')

        style.map('Neon.TButton',
                 background=[('active', self.neon_colors['surface'])],
                 foreground=[('active', self.neon_colors['pink'])])

        # Neon entry style
        style.configure('Neon.TEntry',
                       font=('Segoe UI', 11),
                       fieldbackground=self.neon_colors['surface'],
                       bordercolor=self.neon_colors['cyan'],
                       lightcolor=self.neon_colors['cyan'],
                       darkcolor=self.neon_colors['cyan'],
                       insertcolor=self.neon_colors['text'])

    def create_widgets(self):
        # Ana container
        main_frame = tk.Frame(self.root, bg=self.neon_colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Particle canvas (arka plan efekti)
        self.particle_canvas = tk.Canvas(main_frame, bg=self.neon_colors['bg'],
                                       highlightthickness=0, borderwidth=0)
        self.particle_canvas.pack(fill=tk.BOTH, expand=True)

        # İçerik frame
        content_frame = tk.Frame(self.particle_canvas, bg=self.neon_colors['bg'])
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Başlık
        title_frame = tk.Frame(content_frame, bg=self.neon_colors['bg'])
        title_frame.pack(pady=(0, 30))

        title_label = tk.Label(title_frame, text='PHANTOM AI',
                              font=('Segoe UI', 36, 'bold'),
                              fg=self.neon_colors['cyan'],
                              bg=self.neon_colors['bg'])
        title_label.pack()

        # Glow effect için ikinci layer
        title_glow = tk.Label(title_frame, text='PHANTOM AI',
                             font=('Segoe UI', 36, 'bold'),
                             fg=self.neon_colors['pink'],
                             bg=self.neon_colors['bg'])
        title_glow.pack()
        title_glow.place(x=title_label.winfo_x() + 2, y=title_label.winfo_y() + 2)

        subtitle = tk.Label(title_frame, text='NEON EDITION',
                           font=('Segoe UI', 14),
                           fg=self.neon_colors['orange'],
                           bg=self.neon_colors['bg'])
        subtitle.pack(pady=(10, 0))

        # Server bağlantısı
        connection_frame = tk.Frame(content_frame, bg=self.neon_colors['surface'],
                                   relief='ridge', borderwidth=2)
        connection_frame.pack(fill=tk.X, pady=(0, 20), padx=20)

        ttk.Label(connection_frame, text="Server URL:",
                 foreground=self.neon_colors['text'],
                 background=self.neon_colors['surface']).pack(side=tk.LEFT, padx=(20, 10), pady=10)

        self.url_entry = ttk.Entry(connection_frame, style='Neon.TEntry', width=40)
        self.url_entry.insert(0, self.server_url)
        self.url_entry.pack(side=tk.LEFT, padx=(0, 10), pady=10, fill=tk.X, expand=True)

        self.connect_btn = ttk.Button(connection_frame, text="🔗 BAĞLAN",
                                     style='Neon.TButton', command=self.connect_server)
        self.connect_btn.pack(side=tk.RIGHT, padx=(0, 20), pady=10)

        # Durum göstergesi
        self.status_frame = tk.Frame(connection_frame, bg=self.neon_colors['surface'])
        self.status_frame.pack(side=tk.RIGHT, padx=(10, 0))

        self.status_indicator = tk.Canvas(self.status_frame, width=20, height=20,
                                        bg=self.neon_colors['surface'], highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 5))
        self.status_dot = self.status_indicator.create_oval(5, 5, 15, 15, fill='#666666')

        self.status_label = tk.Label(self.status_frame, text="BAĞLANIYOR...",
                                    font=('Segoe UI', 10),
                                    fg=self.neon_colors['text_secondary'],
                                    bg=self.neon_colors['surface'])
        self.status_label.pack(side=tk.LEFT)

        # Chat container
        chat_container = tk.Frame(content_frame, bg=self.neon_colors['bg'])
        chat_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Chat frame
        chat_frame = tk.Frame(chat_container, bg=self.neon_colors['surface'],
                             relief='ridge', borderwidth=2)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Chat text area
        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg=self.neon_colors['bg'],
            fg=self.neon_colors['text'],
            insertbackground=self.neon_colors['cyan'],
            selectbackground=self.neon_colors['purple'],
            selectforeground=self.neon_colors['text'],
            padx=15,
            pady=15,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True)
        self.chat_text.config(state=tk.DISABLED)

        # Typing indicator
        self.typing_frame = tk.Frame(chat_container, bg=self.neon_colors['bg'])
        self.typing_frame.pack(fill=tk.X, pady=(0, 10))

        self.typing_label = tk.Label(self.typing_frame, text="",
                                    font=('Segoe UI', 10),
                                    fg=self.neon_colors['orange'],
                                    bg=self.neon_colors['bg'])
        self.typing_label.pack(anchor=tk.W, padx=20)

        # Input frame
        input_frame = tk.Frame(chat_container, bg=self.neon_colors['surface'],
                              relief='ridge', borderwidth=2)
        input_frame.pack(fill=tk.X)

        self.message_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=self.neon_colors['surface'],
            fg=self.neon_colors['text'],
            insertbackground=self.neon_colors['cyan'],
            selectbackground=self.neon_colors['purple'],
            selectforeground=self.neon_colors['text'],
            borderwidth=2,
            relief='flat'
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=15, ipady=8)
        self.message_entry.bind('<Return>', self.send_message)

        self.send_btn = tk.Button(
            input_frame,
            text='🚀 GÖNDER',
            command=self.send_message,
            font=('Segoe UI', 11, 'bold'),
            bg=self.neon_colors['cyan'],
            fg=self.neon_colors['bg'],
            activebackground=self.neon_colors['pink'],
            activeforeground=self.neon_colors['bg'],
            borderwidth=0,
            padx=25,
            pady=12,
            cursor='hand2'
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(0, 20))

        # Hoş geldin mesajı
        self.add_message("🌟 PhantomAI Neon Edition'a hoş geldiniz!\n💫 Server'a bağlanın ve büyüleyici sohbet deneyimine başlayın.", "SYSTEM")

        # Particle system başlat
        self.particle_system = ParticleSystem(self.particle_canvas)

    def setup_animations(self):
        # Button hover efektleri
        def on_enter(e):
            e.widget.config(bg=self.neon_colors['pink'])

        def on_leave(e):
            e.widget.config(bg=self.neon_colors['cyan'])

        self.send_btn.bind('<Enter>', on_enter)
        self.send_btn.bind('<Leave>', on_leave)

        # Pulsing effect for status dot
        self.pulse_status()

    def pulse_status(self):
        current_color = self.status_indicator.itemcget(self.status_dot, 'fill')
        if current_color == '#666666':
            self.status_indicator.itemconfig(self.status_dot, fill='#cccccc')
        else:
            self.status_indicator.itemconfig(self.status_dot, fill='#666666')
        self.root.after(1000, self.pulse_status)

    def connect_server(self):
        self.server_url = self.url_entry.get().strip()
        if not self.server_url:
            self.show_error("Server URL boş olamaz!")
            return

        # Bağlantı animasyonu
        self.connect_btn.config(text="⏳ BAĞLANIYOR...")
        self.status_indicator.itemconfig(self.status_dot, fill=self.neon_colors['orange'])
        self.status_label.config(text="BAĞLANIYOR...", fg=self.neon_colors['orange'])

        self.check_connection()

    def check_connection(self):
        def check():
            try:
                response = requests.get(f"{self.server_url}/health", timeout=5)
                if response.status_code == 200:
                    self.root.after(0, lambda: self.on_connection_success())
                else:
                    self.root.after(0, lambda: self.on_connection_error("Server yanıt vermiyor"))
            except:
                self.root.after(0, lambda: self.on_connection_error("Bağlantı hatası"))

        threading.Thread(target=check, daemon=True).start()

    def on_connection_success(self):
        self.connect_btn.config(text="✅ BAĞLI")
        self.status_indicator.itemconfig(self.status_dot, fill=self.neon_colors['green'])
        self.status_label.config(text="BAĞLI", fg=self.neon_colors['green'])
        self.add_message(f"🎉 Server'a başarıyla bağlandı: {self.server_url}", "SYSTEM")

        # Success particles
        for _ in range(20):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            particle_id = self.particle_system.create_particle(x, y)
            self.particle_system.particles[-1]['id'] = particle_id

    def on_connection_error(self, error):
        self.connect_btn.config(text="❌ BAĞLAN")
        self.status_indicator.itemconfig(self.status_dot, fill=self.neon_colors['pink'])
        self.status_label.config(text="BAĞLANTI HATASI", fg=self.neon_colors['pink'])
        self.show_error(f"Bağlantı hatası: {error}")

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Hata")
        error_window.geometry("400x150")
        error_window.configure(bg=self.neon_colors['bg'])
        error_window.resizable(False, False)

        tk.Label(error_window, text="⚠️ " + message,
                font=('Segoe UI', 12),
                fg=self.neon_colors['pink'],
                bg=self.neon_colors['bg']).pack(pady=30)

        ttk.Button(error_window, text="Tamam", command=error_window.destroy).pack()

    def add_message(self, text, sender="PhantomAI"):
        self.chat_text.config(state=tk.NORMAL)

        # Neon renkler ile mesaj formatı
        if sender == "Siz":
            color = self.neon_colors['cyan']
            prefix = "👤 [SİZ]"
        elif sender == "SYSTEM":
            color = self.neon_colors['orange']
            prefix = "⚙️ [SYSTEM]"
        else:
            color = self.neon_colors['pink']
            prefix = "🤖 [PHANTOM AI]"

        self.chat_text.insert(tk.END, f"{prefix} {text}\n\n", sender)
        self.chat_text.tag_configure(sender, foreground=color, font=('Consolas', 11, 'bold'))
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

        # Typing animasyonu için
        if sender != "SYSTEM":
            self.animate_typing()

    def animate_typing(self):
        dots = ["", ".", "..", "..."]
        self.typing_counter = 0

        def animate():
            if self.typing_counter < 12:  # 3 saniye
                self.typing_label.config(text=f"🤖 PhantomAI yazıyor{dots[self.typing_counter % 4]}")
                self.typing_counter += 1
                self.root.after(250, animate)
            else:
                self.typing_label.config(text="")

        animate()

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if not message:
            return

        if "❌" in self.status_label.cget("text") or "BAĞLANTI HATASI" in self.status_label.cget("text"):
            self.show_error("Önce server'a bağlanın!")
            return

        self.add_message(message, "Siz")
        self.message_entry.delete(0, tk.END)

        # Send button animasyonu
        self.send_btn.config(text="⏳ GÖNDERİLİYOR...", state=tk.DISABLED)

        # Worker thread
        worker = ChatWorker(message, self.server_url, self.on_message_received, self.on_error)
        worker.start()

    def on_message_received(self, reply):
        self.root.after(0, lambda: self.finish_send(reply))

    def finish_send(self, reply):
        self.add_message(reply, "PhantomAI")
        self.send_btn.config(text="🚀 GÖNDER", state=tk.NORMAL)

        # Success particles
        for _ in range(10):
            x = random.randint(200, 700)
            y = random.randint(300, 500)
            particle_id = self.particle_system.create_particle(x, y)
            self.particle_system.particles[-1]['id'] = particle_id

    def on_error(self, error_msg):
        self.root.after(0, lambda: self.finish_send_with_error(error_msg))

    def finish_send_with_error(self, error_msg):
        self.add_message(f"❌ {error_msg}", "SYSTEM")
        self.send_btn.config(text="🚀 GÖNDER", state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = NeonChatApp(root)

    # Particle animasyonunu başlat
    app.particle_system.animate()

    root.mainloop()

if __name__ == '__main__':
    main()
