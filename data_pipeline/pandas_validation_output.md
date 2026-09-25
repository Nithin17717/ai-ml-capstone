# Task 6 - Pandas Validation

## 1. pd.read_sql() - High Rated Books

```text
                                                                   title  price_gbp  rating
                                      1,000 Places to See Before You Die      26.08       5
                                  A Time of Torment (Charlie Parker #14)      48.35       5
       What Happened on Beale Street (Secrets of the South Mysteries #2)      25.37       5
The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)      52.30       5
                                       The Silkworm (Cormoran Strike #2)      23.05       5
                                                       The Girl You Lost      12.29       5
                                 A Flight of Arrows (The Pathfinders #2)      55.53       5
                                                            Mrs. Houdini      30.25       5
                                                   The Passion of Dolssa      28.32       5
                                                  Voyager (Outlander #3)      21.07       5
                                                            The Red Tent      35.66       5
                                                  Between Shades of Gray      20.79       5
                                                     While You Were Mine      41.32       5
                       A Spy's Devotion (The Regency Spies of London #1)      16.97       5
      Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      49.43       4
                                        A Year in Provence (Provence #1)      56.88       4
                                                           Sharp Objects      47.82       4
                                                     The Past Never Ends      56.50       4
                         The Murder of Roger Ackroyd (Hercule Poirot #4)      44.10       4
                   Murder at the 42nd Street Library (Raymond Ambler #1)      54.36       4
                        Delivering the Truth (Quaker Midwife Mystery #1)      20.89       4
                     The Mysterious Affair at Styles (Hercule Poirot #1)      24.80       4
  The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70       4
                                               The Marriage of Opposites      28.08       4
                                                       A Paris Apartment      39.01       4
                         World Without End (The Pillars of the Earth #2)      32.97       4
                                                   Lost Among the Living      27.70       4
```

## 2. pd.read_sql() - Price Range

```text
                                                                                            title  price_gbp  price_inr
                                                             Blood Defense (Samantha Brinkman #1)      20.30    2141.65
                                                                             Love, Lies and Spies      20.55    2168.02
                                                                           Between Shades of Gray      20.79    2193.34
                                                 Delivering the Truth (Quaker Midwife Mystery #1)      20.89    2203.90
                                                                           Voyager (Outlander #3)      21.07    2222.89
                                                                The Silkworm (Cormoran Strike #2)      23.05    2431.78
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)      23.21    2448.66
                                                              Career of Evil (Cormoran Strike #3)      24.72    2607.96
                                              The Mysterious Affair at Styles (Hercule Poirot #1)      24.80    2616.40
                                What Happened on Beale Street (Secrets of the South Mysteries #2)      25.37    2676.54
                                                               Extreme Prey (Lucas Davenport #26)      25.40    2679.70
                                                                                         Starlark      25.83    2725.06
                                                               1,000 Places to See Before You Die      26.08    2751.44
                                                                        Girl With a Pearl Earring      26.77    2824.24
                                                                 Poisonous (Max Revere Novels #3)      26.80    2827.40
                                                                                        The Widow      27.26    2875.93
                                                                            Lost Among the Living      27.70    2922.35
                                                                        The Marriage of Opposites      28.08    2962.44
                                                                            The Passion of Dolssa      28.32    2987.76
                        Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton      29.69    3132.30
                                                                                     Mrs. Houdini      30.25    3191.38
                                                                         The Great Railway Bazaar      30.54    3221.97
                                                  World Without End (The Pillars of the Earth #2)      32.97    3478.34
                                                                                The Secret Healer      34.56    3646.08
                                                                                      Most Wanted      35.28    3722.04
                                                                                     The Red Tent      35.66    3762.13
                              Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      36.94    3897.17
                                                                            The House by the Lake      36.95    3898.23
                                                                             Under the Tuscan Sun      37.33    3938.31
                                                                           The Invention of Wings      37.34    3939.37
                                                            In the Woods (Dublin Murder Squad #1)      38.38    4049.09
                                                        Neither Here nor There: Travels in Europe      38.95    4109.23
                                                                                A Paris Apartment      39.01    4115.55
```

## 3. pandas.merge() JOIN Result

```text
 book_id                                                                  title  price_gbp  price_inr  rating  in_stock      category_name
      26                                          Boar Island (Anna Pigeon #19)      59.48    6275.14       3         1            Mystery
      39 The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70    6087.35       4         1            Mystery
       8                                       A Year in Provence (Provence #1)      56.88    6000.84       4         1             Travel
      14                                                    The Past Never Ends      56.50    5960.75       4         1            Mystery
      61                                       The Last Painting of Sara de Vos      55.55    5860.52       2         1 Historical Fiction
      46                                A Flight of Arrows (The Pathfinders #2)      55.53    5858.42       5         1 Historical Fiction
      23                  Murder at the 42nd Street Library (Raymond Ambler #1)      54.36    5734.98       4         1            Mystery
      17                                         The Last Mile (Amos Decker #2)      54.21    5719.16       2         1            Mystery
      43                                    1st to Die (Women's Murder Club #1)      53.98    5694.89       1         1            Mystery
      44                                                     Tipping the Velvet      53.74    5669.57       1         1 Historical Fiction
```

## 4. SQL JOIN Result

```text
 book_id                                                                  title  price_gbp  price_inr  rating  in_stock      category_name
      26                                          Boar Island (Anna Pigeon #19)      59.48    6275.14       3         1            Mystery
      39 The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70    6087.35       4         1            Mystery
       8                                       A Year in Provence (Provence #1)      56.88    6000.84       4         1             Travel
      14                                                    The Past Never Ends      56.50    5960.75       4         1            Mystery
      61                                       The Last Painting of Sara de Vos      55.55    5860.52       2         1 Historical Fiction
      46                                A Flight of Arrows (The Pathfinders #2)      55.53    5858.42       5         1 Historical Fiction
      23                  Murder at the 42nd Street Library (Raymond Ambler #1)      54.36    5734.98       4         1            Mystery
      17                                         The Last Mile (Amos Decker #2)      54.21    5719.16       2         1            Mystery
      43                                    1st to Die (Women's Murder Club #1)      53.98    5694.89       1         1            Mystery
      44                                                     Tipping the Velvet      53.74    5669.57       1         1 Historical Fiction
```

## 5. Equivalence Check

SQL JOIN equals pandas.merge(): **True**
