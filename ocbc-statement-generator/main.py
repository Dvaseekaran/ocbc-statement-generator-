from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime, timedelta
import weasyprint
import os
import logging
from pathlib import Path
from models import Base, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress verbose font logging
logging.getLogger('fontTools').setLevel(logging.WARNING)
logging.getLogger('weasyprint').setLevel(logging.WARNING)

app = FastAPI()

# Configure templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create directories if they don't exist
os.makedirs("static/images", exist_ok=True)  # Updated to create images subdirectory
os.makedirs("generated_statements", exist_ok=True)

# Update logo path with absolute path
LOGO_PATH = os.path.join(os.path.dirname(__file__), "static", "images", "ocbc_logo.png")

# Remove or comment out the old logo path definitions
# LOGO_PATH = "static/ocbc_logo.png"  # Remove this line
# static_path = os.path.join(os.path.dirname(__file__), "static")  # Remove this line
# LOGO_PATH = os.path.join(static_path, "images", "ocbc_logo.png")  # Remove this line

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        language_display = {
            "en": "English",
            "zh": "中文",
            "ta": "தமிழ்",
            "ms": "Bahasa Melayu"
        }
        LOGO_URL = os.getenv("LOGO_URL")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "logo_url": LOGO_URL,
            "languages": list(LANGUAGES.keys()),
            "language_display": language_display
        })
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        raise

# Create templates directory for HTML templates
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
print("LOGO_URL =", os.getenv("LOGO_URL"))


