# i am downloading stock data from yahoo finance
# it is free and works without any api key
# i need to install yfinance first using:  pip install yfinance pandas openpyxl

import yfinance as yf
import pandas as pd
import time
from datetime import datetime


# i want data from 2010 to today
START_DATE  = "2010-01-01"
END_DATE    = datetime.today().strftime("%Y-%m-%d")  # this gives todays date like "2026-03-30"

# this is the name of the excel file that will be saved
OUTPUT_FILE = "yahoo_500_stocks.xlsx"

# i will download 10 stocks at a time because its faster
BATCH_SIZE  = 10

# wait 5 second after each batch so yahoo doesnt block me
DELAY = 5


# these are all the stocks i want to download
# us stocks have no dot at end like AAPL
# indian stocks have .NS at end like RELIANCE.NS
# uk stocks have .L at end like HSBA.L
STOCK_SYMBOLS = [

    # big us tech companies
    "AAPL",   # apple
    "MSFT",   # microsoft
    "GOOGL",  # google
    "AMZN",   # amazon
    "NVDA",   # nvidia
    "META",   # facebook
    "TSLA",   # tesla
    "AVGO",   # broadcom
    "ORCL",   # oracle
    "AMD",    # amd chips
    "INTC",   # intel
    "QCOM",   # qualcomm
    "TXN",    # texas instruments
    "MU",     # micron
    "AMAT",   # applied materials
    "LRCX",   # lam research
    "KLAC",   # kla corporation
    "ADI",    # analog devices
    "MRVL",   # marvell
    "NXPI",   # nxp semiconductors
    "CRM",    # salesforce
    "NOW",    # servicenow
    "SNOW",   # snowflake
    "PLTR",   # palantir
    "UBER",   # uber
    "LYFT",   # lyft
    "ABNB",   # airbnb
    "DASH",   # doordash
    "COIN",   # coinbase
    "RBLX",   # roblox
    "SPOT",   # spotify
    "NFLX",   # netflix
    "DIS",    # disney
    "CMCSA",  # comcast
    "T",      # at&t
    "VZ",     # verizon
    "TMUS",   # t-mobile
    "IBM",    # ibm
    "HPQ",    # hp
    "DELL",   # dell
    "ACN",    # accenture
    "INFY",   # infosys us listing
    "WIT",    # wipro us listing
    "CTSH",   # cognizant

    # us banks and finance companies
    "JPM",    # jpmorgan
    "BAC",    # bank of america
    "WFC",    # wells fargo
    "GS",     # goldman sachs
    "MS",     # morgan stanley
    "C",      # citigroup
    "USB",    # us bancorp
    "PNC",    # pnc bank
    "AXP",    # american express
    "V",      # visa
    "MA",     # mastercard
    "PYPL",   # paypal
    "SQ",     # square / block
    "BRK-B",  # warren buffetts company
    "BLK",    # blackrock
    "SCHW",   # charles schwab
    "COF",    # capital one
    # DFS removed - Discover acquired by Capital One (deal closed Feb 2024)
    "AFL",    # aflac insurance
    "MET",    # metlife
    "PRU",    # prudential
    "AIG",    # aig insurance
    "CB",     # chubb
    "HIG",    # hartford

    # us healthcare and medicine companies
    "JNJ",    # johnson and johnson
    "UNH",    # unitedhealth
    "PFE",    # pfizer
    "ABBV",   # abbvie
    "MRK",    # merck
    "LLY",    # eli lilly
    "BMY",    # bristol myers
    "AMGN",   # amgen
    "GILD",   # gilead
    "BIIB",   # biogen
    "REGN",   # regeneron
    "VRTX",   # vertex pharma
    "MRNA",   # moderna covid vaccine company
    "CVS",    # cvs pharmacy
    "CI",     # cigna
    "HUM",    # humana
    "ELV",    # elevance health
    "MDT",    # medtronic
    "ABT",    # abbott
    "SYK",    # stryker
    "BSX",    # boston scientific
    "ZBH",    # zimmer biomet
    "ISRG",   # intuitive surgical robots
    "DHR",    # danaher
    "TMO",    # thermo fisher

    # us oil and energy companies
    "XOM",    # exxon mobil
    "CVX",    # chevron
    "COP",    # conocophillips
    "EOG",    # eog resources
    "SLB",    # schlumberger
    "HAL",    # halliburton
    "BKR",    # baker hughes
    "PSX",    # phillips 66
    "VLO",    # valero energy
    "MPC",    # marathon petroleum
    "OXY",    # occidental
    "DVN",    # devon energy
    "FANG",   # diamondback energy
    # PXD removed - Pioneer Natural Resources acquired by ExxonMobil (deal closed Oct 2023)
    "NEE",    # nextera energy
    "DUK",    # duke energy
    "SO",     # southern company
    "D",      # dominion energy
    "AEP",    # american electric power
    "EXC",    # exelon

    # us shops and consumer brands
    "WMT",    # walmart
    "COST",   # costco
    "TGT",    # target
    "HD",     # home depot
    "LOW",    # lowes
    "NKE",    # nike
    "SBUX",   # starbucks
    "MCD",    # mcdonalds
    "YUM",    # yum brands kfc pizza hut
    "CMG",    # chipotle
    "DPZ",    # dominos pizza
    "KO",     # coca cola
    "PEP",    # pepsi
    "PM",     # philip morris
    "MO",     # altria tobacco
    "PG",     # procter and gamble
    "CL",     # colgate
    "KMB",    # kimberly clark
    "EL",     # estee lauder
    "ULTA",   # ulta beauty
    "LULU",   # lululemon
    "GPS",    # gap clothing
    "RL",     # ralph lauren
    "PVH",    # pvh tommy hilfiger
    "HBI",    # hanesbrands

    # us defence and manufacturing companies
    "BA",     # boeing
    "LMT",    # lockheed martin
    "RTX",    # raytheon
    "NOC",    # northrop grumman
    "GD",     # general dynamics
    "CAT",    # caterpillar big machines
    "DE",     # john deere tractors
    "MMM",    # 3m
    "GE",     # general electric
    "HON",    # honeywell
    "EMR",    # emerson electric
    "ROK",    # rockwell automation
    "PH",     # parker hannifin
    "ITW",    # illinois tool works
    "ETN",    # eaton
    "CMI",    # cummins engines
    "UPS",    # ups delivery
    "FDX",    # fedex
    "CSX",    # csx trains
    "NSC",    # norfolk southern trains
    "UNP",    # union pacific trains

    # us real estate investment trusts
    "AMT",    # american tower cell towers
    "PLD",    # prologis warehouses
    "CCI",    # crown castle
    "EQIX",   # equinix data centers
    "SPG",    # simon property malls
    "O",      # realty income
    "WELL",   # welltower hospitals
    "VTR",    # ventas senior housing
    "AVB",    # avalonbay apartments
    "EQR",    # equity residential

    # us chemicals and materials
    "LIN",    # linde gases
    "APD",    # air products
    "ECL",    # ecolab cleaning
    "SHW",    # sherwin williams paint
    "PPG",    # ppg paint
    "NEM",    # newmont gold mining
    "FCX",    # freeport copper mining
    "NUE",    # nucor steel
    "AA",     # alcoa aluminium
    "CF",     # cf industries fertilizer
    "MOS",    # mosaic fertilizer

    # indian nifty 50 companies
    "RELIANCE.NS",    # reliance industries oil retail telecom
    "HDFCBANK.NS",    # biggest private bank in india
    "ICICIBANK.NS",   # second biggest private bank
    "INFY.NS",        # infosys it company
    "TCS.NS",         # tata consultancy services biggest it
    "SBIN.NS",        # state bank of india government bank
    "BHARTIARTL.NS",  # airtel telecom
    "LT.NS",          # larsen and toubro construction
    "HINDUNILVR.NS",  # hindustan unilever soap shampoo
    "BAJFINANCE.NS",  # bajaj finance loans
    "KOTAKBANK.NS",   # kotak mahindra bank
    "ITC.NS",         # itc cigarettes fmcg hotels
    "TITAN.NS",       # titan watches tanishq jewellery
    "MM.NS",          # mahindra and mahindra cars tractors [FIXED: was M&M.NS - & breaks URL encoding]
    "NTPC.NS",        # national thermal power corporation
    "HCLTECH.NS",     # hcl technologies it company
    "ULTRACEMCO.NS",  # ultratech cement biggest cement company
    "ONGC.NS",        # oil and natural gas corporation
    "ADANIPORTS.NS",  # adani ports
    "JSWSTEEL.NS",    # jsw steel
    "BAJAJFINSV.NS",  # bajaj finserv insurance finance
    "COALINDIA.NS",   # coal india government company
    "POWERGRID.NS",   # power grid corporation
    "BAJAJ-AUTO.NS",  # bajaj bikes pulsar dominar
    "WIPRO.NS",       # wipro it company
    "ASIANPAINT.NS",  # asian paints
    "MARUTI.NS",      # maruti suzuki cars
    "SUNPHARMA.NS",   # sun pharmaceutical biggest pharma
    "AXISBANK.NS",    # axis bank
    "EICHERMOT.NS",   # eicher motors royal enfield bikes
    "NESTLEIND.NS",   # nestle maggi kitkat munch
    "TATASTEEL.NS",   # tata steel
    "HINDALCO.NS",    # hindalco aluminium copper
    "GRASIM.NS",      # grasim industries
    "DIVISLAB.NS",    # divis laboratories pharma
    "DRREDDY.NS",     # dr reddys laboratories
    "HEROMOTOCO.NS",  # hero motocorp bikes
    "TATACONSUM.NS",  # tata consumer tata tea starbucks india
    "APOLLOHOSP.NS",  # apollo hospitals
    "BRITANNIA.NS",   # britannia biscuits good day
    "CIPLA.NS",       # cipla medicines
    "TECHM.NS",       # tech mahindra it company
    "TATAPOWER.NS",   # tata power electricity
    "INDIGO.NS",      # indigo airlines (interglobe aviation)
    "SBILIFE.NS",     # sbi life insurance

    # indian banks and finance companies
    "BANKBARODA.NS",  # bank of baroda government bank
    "PNB.NS",         # punjab national bank
    "CANBK.NS",       # canara bank
    "UNIONBANK.NS",   # union bank of india
    "IDFCFIRSTB.NS",  # idfc first bank
    "BANDHANBNK.NS",  # bandhan bank
    "FEDERALBNK.NS",  # federal bank kerala
    "AUBANK.NS",      # au small finance bank
    "INDUSINDBK.NS",  # indusind bank
    "RBLBANK.NS",     # rbl bank
    "CHOLAFIN.NS",    # cholamandalam finance vehicles loans
    "BAJAJHLDNG.NS",  # bajaj holdings
    "MUTHOOTFIN.NS",  # muthoot finance gold loans
    "SHRIRAMFIN.NS",  # shriram finance vehicle loans
    "MANAPPURAM.NS",  # manappuram gold loans
    "LICHSGFIN.NS",   # lic housing finance home loans
    "CANFINHOME.NS",  # can fin homes home loans
    "HDFCLIFE.NS",    # hdfc life insurance
    "ICICIPRULI.NS",  # icici prudential life insurance
    "NIACL.NS",       # new india assurance government insurance
    "GICRE.NS",       # general insurance corporation reinsurance
    "ICICIGI.NS",     # icici lombard general insurance
    "HDFCAMC.NS",     # hdfc amc mutual fund
    "ANGELONE.NS",    # angel one stock broker app
    "CDSL.NS",        # cdsl demat account depository
    "BSE.NS",         # bombay stock exchange itself is listed
    "MCX.NS",         # mcx commodity exchange gold silver
    "PFC.NS",         # power finance corporation
    "RECLTD.NS",      # rec limited power loans
    "IRFC.NS",        # indian railway finance corporation
    "HUDCO.NS",       # housing urban development corporation

    # indian it companies
    "LTIMINDTREE.NS", # lti mindtree merged it company
    "MPHASIS.NS",     # mphasis it company
    "COFORGE.NS",     # coforge it company
    "PERSISTENT.NS",  # persistent systems
    "OFSS.NS",        # oracle financial services india
    "KPITTECH.NS",    # kpit technologies automobile software
    "LTTS.NS",        # lt technology services engineering
    "TATAELXSI.NS",   # tata elxsi design technology
    "HEXAWARE.NS",    # hexaware technologies (relisted feb 2025)
    "NAUKRI.NS",      # info edge naukri.com
    "ZOMATO.NS",      # zomato food delivery
    "PAYTM.NS",       # paytm payments
    "NYKAA.NS",       # nykaa beauty ecommerce
    "DELHIVERY.NS",   # delhivery logistics

    # indian pharma companies
    "LUPIN.NS",       # lupin pharma
    "AUROPHARMA.NS",  # aurobindo pharma
    "ALKEM.NS",       # alkem laboratories
    "TORNTPHARM.NS",  # torrent pharma
    "ZYDUSLIFE.NS",   # zydus lifesciences
    "LAURUSLABS.NS",  # laurus labs api manufacturing
    "GRANULES.NS",    # granules india
    "AJANTPHARM.NS",  # ajanta pharma
    "BIOCON.NS",      # biocon biologics
    "ABBOTINDIA.NS",  # abbott india
    "GLAXO.NS",       # gsk pharma india
    "PFIZER.NS",      # pfizer india
    "WOCKPHARMA.NS",  # wockhardt
    "MANKIND.NS",     # mankind pharma
    "FORTIS.NS",      # fortis hospitals
    "ASTER.NS",       # aster dm healthcare
    "NARAYANA.NS",    # narayana health hospitals

    # indian auto companies
    "TATAMOTORS.NS",  # tata motors cars trucks jaguar land rover
    "TVSMOTOR.NS",    # tvs motor bikes
    "ASHOKLEY.NS",    # ashok leyland trucks buses
    "ESCORTS.NS",     # escorts kubota tractors
    "MOTHERSON.NS",   # motherson auto parts
    "BOSCHLTD.NS",    # bosch auto parts india
    "BHARATFORG.NS",  # bharat forge forgings
    "BALKRISIND.NS",  # balkrishna industries bkt tyres
    "MRF.NS",         # mrf tyres most expensive share in india
    "APOLLOTYRE.NS",  # apollo tyres
    "CEATLTD.NS",     # ceat tyres
    "AMARAJAENERGY.NS", # amara raja energy & mobility [FIXED: was AMARAJABAT.NS - company renamed]
    "MINDACORP.NS",   # minda corporation auto parts

    # indian fmcg daily use companies
    "DABUR.NS",       # dabur chyawanprash real juice
    "MARICO.NS",      # marico parachute saffola
    "COLPAL.NS",      # colgate india toothpaste
    "EMAMILTD.NS",    # emami fair and handsome zandu
    "GODREJCP.NS",    # godrej consumer cinthol hit
    "RADICO.NS",      # radico khaitan 8pm whisky
    "MCDOWELL-N.NS",  # united spirits mcdowells
    "BATAINDIA.NS",   # bata shoes india
    "TRENT.NS",       # trent zara westside
    "VMART.NS",       # v mart retail small town shopping
    "ABFRL.NS",       # aditya birla fashion pantaloons
    "PAGEIND.NS",     # page industries jockey innerwear
    "RAYMOND.NS",     # raymond suits fabric

    # indian cement companies
    "SHREECEM.NS",    # shree cement
    "AMBUJACEM.NS",   # ambuja cements
    "ACC.NS",         # acc cement
    "DALMIACEMT.NS",  # dalmia bharat cement
    "JKCEMENT.NS",    # jk cement
    "RAMCOCEM.NS",    # ramco cements south india
    "JKLAKSHMI.NS",   # jk lakshmi cement
    "KAJARIACER.NS",  # kajaria ceramics tiles
    "CENTURYTEX.NS",  # century textiles cement

    # indian power and energy companies
    "ADANIPOWER.NS",  # adani power thermal
    "ADANIGREEN.NS",  # adani green solar wind
    "CESC.NS",        # cesc kolkata electricity
    "TORNTPOWER.NS",  # torrent power gujarat
    "JSWENERGY.NS",   # jsw energy
    "NHPC.NS",        # nhpc hydropower government
    "SJVN.NS",        # sjvn hydro government
    "SUZLON.NS",      # suzlon energy wind turbines
    "BPCL.NS",        # bharat petroleum
    "IOC.NS",         # indian oil corporation
    "HINDPETRO.NS",   # hindustan petroleum hpcl
    "GAIL.NS",        # gail india gas pipelines
    "MGL.NS",         # mahanagar gas mumbai
    "IGL.NS",         # indraprastha gas delhi cng
    "PETRONET.NS",    # petronet lng

    # indian capital goods and engineering
    "SIEMENS.NS",     # siemens india
    "ABB.NS",         # abb india motors transformers
    "CGPOWER.NS",     # cg power motors transformers
    "POLYCAB.NS",     # polycab wires cables
    "HAVELLS.NS",     # havells fans switchgear
    "VOLTAS.NS",      # voltas ac tata group
    "KEC.NS",         # kec international power transmission
    "KALPATARU.NS",   # kalpataru projects [FIXED: was KALPATPOWER.NS - company renamed to Kalpataru Projects]
    "IRB.NS",         # irb infrastructure highways
    "ASHOKA.NS",      # ashoka buildcon roads
    "RITES.NS",       # rites transport consulting government

    # indian chemicals companies
    "PIDILITIND.NS",  # pidilite fevicol adhesives
    "DEEPAKNTR.NS",   # deepak nitrite chemicals
    "NAVINFLUOR.NS",  # navin fluorine specialty chemicals
    "SRF.NS",         # srf chemicals fluorine
    "ATUL.NS",        # atul ltd specialty chemicals
    "AARTI.NS",       # aarti industries chemicals
    "VINATI.NS",      # vinati organics specialty chemicals
    "TATACHEM.NS",    # tata chemicals soda ash
    "CHAMBAL.NS",     # chambal fertilisers
    "COROMANDEL.NS",  # coromandel international fertilisers
    "GNFC.NS",        # gujarat narmada valley fertilizers

    # indian real estate companies
    "DLF.NS",         # dlf biggest real estate company india
    "LODHA.NS",       # lodha macrotech luxury homes
    "OBEROIRLTY.NS",  # oberoi realty mumbai
    "PRESTIGE.NS",    # prestige estates bangalore
    "GODREJPROP.NS",  # godrej properties
    "BRIGADE.NS",     # brigade enterprises bangalore
    "SOBHA.NS",       # sobha limited

    # uk companies on london stock exchange
    "HSBA.L",   # hsbc bank big global bank
    "BP.L",     # bp oil company
    "SHEL.L",   # shell oil company
    "GSK.L",    # gsk glaxosmithkline pharma
    "AZN.L",    # astrazeneca pharma
    "ULVR.L",   # unilever dove lipton
    "VOD.L",    # vodafone uk telecom
    "BA.L",     # bae systems defence
    "DGE.L",    # diageo johnnie walker guinness
    "RIO.L",    # rio tinto mining
    "AAL.L",    # anglo american mining
    "LSEG.L",   # london stock exchange group itself
    "NWG.L",    # natwest group bank
    "LLOY.L",   # lloyds bank uk
    "BARC.L",   # barclays bank

    # european companies
    "ASML.AS",   # asml netherlands chip making machines
    "SAP.DE",    # sap germany software erp
    "SIE.DE",    # siemens germany industrial
    "BMW.DE",    # bmw germany luxury cars
    "VOW3.DE",   # volkswagen germany cars
    "ALV.DE",    # allianz germany insurance
    "BAS.DE",    # basf germany chemicals
    "OR.PA",     # loreal france cosmetics
    "MC.PA",     # lvmh france luxury goods
    "AIR.PA",    # airbus france planes
    "SAN.PA",    # sanofi france pharma
    "BNP.PA",    # bnp paribas france bank
    "NESN.SW",   # nestle switzerland maggi kitkat
    "NOVN.SW",   # novartis switzerland pharma
    "ROG.SW",    # roche switzerland pharma diagnostics
    "UBS.SW",    # ubs switzerland bank

    # asian companies
    "9988.HK",   # alibaba china ecommerce hong kong listed
    "0700.HK",   # tencent china wechat games hong kong listed
    "1299.HK",   # aia group insurance asia
    "2318.HK",   # ping an insurance china
    "9618.HK",   # jd.com china ecommerce
    "7203.T",    # toyota japan cars
    "6758.T",    # sony japan electronics playstation
    "6861.T",    # keyence japan sensors automation
    "9984.T",    # softbank japan tech investments
    "005930.KS", # samsung electronics korea phones chips
    "000660.KS", # sk hynix korea memory chips

]

