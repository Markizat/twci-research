## Can Citizens Verify a Water Treaty? Measuring Observability and Opacity in the Ural (Zhayik) Basin

## 1. What this project is

This project examines whether citizens can independently verify the implementation of transboundary water agreements using publicly available information. It focuses on the Ural (Zhayik) River agreements between Kazakhstan and Russia and compares their observability with obligations in the 1998 Syr Darya agreement. The main question is: which treaty obligations can citizens verify using open information, and which remain difficult to check?

## 2. How it works

The project uses the Citizen Verifiability Index (CVI) to assess treaty obligations across three dimensions:

* Accessibility: whether relevant information is publicly accessible.
* Clarity: whether the obligation and responsible parties are clearly specified.
* Timeliness: whether information is available within a useful timeframe.

Each dimension is scored from 0 to 2. The total score is converted into a percentage of the maximum possible score.

The analysis covers 56 obligations from the Ural agreements and 11 obligations from the 1998 Syr Darya agreement.

A separate satellite-data analysis uses Sentinel-2 SR_HARMONIZED imagery in Google Earth Engine. It examines water-surface observations at Iriklinskoye Reservoir and Shardara Reservoir during 2015–2024. A Bayesian analysis using three priors is also included. Satellite observations measure water-surface area, not water volume or treaty compliance directly.

## 3. Main results

* H1 — Ural observability: The Ural CVI is 18.45%, below the 50% threshold. The hypothesis is supported.
* H2 — Information exchange vs. water-volume obligations: The observed averages were 0.83 and 0.50, respectively. The difference was in the opposite direction to the predicted one, and its interval included zero.
* H3 — Public disclosure: Explicit public-disclosure obligations account for 1.8% (1/56) of Ural obligations. The hypothesis is supported.
* H4 — Satellite observations: For Iriklinskoye, the estimated water-area trend was −0.20 km²/year, with a 95% credible interval of [−0.66, +0.26]. The interval includes zero, so the trend direction is not established. Under the OSF decision rule, H4 is supported because water-surface area was assessed; water volume was not obtained from satellite data.
* H7 — Cross-river comparison: The Ural CVI was 18.45%, compared with 27.27% for the Syr Darya. The difference was +8.82 percentage points, with an interval of [−0.24, 18.53]. The interval includes zero, so the comparison is inconclusive.
* H8 — Institutional responsibilities: Joint-commission obligations had a CVI of 28.12%, compared with 14.71% for obligations assigned to the two states. This comparison is descriptive.
* H9 — Confidentiality: 5.4% (3/56) of Ural obligations were classified as confidentiality-restricted.
* H5 and H6: These hypotheses were not completed in this version. No information requests were sent for H5, and the flood chronology required for H6 was not completed.

## 4. Limitations

The Syr Darya analysis includes only 11 obligations. Its inter-rater Cohen’s kappa for Clarity was 0.25, indicating limited agreement. Satellite observations are incomplete: only 65 of 120 months were valid for Iriklinskoye. The Shardara study area also included nearby lakes, so its measured water area cannot be attributed exclusively to the reservoir. Missing or invalid months were not filled with estimated values. In addition, the 2010 Ural agreement text is a draft version.

5. Files

* code/ — contains analysis.py and twci_2_bayes.py for analysis and Bayesian calculations.
* data/ — contains ural.csv, syrdarya.csv, monthly Iriklinskoye and Shardara data files, and Blind Spot Register lists.
* results/ — contains results_H1-H9.txt, area-change results, and trend files for the three priors.
* notebooks/ — contains TWCI_1_satellite.ipynb and TWCI_2_bayes.ipynb.

## 6. Preregistration and deviations

The research plans were preregistered on OSF:
 [OSF Registration #1](https://osf.io/h3wgn)
 [OSF Registration #2](https://osf.io/z4vde)

Deviations from the preregistrations are documented in the Deviation Log.

## 7. AI use and transparency

Claude and ChatGPT were used for selected research-support tasks, including text editing, method explanations, and code-related assistance. The researcher made the research decisions, evaluated treaty obligations, entered the scores, and determined the final interpretations. Further details are provided in the Disclosure Log.

## 8. Contact and license

Author: Markizat Rakhymzhankyzy

See the LICENSE file for licensing terms.
