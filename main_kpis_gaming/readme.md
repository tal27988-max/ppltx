


# Main KPIs – Gaming Analytics

## Project Overview

This project calculates the main business and product KPIs for a gaming application using SQL and BigQuery.

The analysis is based on player activity, installation events, and in-app purchase data from the following source table:

```sql
`ppltx-ba-course.ds_game.fact`
```

The goal of the project is to understand:

- How many users install and play the game
- How active the players are
- How many players return after installation
- How much revenue the game generates
- What percentage of players make a purchase

---

## Project Structure

```text
main_kpis_gaming/
│
├── DAU.sql
├── installs.sql
├── retention.sql
├── revenue.sql
└── user_explore.sql
```



---

## Main KPIs

| Category | KPI | Description |
|---|---|---|
| Acquisition | Installs | Number of new players who installed the game |
| Engagement | DAU | Unique active users per day |
| Engagement | WAU | Unique active users per week |
| Engagement | MAU | Unique active users per month |
| Retention | Retention | Percentage or number of users returning after installation |
| Monetization | Revenue | Total revenue from in-app purchases |
| Monetization | ARPU | Average revenue per user |
| Monetization | ARPPU | Average revenue per paying user |
| Monetization | ARPDAU | Average revenue per daily active user |
| Monetization | Paying Users | Unique users who made a purchase |
| Monetization | Conversion Rate | Percentage of users who made a purchase |



---



## SQL Files

### `installs.sql`

Calculates the installation date for each player.

The installation date is defined as the first recorded activity date of the user:

```sql
DATE(MIN(event_time))
```

This query can be used to calculate:

- Install date per user
- Number of installs per day
- Installation cohorts

---

### `DAU.sql`

Calculates active-user metrics.

Main metrics:

- **DAU – Daily Active Users**  
  Number of unique users who were active on a specific day.

- **WAU – Weekly Active Users**  
  Number of unique users who were active during a seven-day period.

- **MAU – Monthly Active Users**  
  Number of unique users who were active during a monthly period.

These metrics help measure the size and engagement level of the game's active user base.

---

### `retention.sql`

Calculates player retention after installation.

The query:

1. Finds the installation date of every user.
2. Finds every date on which the user was active.
3. Calculates the number of days between the activity date and the installation date.
4. Counts the number of users who returned on each day.

Example retention periods:

- Day 1 Retention
- Day 2 Retention
- Day 7 Retention
- Day 14 Retention
- Day 30 Retention

Retention helps measure whether players continue using the game after installing it.

---

### `revenue.sql`

Calculates the main monetization KPIs based on in-app purchases.

Main metrics:

- **Total Revenue**  
  Total income generated from in-app purchases.

- **Paying Users**  
  Number of unique users who completed at least one purchase.

- **ARPU – Average Revenue Per User**

```text
Total Revenue / Total Users
```

- **ARPPU – Average Revenue Per Paying User**

```text
Total Revenue / Paying Users
```

- **ARPDAU – Average Revenue Per Daily Active User**

```text
Daily Revenue / DAU
```

- **Conversion Rate**

```text
Paying Users / Total Users
```

The conversion rate shows the percentage of users who became paying users.

---

### `user_explore.sql`

Used for initial data exploration and validation.

The query helps examine:

- Available event types
- User activity
- Purchase events
- Event dates
- Price values
- Duplicate or missing records
- General structure of the source data

This file supports the development and validation of the KPI queries.


---

## Technologies

- SQL
- Google BigQuery
- Git
- GitHub

---

## How to Run

1. Open the required `.sql` file.
2. Make sure the source table path matches your BigQuery environment.
3. Run the query in the BigQuery SQL workspace.
4. Review the results and validate the calculated KPI.

---

## Project Goal

The project creates a basic KPI layer for a gaming application.

It provides a clear view of:

- User acquisition
- Player engagement
- Player retention
- Revenue performance
- User conversion into paying players

These metrics can later be used as a data source for dashboards, reports, and further business analysis.
