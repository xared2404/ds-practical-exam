
# Q5 — Country prioritization ranking

## 1. Purpose

Translate probabilistic regime detection (Q4A) into a practical prioritization tool for policymakers and multilateral institutions. The ranking measures transition readiness, not aggregate mitigation potential or fairness.

---

## 2. Construction

- Primary component: average predicted transition probability in the recent evaluation window (`avg_p_transition_recentN`).
- Diagnostic: recent `d_co2_per_capita` used to check consistency.
- Composite priority score ranks countries by readiness.

---

## 3. Interpretation

- High-ranked countries: persistent declines in per-capita emissions, stable high predicted probabilities.
- Mid-ranked: borderline or volatile signals; candidate for catalytic interventions.
- Low-ranked: weak or volatile signals; prioritize institutional capacity building.

---

## 4. Example ranking (top 30)

| rank | iso3 | priority_score | avg_p_transition_recentN | latest_year | latest_p_transition | avg_d_co2_per_capita_recentN |
|---:|:---:|---:|---:|---:|---:|---:|
| 1 | CHE | 0.897 | 0.897 | 2018 | 0.90 | |
| 2 | LUX | 0.884 | 0.884 | 2018 | 0.887 | |
| 3 | SWE | 0.884 | 0.884 | 2018 | 0.890 | |
| 4 | DNK | 0.869 | 0.869 | 2018 | 0.878 | |
| 5 | GBR | 0.862 | 0.862 | 2018 | 0.869 | |
| 6 | HKG | 0.855 | 0.855 | 2018 | 0.885 | |
| 7 | BMU | 0.844 | 0.844 | 2018 | 0.876 | |
| 8 | AUT | 0.842 | 0.842 | 2018 | 0.857 | |
| 9 | NOR | 0.841 | 0.841 | 2018 | 0.868 | |
| 10 | FIN | 0.841 | 0.841 | 2018 | 0.833 | |
| 11 | ISR | 0.837 | 0.837 | 2018 | 0.843 | |
| 12 | IRL | 0.836 | 0.836 | 2018 | 0.868 | |
| 13 | LIE | 0.832 | 0.832 | 2018 | 0.794 | |
| 14 | FRA | 0.831 | 0.831 | 2018 | 0.876 | |
| 15 | BEL | 0.827 | 0.827 | 2018 | 0.828 | |
| 16 | NLD | 0.825 | 0.825 | 2018 | 0.839 | |
| 17 | DEU | 0.823 | 0.823 | 2018 | 0.841 | |
| 18 | NZL | 0.818 | 0.818 | 2018 | 0.837 | |
| 19 | SGP | 0.818 | 0.818 | 2018 | 0.822 | |
| 20 | JPN | 0.795 | 0.795 | 2018 | 0.845 | |
| 21 | ISL | 0.781 | 0.781 | 2018 | 0.825 | |
| 22 | MAC | 0.779 | 0.779 | 2018 | 0.702 | |
| 23 | ARE | 0.744 | 0.744 | 2018 | 0.720 | |
| 24 | AUS | 0.743 | 0.743 | 2018 | 0.762 | |
| 25 | AND | 0.732 | 0.732 | 2018 | 0.756 | |
| 26 | TTO | 0.728 | 0.728 | 2018 | 0.748 | |
| 27 | CUW | 0.724 | 0.724 | 2018 | 0.661 | |
| 28 | ITA | 0.717 | 0.717 | 2018 | 0.755 | |
| 29 | CAN | 0.709 | 0.709 | 2018 | 0.720 | |
| 30 | ESP | 0.687 | 0.687 | 2018 | 0.703 | |

---

## 5. Caveats

This ranking does not reflect aggregate mitigation potential or equity considerations. Use it alongside Q2/Q3 evidence and policy judgment.

|      3 | SWE    |            0.884 |                      0.884 |          2018 |                 0.89  |                                |
|      4 | DNK    |            0.869 |                      0.869 |          2018 |                 0.878 |                                |
|      5 | GBR    |            0.862 |                      0.862 |          2018 |                 0.869 |                                |
|      6 | HKG    |            0.855 |                      0.855 |          2018 |                 0.885 |                                |
|      7 | BMU    |            0.844 |                      0.844 |          2018 |                 0.876 |                                |
|      8 | AUT    |            0.842 |                      0.842 |          2018 |                 0.857 |                                |
|      9 | NOR    |            0.841 |                      0.841 |          2018 |                 0.868 |                                |
|     10 | FIN    |            0.841 |                      0.841 |          2018 |                 0.833 |                                |
|     11 | ISR    |            0.837 |                      0.837 |          2018 |                 0.843 |                                |
|     12 | IRL    |            0.836 |                      0.836 |          2018 |                 0.868 |                                |
|     13 | LIE    |            0.832 |                      0.832 |          2018 |                 0.794 |                                |
|     14 | FRA    |            0.831 |                      0.831 |          2018 |                 0.876 |                                |
|     15 | BEL    |            0.827 |                      0.827 |          2018 |                 0.828 |                                |
|     16 | NLD    |            0.825 |                      0.825 |          2018 |                 0.839 |                                |
|     17 | DEU    |            0.823 |                      0.823 |          2018 |                 0.841 |                                |
|     18 | NZL    |            0.818 |                      0.818 |          2018 |                 0.837 |                                |
|     19 | SGP    |            0.818 |                      0.818 |          2018 |                 0.822 |                                |
|     20 | JPN    |            0.795 |                      0.795 |          2018 |                 0.845 |                                |
|     21 | ISL    |            0.781 |                      0.781 |          2018 |                 0.825 |                                |
|     22 | MAC    |            0.779 |                      0.779 |          2018 |                 0.702 |                                |
|     23 | ARE    |            0.744 |                      0.744 |          2018 |                 0.72  |                                |
|     24 | AUS    |            0.743 |                      0.743 |          2018 |                 0.762 |                                |
|     25 | AND    |            0.732 |                      0.732 |          2018 |                 0.756 |                                |
|     26 | TTO    |            0.728 |                      0.728 |          2018 |                 0.748 |                                |
|     27 | CUW    |            0.724 |                      0.724 |          2018 |                 0.661 |                                |
|     28 | ITA    |            0.717 |                      0.717 |          2018 |                 0.755 |                                |
|     29 | CAN    |            0.709 |                      0.709 |          2018 |                 0.72  |                                |
|     30 | ESP    |            0.687 |                      0.687 |          2018 |                 0.703 |                                |

How to Use This Ranking

This ranking should be used as an input to strategic allocation decisions, not as a standalone prescription.

In practical terms:
	•	Top-ranked countries are strong candidates for scaling investments, where marginal capital is likely to yield fast and durable emissions reductions.
	•	Mid-ranked countries correspond to the “marginal transition” category in Q5 and may require targeted, catalytic interventions.
	•	Lower-ranked countries are better suited for long-horizon institutional or capacity-building strategies rather than immediate mitigation deployment.

⸻

Important Caveat

This ranking does not measure global mitigation impact, emissions responsibility, or fairness considerations. Countries with high scores tend to be smaller and institutionally strong, reflecting high readiness rather than large aggregate emissions reductions.

Accordingly, the ranking should be interpreted as identifying where interventions are most likely to succeed, not where they are most morally or historically justified.