# Quick summary
print(f"Total symbols: {len(STOCK_SYMBOLS)}")

# this removes duplicate symbols if i accidentally added same stock twice
STOCK_SYMBOLS = list(dict.fromkeys(STOCK_SYMBOLS))
print(f"total stocks i want to download: {len(STOCK_SYMBOLS)}")


# now i will download data for all stocks
# i am using batches because its faster than one by one
print(f"\ndownloading data from {START_DATE} to {END_DATE}")
print("this will take a few minutes please wait...\n")

# i will store each stocks data here
# it works like a dictionary   symbol -> table of data
all_stocks_data = {}

# i will also track which stocks failed to download
failed_symbols = []

total = len(STOCK_SYMBOLS)
count = 0

# i goes 0, 10, 20, 30... jumping by BATCH_SIZE each time
for i in range(0, total, BATCH_SIZE):

    # take 10 symbols at a time from the big list
    batch = STOCK_SYMBOLS[i : i + BATCH_SIZE]
    count = count + len(batch)

    print(f"[{count}/{total}] downloading: {', '.join(batch)}")

    try:
        # yf.download does all the hard work
        # it talks to yahoo finance and gets the data
        raw_data = yf.download(
            tickers     = batch,
            start       = START_DATE,
            end         = END_DATE,
            group_by    = "ticker",    # organizes data by stock name
            auto_adjust = True,        # fixes prices for stock splits automatically
            threads     = True,        # downloads many stocks at same time
            progress    = False        # hides yfinances own loading bar
        )

        # now i separate each stock from the downloaded data
        for symbol in batch:
            try:
                # if only 1 stock was downloaded structure is different
                if len(batch) == 1:
                    df = raw_data.copy()
                else:
                    # for multiple stocks i pick by symbol name
                    df = raw_data[symbol].copy()

                # remove empty rows where all columns are blank
                df = df.dropna(how="all")

                # only save if there is actual data
                if len(df) > 0:

                    # move date from index to a normal column
                    df = df.reset_index()

                    # change date format to look like "30-03-2010"
                    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d-%m-%Y")

                    # round all price columns to 2 decimal places
                    for col in ["Open", "High", "Low", "Close", "Volume"]:
                        if col in df.columns:
                            df[col] = df[col].round(2)

                    # add the stock name as a column so i know which row belongs to which stock
                    df["Symbol"] = symbol

                    # save it
                    all_stocks_data[symbol] = df

                else:
                    # yahoo had no data for this stock
                    print(f"   no data found for {symbol}")
                    failed_symbols.append(symbol)

            except Exception as e:
                print(f"   something went wrong for {symbol}: {e}")
                failed_symbols.append(symbol)

    except Exception as e:
        print(f"   whole batch failed: {e}")
        for symbol in batch:
            failed_symbols.append(symbol)

    # wait a little so yahoo doesnt think i am a bot and block me
    time.sleep(DELAY)


