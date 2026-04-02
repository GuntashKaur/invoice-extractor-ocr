import re


# ================================
# REQUIRED FIELDS (FIXED STRUCTURE)
# ================================
FIELDS = [
    "billing_address", "shipping_address", "invoice_type",
    "order_number", "invoice_number", "order_date", "invoice_details",
    "invoice_date", "seller_info", "seller_pan", "seller_gst",
    "fssai_license", "billing_state_code", "shipping_state_code",
    "place_of_supply", "place_of_delivery", "reverse_charge",
    "amount_in_words", "seller_name", "seller_address",
    "total_tax", "total_amount"
]


# ================================
# INIT EMPTY STRUCTURE
# ================================
def init_data():
    return {field: "" for field in FIELDS}


# ================================
# BRAND DETECTION
# ================================
def detect_brand(text):
    t = text.lower()

    if "amazon" in t:
        return "amazon"
    elif "flipkart" in t:
        return "flipkart"
    elif "blinkit" in t:
        return "blinkit"
    elif "myntra" in t:
        return "myntra"
    elif "nykaa" in t:
        return "nykaa"

    return "unknown"


# ================================
# COMMON HELPERS
# ================================
def find_amounts(text):
    return re.findall(r'\d+\.\d{2}', text)


def clean_text(text):
    return text.replace("■", "₹")


# ================================
# AMAZON LOGIC
# ===========================

def extract_amazon(text, data):
    import re

    if isinstance(text, list):
        text = "\n".join(text)

    if not isinstance(text, str):
        text = str(text)
        

    lines = text.split("\n")

    # ---------------- BASIC ---------------- #

    m = re.search(r"Invoice Number\s*:\s*([A-Z0-9\-]+)", text)
    if m:
        data["invoice_number"] = m.group(1)

    m = re.search(r"Order Number\s*:\s*([0-9\-]+)", text)
    if m:
        data["order_number"] = m.group(1)

    m = re.search(r"Order Date\s*:\s*([0-9.\-]+)", text)
    if m:
        data["order_date"] = m.group(1)

    m = re.search(r"Invoice Date\s*:\s*([0-9.\-]+)", text)
    if m:
        data["invoice_date"] = m.group(1)

    # ---------------- GST / PAN ---------------- #

    m = re.search(r"GST Registration No:\s*([0-9A-Z]+)", text)
    if m:
        data["seller_gst"] = m.group(1)

    m = re.search(r"PAN No:\s*([A-Z0-9]+)", text)
    if m:
        data["seller_pan"] = m.group(1)

    # ---------------- SELLER ---------------- #

    for i, line in enumerate(lines):
        if "Sold By" in line:
            if i + 1 < len(lines):
                data["seller_name"] = lines[i + 1].strip()

                addr = []
                for j in range(i + 2, i + 8):
                    if j < len(lines) and "PAN" not in lines[j]:
                        addr.append(lines[j])
                data["seller_address"] = " ".join(addr)
            break

    # ---------------- ADDRESS ---------------- #

    for i, line in enumerate(lines):

        if "Billing Address" in line:
            block = []
            for j in range(i + 1, i + 8):
                if j < len(lines) and "State/UT Code" not in lines[j]:
                    block.append(lines[j])
            data["billing_address"] = " ".join(block)

        if "Shipping Address" in line:
            block = []
            for j in range(i + 1, i + 8):
                if j < len(lines) and "State/UT Code" not in lines[j]:
                    block.append(lines[j])
            data["shipping_address"] = " ".join(block)

    # ---------------- STATE CODE ---------------- #

    codes = re.findall(r"State/UT Code:\s*(\d+)", text)
    if len(codes) >= 1:
        data["billing_state_code"] = codes[0]
    if len(codes) >= 2:
        data["shipping_state_code"] = codes[1]

    # ---------------- PLACE ---------------- #

    m = re.search(r"Place of supply:\s*([A-Z ]+)", text)
    if m:
        data["place_of_supply"] = m.group(1)

    m = re.search(r"Place of delivery:\s*([A-Z ]+)", text)
    if m:
        data["place_of_delivery"] = m.group(1)

    # ---------------- TOTAL (FIXED) ---------------- #

    # ================== FINAL AMAZON TOTAL FIX ================== #

    # ================= FINAL AMAZON TOTAL + WORDS + PRODUCT ================= #


   

    # ================= SAFETY ================= #
    if not isinstance(text, str):
        text = ""

    if not isinstance(data, dict):
        data = {}

    data.setdefault("total_tax", "")
    data.setdefault("total_amount", "")
    data.setdefault("amount_in_words", "")

    lines = text.split("\n")



    # ================= TOTAL LOGIC (MAIN FIX) ================= #
    # ================= FINAL AMAZON TOTAL (PRECISE) ================= #


