# SQL Query Results

## Query 1 - WHERE

### SQL Query

```sql
SELECT
        title,
        price_gbp,
        rating,
        in_stock
    FROM books
    WHERE rating >= 4;
```

### Output

```
                                                                   title  price_gbp  rating  in_stock
      Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      49.43       4         1
                                        A Year in Provence (Provence #1)      56.88       4         1
                                      1,000 Places to See Before You Die      26.08       5         1
                                                           Sharp Objects      47.82       4         1
                                                     The Past Never Ends      56.50       4         1
                         The Murder of Roger Ackroyd (Hercule Poirot #4)      44.10       4         1
                                  A Time of Torment (Charlie Parker #14)      48.35       5         1
                   Murder at the 42nd Street Library (Raymond Ambler #1)      54.36       4         1
       What Happened on Beale Street (Secrets of the South Mysteries #2)      25.37       5         1
The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)      52.30       5         1
                        Delivering the Truth (Quaker Midwife Mystery #1)      20.89       4         1
                     The Mysterious Affair at Styles (Hercule Poirot #1)      24.80       4         1
                                       The Silkworm (Cormoran Strike #2)      23.05       5         1
  The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70       4         1
                                                       The Girl You Lost      12.29       5         1
                                 A Flight of Arrows (The Pathfinders #2)      55.53       5         1
                                                            Mrs. Houdini      30.25       5         1
                                               The Marriage of Opposites      28.08       4         1
                                                       A Paris Apartment      39.01       4         1
                         World Without End (The Pillars of the Earth #2)      32.97       4         1
                                                   The Passion of Dolssa      28.32       5         1
                                                  Voyager (Outlander #3)      21.07       5         1
                                                            The Red Tent      35.66       5         1
                                                  Between Shades of Gray      20.79       5         1
                                                     While You Were Mine      41.32       5         1
                                                   Lost Among the Living      27.70       4         1
                       A Spy's Devotion (The Regency Spies of London #1)      16.97       5         1
```

## Query 2 - ORDER BY

### SQL Query

```sql
SELECT
        title,
        price_gbp,
        price_inr
    FROM books
    ORDER BY price_inr DESC;
```

### Output

