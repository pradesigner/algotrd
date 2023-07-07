"
lyzer uses tfx data to find consistent patterns

TODO
"

(ns user
  (:require [tablecloth.api :as tc]
            [tech.v3.datatype.functional :as dfn]
            [pradesigner.io :as io]))

(def ds (io/dohlc>ds "resources/tfx/USDCAD/usdcad1D.csv"))

(defn avg
  "calculates averages"
  [& rest]
  (let [k (count rest)
        s (apply + rest)]
    (/ s k)))

(defn mids
  "calculates midpt between 2 values"
  ([ds] ;hilo midpt
   (tc/add-column ds
                  :mid
                  (map #(avg % %2) (ds :h) (ds :l))))
  ([ds lcol fcol] ;midpt btw any 2 of ohlc
   (tc/add-column ds
                  :mid
                  (map #(avg % %2) (ds lcol) (ds fcol)))))

(tc/head (mids ds :h :c))


(defn diff
  "produces new column calculating differences offset by n from given column"
  [ds colnam period difcolnam]
  (let [rowk (tc/row-count ds)]
    (when (> rowk period)
      (let [offset (- rowk period)
            col (ds colnam)
            cal (map #(- % %2)
                     (tc/tail col offset)
                     (tc/head col offset))
            blanks (repeat period :nan)]
        (tc/add-column ds
                   difcolnam
                   (concat blanks cal))))))

(tc/head (diff ds :c 4 :differ))

