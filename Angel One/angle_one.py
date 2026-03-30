

from SmartApi import SmartConnect   # AngelOne API library
import pyotp                        # For generating OTP
import pandas as pd                 # For working with tables (DataFrames)
import requests                     # For downloading files from internet
import time                         # For adding delays
from datetime import datetime, timedelta  # For working with dates
import logging                      #print msg to help tracker


# PART 1: SET UP LOGGING (Track what the code is doing)
# This makes the code print nice messages so you know what's happening
logging.basicConfig(
    level=logging.INFO,  # Show all messages
    format='[%(asctime)s] %(levelname)s: %(message)s'  # Format: [TIME] TYPE: MESSAGE
)
logger = logging.getLogger(__name__)

#   LOGIN DETAILS
API_KEY     = "*******"
CLIENT_ID   = "******"
PASSWORD    = "*****"
TOTP_SECRET = "******"


#  SETTINGS
DAYS        = 365 * 10   # How many past days of data you want
OUTPUT_FILE = "angel-one-data.xlsx"  # Name of the output Excel file
DELAY       = 0.5    # Wait 0.5 seconds between each API call (to avoid getting blocked)
CHUNK_DAYS  = 365     # AngelOne only allows 55 days at a time for 1-minute data


# ============================================================
#  LIST OF STOCKS TO DOWNLOAD
#  (These are correct NSE symbols)
# ============================================================
STOCK_NAMES = [
    # --- Big Companies (NIFTY 50) ---
    "RELIANCE", "HDFCBANK", "ICICIBANK", "INFY", "TCS",
    "SBIN", "BHARTIARTL", "LT", "HINDUNILVR", "BAJFINANCE",
    "KOTAKBANK", "ITC", "TITAN", "M&M", "NTPC",
    "HCLTECH", "ULTRACEMCO", "ONGC", "ADANIPORTS", "JSWSTEEL",
    "BAJAJFINSV", "COALINDIA", "POWERGRID", "BAJAJ-AUTO", "WIPRO",
    "ASIANPAINT", "MARUTI", "SUNPHARMA", "AXISBANK", "EICHERMOT",
    "NESTLEIND", "TATASTEEL", "HINDALCO", "GRASIM", "DIVISLAB",
    "DRREDDY", "HEROMOTOCO", "TATACONSUM", "APOLLOHOSP", "BRITANNIA",
    "CIPLA", "TECHM", "TATAPOWER", "INDIGO", "SBILIFE",
    "ADANIENT", "ZOMATO", "JIOFIN", "MAXHEALTH", "TRENT",

    # --- Banks & Finance ---
    "BANKBARODA", "PNB", "CANBK", "UNIONBANK", "IDBI",
    "INDIANB", "IDFCFIRSTB", "BANDHANBNK", "FEDERALBNK", "AUBANK",
    "EQUITASBNK", "INDUSINDBK", "RBLBANK", "KARURVYSYA", "DCBBANK",
    "CUB", "SOUTHBANK", "J&KBANK", "UJJIVANSFB", "ESAFSFB",
    "ABCAPITAL", "CHOLAFIN", "BAJAJHLDNG", "MUTHOOTFIN", "SHRIRAMFIN",
    "MANAPPURAM", "LICHSGFIN", "CANFINHOME", "AAVAS", "HOMEFIRST",
    "APTUS", "CREDITACC", "SPANDANA", "ARMANFIN", "PAISALO",
    "HDFCLIFE", "ICICIPRULI", "STARHEALTH",
    "NIACL", "GICRE", "ICICIGI", "HDFCAMC", "ICICIAMC",
    "ANGELONE", "CDSL", "BSE",
    "MCX", "IEX", "MFSL", "PFC", "RECLTD",
    "IRFC", "HUDCO", "NBCC", "TATACAP",

    # --- IT & Technology ---
    "LTIMINDTREE", "MPHASIS", "COFORGE", "PERSISTENT", "OFSS",
    "KPITTECH", "LTTS", "INTELLECT", "MASTEK", "TATAELXSI",
    "HEXAWARE", "RATEGAIN", "NAUKRI",
    "POLICYBZR", "PAYTM", "CARTRADE", "NYKAA",
    "DELHIVERY", "MAPMYINDIA", "LATENTVIEW", "DATAMATICS",

    # --- Pharma & Healthcare ---
    "LUPIN", "AUROPHARMA", "ALKEM", "TORNTPHARM", "ZYDUSLIFE",
    "IPCALAB", "LALPATHLAB", "METROPOLIS", "THYROCARE", "LAURUSLABS",
    "GRANULES", "NATCOPHARM", "AJANTPHARM", "APLLTD", "BIOCON",
    "ABBOTINDIA", "GLAXO", "PFIZER", "SANOFI",
    "WOCKPHARMA", "JBCHEPHARM", "ERIS", "GLAND", "SEQUENT",
    "STRIDES", "MANKIND", "FORTIS",
    "ASTER", "NARAYANA", "MEDANTA", "RAINBOW", "KRSNAA",

    # --- Auto & Auto Parts ---
    "TATAMOTORS", "TVSMOTOR", "ASHOKLEY", "ESCORTS", "M&MFIN",
    "MOTHERSON", "BOSCHLTD", "BHARATFORG", "BALKRISIND", "MRF",
    "APOLLOTYRE", "CEATLTD", "JKTYRE", "ENDURANCE", "SUPRAJIT",
    "SUNDRMFAST", "EXIDEIND", "AMARAJABAT", "LUMAXTECH", "CRAFTSMAN",
    "SWARAJENG", "MAHSEAMLES", "TUBEINVEST", "FINCABLES", "MINDACORP",

    # --- FMCG & Daily Use Products ---
    "DABUR", "MARICO", "COLPAL", "EMAMILTD", "GODREJCP",
    "PGHH", "GILLETTE", "JYOTHYLAB", "VBL", "UNITDSPR",
    "RADICO", "MCDOWELL-N", "GODFRYPHLP", "VST", "BATAINDIA",
    "CAMPUS", "RELAXO", "LIBERTY", "MIRZA", "KHADIM",
    "SHOPERSTOP", "VMART", "ABFRL", "PAGEIND",
    "RAYMOND", "ARVIND", "KPRMILL", "NITINSPIN", "WELCORP",

    # --- Cement & Building ---
    "SHREECEM", "AMBUJACEM", "ACC", "DALMIACEMT",
    "JKCEMENT", "RAMCOCEM", "INDIACEM", "HEIDELBERG", "BIRLACORPN",
    "JKLAKSHMI", "EVERESTIND", "CENTURYTEX", "KAJARIACER",
    "ORIENTBELL", "SOMANYCERAMS", "CERA",

    # --- Metals & Mining ---
    "VEDL", "NMDC", "SAIL", "JINDALSTEL", "MOIL", "RATNAMANI",
    "TINPLATE", "HINDZINC", "NATIONALUM", "CONCOR", "MAHLOG",

    # --- Energy & Power ---
    "ADANIPOWER", "ADANIGREEN", "ADANIENSOL",
    "CESC", "TORNTPOWER", "JSWENERGY", "NHPC", "SJVN", "IREDA", "SUZLON",
    "BPCL", "IOC", "HINDPETRO", "GAIL", "OIL",
    "MGL", "IGL", "GSPL", "PETRONET", "ATGL", "AEGISCHEM",

    # --- Capital Goods & Infrastructure ---
    "SIEMENS", "ABB", "HAL", "BEL", "BHEL",
    "CUMMINSIND", "THERMAX", "AIAENG", "GRINDWELL",
    "CGPOWER", "POLYCAB", "HAVELLS", "VOLTAS", "BLUESTARCO",
    "HITACHIENERGY", "POWERINDIA", "KEC", "KALPATPOWER", "KPIL",
    "ENGINERSIN", "IRB", "ASHOKA", "PNCINFRA", "DBCL",
    "RITES", "NLCINDIA", "MAZDOCK", "BDL", "GRSE", "MIDHANI",

    # --- Chemicals ---
    "PCBL", "GNFC", "GSFC", "DEEPAKNTR",
    "FLUOROCHEM", "NAVINFLUOR", "SRF", "ATUL", "AARTI",
    "VINATI", "NOCIL", "VINYLINDIA", "FINEORG", "DMCC",
    "PIDILITIND", "SUDARSCHEM", "ROSSARI", "ANUPAM",
    "LXCHEM", "TATACHEM", "GHCL", "DCMSHRIRAM", "CHAMBAL",

    # --- Real Estate ---
    "DLF", "LODHA", "OBEROIRLTY", "PRESTIGE", "GODREJPROP",
    "BRIGADE", "SOBHA", "PHOENIXLTD", "KOLTEPATIL", "MAHLIFE",
    "ANANTRAJ", "SUNTECK",

    # --- Textiles ---
    "WELSPUNLIV", "VARDHMAN", "TRIDENT", "GOKEX", "SIYARAM", "HIMATSEIDE",

    # --- Telecom ---
    "IDEA", "INDUSTOWER", "ROUTE", "TATACOMM", "RAILTEL", "TANLA",

    # --- Logistics & Hotels ---
    "GMRAIRPORT", "BLUEDART", "ALLCARGO", "GATI",
    "IRCTC", "THOMASCOOK", "MHRIL", "INDHOTEL",
    "LEMONTREE", "CHALET", "EIHOTEL", "TAJGVK",

    # --- Retail & Food ---
    "DMART", "ETERNAL", "DEVYANI", "JUBLFOOD", "WESTLIFE", "BARBEQUE",

    # --- Fertilizers & Agri ---
    "CHAMBLFERT", "COROMANDEL", "RALLIS", "BAYER", "DHANUKA", "PARADEEP",

    # --- Small & Mid Cap ---
    "EIDPARRY", "BALAMINES", "EPIGRAL", "TATVA", "CHEMPLASTS",
    "TNPL", "REFEX", "KENNAMETAL", "SUNDARAM", "SUBROS",
    "LUMAXIND", "GAEL", "VSTIND", "VGUARD", "CROMPTON",
    "SOLARINDS", "PREMIER", "ELECON",
    "JMFINANCIL", "PNBHOUSING", "POONAWALLA", "UGROCAP", "SBFC",
    "FIVESTAR", "OLECTRA", "GREENPANEL", "CENTURYPLY",
    "GREENLAM", "GREENPLY", "NEWGEN", "KFINTECH", "CAMS", "NUVOCO",
    "HEMIPROP",

    # --- Other Finance ---
    "IIFL", "MOTILALOFS", "5PAISA", "GEOJITFSL", "VENKEYS",
    "GOLDBEES", "NIFTYBEES",
]

