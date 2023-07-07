(ns oas.core
  (:gen-class)
  (:require [oas.nuen]
            [oas.oandpts]))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!")
  ;(oas.nuen/do-nuen "blahblah" "H")
  (println (oas.oandpts/accounts)))
