"
io functions for algotrd
"

(ns pradesigner.io
  "processes io for various data"
  (:require [tablecloth.api :as tc]))

(defn dohlc>ds
  "puts dohlc into dataset renaming columns to dohlc"
  [fpath]
  (-> (tc/dataset fpath
                  {:header-row? false})
      (tc/rename-columns {"column-0" :d
                          "column-1" :o
                          "column-2" :h
                          "column-3" :l
                          "column-4" :c})))


