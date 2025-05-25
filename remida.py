import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import threading
import os


try:
    import g4f
    from g4f.Provider import You
    g4f_available = True
except ImportError:
    g4f_available = False

def simple_chatbot(user_input):
    user_input = user_input.lower()
    responses = {
       "burn": "For minor burns, cool the area with running water for 10-15 minutes. Do not apply ice or butter.",
    "cut": "Apply pressure with a clean cloth to stop bleeding. Elevate if possible. Seek medical help if severe.",
    "bleeding": "Apply pressure with a clean cloth to stop bleeding. Elevate if possible. Seek medical help if severe.",
    "faint": "Lay the person flat and elevate their legs. Loosen tight clothing and ensure fresh air.",
    "fainted": "Lay the person flat and elevate their legs. Loosen tight clothing and ensure fresh air.",
    "choking": "Encourage coughing. If choking continues, perform the Heimlich maneuver or seek emergency help.",
    "fracture": "Immobilize the area with a splint. Avoid moving the person and seek medical attention immediately.",
    "broken bone": "Immobilize the area with a splint. Avoid moving the person and seek medical attention immediately.",
    "nosebleed": "Lean forward and pinch the nostrils together for 10 minutes. Do not tilt the head back.",
    "heart attack": "Call emergency services. Help the person sit and stay calm. Give aspirin if advised.",
    "cpr": "Perform 30 chest compressions followed by 2 rescue breaths. Repeat until help arrives.",
    "burning sensation in chest": "This may be a sign of heart attack. Call emergency services and stay with the person.",
    "chest pain": "This may be a sign of heart attack. Call emergency services and stay with the person.",
    "seizure": "Protect the person from injury. Do not hold them down. Once it ends, turn them on their side.",
    "snake bite": "Keep the victim calm and still. Immobilize the bitten area and seek emergency help immediately.",
    "unconscious": "Check for breathing. Call emergency services. If not breathing, begin CPR.",
    "eye injury": "Avoid rubbing the eye. Rinse with clean water and seek medical care.",
    "thank you": "You're welcome! Stay safe and always be prepared.",
    "thanks": "You're welcome! Stay safe and always be prepared.",
    "stroke": "Call emergency services immediately. Note the time symptoms started. Keep the person calm and monitor their condition.",
    "allergic reaction": "If the person has an epinephrine auto-injector, help them use it. Call emergency services immediately.",
    "anaphylaxis": "Administer epinephrine immediately if available. Call emergency services and keep the person lying down.",
    "asthma attack": "Help the person use their inhaler. If symptoms persist, call emergency services.",
    "diabetic emergency": "If conscious, give the person a sugary drink or snack. If unconscious, do not give anything by mouth and call emergency services.",
    "hypoglycemia": "Provide a sugary drink or snack if the person is conscious. Seek medical help if symptoms do not improve.",
    "hyperglycemia": "Encourage the person to take their insulin if prescribed. Seek medical advice promptly.",
    "heat exhaustion": "Move the person to a cool place, have them lie down, and give them water. Seek medical help if symptoms worsen.",
    "heat stroke": "Call emergency services immediately. Move the person to a cooler environment and cool them with damp cloths.",
    "hypothermia": "Move the person to a warm place, remove wet clothing, and warm them gradually. Seek medical attention.",
    "frostbite": "Warm the affected area with body heat or warm water. Do not rub or massage the area. Seek medical care.",
    "drowning": "Call emergency services. If trained, begin CPR immediately after removing the person from the water.",
    "electric shock": "Do not touch the person if they are still in contact with the source. Turn off the power and call emergency services.",
    "poisoning": "Call the poison control center or emergency services. Do not induce vomiting unless instructed.",
    "drug overdose": "Call emergency services immediately. If trained, administer naloxone if available.",
    "alcohol poisoning": "Call emergency services. Keep the person awake and sitting up if possible.",
    "head injury": "Keep the person still and monitor for changes in consciousness. Seek medical attention.",
    "spinal injury": "Do not move the person. Call emergency services and keep them still.",
    "eye chemical exposure": "Rinse the eye with clean water for at least 15 minutes and seek medical help.",
    "nose fracture": "Apply a cold compress to reduce swelling. Seek medical attention.",
    "tooth knocked out": "Place the tooth in milk or saline solution and seek dental care immediately.",
    "animal bite": "Wash the area with soap and water. Apply a clean bandage and seek medical attention.",
    "insect sting": "Remove the stinger if present. Apply a cold pack and monitor for allergic reactions.",
    "tick bite": "Remove the tick with tweezers, clean the area, and monitor for signs of illness.",
    "bee sting": "Remove the stinger, apply a cold pack, and monitor for allergic reactions.",
    "wasp sting": "Clean the area, apply a cold pack, and monitor for allergic reactions.",
    "spider bite": "Clean the area, apply a cold pack, and seek medical attention if symptoms worsen.",
    "scorpion sting": "Clean the area, apply a cold pack, and seek medical attention.",
    "jellyfish sting": "Rinse with vinegar or salt water. Do not use fresh water. Seek medical help if necessary.",
    "marine animal sting": "Rinse with vinegar or salt water and seek medical attention.",
    "chemical burn": "Remove contaminated clothing and rinse the area with water for at least 20 minutes. Seek medical care.",
    "sunburn": "Cool the skin with damp cloths, apply aloe vera, and stay hydrated.",
    "blister": "Keep the blister clean and covered. Do not pop it unless necessary.",
    "sprain": "Rest, ice, compress, and elevate the injured area. Seek medical advice if severe.",
    "strain": "Rest the muscle, apply ice, and avoid strenuous activity.",
    "dislocation": "Do not attempt to reposition. Immobilize the joint and seek medical attention.",
    "cramps": "Stretch and massage the muscle. Stay hydrated.",
    "nose injury": "Apply a cold compress and keep the head elevated. Seek medical help if bleeding persists.",
    "ear injury": "Keep the ear clean and dry. Seek medical attention if there is bleeding or hearing loss.",
    "foreign object in eye": "Do not rub the eye. Rinse with clean water and seek medical care.",
    "foreign object in ear": "Do not attempt to remove it yourself. Seek medical attention.",
    "foreign object in nose": "Do not attempt to remove it yourself. Seek medical attention.",
    "foreign object in skin": "Clean the area and remove the object if possible. Seek medical help if necessary.",
    "puncture wound": "Clean the wound, apply a bandage, and seek medical attention.",
    "abrasion": "Clean the area with water, apply an antibiotic ointment, and cover with a bandage.",
    "laceration": "Apply pressure to stop bleeding, clean the wound, and seek medical attention.",
    "amputation": "Call emergency services. Control bleeding and preserve the amputated part in a clean, moist cloth.",
    "crush injury": "Call emergency services. Do not remove the crushing object if it's still in place.",
    "internal bleeding": "Call emergency services immediately. Keep the person lying down and still.",
    "shock": "Lay the person down, elevate their legs, keep them warm, and call emergency services.",
    "panic attack": "Encourage slow, deep breaths and provide reassurance. Seek medical help if necessary.",
    "hyperventilation": "Encourage slow breathing and provide reassurance. Seek medical help if necessary.",
    "severe vomiting": "Keep the person hydrated and seek medical attention if vomiting persists.",
    "diarrhea": "Encourage fluid intake and monitor for signs of dehydration.",
    "constipation": "Encourage fluid intake, dietary fiber, and physical activity.",
    "abdominal pain": "Monitor the pain and seek medical attention if it persists or worsens.",
    "appendicitis": "Seek immediate medical attention for severe abdominal pain, especially in the lower right side.",
    "menstrual cramps": "Apply heat to the abdomen and consider over-the-counter pain relief.",
    "urinary tract infection": "Encourage fluid intake and seek medical attention.",
    "kidney stones": "Seek medical attention for severe flank pain and blood in urine.",
    "respiratory distress": "Call emergency services. Help the person sit upright and stay calm.",
    "difficulty breathing": "Call emergency services. Help the person sit upright and stay calm.",
    "shortness of breath": "Call emergency services. Help the person sit upright and stay calm.",
    "chest tightness": "Call emergency services. Help the person sit upright and stay calm.",
    "palpitations": "Encourage relaxation and seek medical attention if symptoms persist.",
    "high blood pressure": "Seek medical attention if experiencing symptoms like headache or chest pain.",
    "low blood pressure": "Lay the person down and elevate their legs. Seek medical attention.",
    "fever": "Encourage rest and fluid intake. Seek medical attention if fever is high or persistent.",
    "cough": "Stay hydrated and rest. Seek medical attention if cough persists.",
    "sore throat": "Stay hydrated and rest. Seek medical attention if symptoms worsen.",
    "earache": "Apply a warm compress and seek medical attention if pain persists.",
    "toothache": "Rinse the mouth with warm water and seek dental care.",
    "rash": "Keep the area clean and avoid scratching. Seek medical attention if rash spreads.",
    "hives": "Avoid known allergens and consider antihistamines. Seek medical attention if symptoms worsen.",
    "eczema": "Keep the skin moisturized and avoid irritants. Seek medical advice for treatment.",
    "psoriasis": "Follow prescribed treatments and avoid triggers. Consult a healthcare provider.",
    "acne": "Keep the skin clean and avoid picking at pimples. Consult a dermatologist for treatment options.",
    "migraine": "Rest in a dark, quiet room and consider prescribed medications. Seek medical attention if migraines are frequent.",
    "headache": "Rest and stay hydrated. Seek medical attention if headaches are severe or persistent."
    
    }
    for key in responses:
        if key in user_input:
            return responses[key]
    return "I'm not sure about that. Please ask me about common first aid or emergency situations."