# Create HTML template for the statement
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4; margin: 2cm; }
        body { font-family: Arial, "Microsoft YaHei", "Noto Sans SC", "Noto Sans Tamil", sans-serif; color: #222; }
        .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
        .logo { width: 120px; }
        .statement-info { text-align: right; font-size: 14px; }
        .customer-details { margin-bottom: 10px; }
        .account-summary, .payment-summary, .rewards-summary, .campaign-box { border: 1px solid #dc1f27; border-radius: 6px; margin: 20px 0; padding: 18px 20px; background: #fff; }
        .account-summary-title, .payment-summary-title, .transaction-title, .rewards-title { color: #dc1f27; font-weight: bold; font-size: 16px; margin-bottom: 10px; }
        .summary-grid { display: flex; gap: 20px; }
        .summary-col { flex: 1; }
        .summary-label { color: #888; font-size: 13px; }
        .summary-value { font-size: 18px; font-weight: bold; margin-bottom: 8px; }
        .summary-highlight { color: #dc1f27; font-weight: bold; }
        .transactions-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        .transactions-table th, .transactions-table td { padding: 8px 10px; border-bottom: 1px solid #eee; font-size: 13px; }
        .transactions-table th { background: #f8f8f8; color: #dc1f27; text-align: left; }
        .transactions-table td.amount { text-align: left; } /* <-- Change from right to left */
        .campaign-box { border: 2px solid #dc1f27; background: #fff6f6; color: #dc1f27; text-align: center; font-size: 15px; margin-bottom: 20px; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <img src="{{ logo_url }}" class="logo">
        <div class="statement-info">
            <div><b>{{ statement_title }}</b></div>
            <div>{{ statement_period_label }}: {{ statement_period }}</div>
            <div>Statement Date: {{ payment_due_date }}</div>
        </div>
    </div>

    <div class="customer-details">
        <b>{{ customer_name }}</b><br>
        {{ address }}<br>
        {{ card_number_label }}: {{ card_number }}
    </div>

    <div class="campaign-box">
        <b>Credit Card eStatement Campaign 2025</b><br>
        Switch to eStatements now and stand a chance to win exciting prizes!<br>
        Go paperless to reduce your carbon footprint and enjoy hassle-free banking.
    </div>

    <div class="account-summary">
        <div class="account-summary-title">{{ account_summary_label }}</div>
        <div class="summary-grid">
            <div class="summary-col">
                <div class="summary-label">{{ credit_limit_label }}</div>
                <div class="summary-value">S$ {{ credit_limit }}</div>
                <div class="summary-label">{{ previous_balance_label }}</div>
                <div class="summary-value">S$ {{ previous_balance }}</div>
                <div class="summary-label">{{ new_balance_label }}</div>
                <div class="summary-value summary-highlight">S$ {{ new_balance }}</div>
            </div>
            <div class="summary-col">
                <div class="summary-label">{{ minimum_payment_label }}</div>
                <div class="summary-value summary-highlight">S$ {{ minimum_payment }}</div>
                <div class="summary-label">{{ payment_due_date_label }}</div>
                <div class="summary-value">{{ payment_due_date }}</div>
                <div class="summary-label">{{ points_balance_label }}</div>
                <div class="summary-value">{{ points_balance }}</div>
            </div>
        </div>
    </div>

    <div class="payment-summary">
        <div class="payment-summary-title">PAYMENT & TRANSACTIONS SUMMARY</div>
        <table class="transactions-table">
            <tr><td class="summary-label">Previous Balance</td><td class="amount">S$ {{ previous_balance }}</td></tr>
            <tr><td class="summary-label">Payments</td><td class="amount">- S$ 0.00</td></tr>
            <tr><td class="summary-label">Purchases</td><td class="amount">+ S$ {{ new_balance }}</td></tr>
            <tr><td class="summary-label">Cashback Earned</td><td class="amount">+ S$ {{ cashback_earned }}</td></tr>
            <tr><td class="summary-label">Interest Charges</td><td class="amount">+ S$ 0.00</td></tr>
            <tr><td class="summary-label"><b>Current Balance</b></td><td class="amount"><b>S$ {{ new_balance }}</b></td></tr>
        </table>
    </div>

    <div class="transaction-title">TRANSACTION DETAILS</div>
    <table class="transactions-table">
        <thead>
            <tr>
                <th>{{ date_label }}</th>
                <th>{{ description_label }}</th>
                <th>{{ category_label }}</th>
                <th>{{ amount_label }}</th>
                <th>{{ points_label }}</th>
            </tr>
        </thead>
        <tbody>
            {% for tx in transactions %}
            <tr>
                <td>{{ tx.date.strftime('%d/%m/%Y') }}</td>
                <td>{{ tx.merchant }}</td>
                <td>{{ tx.category }}</td>
                <td class="amount">{{ "%.2f"|format(tx.amount) }}</td> <!-- Remove $ from here -->
                <td class="amount">{{ tx.points }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="rewards-summary">
        <div class="rewards-title">REWARDS AND BENEFITS</div>
        <div class="summary-label">{{ points_earned_label }}: {{ points_earned }}</div>
        <div class="summary-label">{{ points_balance_label }}: {{ points_balance }}</div>
        <div class="summary-label">{{ cashback_earned_label }}: S$ {{ cashback_earned }}</div>
        <div class="summary-label">{{ ytd_cashback_label }}: S$ {{ ytd_cashback }}</div>
    </div>

    <div class="footer">
        <p>{{ footer_label }}</p>
        <p>{{ signature_note_label }}</p>
    </div>
</body>
</html>
"""

# Save the template
with open(templates_dir / "statement_template.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# Update the generate_statement function
# Add more languages to the LANGUAGES dictionary
# Move LANGUAGES dictionary before the read_root function
LANGUAGES = {
    "en": {
        "title": "Credit Card Statement",
        "account_summary": "Account Summary",
        "credit_limit": "Credit Limit",
        "previous_balance": "Previous Balance",
        "new_balance": "New Balance",
        "minimum_payment": "Minimum Payment",
        "payment_due_date": "Payment Due Date",
        "points": "Points",
        "points_balance": "Points Balance",
        "points_earned": "Points Earned",
        "miles": "Miles",
        "miles_balance": "Miles Balance",
        "miles_earned": "Miles Earned",
        "cashback": "Cashback",
        "cashback_earned": "Cashback Earned",
        "ytd_cashback": "YTD Cashback",
        "date": "Date",
        "description": "Description",
        "category": "Category",
        "amount": "Amount (SGD)",
        "card_number": "Card Number",
        "statement_period": "Statement Period",
        "footer": "For any inquiries, please contact OCBC Customer Service at 1800 363 3333",
        "signature_note": "This is a computer-generated statement and requires no signature"
    },
    "zh": {
        "title": "信用卡对账单",
        "account_summary": "账户摘要",
        "credit_limit": "信用额度",
        "previous_balance": "上期余额",
        "new_balance": "本期余额",
        "minimum_payment": "最低付款额",
        "payment_due_date": "付款截止日期",
        "points": "积分",
        "points_balance": "积分余额",
        "points_earned": "已赚取积分",
        "miles": "里程",
        "miles_balance": "里程余额",
        "miles_earned": "已赚取里程",
        "cashback": "现金回馈",
        "cashback_earned": "已赚取现金回馈",
        "ytd_cashback": "年度现金回馈",
        "date": "日期",
        "description": "说明",
        "category": "类别",
        "amount": "金额 (SGD)",
        "card_number": "卡号",
        "statement_period": "账单周期",
        "footer": "如有任何询问，请致电 1800 363 3333 联系华侨银行客户服务",
        "signature_note": "这是计算机生成的声明，无需签名"
    },
    "ta": {
        "title": "கடன் அட்டை அருக்கம்",
        "account_summary": "கணக்கு சுருக்கம்",
        "credit_limit": "கடன் வரம்பு",
        "previous_balance": "முந்தைய இருப்பு",
        "new_balance": "புதிய இருப்பு",
        "minimum_payment": "குறைந்தபட்ச கட்டணம்",
        "payment_due_date": "கட்டணக் கடைசி தேதி",
        "points": "புள்ளிகள்",
        "points_balance": "புள்ளிகள் இருப்பு",
        "points_earned": "சேகரிக்கப்பட்ட புள்ளிகள்",
        "miles": "மைல்கள்",
        "miles_balance": "மைல்கள் இருப்பு",
        "miles_earned": "சேகரிக்கப்பட்ட மைல்கள்",
        "cashback": "பணத் திரும்பப்பெறுதல்",
        "cashback_earned": "சேகரிக்கப்பட்ட பணத் திரும்பப்பெறுதல்",
        "ytd_cashback": "வருடாந்திர பணத் திரும்பப்பெறுதல்",
        "date": "தேதி",
        "description": "விவரம்",
        "category": "வகை",
        "amount": "தொகை (SGD)",
        "card_number": "அட்டை எண்",
        "statement_period": "அறிக்கை காலம்",
        "footer": "எந்த விசாரணைகளுக்கும், OCBC வாடிக்கையாளர் சேவையை 1800 363 3333 இல் தொடர்பு கொள்ளவும்",
        "signature_note": "இது கணினி மூலம் உருவாக்கப்பட்ட அறிக்கை, கையொப்பம் தேவையில்லை"
    },
    "ms": {
        "title": "Penyata Kad Kredit",
        "account_summary": "Ringkasan Akaun",
        "credit_limit": "Had Kredit",
        "previous_balance": "Baki Sebelumnya",
        "new_balance": "Baki Baharu",
        "minimum_payment": "Bayaran Minimum",
        "payment_due_date": "Tarikh Akhir Bayaran",
        "points": "Mata Ganjaran",
        "points_balance": "Baki Mata Ganjaran",
        "points_earned": "Mata Diperoleh",
        "miles": "Batu",
        "miles_balance": "Baki Batu",
        "miles_earned": "Batu Diperoleh",
        "cashback": "Pulangan Tunai",
        "cashback_earned": "Pulangan Tunai Diperoleh",
        "ytd_cashback": "Pulangan Tunai Tahunan",
        "date": "Tarikh",
        "description": "Perihal",
        "category": "Kategori",
        "amount": "Jumlah (SGD)",
        "card_number": "Nombor Kad",
        "statement_period": "Tempoh Penyata",
        "footer": "Untuk sebarang pertanyaan, sila hubungi Khidmat Pelanggan OCBC di 1800 363 3333",
        "signature_note": "Ini adalah penyata yang dijana komputer dan tidak memerlukan tandatangan"
    }
}
# Remove the duplicate LANGUAGES dictionary from generate_statement function
@app.post("/generate-statement")
async def generate_statement(
    request: Request,
    card_id: str = Form(...),
    language: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...)
):
    try:
        logger.info("Starting DB session")
        db = SessionLocal()
        logger.info("Querying transactions")
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        transactions = db.query(Transaction).filter(
            Transaction.card_id == card_id,
            Transaction.date.between(start, end)
        ).all()
        
        # Calculate summary statistics
        total_amount = sum(tx.amount for tx in transactions)
        reward_points = sum(tx.amount * 0.4 for tx in transactions)
        dining_transactions = [tx for tx in transactions if tx.category == "Dining"]
        dining_rewards = sum(tx.amount * 0.6 for tx in dining_transactions)

        # Assign points to each transaction
        for tx in transactions:
            if tx.category == "Dining":
                tx.points = round(tx.amount * 0.6)
            else:
                tx.points = round(tx.amount * 0.4)

        # Prepare template data with improved alignment
        # Generate PDF filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"generated_statements/statement_{card_id}_{timestamp}.pdf"
        
        # Prepare template data with improved alignment
        lang = LANGUAGES.get(language, LANGUAGES["en"])
        template_data = {
            # Customer Information
            "customer_name": "JOHN DOE",
            "address": "123 SAMPLE STREET SINGAPORE 123456",
            "card_number": f"xxxx-xxxx-xxxx-{card_id[-4:]}",
            "card_type": "Visa Platinum",
            "member_since": "2018-03-15",
            "statement_period": f"{start_date} to {end_date}",

            # Account Details
            "credit_limit": "25,000.00",
            "previous_balance": "3,245.60",
            "new_balance": format(total_amount, ",.2f"),
            "minimum_payment": format(total_amount * 0.05, ",.2f"),
            "payment_due_date": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),

            # Rewards Information
            "points_balance": "45,000",
            "points_earned": format(reward_points, ",.0f"),
            "miles_balance": "35,000",
            "miles_earned": "1,500",
            "cashback_earned": format(total_amount * 0.03, ",.2f"),
            "ytd_cashback": "2,150.75",

            # Transaction and Language Data
            "transactions": transactions,
            "lang": lang,

            # Pass only the selected language's text for these fields
            "statement_title": lang["title"],
            "account_summary_label": lang["account_summary"],
            "credit_limit_label": lang["credit_limit"],
            "previous_balance_label": lang["previous_balance"],
            "new_balance_label": lang["new_balance"],
            "minimum_payment_label": lang["minimum_payment"],
            "payment_due_date_label": lang["payment_due_date"],
            "points_label": lang["points"],
            "points_balance_label": lang["points_balance"],
            "points_earned_label": lang["points_earned"],
            "miles_label": lang["miles"],
            "miles_balance_label": lang["miles_balance"],
            "miles_earned_label": lang["miles_earned"],
            "cashback_label": lang["cashback"],
            "cashback_earned_label": lang["cashback_earned"],
            "ytd_cashback_label": lang["ytd_cashback"],
            "date_label": lang["date"],
            "description_label": lang["description"],
            "category_label": lang["category"],
            "amount_label": lang["amount"],
            "card_number_label": lang["card_number"],
            "statement_period_label": lang["statement_period"],
            "footer_label": lang["footer"],
            "signature_note_label": lang["signature_note"],
            "logo_url": os.environ.get("LOGO_URL", "/static/images/ocbc_logo.png"),
        }

        # Remove the duplicate LANGUAGES dictionary and read_root function from here
        
        # Generate HTML
        html = templates.get_template("statement_template.html").render(template_data)
        
        # Generate PDF using WeasyPrint
        # Use absolute file path for logo in PDF
        logo_path_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "static", "images", "ocbc_logo.png"))
        template_data["logo_url"] = f"file:///{logo_path_pdf.replace(os.sep, '/')}"
        html = templates.get_template("statement_template.html").render(template_data)
        pdf = weasyprint.HTML(string=html, base_url=str(Path(__file__).parent))
        pdf.write_pdf(pdf_filename, presentational_hints=True)  # Add presentational_hints

        return FileResponse(
            pdf_filename,
            media_type="application/pdf",
            filename=f"statement_{card_id}.pdf"
        )
        
    except Exception as e:
        logger.error(f"Error generating statement: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

# Database setup
DATABASE_URL = "sqlite:///./ocbc_statements.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.post("/insert-sample-data")
async def insert_sample_data():
    try:
        db = SessionLocal()
        
        # Sample merchants and categories
        merchants = ["NTUC FairPrice", "Grab", "Shell", "McDonald's", "Uniqlo"]
        categories = ["Groceries", "Transport", "Fuel", "Dining", "Shopping"]
        
        # Generate sample transactions for CARD45678
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(20):  # Generate 20 sample transactions
            transaction = Transaction(
                card_id="CARD45678",
                date=start_date + timedelta(days=random.randint(0, 30)),
                amount=round(random.uniform(10, 500), 2),
                description=f"Purchase at {random.choice(merchants)}",
                merchant=random.choice(merchants),
                category=random.choice(categories)
            )
            db.add(transaction)
        
        db.commit()
        return {"status": "success", "message": "Sample data inserted successfully"}
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)