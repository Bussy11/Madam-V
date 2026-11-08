import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from urllib.parse import quote
from io import BytesIO
import base64
import html
import mimetypes

from PIL import Image  # Pillow is installed together with Streamlit

# =====================================================
# MAMA-V-RAW FOOD COMPLEX
# PROFESSIONAL BUSINESS WEBSITE
# =====================================================

st.set_page_config(
    page_title="MAMA-V-RAW FOOD COMPLEX",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# BUSINESS SETTINGS
# =====================================================

BUSINESS_NAME = "MAMA-V-RAW FOOD COMPLEX"
TAGLINE = "Quality & Farm-Fresh Raw Foodstuffs"
CEO_NAME = "Adeyemi Mary Owoeye"

# Replace with the actual WhatsApp number (country code, no + or spaces)
WHATSAPP_NUMBER = "2348000000000"
PLACEHOLDER_NUMBER = "2348000000000"

# Better: put ADMIN_PASSWORD in .streamlit/secrets.toml.
# The fallback below is only used if no secret is set. CHANGE IT.
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except Exception:
    ADMIN_PASSWORD = "ChangeMyAdminPassword"

BASE_DIR = Path(__file__).parent
ASSET_FOLDER = BASE_DIR / "assets"
ASSET_FOLDER.mkdir(exist_ok=True)


# =====================================================
# IMAGE FILENAMES (these files must exist in /assets)
# =====================================================

IMAGES = {
    "Business Logo": "logo.jpg",
    "CEO Portrait": "ceo.jpg",
    "CEO Inspection": "ceo2.jpg",
    "CEO Customer Relations": "ceo3.jpg",
    "Beans": "bean.jpg",
    "Rice": "rice.jpg",
    "Semovita": "semovita.jpg",
    "Tin Tomatoes": "tomato.jpg",
}


# =====================================================
# PRODUCT DATABASE
# =====================================================

PRODUCTS = [
    {"name": "Honey/Oloyin Beans", "price": 45000, "unit": "Bag", "image": "bean.jpg"},
    {"name": "50kg Premium Rice", "price": 65000, "unit": "Bag", "image": "rice.jpg"},
    {"name": "Semovita (10kg)", "price": 12500, "unit": "Pack", "image": "semovita.jpg"},
    {"name": "Tin Tomatoes", "price": 18000, "unit": "Carton", "image": "tomato.jpg"},
]


# =====================================================
# SESSION MANAGEMENT
# =====================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

if "flash" not in st.session_state:
    st.session_state.flash = None

# Show a message that was set just before a rerun
if st.session_state.flash:
    st.toast(st.session_state.flash)
    st.session_state.flash = None


# =====================================================
# CUSTOM WEBSITE DESIGN
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Poppins, sans-serif;
}

.stApp {
    background: #f4f7f3;
}

.block-container {
    max-width: 1250px;
    padding-top: 1rem;
}

.brand {
    background: white;
    padding: 25px;
    text-align: center;
    border-radius: 15px;
    border-top: 5px solid #2e7d32;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
}

.brand img {
    max-height: 140px;
    max-width: 100%;
    margin-bottom: 10px;
}

.brand h1 {
    color: #1b5e20;
    font-size: 30px;
    font-weight: 800;
}

.section-title {
    text-align: center;
    color: #1b5e20;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 25px;
}

