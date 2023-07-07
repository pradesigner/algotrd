"
REDO to fit algotrd system
commonly used libs for algotrd
"

(ns pradesigner.algolibs
  "core functions which can be used for any price analyses"
  (:require [clojure.string :as str]
            [tablecloth.api :as tc]))


(def fpaths-truefx
  "produces a list of truefx path strings"
  (sort (filter #(re-find #"1D|4H|1H" %)
                (map #(.getPath %)
                     (file-seq (clojure.java.io/file "/home/truefx"))))))

(defn fname-from-fpath
  "gets filename from a given filepath"
  [filepath]
  (last (str/split filepath #"/")))

(defn pip-factor
  "calculates pip-factor based on JPY pairs"
  [instrument]
  (if (str/includes? (str/lower-case instrument) "jpy")
    100
    10000))

(defn pips
  "calculates directional pip difference from pt1 to pt2 given pip-factor"
  [pt1 pt2 pipfactor]
  (Math/round (* pipfactor (- pt2 pt1))))

(defn dohlc>ds
  "creates dataset dohlc"
  [itm]
  (-> itm
      (tc/dataset {:header-row? false})
      (tc/rename-columns {"column-0" :d
                          "column-1" :o
                          "column-2" :h
                          "column-3" :l
                          "column-4" :c})))

(defn maxmin?
  "determines if itm is max or min of coll"
  [mm itm coll]
  (= itm (apply mm coll)))

(defn renu
  "cleans up nu keeping only legitimate items"
  [nu mm]
  (loop [tmp nu
         fin []]
    (if (empty? tmp)
      fin
      (if (maxmin? mm (first tmp) tmp)
        (recur (rest tmp) (conj fin (first tmp)))
        (recur (rest tmp) fin)))))

(defn nu-finder
  "finds nu given a tohlc dataset and &partition-size
  using partitions and nuf function returns [[nn] [uu]]"
  [dohlc & [ps]]
  (let [size (tc/row-count dohlc)
        part-size (or ps 7)
        midpt (quot part-size 2)
        hi-parts (partition part-size 1 (:high dohlc))
        lo-parts (partition part-size 1 (:low dohlc))
        nuf (fn [parts mm]
              (let [nu (for [p parts
                             :let [itm (nth p midpt)]
                             :when (maxmin? mm itm p)]
                         itm)]
                (renu nu mm)))]
    [(nuf hi-parts max) (nuf lo-parts min)]))