# now save everything to excel
# i am making 3 files so i have options
print(f"\nsaving files now...")


# file 1 - each stock gets its own tab in excel
output_a = "yahoo_stocks_each_tab.xlsx"
print(f"saving {output_a}  (one tab per stock)...")

with pd.ExcelWriter(output_a, engine="openpyxl") as writer:
    for symbol, df in all_stocks_data.items():

        # excel tab names cant have dots or & and max 31 characters
        sheet_name = symbol.replace(".", "_").replace("&", "n")[:31]

        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"   saved!")


# file 2 - all stocks together in one single sheet
output_b = "yahoo_stocks_all_combined.xlsx"
print(f"saving {output_b}  (everything in one sheet)...")

# stack all the tables on top of each other into one big table
all_combined = pd.concat(all_stocks_data.values(), ignore_index=True)

# put columns in a nice order
cols = ["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"]
cols = [c for c in cols if c in all_combined.columns]
all_combined = all_combined[cols]

all_combined.to_excel(output_b, index=False, engine="openpyxl")
print(f"   saved!")


# file 3 - csv is a simple text file smaller than excel good for python later
output_c = "yahoo_stocks_combined.csv"
print(f"saving {output_c}  (csv format smallest size)...")
all_combined.to_csv(output_c, index=False)
print(f"   saved!")


