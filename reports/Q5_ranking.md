# Q5 Country Prioritization Ranking

This table ranks countries using a simple, interpretable composite score based on:

- Average predicted probability of transition in the most recent window (primary driver)

- Recent emissions dynamics (`d_co2_per_capita`) as a secondary adjustment



|   rank | iso3   |   priority_score |   avg_p_transition_recentN |   latest_year |   latest_p_transition |   avg_d_co2_per_capita_recentN |
|-------:|:-------|-----------------:|---------------------------:|--------------:|----------------------:|-------------------------------:|
|      1 | USA    |            0.225 |                      0.225 |          2023 |                 0.098 |                         -0.35  |
|      2 | MEX    |            0.025 |                      0.025 |          2023 |                 0     |                         -0.008 |