```
                                                                                            title  price_gbp  price_inr
                                                                    Boar Island (Anna Pigeon #19)      59.48    6275.14
                           The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70    6087.35
                                                                 A Year in Provence (Provence #1)      56.88    6000.84
                                                                              The Past Never Ends      56.50    5960.75
                                                                 The Last Painting of Sara de Vos      55.55    5860.52
                                                          A Flight of Arrows (The Pathfinders #2)      55.53    5858.42
                                            Murder at the 42nd Street Library (Raymond Ambler #1)      54.36    5734.98
                                                                   The Last Mile (Amos Decker #2)      54.21    5719.16
                                                              1st to Die (Women's Murder Club #1)      53.98    5694.89
                                                                               Tipping the Velvet      53.74    5669.57
                         The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1)      52.30    5517.65
                                                The Guernsey Literary and Potato Peel Pie Society      49.53    5225.42
                               Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond      49.43    5214.86
                               See America: A Celebration of Our National Parks & Treasured Sites      48.87    5155.78
                                                           A Time of Torment (Charlie Parker #14)      48.35    5100.92
                                                                                    Sharp Objects      47.82    5045.01
                                                                            Girl in the Blue Coat      46.83    4940.56
                                                  Glory over Everything: Beyond The Kitchen House      45.84    4836.12
                                                                          It's Only the Himalayas      45.17    4765.44
                                                                               A Summer In Europe      44.34    4677.87
                                                  The Murder of Roger Ackroyd (Hercule Poirot #4)      44.10    4652.55
                                                                                       The Exiled      43.45    4583.98
                                                                              While You Were Mine      41.32    4359.26
                                                                                A Paris Apartment      39.01    4115.55
                                                        Neither Here nor There: Travels in Europe      38.95    4109.23
                                                            In the Woods (Dublin Murder Squad #1)      38.38    4049.09
                                                                           The Invention of Wings      37.34    3939.37
                                                                             Under the Tuscan Sun      37.33    3938.31
                                                                            The House by the Lake      36.95    3898.23
                              Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel      36.94    3897.17
                                                                                     The Red Tent      35.66    3762.13
                                                                                      Most Wanted      35.28    3722.04
                                                                                The Secret Healer      34.56    3646.08
                                                  World Without End (The Pillars of the Earth #2)      32.97    3478.34
                                                                         The Great Railway Bazaar      30.54    3221.97
                                                                                     Mrs. Houdini      30.25    3191.38
                        Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton      29.69    3132.30
                                                                            The Passion of Dolssa      28.32    2987.76
                                                                        The Marriage of Opposites      28.08    2962.44
                                                                            Lost Among the Living      27.70    2922.35
                                                                                        The Widow      27.26    2875.93
                                                                 Poisonous (Max Revere Novels #3)      26.80    2827.40
                                                                        Girl With a Pearl Earring      26.77    2824.24
                                                               1,000 Places to See Before You Die      26.08    2751.44
                                                                                         Starlark      25.83    2725.06
                                                               Extreme Prey (Lucas Davenport #26)      25.40    2679.70
                                What Happened on Beale Street (Secrets of the South Mysteries #2)      25.37    2676.54
                                              The Mysterious Affair at Styles (Hercule Poirot #1)      24.80    2616.40
                                                              Career of Evil (Cormoran Strike #3)      24.72    2607.96
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)      23.21    2448.66
                                                                The Silkworm (Cormoran Strike #2)      23.05    2431.78
                                                                           Voyager (Outlander #3)      21.07    2222.89
                                                 Delivering the Truth (Quaker Midwife Mystery #1)      20.89    2203.90
                                                                           Between Shades of Gray      20.79    2193.34
                                                                             Love, Lies and Spies      20.55    2168.02
                                                             Blood Defense (Samantha Brinkman #1)      20.30    2141.65
                                                                             In a Dark, Dark Wood      19.63    2070.96
                                                        The Cuckoo's Calling (Cormoran Strike #1)      19.21    2026.66
                                                                                      Lilac Girls      17.28    1823.04
                                                A Spy's Devotion (The Regency Spies of London #1)      16.97    1790.33
                                                          A Study in Scarlet (Sherlock Holmes #1)      16.73    1765.02
                                                                                 A Murder in Time      16.64    1755.52
                                                       The Constant Princess (The Tudor Court #1)      16.62    1753.41
                                                        The Girl In The Ice (DCI Erika Foster #1)      15.85    1672.18
                                                           That Darkness (Gardiner and Renner #1)      13.92    1468.56
                                                                                Playing with Fire      13.71    1446.41
                                                                                The Girl You Lost      12.29    1296.59
                                                                       Hide Away (Eve Duncan #20)      11.84    1249.12
                                                             Tastes Like Fear (DI Marnie Rome #3)      10.69    1127.79
```

## Query 3 - LIMIT

### SQL Query

```sql
SELECT
        title,
        price_gbp,
        rating
    FROM books
    ORDER BY price_gbp DESC
    LIMIT 10;
```

### Output

```
                                                                 title  price_gbp  rating
                                         Boar Island (Anna Pigeon #19)      59.48       3
The No. 1 Ladies' Detective Agency (No. 1 Ladies' Detective Agency #1)      57.70       4
                                      A Year in Provence (Provence #1)      56.88       4
                                                   The Past Never Ends      56.50       4
                                      The Last Painting of Sara de Vos      55.55       2
                               A Flight of Arrows (The Pathfinders #2)      55.53       5
                 Murder at the 42nd Street Library (Raymond Ambler #1)      54.36       4
                                        The Last Mile (Amos Decker #2)      54.21       2
                                   1st to Die (Women's Murder Club #1)      53.98       1
                                                    Tipping the Velvet      53.74       1
```

## Query 4 - DISTINCT

### SQL Query

```sql
SELECT DISTINCT
        rating
    FROM books
    ORDER BY rating;
```

### Output

```
 rating
      1
      2
      3
      4
      5
```

## Query 5 - BETWEEN

### SQL Query

```sql
SELECT
        title,
        price_gbp,
        price_inr
    FROM books
    WHERE price_gbp BETWEEN 20 AND 40
    ORDER BY price_gbp;
```

### Output

```
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

## Query 6 - JOIN

### SQL Query

```sql
SELECT
        b.book_id,
        b.title,
        b.price_gbp,
        b.price_inr,
        b.rating,
        b.in_stock,
        c.category_name
    FROM books b
    JOIN categories c
        ON b.category_id = c.category_id
    ORDER BY b.price_gbp DESC
    LIMIT 10;
```

### Output

```
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