/* Cards built with st.container(border=True) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.07);
}

.price {
    color: #2e7d32;
    font-size: 21px;
    font-weight: 800;
}

.footer {
    text-align: center;
    padding: 30px;
    color: #777;
}

div.stButton > button {
    background: #2e7d32;
    color: white;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# IMAGE HELPERS
# =====================================================

def image_path(filename):
    return ASSET_FOLDER / filename


def display_image(filename, height=200):
    path = image_path(filename)

    if path.is_file():
        st.image(str(path), use_container_width=True)
    else:
        st.markdown(f"""
        <div style="
            height:{height}px;
            background:#e8f5e9;
            border:1px dashed #2e7d32;
            border-radius:12px;
            display:flex;
            align-items:center;
            justify-content:center;
            text-align:center;
            color:#1b5e20;
        ">
            <div>
                <h2>🖼️</h2>
                <b>Image unavailable</b><br>
                {html.escape(filename)}
            </div>
        </div>
        """, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _encode_image(path_str, modified_time):
    """Cached base64 encoding. modified_time makes the cache refresh
    automatically when an image is replaced."""
    path = Path(path_str)
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{encoded}"


def image_data(filename):
    path = image_path(filename)

    if not path.is_file():
        return None

    return _encode_image(str(path), path.stat().st_mtime)


def save_as_jpeg(uploaded_file, destination):
    """Convert any uploaded image (png/webp/jpg) to a real JPEG so the
    content always matches the .jpg filename."""
    img = Image.open(BytesIO(uploaded_file.getvalue()))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")
    img.save(destination, format="JPEG", quality=90)


# =====================================================
# CEO AUTOMATIC SLIDESHOW
# =====================================================

def ceo_slideshow():
    slide_details = [
        ("ceo.jpg", CEO_NAME, "CEO & Founder"),
        ("ceo2.jpg", "Quality Assurance", "Inspecting quality food products"),
        ("ceo3.jpg", "Customer Relations", "Serving customers with excellence"),
    ]

    slides = []

    for filename, title, subtitle in slide_details:
        img = image_data(filename)
        if img:
            slides.append((img, title, subtitle))

    if not slides:
        st.info("Upload CEO pictures using the Admin Dashboard.")
        return

    slide_html = ""

    for i, (img, title, subtitle) in enumerate(slides):
        active = "active" if i == 0 else ""
        slide_html += f"""
        <div class="slide {active}">
            <img src="{img}">
            <div class="caption">
                <h3>{html.escape(title)}</h3>
                <p>{html.escape(subtitle)}</p>
            </div>
        </div>
        """

    page = f"""
    <html>
    <head>
    <style>

    body {{
        margin:0;
        font-family:Arial;
    }}

    .carousel {{
        position:relative;
        height:400px;
        overflow:hidden;
        border-radius:15px;
    }}

    .slide {{
        display:none;
        position:absolute;
        width:100%;
        height:100%;
    }}

    .slide.active {{
        display:block;
    }}

    .slide img {{
        width:100%;
        height:100%;
        object-fit:cover;
    }}

    .caption {{
        position:absolute;
        bottom:0;
        width:100%;
        background:linear-gradient(transparent,black);
        color:white;
        text-align:center;
        padding:30px 10px 15px;
        box-sizing:border-box;
    }}

    </style>
    </head>

    <body>

    <div class="carousel">
        {slide_html}
    </div>

    <script>

    let slides = document.querySelectorAll(".slide");
    let current = 0;

    function nextSlide() {{
        slides[current].classList.remove("active");
        current = (current + 1) % slides.length;
        slides[current].classList.add("active");
    }}

    if (slides.length > 1) {{
        setInterval(nextSlide, 20000);
    }}

    </script>

    </body>
    </html>
    """

    components.html(page, height=420)


# =====================================================
# WEBSITE HEADER
# (built in ONE markdown block so the HTML is not broken)
# =====================================================

logo = image_data("logo.jpg")
logo_html = f'<img src="{logo}" alt="Logo"><br>' if logo else ""

st.markdown(f"""
<div class="brand">
    {logo_html}
    <h1>{html.escape(BUSINESS_NAME)}</h1>
    <p>{html.escape(TAGLINE)}</p>
    <b>Welcome! Quality foodstuffs at affordable prices.</b>
</div>
""", unsafe_allow_html=True)


# =====================================================
# LEADERSHIP SECTION
# =====================================================

st.markdown(
    '<h2 class="section-title">LEADERSHIP & VISION</h2>',
    unsafe_allow_html=True
)

ceo_slideshow()


# =====================================================
# PRODUCT CATALOGUE
# =====================================================

st.markdown(
    '<h2 class="section-title">OUR PREMIUM PRODUCTS</h2>',
    unsafe_allow_html=True
)

columns = st.columns(len(PRODUCTS))

for index, product in enumerate(PRODUCTS):

    with columns[index]:

        with st.container(border=True):

            display_image(product["image"])

            st.subheader(product["name"])

            st.markdown(
                f'<div class="price">₦{product["price"]:,}</div>',
                unsafe_allow_html=True
            )

            st.caption(f'Price per {product["unit"]}')

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=100,
                value=1,
                key=f"quantity_{index}"
            )

            if st.button("ADD TO ORDER", key=f"add_{index}"):

                product_name = product["name"]

                if product_name in st.session_state.cart:
                    st.session_state.cart[product_name]["quantity"] += quantity
                else:
                    st.session_state.cart[product_name] = {
                        "price": product["price"],
                        "quantity": quantity
                    }

                # No st.rerun() here: the cart below is drawn later in
                # this same run, so it already shows the new item.
                st.success("Product added to cart.")


# =====================================================
# SHOPPING CART
# =====================================================

st.markdown(
    '<h2 class="section-title">YOUR SHOPPING CART</h2>',
    unsafe_allow_html=True
)

with st.container(border=True):

    total = 0

    if st.session_state.cart:

        for item_name, item in list(st.session_state.cart.items()):

            amount = item["price"] * item["quantity"]
            total += amount

            col1, col2, col3 = st.columns([4, 2, 1])

            col1.write(item_name)
            col2.write(f'{item["quantity"]} unit(s) - ₦{amount:,}')

            if col3.button("❌", key=f"remove_{item_name}"):
                del st.session_state.cart[item_name]
                st.rerun()

        st.divider()

        st.markdown(f"## TOTAL: :green[₦{total:,}]")

    else:
        st.info("Your shopping cart is empty.")

    if st.button("CLEAR SHOPPING CART"):
        st.session_state.cart = {}
        st.rerun()


# =====================================================
# CUSTOMER ORDER FORM
# =====================================================

st.markdown(
    '<h2 class="section-title">CUSTOMER DELIVERY INFORMATION</h2>',
    unsafe_allow_html=True
)

with st.container(border=True):

    with st.form("customer_form"):

        customer_name = st.text_input("Full Name *")
        phone = st.text_input("Phone Number *")
        address = st.text_area("Delivery Address *")
        notes = st.text_area("Additional Instructions (Optional)")

        submit = st.form_submit_button("PREPARE WHATSAPP ORDER")

    if submit:

        if not st.session_state.cart:
            st.error("Please add products to your cart.")

        elif not customer_name.strip() or not phone.strip() or not address.strip():
            st.error("Please complete all required information.")

        elif WHATSAPP_NUMBER == PLACEHOLDER_NUMBER:
            st.error("Please enter the actual business WhatsApp number in the code.")

        else:

            order_lines = []
            final_total = 0

            for product_name, item in st.session_state.cart.items():
                amount = item["price"] * item["quantity"]
                final_total += amount
                order_lines.append(
                    f"- {product_name}: {item['quantity']} unit(s) - ₦{amount:,}"
                )

            order_details = "\n".join(order_lines)
            extra = notes.strip() if notes.strip() else "None"

            message = (
                f"NEW ORDER - {BUSINESS_NAME}\n\n"
                f"CUSTOMER DETAILS\n"
                f"Name: {customer_name.strip()}\n"
                f"Phone: {phone.strip()}\n"
                f"Address: {address.strip()}\n\n"
                f"ORDER DETAILS\n"
                f"{order_details}\n\n"
                f"TOTAL AMOUNT: ₦{final_total:,}\n\n"
                f"Additional Instructions: {extra}\n\n"
                f"Please confirm availability and delivery arrangements."
            )

            whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"

            st.success("Your order is ready.")

            st.link_button(
                "🟢 OPEN WHATSAPP TO SEND ORDER",
                whatsapp_url,
                use_container_width=True
            )


# =====================================================
# ADMINISTRATOR DASHBOARD
# UPLOAD OR CHANGE BUSINESS IMAGES
# =====================================================

st.markdown(
    '<h2 class="section-title">ADMINISTRATOR DASHBOARD</h2>',
    unsafe_allow_html=True
)

with st.expander("🔐 ADMIN LOGIN AND IMAGE MANAGEMENT"):

    if not st.session_state.admin_login:

        password = st.text_input("Administrator Password", type="password")

        if st.button("LOGIN AS ADMIN"):

            if password == ADMIN_PASSWORD:
                st.session_state.admin_login = True
                st.session_state.flash = "Administrator access granted."
                st.rerun()
            else:
                st.error("Incorrect administrator password.")

    else:

        st.success("Welcome to the administrator dashboard.")

        st.subheader("Upload or Replace Business Images")

        selected = st.selectbox("Select image category", list(IMAGES.keys()))

        target_file = IMAGES[selected]

        uploaded = st.file_uploader(
            f"Upload {selected}",
            type=["jpg", "jpeg", "png", "webp"]
        )

        if uploaded:

            st.image(uploaded, caption="Image preview", use_container_width=True)

            if st.button("SAVE IMAGE"):

                try:
                    save_as_jpeg(uploaded, ASSET_FOLDER / target_file)
                    st.session_state.flash = f"Image saved as {target_file}"
                    st.rerun()
                except Exception as error:
                    st.error(f"Could not save the image: {error}")

        st.divider()

        st.subheader("Image Upload Status")

        for label, file_name in IMAGES.items():

            if (ASSET_FOLDER / file_name).exists():
                st.success(f"{label}: {file_name} - Uploaded")
            else:
                st.warning(f"{label}: {file_name} - Missing")

        if st.button("LOGOUT ADMIN"):
            st.session_state.admin_login = False
            st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.markdown(f"""
<div class="footer">
    <h3>{html.escape(BUSINESS_NAME)}</h3>
    <p>{html.escape(TAGLINE)}</p>
    <p>© 2026 All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
