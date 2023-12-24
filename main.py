from imports import *

load_dotenv()
KEY = os.getenv("KEY")
SECRET = os.getenv("SECRET")

trading_client = TradingClient(KEY, SECRET, paper = True)
account = trading_client.get_account()
buying_power = account.non_marginable_buying_power

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)

driver.get("https://www.biopharmcatalyst.com/fda-calendar")

eligible = []

for x in range(10):
    query = "html body #app main div div section div div:nth-of-type(3) div:nth-of-type(2) div div table tbody tr:nth-of-type(" + str(x + 1) + ")"
    stage = driver.find_element(by=By.CSS_SELECTOR, value=query + " td:nth-of-type(7) div div")
    stage = stage.text
    if (stage[:7] != "Phase 2"):
        continue

    date = driver.find_element(by=By.CSS_SELECTOR, value=query + " td:nth-of-type(8) div")
    date = date.get_attribute("blurred-text")
    if (abs(datetime.strptime(date, "%Y-%m-%d") - datetime.now()) > timedelta(days=3)):
         continue
    
    ticker = driver.find_element(by=By.CSS_SELECTOR, value=query + " td div")
    ticker = ticker.get_attribute("blurred-text")
    eligible.append(ticker)
    
spending = int(buying_power)/len(eligible)

for el in eligible:
    positions = trading_client.get_all_positions()
    owned = False
    for position in positions:
        if position.symbol == ticker:
            owned = True

    if not owned:
        trailing_stop_data = TrailingStopOrderRequest(
            symbol = el,
            notional = spending,
            side = OrderSide.SELL,
            time_in_force = TimeInForce.GTC, 
            trail_percent = 2.5
        )
        trading_client.submit_order(order_data=trailing_stop_data)

driver.quit()