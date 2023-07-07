"
TODO

stop using all nu in 36 bars - some should be zapped
"

(ns nuen.clj
  (:require [algolibs.core :as b]
            [algolibs.oandpts :as ep]))

(defn ds-candles
  "creates ncandles dataset for instrument at granularity and M bidaskmed pricing"
  [instrument ncandles granularity & [bidaskmed]]
  (let [bam (or bidaskmed "M")
        cans (ep/get-candles instrument ncandles granularity "M")
        timemid (for [itm (get cans "candles")]
                  (conj {"column-0" (clojure.string/replace (get itm "time")
                                                            #"T|.0*Z" " ")}
                        (get itm "mid")))
        rencols (map #(clojure.set/rename-keys % {"o" "column-1"
                                                  "h" "column-2"
                                                  "l" "column-3"
                                                  "c" "column-4"})
                     timemid)
        tohlc (b/mk-tohlc rencols)
        ]
    tohlc))

(ds-candles "EUR_USD" 2 "D")

(b/nu-finder (ds-candles "USD_JPY" 36 "H1"))


(defn nuen-orders
  "places brs and prs entry orders given instrument and granularity"
  [instrument granularity]
  (let [
        nus (flatten (b/nu-finder (ds-candles instrument 36 granularity)))
        cprice (-> (ep/current-price-info instrument)
                   (get "prices")
                   (get 0)
                   (get "closeoutAsk")
                   Double/parseDouble)
        sltp (/ 12.0 (b/pip-factor instrument))]
    (for [nu nus]
      ;; (if (> nu cprice) ; brs
      ;;   (ep/order instrument -10000 (+ nu sltp) (- nu sltp) nu)
      ;;   (ep/order instrument +10000 (- nu sltp) (+ nu sltp) nu))
      (if (> nu cprice) ; prs
        (ep/order instrument +10000 (- nu sltp) (+ nu sltp) nu)
        (ep/order instrument -10000 (+ nu sltp) (- nu sltp) nu))
      )))

(def instrumentv ["EUR_USD" "USD_JPY" "USD_CAD" "EUR_JPY" "AUD_USD" "EUR_GBP"])
(def cancel-orders (map #(ep/cancel-instrument-orders %) instrumentv))
(def place-orders (map #(nuen-orders % "H1") instrumentv))

;;5922
;;5864
;;5827
;;5778

;;5784
;;5642
;;5618
;;5600 - due to afternoon eurjpy test order
;;5488
;;5279
;;


(def s "hello there")
(clojure.string/replace s #"h|t" " ")