# Extract only the FINAL TOTAL block (between TOTAL and Amount in Words)
    # ================= FINAL AMAZON TOTAL (STRICT TABLE FIX) ================= #


    # ================= FINAL AMAZON TOTAL (PRODUCTION LEVEL FIX) ================= #


# ---------- STEP 1: GET TOTAL FROM AMOUNT IN WORDS ----------
    words_line = ""

    for i, line in enumerate(lines):
        if "amount in words" in line.lower():
            if i + 1 < len(lines):
                words_line = lines[i + 1].strip()
                data["amount_in_words"] = words_line
            break

# Convert words → number (very reliable)
    def words_to_number(text):
        try:
            from word2number import w2n
            text = text.lower().replace("only", "").strip()
            return float(w2n.word_to_num(text))
        except:
            return None

    val = words_to_number(words_line)

    if val:
        data["total_amount"] = f"{val:.2f}"


# ---------- STEP 2: GET TOTAL TAX FROM FINAL TOTAL BLOCK ----------
    m = re.search(r"TOTAL[:\s]*(.*?)Amount in Words", text, re.DOTALL | re.IGNORECASE)

    if m:
        block = m.group(0)

        if isinstance(block, list):
            block = " ".join(block)

        if not isinstance(block, str):
            block = str(block)

    nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", block)

    values = []
    for n in nums:
        try:
            v = float(n.replace(",", ""))
            if v < float(data.get("total_amount", 999999)):  # ignore total amount
                values.append(v)
        except:
            continue

    values = sorted(values, reverse=True)

    if values:
        data["total_tax"] = f"{values[0]:.2f}"

    # ================= FALLBACK (VERY IMPORTANT) ================= #
        # ================= FALLBACK ================= #

    if not data.get("total_amount"):
        for i, line in enumerate(lines):
            if "TOTAL" in line.upper():
                block = " ".join(lines[i:i+4])

            nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", block)

            if len(nums) >= 2:
                v1 = float(nums[-2].replace(",", ""))
                v2 = float(nums[-1].replace(",", ""))

                data["total_tax"] = f"{min(v1, v2):.2f}"
                data["total_amount"] = f"{max(v1, v2):.2f}"
                break

    # ================= AMOUNT IN WORDS ================= #
    for i, line in enumerate(lines):
        if "amount in words" in line.lower():
            if i + 1 < len(lines):
                data["amount_in_words"] = lines[i + 1].strip()
                break

    # ================= AUTO GENERATE ================= #
    if not data["amount_in_words"] and data["total_amount"]:
        try:
            from num2words import num2words
            val = float(data["total_amount"])
            data["amount_in_words"] = num2words(val, lang="en").title() + " Only"
        except:
            data["amount_in_words"] = str(data["total_amount"]) + " Only"

    

    # ---------------- your existing code ----------------
    # invoice number, order number, GST, etc.

    # ================= PRODUCT NAME =================
    # your existing product code


    # ===================================================
    # ✅ ADD EVERYTHING BELOW THIS LINE
    # ===================================================

    # ===== TOTAL (FROM TOTAL LINE) =====
    for line in text.split("\n"):
        if "total" in line.lower():
            nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

            if len(nums) >= 2:
                data["total_tax"] = nums[-2].replace(",", "")
                data["total_amount"] = nums[-1].replace(",", "")


    # ===== FALLBACK (Invoice Value) =====
    if not data.get("total_amount"):
        m = re.search(r"Invoice Value[:\s]*₹?\s*([\d,]+\.\d{2})", text, re.IGNORECASE)
        if m:
            data["total_amount"] = m.group(1).replace(",", "")


    # ===== REVERSE CHARGE =====
    m = re.search(r"reverse charge.*?(yes|no)", text, re.IGNORECASE)

    if m:
        data["reverse_charge"] = m.group(1).capitalize()
    else:
        data["reverse_charge"] = "None"


    # ===================================================
    # 🔴 DO NOT TOUCH THIS
    # ===================================================
    # ================= TAX AMOUNT (COLUMN BASED) =================

    tax_candidates = []

    for line in text.split("\n"):
        if "tax" in line.lower():
            nums = re.findall(r"\d{1,3}(?:,\d{3})*\.\d{2}", line)

        for n in nums:
            val = float(n.replace(",", ""))

            # ignore very large numbers (total amount)
            if val < 10000:
                tax_candidates.append(val)