# Remove duplicate stock names from the list
STOCK_NAMES = list(dict.fromkeys(STOCK_NAMES))
print(f"Total unique stocks in list: {len(STOCK_NAMES)}")


# ============================================================
#  STEP 1: Download the list of all NSE stocks with tokens
#  (Token = a number that AngelOne uses to identify each stock)
# ============================================================
print("\nStep 1: Downloading instrument master file...")

master_url  = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
master_data = requests.get(master_url).json()

print(f"  Master file downloaded. Total instruments: {len(master_data)}")


# ============================================================
#  STEP 2: Match our stock names to their tokens
# ============================================================
print("\nStep 2: Finding tokens for our stocks...")

# This dictionary will store:  stock name --> token number
# Example: { "RELIANCE": "2885", "TCS": "11536", ... }
token_map = {}

for item in master_data:
    symbol       = item.get("symbol", "").upper()
    token        = item.get("token", "")
    exchange_seg = item.get("exch_seg", "")

    # NSE stocks end with "-EQ", so we remove it to get clean name
    # Example: "RELIANCE-EQ" --> "RELIANCE"
    clean_symbol = symbol.replace("-EQ", "")

    # We only want NSE stocks that are in our list
    if exchange_seg == "NSE" and clean_symbol in STOCK_NAMES:
        token_map[clean_symbol] = token