# print a summary of what i downloaded
total_rows = sum(len(df) for df in all_stocks_data.values())

print(f"\n{'='*50}")
print("done!")
print(f"{'='*50}")
print(f"  stocks downloaded : {len(all_stocks_data)}")
print(f"  total rows        : {total_rows:,}")
print(f"  date range        : {START_DATE} to {END_DATE}")
print(f"\n  files i created:")
print(f"    1. {output_a}")
print(f"    2. {output_b}")
print(f"    3. {output_c}")

# show which stocks failed if any
if len(failed_symbols) > 0:
    print(f"\n  these stocks failed to download ({len(failed_symbols)} total):")
    for s in failed_symbols:
        print(f"     {s}")
    print("\n  these might be delisted or renamed on yahoo finance")
else:
    print("\n  all stocks downloaded successfully!")

# count how many from each country i got
print(f"\n  breakdown by market:")
print(f"    us stocks      : {sum(1 for s in all_stocks_data if '.' not in s)}")
print(f"    india .NS      : {sum(1 for s in all_stocks_data if '.NS' in s)}")
print(f"    uk .L          : {sum(1 for s in all_stocks_data if '.L' in s)}")
print(f"    europe         : {sum(1 for s in all_stocks_data if any(x in s for x in ['.DE','.PA','.SW','.AS']))}")
print(f"    asia           : {sum(1 for s in all_stocks_data if any(x in s for x in ['.HK','.T','.KS']))}")


import pandas as pd

file = "stock_data_100.xlsx"
xls = pd.ExcelFile(file)

total_rows = 0

for sheet in xls.sheet_names:
    df = pd.read_excel(file, sheet_name=sheet)
    total_rows += len(df)

print("Total stocks scraped:", len(xls.sheet_names))

print("Total rows scraped:", total_rows)