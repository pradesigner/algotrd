(defn outlier-spotter
  "finds outliers in ohlc files"
  [fp]
  (let [m (to-matrix (mk-dohlc fp))
        ops (sel m :cols 1)
        his (sel m :cols 2)
        los (sel m :cols 3)
        cls (sel m :cols 4)
        sd-factor 6
        av-his (mean his)
        sd-his (sd his)
        av-los (mean los)
        sd-los (sd los)
        hi-lim (+ av-his (* sd-his sd-factor))
        lo-lim (- av-los (* sd-los sd-factor))]
    ;(view (scatter-plot (range (nrow los)) los))
    (remove nil? (for [h his] (if (> h hi-lim) [fp h])))
    (remove nil? (for [l los] (if (< l lo-lim) [fp l])))
    ))

(outlier-spotter (get truefx-filepaths 13))

(map outlier-spotter (drop 30 truefx-filepaths))
