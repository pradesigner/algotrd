"
barchar explores characteristics of bars and subsequent effects

TODO
see prev candle has any bearing on next one - some patterns?
examine diff and graph +- histograms of close or avg prices? 
relate to ticks?
classify pa based on clop, bias, as well as comb possibilities
since clop0-clop1 corr is .97, is there a pattern to when that is broken?
strong corr may not be necessary if we are looking for pips perhaps
"


(defn adjacent-confluence
  "
  determines oc confluence behavior of adjacent bars

  (map adjacent-confluence truefx-filepaths)
  (map adjacent-confluence (take 15 truefx-filepaths))
  (mean (map adjacent-confluence (drop 30 truefx-filepaths)))
  "
  [filepath]
  (let [[ops his los cls filename pipfactor] (instrument-info filepath)
        co (map pips cls ops (repeat pipfactor))
        pn (map #(pos? (* %1 %2)) co (drop 1 co))
        p% (Math/round (/ (count (filter true? pn)) (float (count pn)) 0.01))]
    (printf "%s %d %n" filename p%)
    p%))

(defn adjacent-confluence
  "determines oc confluence behavior of adjacent bars"
  [fpath]
  (let [d1 (b/mk-tohlc fpath)
        d2 (ds/new-column d1 :oc (dfn/- (:close d1) (:open d1)))
        ]
    d2))

(adjacent-confluence (first b/fpaths-truefx))

;;results for uu|dd are all near or under 50%
;;though decreasing as timeframe gets smaller suggesting that difluence may have good chance


(defn anulysis
  "
  analyzes brs and prs price action on nu

  dohlc dataset columns :d date :o open :h high :l low :c close
  identify nu using partition
  map bsr? psr? to hilo and determine how many of each
  "
  [filepath]
  (let [[dohlc filename pipfactor] (instrument-dohlc filepath)
        dohlc (d/select-rows dohlc (range 33))
        dohlc-size (nrow dohlc) ;size of dataset less 2 because of header
        buffer (/ 12.0 pipfactor) ;buffer line calculation in pips for pair
        part-size 7 ;size of partition chosen
        [nseq useq] (nu-finder dohlc)

        brs? (fn [nu cl hilo >< -+]
               "n: (brs? n cl hi < -) u: (bsr? u cl lo > +)"
               (and (btn? hilo (- nu buffer) (+ nu buffer))
                    (>< cl (-+ nu buffer))))
        prs? (fn [nu cl hilo1 hilo2 >< -+]
               "n: (prs? n cl hi lo > +) u: (prs? u cl lo hi < -"
               (and (>< cl nu)
                    (>< hilo1 (-+ nu buffer))
                    (>< nu hilo2)))
        ;; v0
        ratios (fn [rs nu-seq]
                 (loop [nu nu-seq
                        brs 0
                        prs 0
                        i 0]
                   (if (or (> i (- dohlc-size part-size))
                           (empty? nu))
                     [brs prs]
                     (let [nu0 (first nu-seq)
                           hi ($ i :h dohlc)
                           lo ($ i :l dohlc)
                           cl ($ i :c dohlc)
                           [is-brs is-prs] (if (= rs "r")
                                             [(brs? nu0 cl hi < -) (prs? nu0 cl hi lo > +)]
                                             [(brs? nu0 cl lo > +) (prs? nu0 cl lo hi < -)])
                           ]
                       (cond
                         is-brs (recur nu (inc brs) prs (inc i))
                         is-prs (recur (drop 1 nu) brs (inc prs) (inc i))
                         :else (recur nu brs prs (inc i)))))))
        
        n-ratio (ratios "r" nseq)
        u-ratio (ratios "s" useq)
        ]
    ;;    [n-ratio1 u-ratio1 n-ratio u-ratio]
    [n-ratio u-ratio]
    ))

(anulysis (first truefx-filepaths))
;; => [[3 3] [4 4]] 33
;; the brs and prs are being counted before the nu forms -> alter algorithm

(view (anulysis (first truefx-filepaths)))

;; => [215 220]
;; => [288 302]


