;;; xpt with ticks and csv data ;;;
(def csv-file "/zata/truefx/USDCAD/USDCAD-2018-12.csv")
(def nrows 999)

;; incanter dataset
(def ticks-dataset (read-dataset csv-file))

(def ds999 (sel ticks-dataset :rows (range nrows)))

(with-data ds999
  (doto
      (scatter-plot (range nrows) ($ :col3))
    view))

(mean ($ :col2 ds999))
;; => 1.3250638838838842
(sd ($ :col2 ds999))
;; => 6.044039533359644E-4
(with-data ds999
  ["mean = " (mean ($ :col2 ds999))
   "stdv = " (sd ($ :col2 ds999))])
;; => ["mean = " 1.3250638838838842 "stdv = " 6.044039533359644E-4]

(head ticks-dataset)
;; => 
|   :col0 |                 :col1 |   :col2 |   :col3 |
|---------+-----------------------+---------+---------|
| USD/CAD | 20181202 22:04:20.855 | 1.32333 |   1.325 |
| USD/CAD | 20181202 22:04:39.712 | 1.32333 | 1.32438 |
| USD/CAD | 20181202 22:04:39.768 | 1.32338 | 1.32438 |
| USD/CAD | 20181202 22:04:48.737 | 1.32338 | 1.32503 |
| USD/CAD | 20181202 22:04:48.849 | 1.32327 | 1.32503 |
| USD/CAD | 20181202 22:04:51.633 | 1.32333 |   1.325 |
| USD/CAD | 20181202 22:05:01.765 | 1.32335 | 1.32485 |
| USD/CAD | 20181202 22:05:02.883 | 1.32334 | 1.32492 |
| USD/CAD | 20181202 22:05:03.884 |  1.3233 | 1.32492 |
| USD/CAD | 20181202 22:05:04.454 | 1.32338 | 1.32492 |

($ :col3 (head ticks-dataset))
;; => (1.325 1.32438 1.32438 1.32503 1.32503 1.325 1.32485 1.32492 1.32492 1.32492)

(def m999 (to-matrix ds999))
(clojure.core.matrix/esum ds999 )
(ds/column-names ds999)





;; diversion with ticks and read-csv
(def ticks-csv (clojure.data.csv/read-csv
                (slurp csv-file))) ;need to slurp file to read-csv

(def csv999 (sel ticks-csv :rows (range nrows))) ;just a collection of strings - no columns even
(def ds-from-csv999 (to-dataset ds999)) ;change it to dataset and it is same as ds999

