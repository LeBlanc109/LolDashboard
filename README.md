# 🎮 League of Legends Performance Dashboard

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Riot Games API](https://img.shields.io/badge/Riot%20Games-D32936?style=for-the-badge&logo=riotgames&logoColor=white)

---

## 📋 Overview (SIMPLY PROOF OF CONCEPT)

I'm REALLY bad at League of Legends, so in order to get better I thought I'd take a look at the stats to see where I could improve, but due to the overwhelming amount of data points provided by Riot, I was quickly overwhelmed. 
That led me to creating this project, a custom Power BI dashboard, showcasing raw match timeline data from the Riot Games API into actionable insights through interactive visualizations.
The goal of this project is to lay a strong foundation from which we can create more advanced stats, and hope to expose new insights by studying and analyzing the information available, by providing:

- **Frame-by-frame performance tracking** (gold, CS, damage over time)
- **Lane opponent comparisons** (CS diff, gold diff, kill matchups)
- **Team contribution metrics** (damage share, tank score, kill participation)
- **Vision control analysis** (wards placed/cleared, vision score)
- **Rank benchmarking** (compare your stats vs Silver (because I am a Silver) average)

---

## 🖼️ Dashboard Preview
![Proof_of_concept](https://github.com/LeBlanc109/LolDashboard/blob/00cb67299c62a70d1053717955da533567a84eca/images/page_1_proof.png)
![Dashboard](https://github.com/LeBlanc109/LolDashboard/blob/00cb67299c62a70d1053717955da533567a84eca/images/page_1_rough.png)
![Cont_proofs](https://github.com/LeBlanc109/LolDashboard/blob/00cb67299c62a70d1053717955da533567a84eca/images/page_2_proof.png)

> *Actual UX designed dash + additional pages as mentioned below coming soon*

##
### Pages I'd LIKE TO Include:
1. **Overview** - KDA, CS, Vision, Result at a glance
2. **Damage Analysis** - Efficiency gauge, damage over time, trade balance
3. **Team Comparison** - Tank score distribution, gold advantage timeline
4. **Kill Analysis** - Kill matrix (who killed who), death timeline
5. **Vision Control** - Wards placed/cleared by player
6. **Lane Matchup** - Direct comparison vs lane opponent
7. **Rank Comparison** - Your performance vs Silver average

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Riot Games    │      │     Python      │      │    Power BI     │
│      API        │ ───▶ │   Processing    │ ───▶ │   Dashboard     │
│                 │      │                 │      │                 │
│ • Match Timeline│      │ • Data Cleaning │      │ • DAX Measures  │
│ • Match Info    │      │ • Flattening    │      │ • Visualizations│
│ • Ranked Data   │      │ • Enrichment    │      │ • Interactivity │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

## 📊 Data Model

### Tables

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `df1` | Player stats per frame (minute) | `frame`, `player_gamertag`, `position`, `team`, `totalGold`, `creep_score`, `totalDamageDoneToChampions` |
| `events_df` | Game events | `type`, `killerId`, `victimId`, `creatorId`, `timestamp`, `winningTeam` |
| `rank_df` | Silver rank benchmarks | Same structure as df1, aggregated across Silver games |
| `PlayerSelector` | Slicer table | `player_gamertag` |

### Event Types Tracked

| Event | Use Case |
|-------|----------|
| `CHAMPION_KILL` | K/D/A, Kill matrix |
| `WARD_PLACED` | Vision score |
| `WARD_KILL` | Vision score |
| `BUILDING_KILL` | Objective tracking |
| `ELITE_MONSTER_KILL` | Dragon/Baron participation |
| `TURRET_PLATE_DESTROYED` | Early gold tracking |
| `GAME_END` | Win/Loss determination |

---

## 📈 DAX Measures

### Core Metrics
- `PlayerKills`, `PlayerDeaths`, `PlayerAssists`
- `PlayerKDA` - (K+A) / max(D,1)
- `PlayerCS`, `LaneAvgCS`, `PlayerCS - LaneAvgCS`
- `PlayerResult` - WIN/LOSS

### Damage Analysis
- `PlayerDamageEfficiency` - Damage dealt / Damage taken
- `PlayerTradeBalance` - Net damage (dealt - taken)
- `PlayerTankScore` - % of team damage absorbed
- `PlayerDamageShare` - % of team damage dealt

### Economy
- `PlayerGPM` - Gold per minute
- `PlayerCSPM` - CS per minute
- `PlayerGoldShare` - % of team gold

### Vision
- `PlayerWardsPlaced`, `PlayerWardsCleared`
- `PlayerVisionScore` - Combined wards placed + cleared

### Lane Analysis
- `PlayerLaneOpponent` - Identifies opposing laner
- `PlayerCS_VsLaneOpponent` - CS differential
- `PlayerGold_VsLaneOpponent` - Gold differential
- `PlayerCSDiff_At10`, `PlayerCSDiff_At15` - Timed snapshots

### Rank Comparison
- `PlayerCS_VsRank` - Your CS vs Silver average
- `PlayerGold_VsRank` - Your gold vs Silver average

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Power BI Desktop
- Riot Games API Key ([Get one here](https://developer.riotgames.com/))


## 📁 Project Structure

```
lol-dashboard/
├── README.md
├── data/
│   ├── match_timeline.json      # Raw API response
│   ├── df1_stats.csv            # Processed player stats
│   ├── df3_events.csv           # Processed events
│   └── rank_df.csv              # Silver benchmark data
├── scripts/
│   ├── lg_stats.py              # first_function() - Player frame stats
│   ├── lg_events.py             # third_function() - Event processing
│   └── lg_rank.py               # second_function() - Rank data collection
├── powerbi/
│   └── lol_dashboard.pbix       # Power BI dashboard file
└── docs/
    ├── dax_measures.md          # Complete DAX reference
    └── visualization_guide.md   # Chart setup instructions
```

---

## 🔧 Python Scripts

### `lg_stats.py` - Player Frame Stats
Extracts per-minute stats for all 10 players:
- Gold, CS, Level, XP
- Damage dealt/taken (total, physical, magic, true)
- Position coordinates (x, y)
- Champion stats (armor, MR, attack damage, etc.)

### `lg_events.py` - Event Processing
Parses game events with enrichment:
- Converts `assistingParticipantIds` to searchable string
- Adds `killerTeamId` for kill participation calculations
- Extracts position coordinates

### `lg_rank.py` - Rank Benchmarks
Collects data from Silver ranked games:
- Samples games from Silver I-IV
- Provides baseline for performance comparison

---

## 🎯 Roadmap

### ✅ Phase 1: Core Metrics (Complete)
- [x] Basic KDA tracking
- [x] CS and gold tracking
- [x] Win/Loss detection
- [x] Map of Kills Plotted on a "ghost image" of Summoner's Rift
- [x] Player selector functionality

### 🔄 Phase 2: Advanced Metrics (In Progress)
- [x] Damage efficiency
- [x] Trade balance
- [x] Tank score
- [ ] Kill participation %
- [ ] Solo kills
- [ ] First blood tracking

## Additional Phases I'd like to build this project INTO:
### 📋 Phase 3: Time-Based Analysis (Planned)
- [ ] Early/Mid/Late game breakdowns
- [ ] Power spike detection (Level 6/11/16)
- [ ] Phase-specific performance

### 📋 Phase 4: Positional Analysis (Planned)
- [ ] Lane opponent identification
- [ ] CS/Gold diff at 10/15 min
- [ ] Direct matchup stats
- [ ] Roaming detection

### 📋 Phase 5: Multi-Game Tracking (Planned)
- [ ] Match history collection
- [ ] Win rate trends
- [ ] Champion pool analysis
- [ ] Consistency metrics


## ⚠️ API Rate Limits

The Riot Games API has rate limits. This project implements:
- 1.2-1.5 second delays between requests (SUPER SIMPLE method because the RIOT API is very lenient with it's allowed usage)
- Error handling for rate limit responses
- Caching of responses where possible

**Development API Key Limits:**
- 20 requests per second
- 100 requests per 2 minutes

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Riot Games API](https://developer.riotgames.com/) for providing the data
- Power BI community for DAX guidance
- League of Legends community for inspiration
---

*This project isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.*