print(f"  Tokens found: {len(token_map)} out of {len(STOCK_NAMES)} stocks")


# Show stocks that were not found (wrong name or not listed on NSE)
print("\n  Stocks NOT found (check if name is correct or listed on NSE):")
not_found_count = 0
for name in STOCK_NAMES:
    if name not in token_map:
        print(f"    ✗ {name}")
        not_found_count += 1

if not_found_count == 0:
    print("    All stocks found!")


# ============================================================
#  STEP 3: Login to AngelOne
# ============================================================
print("\nStep 3: Logging in to AngelOne...")

smart    = SmartConnect(api_key=API_KEY)   # Create connection object
otp_code = pyotp.TOTP(TOTP_SECRET).now()  # Generate OTP using your secret key
smart.generateSession(CLIENT_ID, PASSWORD, otp_code)  # Login

print("  Login successful!")


# ============================================================
#  STEP 4: Set up date range
#  AngelOne allows only 55 days at a time for 1-minute data.
#  So we split 365 days into multiple 55-day chunks.
# ============================================================
print("\nStep 4: Setting up date ranges...")

today = datetime.now()
past  = today - timedelta(days=DAYS)

# This function splits a big date range into smaller chunks
def split_into_chunks(start_date, end_date, chunk_size_days):
    chunks = []        # Empty list to store all chunks
    current = start_date

    while current < end_date:
        chunk_end = current + timedelta(days=chunk_size_days)

        # Don't go beyond the end date
        if chunk_end > end_date:
            chunk_end = end_date

        # Format date as string like "2025-03-30 09:15"
        from_str = current.strftime("%Y-%m-%d 09:15")
        to_str   = chunk_end.strftime("%Y-%m-%d 15:30")

        chunks.append((from_str, to_str))

        # Move to next chunk (start from the next day)
        current = chunk_end + timedelta(days=1)

    return chunks


