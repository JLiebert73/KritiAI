from PIL import Image, ImageDraw, ImageFont
import os

def generate_pmfby_form(filename, farmer_name, aadhaar, khasra, crop, hazard, date, notes, is_valid=True):
    width, height = 900, 1100
    image = Image.new('RGB', (width, height), color="white")
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 22)
        title_font = ImageFont.truetype("arial.ttf", 32)
        bold_font = ImageFont.truetype("arialbd.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        title_font = font
        bold_font = font

    # Header
    draw.text((150, 40), "PRADHAN MANTRI FASAL BIMA YOJANA (PMFBY)", fill="black", font=title_font)
    draw.text((250, 80), "CROP LOSS INTIMATION & CLAIM FORM", fill="black", font=bold_font)
    draw.line((50, 120, 850, 120), fill="black", width=3)

    # Farmer Details
    y = 150
    spacing = 50
    
    draw.text((50, y), "PART A: FARMER DETAILS", fill="black", font=bold_font)
    y += spacing
    draw.text((50, y), f"1. Farmer Name: {farmer_name}", fill="black", font=font)
    draw.text((450, y), f"2. Aadhaar No: {aadhaar}", fill="black", font=font)
    y += spacing
    draw.text((50, y), "3. Bank Account: XXXXXXXXXX4321", fill="black", font=font)
    draw.text((450, y), "4. State/District: Assam / Kamrup", fill="black", font=font)
    
    y += spacing + 20
    draw.line([50, y, 850, y], fill="gray", width=1)
    y += 30

    # Crop Details
    draw.text((50, y), "PART B: CROP & LAND DETAILS", fill="black", font=bold_font)
    y += spacing
    draw.text((50, y), f"5. Crop Name: {crop}", fill="black", font=font)
    draw.text((450, y), f"6. Sowing Date: {date.split('-')[1]}-{date.split('-')[2]}", fill="black", font=font) # rough
    y += spacing
    draw.text((50, y), f"7. Khasra / Survey No: {khasra}", fill="black", font=font)
    draw.text((450, y), "8. Insured Area (Hectare): 2.5", fill="black", font=font)

    y += spacing + 20
    draw.line([50, y, 850, y], fill="gray", width=1)
    y += 30

    # Loss Details
    draw.text((50, y), "PART C: LOSS INTIMATION", fill="black", font=bold_font)
    y += spacing
    draw.text((50, y), f"9. Cause of Loss: {hazard}", fill="black", font=font)
    y += spacing
    draw.text((50, y), f"10. Date of Occurrence: {date}", fill="black", font=font)
    y += spacing
    draw.text((50, y), "11. Estimated Loss (%): 80%", fill="black", font=font)

    y += spacing + 40
    
    # Official Section
    draw.rectangle((40, y, 860, y + 250), outline="black", width=2)
    draw.text((50, y + 10), "FOR OFFICIAL USE ONLY (Surveyor/Inspector Remarks)", fill="black", font=bold_font)
    
    # Simulate handwritten notes
    draw.text((70, y + 60), f"Handwritten Remarks: {notes}", fill="darkblue", font=font)
    
    if is_valid:
        draw.ellipse((650, y + 80, 800, y + 230), outline="green", width=4)
        draw.text((680, y + 140), "VERIFIED\nPMFBY", fill="green", font=bold_font)
    else:
        draw.ellipse((650, y + 80, 800, y + 230), outline="red", width=4)
        draw.text((670, y + 140), "REJECTED\nDISCREPANCY", fill="red", font=bold_font)

    # Coordinates added manually in margin
    draw.text((50, height - 50), f"Geo-Tag: Lat 26.25, Lon 91.25", fill="gray", font=font)

    image.save(filename)
    print(f"Generated {filename}")

if __name__ == "__main__":
    os.makedirs("mock_data", exist_ok=True)
    
    generate_pmfby_form(
        "mock_data/pmfby_flood_valid.jpg",
        "Arun Sharma", "XXXX-XXXX-1234", "KH-405-A", "Paddy (Rice)", "Inundation / Flooding", "18-July-2025",
        "Field inspection confirms heavy waterlogging. Crop destroyed.", is_valid=True
    )
    
    generate_pmfby_form(
        "mock_data/pmfby_drought_fake.jpg",
        "Bikash Das", "XXXX-XXXX-9876", "KH-112-B", "Jute", "Severe Drought", "10-July-2025",
        "Claiming drought but soil is wet. Suspected fraud.", is_valid=False
    )
