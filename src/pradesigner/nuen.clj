"
REDO to fit algotrd system
TODO
redo nu-finder with checking legitimacy in formation
develop trading tracker to see which trades worked
"

(ns oas.nuen
  "ns for nuen which creates entries based on nu"
  (:require [algolibs.core :as alco]
            [oas.oandpts :as aloa]))

(defn ds-candles
  "creates ncandles dataset for inst at granularity and M bidaskmed pricing"
  [inst ncandles granularity & [bidaskmed]]
  (let [bam (or bidaskmed "M")
        cands (aloa/get-candles inst ncandles granularity "M") ;gets the candles
        timemid (for [itm (get cands "candles")] ;sets up tohlc values as per json 
                  (conj {"column-0" (clojure.string/replace (get itm "time")
                                                            #"T|.0*Z" " ")} ;cleans up time
                        (get itm "mid")))
        rencols (map #(clojure.set/rename-keys % {"o" "column-1"
                                                  "h" "column-2"
                                                  "l" "column-3"
                                                  "c" "column-4"}) 
                     timemid)
        tohlc (alco/mk-tohlc rencols) ;creates tohlc db
        ]
    tohlc))

(defn nuen-orders
  "places brs and prs entry orders given inst and granularity"
  [inst granularity]
  (let [numcandles 36
        vol+ 10000
        vol- (* -1 vol+)
        [ns us] (alco/nu-finder (ds-candles inst numcandles granularity))
        cprice (-> (aloa/current-price-info inst) ;get current price
                   (get "prices")
                   (get 0)
                   (get "closeoutAsk")
                   Double/parseDouble)
        sltp-mul 2 
        sl (/ 6.0 (alco/pip-factor inst))
        tp (* sltp-mul sl)
        nubr (/ 1.0 (alco/pip-factor inst))
        nupr (/ 13.0 (alco/pip-factor inst))
        ]
    (doseq [n ns :let [nbr (- n nubr)
                       npr (+ n nupr)]] 
      (aloa/order inst vol- (+ nbr sl) (- nbr tp) nbr)
      (aloa/order inst vol+ (- npr sl) (+ npr tp) npr))
    (doseq [u us :let [ubr (+ u nubr)
                       upr (- u nupr)]] 
      (aloa/order inst vol+ (- ubr sl) (+ ubr tp) ubr)
      (aloa/order inst vol- (+ upr sl) (- upr tp) upr))))


(nuen-orders "EUR_USD" "H1")
(alco/nu-finder (ds-candles "EUR_JPY" 36 "H1"))


(defn do-nuen
  "places or cancels orders"
  [place-or-cancel granularity]
  (let [insts ["EUR_USD" "USD_JPY" "USD_CAD" "EUR_JPY" "AUD_USD" "EUR_GBP"]]
    (cond
      (= place-or-cancel "p") (map #(nuen-orders % granularity) insts)
      (= place-or-cancel "c") (map #(aloa/cancel-instrument-orders %) insts)
      :else (println "ERROR - use p/c D/H4/H1"))))


(do-nuen "p" "H4")
(do-nuen "c" "H4")


;; ds-candles tests
;; (ds-candles "EUR_USD" 2 "D")
;; (alco/nu-finder (ds-candles "USD_JPY" 36 "H1"))

;; manual place and cancel
;; (def instv ["EUR_USD" "USD_JPY" "USD_CAD" "EUR_JPY" "AUD_USD" "EUR_GBP"])
;; (def cancel-orders (map #(aloa/cancel-inst-orders %) instv) )
;; (def place-orders (map #(nuen-orders % "H1") instv))


;;5053
;;4782
;;4867
;;4647
;;4622
;;4446
;;4177
;;3987
;;3900
;;3787
;;3775 taking the br 1pip away
;;3722
;;3706

;; 4H
;;3686
;;3665
;;3646
;;3628
;;3574
;;3585
;;3625



(def as [1 2])
(def bs [3 4])

(do
  (for [a as] (println a))
  (for [b bs] (println b)))

(for [[a b] [as bs]] [(println a) (println b)])