def ai_chatbot_response(prompt):
    try:
        return g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        return f"AI mode error: {str(e)}"

# GUI Functions
def show_chat_page():
    welcome_frame.pack_forget()
    chat_frame.pack(fill="both", expand=True)

def show_welcome_page():
    chat_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True)

def send_message():
    user_input = entry_box.get()
    if user_input.strip() == "":
        return
    chat_log.configure(state="normal")
    chat_log.insert("end", f"You: {user_input}\n")
    chat_log.configure(state="disabled")
    chat_log.see("end")
    entry_box.delete(0, "end")

    def process_response():
        chat_log.configure(state="normal")
        if mode_var.get() == "local":
            bot_response = simple_chatbot(user_input)
        elif mode_var.get() == "ai":
            bot_response = ai_chatbot_response(user_input)
        else:
            bot_response = "Invalid mode selected."
        chat_log.insert("end", f"Remida: {bot_response}\n\n")
        chat_log.configure(state="disabled")
        chat_log.see("end")

    threading.Thread(target=process_response).start()

# App config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Remida ver1.0.0")
app.geometry("750x750")

# Welcome screen
welcome_frame = ctk.CTkFrame(app, fg_color="transparent")
welcome_frame.pack(fill="both", expand=True)

# Background image
bg_image_path = os.path.join(os.getcwd(), "welcome_bg.jpg")
if os.path.exists(bg_image_path):
    pil_img = Image.open(bg_image_path).resize((750, 750))
    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(750, 750))
    bg_label = ctk.CTkLabel(welcome_frame, image=ctk_img, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Ask button
ask_button = ctk.CTkButton(
    welcome_frame,
    text="ASK",
    width=180,
    height=70,
    font=ctk.CTkFont(size=28, weight="bold"),
    fg_color="#4CAF50",       
    hover_color="#388E3C",     
    text_color="white",
    corner_radius=0,
    command=show_chat_page
)
ask_button.place(x=500, y=540)  


# Chat page
chat_frame = ctk.CTkFrame(app)

back_button = ctk.CTkButton(chat_frame, text="⭠ Back", command=show_welcome_page,
                            fg_color="#d32f2f", hover_color="#b71c1c", width=100)
back_button.pack(anchor="nw", padx=10, pady=10)

title_label = ctk.CTkLabel(chat_frame, text="🩺 Remida – Ask me First Aid or Emergency Questions",
                           font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
title_label.pack(fill="x", pady=(0, 5))

chat_log = ctk.CTkTextbox(chat_frame, height=480, font=("Segoe UI", 13),
                          wrap="word", state="disabled", activate_scrollbars=True)
chat_log.pack(padx=10, pady=10, fill="both", expand=True)

mode_var = ctk.StringVar(value="local")
mode_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
mode_frame.pack(padx=10, pady=(5, 10), anchor="w")

ctk.CTkLabel(mode_frame, text="Mode:", font=("Segoe UI", 12)).pack(side="left", padx=(0, 10))
ctk.CTkRadioButton(mode_frame, text="Base", variable=mode_var, value="local").pack(side="left")
ctk.CTkRadioButton(mode_frame, text="AI", variable=mode_var, value="ai",
                   state="normal" if g4f_available else "disabled").pack(side="left")

entry_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
entry_frame.pack(padx=10, pady=10, fill="x")

entry_box = ctk.CTkEntry(entry_frame, placeholder_text="Type your message here...", font=("Segoe UI", 13))
entry_box.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=6)

send_button = ctk.CTkButton(entry_frame, text="Send", command=send_message, corner_radius=20)
send_button.pack(side="right")


show_welcome_page()

app.mainloop()
