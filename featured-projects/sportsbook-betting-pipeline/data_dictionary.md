# Data Dictionary — NFL Sports Betting Pipeline

---

## Betting_Log

| Field | Key | Type | Null | Description |
|-------|-----|------|------|-------------|
| Bet_ID | PK | SERIAL | NOT NULL | Unique identifier for each bet placed |
| Customer_ID | FK → Customer | INT | NOT NULL | Customer who placed the bet |
| Game_Code | FK → Schedule | VARCHAR(30) | NOT NULL | Game identifier, formatted as `YYYYWW-HOME-AWAY` (e.g. `202301-KC-DET`) |
| Bet_On | | VARCHAR(30) | NOT NULL | Team name (line bet) or `over`/`under`/`push` (over-under bet) |
| Bet_Amount | | SMALLINT | NOT NULL | Dollar amount bet (1–20,000), excluding commission |
| Result | | VARCHAR(4) | NOT NULL | Outcome: `win`, `loss`, or `push` |
| Commission | | NUMERIC(7,2) | NOT NULL | Commission collected on the bet |

---

## Customer

| Field | Key | Type | Null | Description |
|-------|-----|------|------|-------------|
| Customer_ID | PK | SERIAL | NOT NULL | Unique customer identifier |
| First_Name | | VARCHAR(25) | NOT NULL | Customer first name |
| Last_Name | | VARCHAR(25) | | Customer last name |
| Age | | SMALLINT | | Age, rounded down to nearest whole number |
| Customer_Type | | VARCHAR(10) | | Betting method: `local`, `online`, or `phone` |
| Customer_Since | | SMALLINT | | Year first recorded (≥ 1900, not future) |
| Customer_Income | | INT | | Annual income in USD (> 0) |
| Household_Size | | SMALLINT | | Number of people in household (1–15) |
| Mode_Color | | VARCHAR(6) | | Personality type: `red`, `yellow`, `blue`, `orange`, `green`, `purple`, `black`, or `white` |

---

## Schedule

| Field | Key | Type | Null | Description |
|-------|-----|------|------|-------------|
| Game_ID | PK | SERIAL | NOT NULL | Auto-incrementing game identifier |
| Game_Code | | VARCHAR(30) | NOT NULL | Formatted game code (`YYYYWW-HOME-AWAY`) |
| Game_Date | | DATE | | Date played (YYYY-MM-DD) |
| Schedule_Season | | SMALLINT | | Year the game was played |
| Schedule_Week | | CHAR(2) | | Week number (01–22) |
| Schedule_Playoff | | BOOLEAN | | TRUE for weeks 19–22 (playoffs) |
| Home_Team_ID | FK → Teams | VARCHAR(3) | NOT NULL | Home team ID |
| Score_Home | | SMALLINT | | Home team final score |
| Away_Team_ID | FK → Teams | VARCHAR(3) | NOT NULL | Away team ID |
| Score_Away | | SMALLINT | | Away team final score |
| Team_Favorite_ID | | VARCHAR(4) | NOT NULL | Sportsbook favorite team ID |
| Spread_Favorite | | NUMERIC(3,1) | | Point spread for the favorite (negative value) |
| Over_Under_Line | | NUMERIC(3,1) | | Expected combined score |
| Stadium_ID | FK → Stadium | INT | | Stadium where game was played |
| Stadium_Neutral | | BOOLEAN | | TRUE if neutral site game |
| Weather_Temp | | SMALLINT | | Temperature at game time (°F) |
| Weather_Wind_MPH | | SMALLINT | | Wind speed at game time (MPH, ≥ 0) |
| Weather_Humidity | | SMALLINT | | Relative humidity (0–100%) |
| Weather_Detail | | VARCHAR(25) | | Weather condition: `fog`, `indoor`, `rain`, `snow`, etc. |
| Winner_Line | | CHAR(4) | | Spread winner: `home`, `away`, or `push` |
| Winner_ou | | VARCHAR(5) | | Over-under result: `over`, `under`, or `push` |

---

## Stadium

| Field | Key | Type | Null | Description |
|-------|-----|------|------|-------------|
| Stadium_ID | PK | SERIAL | NOT NULL | Unique stadium identifier |
| Stadium_Name | | VARCHAR(50) | NOT NULL | Stadium name |
| Stadium_Location | | VARCHAR(40) | | City and state |
| Stadium_Open | | SMALLINT | | Year opened (1900–present) |
| Stadium_Close | | SMALLINT | | Year closed (≥ Stadium_Open) |
| Stadium_Type | | VARCHAR(12) | | `indoor`, `outdoor`, or `retractable` |
| Stadium_Address | | VARCHAR(120) | | Full street address |
| Stadium_Capacity | | INT | | Max capacity (0–200,000) |
| Stadium_Surface | | VARCHAR(25) | | Playing surface type |
| Stadium_Weather_Station_Code | | VARCHAR(25) | | Postal code / weather station code |
| Stadium_Weather_Type | | VARCHAR(10) | | Typical weather: `moderate`, `cold`, or `dome` |
| STATION | | CHAR(11) | | Weather station unique ID |
| Station_Name | | VARCHAR(55) | | Weather station location name |
| Latitude | | NUMERIC(8,5) | | Station latitude (-90 to 90) |
| Longitude | | NUMERIC(8,5) | | Station longitude (-180 to 180) |
| Elevation | | NUMERIC(5,1) | | Meters above sea level |

---

## Teams

| Field | Key | Type | Null | Description |
|-------|-----|------|------|-------------|
| Team_PK | PK | SERIAL | NOT NULL | Unique team identifier |
| Team_Name | | VARCHAR(30) | NOT NULL | Full team name |
| Team_Name_Short | | VARCHAR(20) | NOT NULL | Short/marketing name |
| Team_ID | | VARCHAR(3) | NOT NULL | 2–3 letter team ID |
| Team_ID_PFR | | CHAR(3) | NOT NULL | Pro Football Reference 3-letter ID |
| Team_Conference | | CHAR(3) | | `NFC` or `AFC` |
| Team_Division | | VARCHAR(15) | | Division (e.g. `AFC North`) |
| Team_Conference_Pre2002 | | CHAR(3) | | Pre-2002 conference |
| Team_Division_Pre2002 | | VARCHAR(15) | | Pre-2002 division |

---

## Exception

| Field | Key | Type | Null | Description |
|-------|-----|------|------|-------------|
| Exception_ID | PK | SERIAL | NOT NULL | Unique identifier for the problematic row |
| Row_Data | | TEXT | NOT NULL | Full pipe-delimited raw row that failed validation |
| Filename | | VARCHAR(50) | NOT NULL | Source filename for traceability |
