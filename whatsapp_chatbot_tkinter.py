#!/usr/bin/env python3
"""
Yacchu's Hair Garage - AI Chatbot GUI
Modern chatbot interface similar to online LLM chat interfaces (like ChatGPT).
Standalone .exe - no terminal needed.
"""

import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading

from cli_chatbot import faq_lookup, agent, detect_greeting, get_greeting_response, get_farewell_response

# ==============================
# THEME / STYLING
# ==============================
PRIMARY_COLOR = "#3b82f6"        # Blue accent like ChatGPT
USER_MSG_BG = "#e3f2fd"          # Light blue for user messages
BOT_MSG_BG = "#f3f4f6"           # Light gray for bot messages
SIDEBAR_BG = "#fafafa"           # Light gray sidebar
HEADER_BG = "#ffffff"
TEXT_COLOR = "#333333"
AVATAR_BG = "#10a37f"            # Green avatar for bot
USER_AVATAR_BG = "#5436da"       # Purple avatar for user
FONT_PRIMARY = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 11, "bold")

# Apply basic theme to ttk
try:
    style = tk.ttk.Style()
    style.theme_use('clam')
    style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
    style.configure("Main.TFrame", background="#ffffff")
    style.configure("Input.TFrame", background="#ffffff")
    style.configure("Sidebar.TLabel", background=SIDEBAR_BG, foreground="#333333")
    style.configure("Primary.TButton", foreground="white", background=PRIMARY_COLOR)
