;;;; date time items ;;;;

;;; https://www.tutorialspoint.com/clojure/clojure_date_and_time.htm

(defn Example []
   (def date (.toString (java.util.Date.)))
   (println date))

(defn Example1 []
  (def date (.format (java.text.SimpleDateFormat. "MM/dd/yyyy")
                     (new java.util.Date)))
   (println date))

(def loch4h (read-dataset "/zata/truefx/AUDJPY/audjpy4H.csv"))

(source head)

(defn myhead
  ([len mat]
   ($ (range (min len (nrow mat))) :rows mat)))