# pick most reasonable tax
    if tax_candidates:
        data["total_tax"] = f"{max(tax_candidates):.2f}"

    return data
# ================================
# FLIPKART LOGIC
# ================================

def extract_flipkart(text, data):
    import re

    # ensure string
    if isinstance(text, list):
        text = "\n".join(text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # ================= HEADER EXTRACTION =================
    for line in lines:

        if "order id" in line.lower():
            data["order_number"] = line.split(":")[-1].strip()

        if "invoice no" in line.lower():
            data["invoice_number"] = line.split(":")[-1].strip()

        if "order date" in line.lower():
            data["order_date"] = line.split(":")[-1].strip()

        if "invoice date" in line.lower():
            data["invoice_date"] = line.split(":")[-1].strip()

        if "gstin" in line.lower():
            data["seller_gst"] = line.split(":")[-1].strip()

        if "pan" in line.lower():
            data["seller_pan"] = line.split(":")[-1].strip()

    # ================= BLOCK FUNCTION =================
    def extract_block(start_keyword):
        block = []
        capture = False

        for line in lines:
            if start_keyword.lower() in line.lower():
                capture = True
                continue

            if capture:
                if any(k in line.lower() for k in [
                    "sold by", "billing address", "shipping address",
                    "order id", "invoice", "gstin", "pan"
                ]):
                    break

                block.append(line)

        return " ".join(block)

    # ================= SELLER =================
    seller_block = extract_block("Sold By")
    data["seller_name"] = seller_block.split(",")[0] if seller_block else ""
    data["seller_info"] = seller_block

    # ================= ADDRESSES =================
    billing = extract_block("Billing Address")
    shipping = extract_block("Shipping")

    data["billing_address"] = billing
    data["shipping_address"] = shipping

    # ================= PIN CODE =================
    def get_pin(text_block):
        m = re.search(r"\b\d{6}\b", text_block)
        return m.group(0) if m else ""

    data["billing_state_code"] = get_pin(billing)
    data["shipping_state_code"] = get_pin(shipping)

    # ================= PLACE =================
    def get_city(text_block):
        m = re.search(r"([A-Za-z ]+)\s*-\s*\d{6}", text_block)
        return m.group(1).strip() if m else ""

    data["place_of_supply"] = get_city(billing)
    data["place_of_delivery"] = get_city(shipping)

    # ================= PRODUCT DETAILS =================
    product_text = ""
    capture = False

    for line in lines:
        if "product description" in line.lower():
            capture = True
            continue

        if capture:
            if "total qty" in line.lower():
                break
            product_text += " " + line

    data["invoice_details"] = product_text.strip()

    # ================= TOTAL =================
    for line in lines:
        if "total price" in line.lower():
            nums = re.findall(r"\d+\.\d{2}", line)
            if nums:
                data["total_amount"] = nums[-1]

    # ================= TAX =================
    tax_vals = []
    for line in lines:
        if "igst" in line.lower():
            nums = re.findall(r"\d+\.\d{2}", line)
            if len(nums) >= 2:
                tax_vals.append(float(nums[-2]))

    if tax_vals:
        data["total_tax"] = f"{sum(tax_vals):.2f}"

    # ================= AMOUNT IN WORDS =================
    if data.get("total_amount"):
        try:
            from num2words import num2words
            amt = float(data["total_amount"])
            data["amount_in_words"] = num2words(amt).title() + " Rupees Only"
        except:
            data["amount_in_words"] = ""

    # ================= REVERSE CHARGE =================
    data["reverse_charge"] = "None"

    return data

def extract_blinkit(text, data):
    import re

    raw_text = text
    text = re.sub(r"\s+", " ", text.lower())

    # -------- INVOICE TYPE --------
    data["invoice_type"] = "pdf"

    # -------- INVOICE NUMBER --------
    m = re.search(r"invoice\s*number\s*[:\-]?\s*([a-z0-9]+)", text)
    if m:
        data["invoice_number"] = m.group(1).upper()

    # -------- ORDER NUMBER --------
    m = re.search(r"order\s*id\s*[:\-]?\s*(\d+)", text)
    if m:
        data["order_number"] = m.group(1)

    # -------- INVOICE DATE --------
    m = re.search(r"\d{2}-[a-z]{3}-\d{4}", text)
    if m:
        data["invoice_date"] = m.group(0)

    # -------- PLACE OF SUPPLY --------
    m = re.search(r"place\s*of\s*supply\s*[:\-]?\s*([a-z ]+)", text)
    if m:
        data["place_of_supply"] = m.group(1).strip().title()

    # ===============================
    # 🔹 SELLER ADDRESS (TOP BLOCK)
    # ===============================
    seller_block = re.search(
        r"sold by\s*/?\s*seller\s*(.*?)\s*gstin",
        text,
        re.DOTALL
    )
    if seller_block:
        seller_addr = seller_block.group(1).strip()
        data["seller_address"] = seller_addr
        data["seller_name"] = "Blinkit"

        # Extract seller PIN (state code)
        pin = re.search(r"\b\d{6}\b", seller_addr)
        if pin:
            data["billing_state_code"] = pin.group(0)

    # ===============================
    # 🔹 BILLING + SHIPPING ADDRESS
    # ===============================
    invoice_block = re.search(
        r"invoice to.*?address\s*:\s*(.*?)\s*pin\s*code",
        text,
        re.DOTALL
    )
    if invoice_block:
        addr = invoice_block.group(1).strip()
        data["billing_address"] = addr
        data["shipping_address"] = addr

    # PIN CODE (Customer)
    pin = re.search(r"pin\s*code\s*[:\-]?\s*(\d{6})", text)
    if pin:
        data["shipping_state_code"] = pin.group(1)

    # PLACE OF DELIVERY
    state = re.search(r"state\s*[:\-]?\s*([a-z ]+)", text)
    if state:
        data["place_of_delivery"] = state.group(1).strip().title()

    # ===============================
    # 🔹 GST + PAN
    # ===============================
    gst = re.search(r"\b[0-9]{2}[a-z]{5}[0-9]{4}[a-z][0-9a-z]{3}\b", text)
    if gst:
        data["seller_gst"] = gst.group(0).upper()

    pan = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", raw_text)
    if pan:
        data["seller_pan"] = pan.group(0)

    # ===============================
    # 🔹 TOTAL AMOUNT
    # ===============================
    nums = re.findall(r"\d+\.\d{2}", text)
    if nums:
        data["total_amount"] = nums[-1]

    # ===============================
    # 🔹 TOTAL TAX (CGST + SGST LAST ROW)
    # ===============================
    try:
        cgst_vals = re.findall(r"cgst.*?(\d+\.\d{2})", text)
        sgst_vals = re.findall(r"sgst.*?(\d+\.\d{2})", text)

        if cgst_vals and sgst_vals:
            total_tax = float(cgst_vals[-1]) + float(sgst_vals[-1])
            data["total_tax"] = f"{total_tax:.2f}"
    except:
        pass

    # ===============================
    # 🔹 AMOUNT IN WORDS
    # ===============================
    words = re.search(
        r"amount\s*in\s*words\s*:\s*(.*?)\s*blink",
        text,
        re.DOTALL
    )
    if words:
        data["amount_in_words"] = words.group(1).strip().title()

    # ===============================
    # 🔹 REVERSE CHARGE
    # ===============================
    if "reverse charge - no" in text:
        data["reverse_charge"] = "No"
    elif "reverse charge - yes" in text:
        data["reverse_charge"] = "Yes"

    return data
def extract_zomato(text, data):
    import re

    raw_text = text
    text = re.sub(r"\s+", " ", text.lower())

    # ===============================
    # ✅ INVOICE TYPE
    # ===============================
    data["invoice_type"] = "pdf"

    # ===============================
    # ✅ INVOICE NUMBER
    # ===============================
    m = re.search(r"invoice\s*no\.?\s*[:\-]?\s*([a-z0-9]+)", text)
    if m:
        data["invoice_number"] = m.group(1).upper()

    # ===============================
    # ✅ ORDER NUMBER
    # ===============================
    m = re.search(r"order\s*id\s*[:\-]?\s*(\d+)", text)
    if m:
        data["order_number"] = m.group(1)

    # ===============================
    # ✅ INVOICE DATE
    # ===============================
    m = re.search(r"\d{2}/\d{2}/\d{4}", text)
    if m:
        data["invoice_date"] = m.group(0)

    # ===============================
    # ✅ SELLER INFO (RESTAURANT)
    # ===============================
    m = re.search(r"restaurant name\s*:\s*(.*?)\s*restaurant address", text)
    if m:
        data["seller_name"] = m.group(1).strip().title()

    m = re.search(r"restaurant address\s*:\s*(.*?)\s*restaurant gstin", text)
    if m:
        data["seller_address"] = m.group(1).strip()

    # GST
    gst = re.search(r"\b[0-9]{2}[a-z]{5}[0-9]{4}[a-z][0-9a-z]{3}\b", text)
    if gst:
        data["seller_gst"] = gst.group(0).upper()

    # ===============================
    # ✅ CUSTOMER ADDRESS (IMPORTANT)
    # ===============================
    m = re.search(r"delivery address\s*:\s*(.*?)\s*state name", text)
    if m:
        addr = m.group(1).strip()
        data["billing_address"] = addr
        data["shipping_address"] = addr

        # PIN CODE
        pin = re.search(r"\b\d{6}\b", addr)
        if pin:
            data["shipping_state_code"] = pin.group(0)
            data["billing_state_code"] = pin.group(0)

    # ===============================
    # ✅ PLACE OF SUPPLY
    # ===============================
    m = re.search(r"place of supply\s*[:\-]?\s*([a-z]+)", text)
    if m:
        data["place_of_supply"] = m.group(1).title()
        data["place_of_delivery"] = m.group(1).title()

    # ===============================
    # ✅ TOTAL AMOUNT (IMPORTANT FIX)
    # ===============================
    m = re.search(r"total value.*?(\d+\.\d{2,3})", text)
    if m:
        data["total_amount"] = m.group(1)

    # ===============================
    # ✅ TOTAL TAX (CGST + SGST)
    # ===============================
    try:
        cgst_vals = re.findall(r"cgst.*?(\d+\.\d+)", text)
        sgst_vals = re.findall(r"sgst.*?(\d+\.\d+)", text)

        if cgst_vals and sgst_vals:
            total_tax = float(cgst_vals[-1]) + float(sgst_vals[-1])
            data["total_tax"] = f"{total_tax:.2f}"
    except:
        pass

    # ===============================
    # ✅ AMOUNT IN WORDS
    # ===============================
    m = re.search(r"amount\s*\(in words\)\s*:\s*(.*?)\s*amount of", text)
    if m:
        data["amount_in_words"] = m.group(1).strip().title()

    # ===============================
    # ✅ REVERSE CHARGE
    # ===============================
    if "reverse charge : no" in text or "reverse charge - no" in text:
        data["reverse_charge"] = "No"
    elif "reverse charge : yes" in text:
        data["reverse_charge"] = "Yes"

    # ===============================
    # ✅ INVOICE DETAILS (ITEMS)
    # ===============================
    items = re.findall(r"\d+\s*x\s*[a-zA-Z ].*?\d+\.\d+", raw_text)
    if items:
        data["invoice_details"] = " | ".join(items[:5])

    return data

# ================================
# UNIVERSAL FALLBACK
# ================================
def extract_universal(text, data):
    amounts = find_amounts(text)

    if amounts:
        data["total_amount"] = max(amounts)

    m = re.search(r'(\d{2}[./-]\d{2}[./-]\d{4})', text)
    if m:
        data["invoice_date"] = m.group(1)

    return data


# ================================
# MAIN FUNCTION
# ================================
def extract_fields(raw_text):
    text = clean_text(raw_text)

    data = init_data()

    brand = detect_brand(text)
    data["seller_name"] = brand.upper()

    if brand == "amazon":
        data = extract_amazon(text, data)

    elif brand == "flipkart":
        data = extract_flipkart(text, data)

    elif brand == "blinkit":
        data = extract_blinkit(text,data)

    elif brand == "zomato":
        data = extract_zomato(text, data)

    else:
        data = extract_universal(text, data)

    return data