except Exception:
    pass


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yacchu's Hair Garage - AI Chat")
        self.root.geometry("1000x700")
        self.root.minsize(760, 540)

        # Root window styling - use tk.Frame instead of ttk for custom bg
        self.root_frame = tk.Frame(root, bg="#ffffff")
        self.root_frame.pack(fill="both", expand=True)

        # Left sidebar
        self.create_sidebar()

        # Main chat area
        self.create_main_area()

        # Initial greeting
        self.display_message("bot", "Hi there! 👋 Welcome to Yacchu's Hair Garage. How can I help you today?")
        self.status_var.set("Ready")

    def create_sidebar(self):
        """Create left sidebar with bot name and new chat button"""
        # Use tk.Frame directly for custom background
        self.sidebar = tk.Frame(self.root_frame, width=260, bg=SIDEBAR_BG, relief="flat", bd=0)
        self.sidebar.pack(side="left", fill="y", padx=12)

        # Sidebar header (bot avatar + name)
        header = tk.Frame(self.sidebar, bg=SIDEBAR_BG, padx=16, pady=8)
        header.pack(fill="x")

        avatar = tk.Frame(header, width=40, height=40, background=AVATAR_BG)
        avatar.pack(side="left", padx=10)
        tk.Label(avatar, text="✂", bg=AVATAR_BG, fg="white",
                 font=("Segoe UI", 18), width=2).pack()

        tk.Label(header, text="Yacchu's Hair Garage\nAI Assistant",
                 bg=SIDEBAR_BG, fg="white",
                 font=("Segoe UI", 12), anchor="w").pack(side="left", fill="x")

        # Divider
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=16, pady=8)

        # New chat button - use tk.Button with command
        new_btn = tk.Button(self.sidebar, text="✎ New chat",
                            command=self.new_chat,
                            bg="#ffffff", fg="#333333",
                            font=("Segoe UI", 9),
                            activebackground="#e5e7eb",
                            activeforeground="#333333",
                            relief="flat", bd=0, cursor="hand2")
        new_btn.pack(fill="x", padx=16, pady=8)

        # Sidebar separator
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=16, pady=8)

        # Info section
        info_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG, padx=16, pady=16)
        info_frame.pack(fill="x")
        tk.Label(info_frame, text="Powered by Needle 3 (121M)\n👈 Hair services & pricing",
                 bg=SIDEBAR_BG, fg="#8a8f98", font=("Segoe UI", 9), anchor="w").pack(anchor="w")

    def create_main_area(self):
        """Create main chat area with messages and input"""
        # Main container
        self.main_container = tk.Frame(self.root_frame, bg="#ffffff")
        self.main_container.pack(side="left", fill="both", expand=True, padx=14, pady=14)

        # Messages scrollable area
        self.chat_frame = tk.Frame(self.main_container, bg="#ffffff")
        self.chat_frame.pack(fill="both", expand=True)

        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            bg="#ffffff",
            fg=TEXT_COLOR,
            state="disabled",
            padx=14,
            pady=14,
            font=FONT_PRIMARY,
            highlightthickness=0
        )
        self.chat_display.pack(fill="both", expand=True)

        # Configure message styling
        self.chat_display.tag_config("user_header", foreground="#5f6368", font=("Segoe UI", 9))
        self.chat_display.tag_config("user_body", foreground="#202123", font=("Segoe UI", 10))
        self.chat_display.tag_config("bot_header", foreground="#5f6368", font=("Segoe UI", 9))
        self.chat_display.tag_config("bot_body", foreground="#202123", font=("Segoe UI", 10))

        # Input container (at bottom)
        self.input_container = tk.Frame(self.main_container, bg="#ffffff")
        self.input_container.pack(fill="x", pady=16)

        # Input box wrapper
        self.input_frame = tk.Frame(self.input_container, bg="#f1f3f4", relief="flat", bd=2)
        self.input_frame.pack(fill="x", pady=6)

        self.message_var = tk.StringVar()
        self.message_var.trace("w", self.auto_resize)

        # Text area for input (maxheight unsupported in Python 3.14 Tcl/Tk)
        self.input_box = tk.Text(
            self.input_frame,
            wrap=tk.WORD,
            bg="#ffffff",
            fg=TEXT_COLOR,
            padx=12,
            pady=8,
            font=FONT_PRIMARY,
            height=2,
            highlightthickness=1,
            highlightcolor=PRIMARY_COLOR,
            highlightbackground="#dcdcdc"
        )
        self.input_box.pack(fill="both", expand=True)

        # Bottom toolbar
        toolbar = tk.Frame(self.input_frame, bg="#f1f3f4", relief="flat", bd=0)
        toolbar.pack(fill="x", pady=6)

        # Attachment button (decorative)
        attach_btn = tk.Button(
            toolbar, text="+", bg="#f1f3f4", fg="#333333",
            font=("Segoe UI", 9), relief="flat", cursor="hand2",
            command=self.show_info, width=3
        )
        attach_btn.pack(side="left", padx=8)

        # Send button
        send_btn = tk.Button(
            toolbar, text="Send", bg=PRIMARY_COLOR, fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.on_send, relief="flat", cursor="hand2"
        )
        send_btn.pack(side="right")

        # Enter key binding
        self.input_box.bind("<Return>", self.on_enter)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(
            self.input_frame,
            text=self.status_var.get(),
            font=("Segoe UI", 8),
            foreground="#8a8f98",
            bg="#f1f3f4"
        )
        self.status_bar.pack(anchor="e", pady=4)

    def auto_resize(self, *args):
        """Auto-resize input text area based on content"""
        count = len(self.message_var.get())
        if count == 0:
            self.root.after(10, self.reset_input_height)

    def reset_input_height(self):
        """Reset input box height to default"""
        self.input_box.configure(height=2)

    def on_enter(self, event):
        """Handle Enter key in input box"""
        # Check if Shift+Enter pressed
        if event.state & 0x0001:
            return
        self.on_send()
        return "break"

    def on_send(self):
        """Send user message and process with AI"""
        message = self.input_box.get("1.0", "end-1c").strip()
        if not message:
            return

        # Clear input box
        self.input_box.delete("1.0", tk.END)
        self.root.after(10, self.reset_input_height)

        # Display user message
        self.display_message("user", message)

        # Update status
        self.status_var.set("Bot is typing...")
        self.root.update()

        # Get bot response in background thread
        thread = threading.Thread(target=self.get_bot_response, args=(message,), daemon=True)
        thread.start()

    def get_bot_response(self, message):
        """Get response from chatbot and display it"""
        # First, check for greeting/farewell
        greeting_type = detect_greeting(message)
        if greeting_type == "greeting":
            answer = get_greeting_response()
        elif greeting_type == "farewell":
            answer = get_farewell_response()
        else:
            # Use the Needle agent (same as chatbotcli) to get the answer
            try:
                result = agent.run(message)
                answer = None
                if result.get('results'):
                    for r in result['results']:
                        if isinstance(r, dict) and 'answer' in r:
                            answer = r['answer']
                            break
                # Fallback to direct faq_lookup if agent returns nothing
                if not answer:
                    direct = faq_lookup(message)
                    answer = direct.get("answer", "Sorry, I couldn't find an answer.")
            except Exception:
                answer = "Sorry, an error occurred. Please try again."

        self.root.after(0, self.display_message, "bot", answer)
        self.root.after(0, self.status_var.set, "Ready")

    def display_message(self, sender, message):
        """Display a message in the chat window"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, "\n")

        if sender == "user":
            # Header
            self.chat_display.insert(tk.END, "You\n", "user_header")
            # User message bubble in an embedded window
            user_frame = tk.Frame(self.chat_display, bg="#e3f2fd", relief="flat", bd=1)
            user_frame.pack(fill="x", pady=2)
            # Make it look like a message bubble
            txt = tk.Label(user_frame, text=message, bg="#e3f2fd", fg="#202123",
                           font=FONT_PRIMARY, justify=tk.LEFT, wraplength=650, anchor="w")
            txt.pack(fill="x", padx=10, pady=6)
        else:
            # Bot header
            self.chat_display.insert(tk.END, "Yacchu's Hair Garage AI\n", "bot_header")
            # Bot message bubble
            bot_frame = tk.Frame(self.chat_display, bg="#fafafa", relief="flat", bd=1)
            bot_frame.pack(fill="x", pady=2)
            txt = tk.Label(bot_frame, text=message, bg="#fafafa", fg="#202123",
                           font=FONT_PRIMARY, justify=tk.LEFT, wraplength=650, anchor="w")
            txt.pack(fill="x", padx=10, pady=6)

        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.configure(state="disabled")

    def new_chat(self):
        """Clear chat and start a new conversation"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state="disabled")
        self.display_message("bot", "Hi there! 👋 Welcome to Yacchu's Hair Garage. How can I help you today?")

    def show_info(self):
        """Show info about the app"""
        self.display_message("bot", """
        Yacchu's Hair Garage AI Assistant
        Powered by Needle 3 (121M parameters)
        """)


# ==============================
# ENTRY POINT
# ==============================
def main():
    root = tk.Tk()
    root.title("Yacchu's Hair Garage - AI Chat")
    root.geometry("1000x700")
    # Allow window resize
    root.minsize(760, 540)
    app = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()