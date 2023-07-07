(ns oas.oandpts
  "endpts for oanda api"
  (:require
   [algolibs.core :refer [pip-factor]]
   [clj-http.client :as client]
   [clojure.data.json :as json]))


;;; definitions ;;;

(def prac
  "practice account parameters"
  {:url "https://api-fxpractice.oanda.com"
   :strurl "https://stream-fxpractice.oanda.com"
   :accnum "/101-002-9789110-003"
   :header {"Content-Type" "application/json"
             "Authorization" "Bearer 8682793479e663dfa1520ad753566ca7-7212ebf93fb7ecba4941835537a0f6f7"}})

(def live
  "live account parameters"
  {:url ""
   :strurl ""
   :accnum ""
   :header {"Content-Type" "application/json"
            "Authorization" ""}})

(def acct
  "set account to prac or live through acct"
  prac) 

(def accnumstr
  "set account number string: url + /v3/accounts + /account-number"
  (str
   (acct :url)
   "/v3/accounts"
   (acct :accnum))) 


;;; functions ;;;

(defn client-get [q]
  "client/get request"
  (client/get q {:headers (acct :header)}))

(defn client-post [q jsonvar]
  "client/post request"
  (client/post q {:headers (acct :header)
                  :body jsonvar}))

(defn client-put [q]
  "client/post request"
  (client/put q {:headers (acct :header)}))

(defn json-str [a]
  "json/read-str parsing"
  (json/read-str (:body a)))


                                        ; account endpts

(defn accounts
  "get list of all authorized accounts"
  []
  (let [q (str (acct :url) "/v3/accounts")]
    (json-str (client-get q))))

(defn details
  "get account details"
  []
  (let [q accnumstr]
    (json-str (client-get q))))

(defn acct-summary
  "get account summary"
  []
  (let [q (str accnumstr "/summary")]
    (json-str (client-get q))))

(defn instruments
  "get list of tradable instruments"
  []
  (let [q (str accnumstr "/instruments")]
    (json-str (client-get q))))

(defn changes
  "get account state and changes since a specified transaction"
  [transactionID]
  (let [q (str accnumstr "/changes?sinceTransactionID=" transactionID)]
    (json-str (client-get q))))


                                        ; instrument endpts
(defn get-candles
  "gets num-candles of granularity with BidAskMid price for ins"
  [instrument num-candles granularity bidaskmid]
  (let [q (str (acct :url) "/v3/instruments"
               "/" instrument "/candles?"
               "count=" num-candles
               "&price=" bidaskmid
               "&granularity=" granularity)]
    (json-str (client-get q))))

(defn order-book
  "Get orderbook for instrument possibly for a fixed datetime"
  [instrument & datetime]
  (let [url (str (acct :url) "/v3/instruments/" instrument "/orderBook")
        q (if (empty? datetime)
            url
            (str url "?time=" (first datetime)))]
    (json-str (client-get q))))

(defn position-book
  "Get postionbook for instrument possibly for a fixed datetime"
  [instrument & datetime]
  (let [url (str (acct :url) "/v3/instruments/" instrument "/positionBook")
        q (if (empty? datetime)
            url
            (str url "?time=" (first datetime)))]
    (json-str (client-get q))))


                                        ; price endpts

(defn current-price-info
  "gets the current price for instrument"
  [instrument]
  (let [q (str (acct :url) "/v3/accounts" (acct :accnum) "/pricing?instruments=" instrument)]
    (json-str (client-get q)) ))

(defn ask-bid-mean
  "determines order labels tif (FOK, GTC) and typ (MARKET, STOP, LIMIT)"
  [instrument]
  (let [cpi (current-price-info instrument)
        ask (Float/parseFloat (get-in cpi ["prices" 0 "asks" 0 "price"]))
        bid (Float/parseFloat (get-in cpi ["prices" 0 "bids" 0 "price"]))]
    (/ (+ ask bid) 2)))



                                        ; order endpts

(defn get-order-type
  "determines order type STOP or LIMIT"
  [entry-price current-price volume]
  (let [entry-price entry-price
        volume volume
        result (cond
                 (and (neg? volume) (> entry-price current-price)) "LIMIT"
                 (and (neg? volume) (< entry-price current-price)) "STOP"
                 (and (pos? volume) (> entry-price current-price)) "STOP"
                 (and (pos? volume) (< entry-price current-price)) "LIMIT")]
    result))

(defn prep-price
  "preps prices sltpen for order"
  [pr instrument]
  (let [pf (inc (int (Math/log10 (pip-factor instrument))))
        p (format (str "%." pf "f") pr)]
    p))

(defn order
  "create market or entry order depending on whether entry-price is nil"
  [instrument volume stoploss takeprofit entry-price]
  (let [nil-entry-price (nil? entry-price)
        current-price (ask-bid-mean instrument)
        time-in-force (if nil-entry-price
                        "FOK"
                        "GTC")
        order-type (if nil-entry-price
                     "MARKET"
                     (get-order-type entry-price current-price volume))
        jsonvar (json/write-str {"order" {"instrument" instrument
                                          "price" (prep-price entry-price instrument)
                                          "units" (str volume)
                                          "timeInForce" time-in-force
                                          "type" order-type
                                          "positionFill" "DEFAULT"
                                          "stopLossOnFill" {"timeInForce" "GTC"
                                                            "price" (prep-price stoploss instrument)}
                                          "takeProfitOnFill" {"timeInForce" "GTC"
                                                              "price" (prep-price takeprofit instrument)}}})
        q (str accnumstr "/orders")]
    (client-post q jsonvar)))




(defn orders-pending-for-account
  "gets all pending orders for the account"
  []
  (let [q (str accnumstr
               "/pendingOrders")]
    (json-str (client-get q))))

(defn order-ids-for-instrument
  "get all orders ids for a particular instrument"
  [instrument]
  (let [q (str accnumstr
               "/orders?instrument="
               instrument)]
    (json-str (client-get q))))

(defn order-id-details
  "gets order details by id number"
  [id]
  (let [q (str accnumstr
               "/orders/"
               (str id))]
    (json-str (client-get q))))

(defn cancel-order-by-id
  "cancels a pending order for an instrument given the id"
  [id]
  (let [q (str accnumstr
               "/orders/"
               (str id)
               "/cancel")]
    (json-str (client-put q))))

(defn cancel-instrument-orders
  "cancels all pending orders for an instrument"
  [instrument]
  (let [
        ids (map #(Integer/parseInt %)
                 (map #(get % "id")
                      (get (order-ids-for-instrument instrument) "orders")))
        ]
    (map cancel-order-by-id ids)))