date_chunks = split_into_chunks(past, today, CHUNK_DAYS)
print(f"  Date range: {past.strftime('%d-%m-%Y')} to {today.strftime('%d-%m-%Y')}")
print(f"  Split into {len(date_chunks)} chunks of {CHUNK_DAYS} days each")


# ============================================================
#  STEP 5: Download data for each stock
# ============================================================
print("\n" + "="*50)
print("Step 5: Downloading stock data...")
print("="*50)

# This dictionary will store all data:  stock name --> table of data
all_stocks_data = {}

# Track which stocks failed
failed_stocks = []

total = len(token_map)
count = 0

for stock_name, token_number in token_map.items():
    count = count + 1
    print(f"\n[{count}/{total}] Downloading {stock_name}...")

    # List to store data from all date chunks for this stock
    all_chunks_data = []

    # Download data chunk by chunk
    for from_date, to_date in date_chunks:

        # Try up to 3 times if we get a "too many requests" error
        for attempt in range(1, 4):   # attempt = 1, 2, or 3
            try:
                # Ask AngelOne API for data
                result = smart.getCandleData({
                    "exchange":    "NSE",
                    "symboltoken": token_number,
                    "interval":    "ONE_MINUTE",
                    "fromdate":    from_date,
                    "todate":      to_date
                })

                # If data was returned, save it
                if result and result["data"]:
                    chunk_df = pd.DataFrame(
                        result["data"],
                        columns=["date", "open", "high", "low", "close", "volume"]
                    )
                    all_chunks_data.append(chunk_df)

                # Wait a little before next request
                time.sleep(DELAY)
                break   # Success! Exit the retry loop

            except Exception as error:
                error_message = str(error)

                if "AB1019" in error_message or "Too many requests" in error_message:
                    # We sent too many requests — wait longer and try again
                    wait_time = 10 * attempt   # 10s, 20s, 30s
                    print(f"   ⚠ Too many requests! Waiting {wait_time} seconds... (attempt {attempt}/3)")
                    time.sleep(wait_time)
                else:
                    # Some other error — skip this chunk
                    print(f"   ✗ Error for {stock_name}: {error_message}")
                    break


    # Combine all chunks into one big table
    if len(all_chunks_data) > 0:
        # pd.concat stacks multiple tables on top of each other
        final_df = pd.concat(all_chunks_data, ignore_index=True)

        # Remove any duplicate rows (same date appearing twice)
        final_df = final_df.drop_duplicates(subset="date")

        # Sort by date (oldest first)
        final_df = final_df.sort_values("date").reset_index(drop=True)

        # Convert date to readable format like "30-03-2025 09:15"
        final_df["date"] = pd.to_datetime(final_df["date"]).dt.strftime("%d-%m-%Y %H:%M")

        # Add a column with the stock name
        final_df["stock"] = stock_name

        # Save this stock's data
        all_stocks_data[stock_name] = final_df
        print(f"   ✓ Done! {len(final_df):,} rows downloaded")

    else:
        print(f"   ✗ No data received — skipping {stock_name}")
        failed_stocks.append(stock_name)


# ============================================================
#  STEP 6: Save everything to Excel
#  Each stock gets its own sheet (tab) in the Excel file
# ============================================================
print("\n" + "="*50)
print("Step 6: Saving to Excel file...")
print("="*50)

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    for stock_name, df in all_stocks_data.items():

        # Excel sheet names can be max 31 characters
        sheet_name = stock_name[:31]

        df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"  Saved sheet: {sheet_name}")


# ============================================================
#  STEP 7: Print final summary
# ============================================================
total_rows = sum(len(df) for df in all_stocks_data.values())

print("\n" + "="*50)
print("ALL DONE!")
print("="*50)
print(f"  File saved as : {OUTPUT_FILE}")
print(f"  Stocks saved  : {len(all_stocks_data)}")
print(f"  Total rows    : {total_rows:,}")

if len(failed_stocks) > 0:
    print(f"\n  Failed stocks ({len(failed_stocks)}):")
    for s in failed_stocks:
        print(f"    ✗ {s}")
else:
    print("\n  All stocks downloaded successfully!")

print("---------------------------------------------------")
import pandas as pd

file = "stock_data_100.xlsx"
xls = pd.ExcelFile(file)

total_rows = 0

for sheet in xls.sheet_names:
    df = pd.read_excel(file, sheet_name=sheet)
    total_rows += len(df)

print("Total stocks scraped:", len(xls.sheet_names))

print("Total rows scraped:", total_rows)

