import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import joblib

# Load model
model = joblib.load("house_price_model.pkl")

# Setup root
root = tk.Tk()
root.title("🏡 House Price Predictor")
root.geometry("700x820")

# Load and set background
bg_img = Image.open("background.jpg").resize((700, 820))
bg_photo = ImageTk.PhotoImage(bg_img)

# Defaults
defaults = {
    'bedrooms': 3, 'bathrooms': 2, 'sqft_living': 1800, 'sqft_lot': 5000,
    'floors': 1, 'waterfront': 0, 'view': 0, 'condition': 3,
    'sqft_above': 1500, 'sqft_basement': 300, 'yr_built': 2000,
    'yr_renovated': 0, 'city': 'Seattle', 'statezip': 'WA 98133'
}
cities = ['Seattle', 'Redmond', 'Kent', 'Bellevue', 'Shoreline']
statezips = ['WA 98133', 'WA 98119', 'WA 98042', 'WA 98008', 'WA 98052']

def safe_cast(val, typ, default):
    try: return typ(val)
    except: return default

def predict_price():
    try:
        data = {
            'bedrooms': safe_cast(entry_bedrooms.get(), float, defaults['bedrooms']),
            'bathrooms': safe_cast(entry_bathrooms.get(), float, defaults['bathrooms']),
            'sqft_living': safe_cast(entry_sqft_living.get(), int, defaults['sqft_living']),
            'sqft_lot': safe_cast(entry_sqft_lot.get(), int, defaults['sqft_lot']),
            'floors': safe_cast(entry_floors.get(), float, defaults['floors']),
            'waterfront': safe_cast(entry_waterfront.get(), int, defaults['waterfront']),
            'view': safe_cast(entry_view.get(), int, defaults['view']),
            'condition': safe_cast(entry_condition.get(), int, defaults['condition']),
            'sqft_above': safe_cast(entry_sqft_above.get(), int, defaults['sqft_above']),
            'sqft_basement': safe_cast(entry_sqft_basement.get(), int, defaults['sqft_basement']),
            'yr_built': safe_cast(entry_yr_built.get(), int, defaults['yr_built']),
            'yr_renovated': safe_cast(entry_yr_renovated.get(), int, defaults['yr_renovated']),
            'city': city_var.get(), 'statezip': statezip_var.get()
        }
        df = pd.DataFrame([data])
        pred = model.predict(df)[0]
        messagebox.showinfo("Predicted Price", f"🏠 Estimated Price: ₹{int(pred):,}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Frame setup
frame1 = tk.Frame(root, width=700, height=820)
frame2 = tk.Frame(root, width=700, height=820)
for frame in (frame1, frame2):
    frame.pack_propagate(0)
    frame.place(x=0, y=0)

def set_background(frame):
    bg_label = tk.Label(frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Page 1: Basic Info
set_background(frame1)
tk.Label(frame1, text="👋 Let's get started!", font=("Comic Sans MS", 24, "bold"), bg="#ffffff").pack(pady=25)

form1 = tk.Frame(frame1, bg="#ffffff")
form1.pack()

def add_field(frame, label_text):
    tk.Label(frame, text=label_text, font=("Helvetica", 15), bg="#ffffff").pack(pady=4)
    entry = ttk.Entry(frame, font=("Helvetica", 13))
    entry.pack(pady=4)
    return entry

entry_bedrooms = add_field(form1, "🛏️ Bedrooms")
entry_bathrooms = add_field(form1, "🛁 Bathrooms")
entry_sqft_living = add_field(form1, "📏 Sqft Living")
entry_sqft_lot = add_field(form1, "🌿 Sqft Lot")
entry_floors = add_field(form1, "🏢 Floors")
entry_waterfront = add_field(form1, "🌊 Waterfront (0 or 1)")

ttk.Button(frame1, text="➡️ Next", command=lambda: frame2.tkraise(), style="Big.TButton").pack(pady=40)

# Page 2: More Details
set_background(frame2)
tk.Label(frame2, text="📋 A few more things!", font=("Comic Sans MS", 24, "bold"), bg="#ffffff").pack(pady=20)

form2 = tk.Frame(frame2, bg="#ffffff")
form2.pack()

entry_view = add_field(form2, "👀 View (0-4)")
entry_condition = add_field(form2, "🔧 Condition (1-5)")
entry_sqft_above = add_field(form2, "⬆️ Sqft Above")
entry_sqft_basement = add_field(form2, "⬇️ Sqft Basement")
entry_yr_built = add_field(form2, "📆 Year Built")
entry_yr_renovated = add_field(form2, "🛠️ Year Renovated (0 if never)")

tk.Label(form2, text="🏙️ City", font=("Helvetica", 14), bg="#ffffff").pack(pady=5)
city_var = tk.StringVar(value=defaults['city'])
ttk.Combobox(form2, textvariable=city_var, values=cities, state="readonly", font=("Helvetica", 12)).pack(pady=4)

tk.Label(form2, text="📮 State/Zip", font=("Helvetica", 14), bg="#ffffff").pack(pady=5)
statezip_var = tk.StringVar(value=defaults['statezip'])
ttk.Combobox(form2, textvariable=statezip_var, values=statezips, state="readonly", font=("Helvetica", 12)).pack(pady=4)

# Buttons
btns = tk.Frame(frame2, bg="#ffffff")
btns.pack(pady=20)
ttk.Button(btns, text="⬅️ Back", command=lambda: frame1.tkraise(), style="Big.TButton").grid(row=0, column=0, padx=15)
ttk.Button(btns, text="💰 Predict Price", command=predict_price, style="Big.TButton").grid(row=0, column=1, padx=15)

# Custom Button Style
style = ttk.Style()
style.configure("Big.TButton", font=("Helvetica", 14), padding=10)

# Start
frame1.tkraise()
root.mainloop()
