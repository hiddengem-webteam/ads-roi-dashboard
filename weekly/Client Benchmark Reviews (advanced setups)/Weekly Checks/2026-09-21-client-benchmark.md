# Client Benchmark Review (advanced setups) — 2026-09-21

Run: 21 September 2026 (tables regenerated 2026-09-23 under the live-campaigns-only rule). Live reads via the Meta connector; CSV export 2026-09-01 to 2026-09-21 for the 4 accounts the connector cannot read. Scope: clients marked **Advanced** in the CRM "Meta Ads" column (Clients - Onboarding tab). Only Lead Gen (MoF) and Sales/Retargeting (BoF) campaigns are scored; IG Discovery and Keyword (ToF) spend is shown for context only.

| Advanced clients | Live reads | From CSV | Campaigns scored | Under spend gate | Flag to Shawal | Review w/ HG AI | Monitor | Healthy | Scale w/ HG AI |
|---|---|---|---|---|---|---|---|---|---|
| 16 | 12 | 4 | 28 | 7 | 0 | 12 | 4 | 6 | 6 |

States come from the Decision Making table in the Benchmarks doc. Lead Gen: CPL under $0.30 Scale, $0.30–0.50 Healthy, $0.50–1.00 Monitor, $1.00–2.50 Review, $2.50+ Flag, 30-day window, $100 gate. Sales/Retargeting: ROAS above 15x Scale, 8–15x Healthy, 5–8x Monitor, 2–5x Review, under 2x Flag, 14-day window, $200 gate. Band edges are inclusive on the lower bound.

## Weekly Meta Ads meetings since last run (Notes by Gemini)

Source: "Notes by Gemini" docs attached to the calendar events, read via Drive. Summary, decisions and next steps as Gemini wrote them; client-specific sentences are pulled into each client's section below. Transcript not used.

### Meta Ads Strategy — 2026-09-16 — doc `1Hoq1JUk1tFxSCUeYexeEELfVSZwTq7eJ2Pi_NvVDF4A`

The team aligned on tracking improvements, strategic offer shifts, and implementing AI driven sales proposals.

AI Tracking Strategy Improvements

Training the system improves reservation data accuracy by linking guest information across platforms. Custom landing pages will resolve existing bottom of funnel tracking limitations.

Core Offer Pricing Strategy

Strategy shifted away from fixed dollar discounts toward variable seasonal offers and resort credits. This adjustment protects client revenue during slower periods.

AI Driven Onboarding Planning

Sales calls will now utilize customized AI game plans instead of static budget recommendations. Dedicated AI projects will integrate property data to generate tailored proposals.

Decisions:
- Timeline for Hidden Gem AI rollout Leshan Patterson aims to have Hidden Gem AI available and ready for the team to use by the end of the day tomorrow, pending loop testing and stability checks.
- Creation of Claude project for game plans Dustin Baker will create a Claude project containing marketing strategy information, the kickoff call game plan template, transcripts, questionnaire results, and website links to generate preliminary account game plans.

Next steps:
- [Dustin Baker] Create Game Plan: Develop a project in Claude containing marketing strategy, presentation templates, sales call transcripts, questionnaire results, and website links.
- [Dustin Baker] Sync with Brandon: Discuss the design vision for custom bottom of funnel landing pages to assess potential benefits for tracking and performance.
- [Leshan Patterson] Release Hidden Gem AI: Finalize the platform configuration and stability checks to ensure availability for the account management team by the end of the day tomorrow.
- [Shawal Nazir] Update Onboarding Form: Incorporate additional questions regarding property management system data into the client intake questionnaire to improve strategy insights.

### Meta Ads Sync — 2026-09-17 — doc `1oMlKzZdFQxYCXKMiFnaG-2ews_EkudXgG0zivvI2l1c`

Campaign optimization strategies and budget scaling via geographic targeting and workflow adjustments

Geographic Targeting and Creatives

Optimization focused on shifting ad radius to local cities and pausing summer creatives to improve performance.

Budget Scaling and Testing

Budgets were increased gradually for high-performing accounts while planning broad audience segment tests.

Operational Workflow Updates

A weekly review structure was established to document and implement ad operation changes.

Decisions:
- Summer ad creative pause in lookalike campaigns The team agreed to pause summer ad creatives in lookalike campaigns and focus on fall and winter messaging.
- Budget increases for high-performing ad accounts The participants agreed to increase ad budgets for accounts achieving over a tenfold return on ad spend.
- Audience segment campaign test for Tabber The team agreed to test audience segment campaigns as a replacement for lookalike targeting on the Tabber account.
- Ad operations weekly review and workflow structure The team established a weekly ad operations workflow involving performance reviews, collaborative discussions, and documented updates.

Next steps:
- [Shawal Nazir] Pause Summer Creatives: Deactivate summer advertisement creatives within the lookalike campaigns.
- [Shawal Nazir] Increase Ad Budgets: Increase daily budgets for high performing ad accounts to optimize spend based on current return on ad spend.
- [Shawal Nazir] Configure Audience Segments: Implement audience segments to provide Meta with signals for high intent purchasers.
- [Shawal Nazir] Prepare Ad Recommendations: Draft ad operations recommendations weekly for the top spending clients.
- [Shawal Nazir] Post Ad Updates: Communicate implemented campaign changes to account managers via the meta ad creatives channel.
- [Gillian Conley] Inform Account Managers: Explain the new weekly ad operations process and workflow to the team.
- [Gillian Conley] Send Meeting Invite: Provide a calendar invitation for the upcoming session to Shawal.

## Action needed

Sales and Retargeting campaigns first, then Lead Gen. Within each, Flag to Shawal before Review w/ HG AI, highest spend first.

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Tàberg Falls | Alicia | MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | $1,417 / 14d | ROAS 3.3x | Review w/ HG AI | New (first run) |
| Tàberg Falls | Alicia | BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | $1,404 / 14d | ROAS 4.5x | Review w/ HG AI | New (first run) |
| Paradise Pointe | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $1,026 / 21d | ROAS 2.7x | Review w/ HG AI | New (first run) |
| Stay Saluda NC | Makenna | BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | $414 / 14d | ROAS 4.3x | Review w/ HG AI | New (first run) |
| Stay On 30A | Charlotte | MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | $1,512 / 30d | CPL $2.23 | Review w/ HG AI | New (first run) |
| Treetop Escapes | Makenna | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $901 / 30d | CPL $1.10 | Review w/ HG AI | New (first run) |
| Starlight Haven Weiss Lake | Charlotte | New Leads Campaign - 03/03/26 | Lead Gen (MoF) | $758 / 30d | CPL $1.37 | Review w/ HG AI | New (first run) |
| Stay Saluda NC | Makenna | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $593 / 30d | CPL $1.19 | Review w/ HG AI | New (first run) |
| American River Resort | Nicole | MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | $302 / 30d | CPL $1.39 | Review w/ HG AI | New (first run) |
| Green Springs Inn | Alicia | MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | $238 / 30d | CPL $2.29 | Review w/ HG AI | New (first run) |
| AwayFrames | Alicia | MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | $150 / 30d | CPL $2.35 | Review w/ HG AI | New (first run) |
| Endless Stays | Nicole | MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | $119 / 21d | CPL $1.29 | Review w/ HG AI | New (first run) |

## Scale candidates

| Client | AM | Campaign | Type | Spend / window | Governing metric | State | Status vs last week |
|---|---|---|---|---|---|---|---|
| Stay On 30A | Charlotte | MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | $2,177 / 14d | ROAS 23.7x | Scale w/ HG AI | New (first run) |
| Stay On 30A | Charlotte | BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | $1,456 / 14d | ROAS 30.0x | Scale w/ HG AI | New (first run) |
| Starlight Haven Weiss Lake | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $627 / 14d | ROAS 19.8x | Scale w/ HG AI | New (first run) |
| Ponderosa Pines Resort | Anna | Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | $472 / 21d | ROAS 24.9x | Scale w/ HG AI | New (first run) |
| Asheville River Cabins | Charlotte | BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | $420 / 14d | ROAS 49.5x | Scale w/ HG AI | New (first run) |
| Starlight Haven Hot Springs | Charlotte | Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | $280 / 14d | ROAS 20.1x | Scale w/ HG AI | New (first run) |

## Per client, ordered by scored MoF + BoF spend

### Stay On 30A — AM Charlotte — account Stay on 30a Ads (25640434272252212) — live read

ToF (Discovery / Keyword) spend, not scored: $2,987 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - RT Engagers - 07/16/26 | Lead Gen (MoF) | 30d | $1,512 | 678 leads | CPL $2.23 | Review w/ HG AI | CPC $0.45 > $0.30; CPM $39.10 > $14.84 | 14d CPL $1.39 | First run |
| MoF - Sales Campaign - HiddenGem Pixel LoL - 07/17/26 | Sales (MoF lookalike) | 14d | $2,177 | 14 purchases | ROAS 23.7x | Scale w/ HG AI | CPC $0.80 > $0.62; CPM $28.68 > $16.50; cost/booking $155.51 > $90 | 30d ROAS 18.1x, 27 purchases | First run |
| BoF - Sales Campaign - RT Website Visitors - 07/13/26 | Retargeting (BoF) | 14d | $1,456 | 10 purchases | ROAS 30.0x | Scale w/ HG AI | CPC $1.24 > $0.62; CPM $31.19 > $16.50; cost/booking $145.60 > $90; freq 4.2 > 3.0 | 30d ROAS 22.4x, 19 purchases | First run |

Monthly ROI: August: spend $12,420, 85 Meta-attributed bookings, blended ROAS 17.8x, retargeting ROAS 15.5x, CPL $2.58 on 594 leads · July: spend $6,407, 67 Meta-attributed bookings, blended ROAS 32.3x, retargeting ROAS 14.6x, CPL $1.24 on 583 leads.

Meeting notes (Meta Ads Sync 2026-09-17): Budget Scaling for High-Performing Accounts: Shawal Nazir noted that Stay on 30A had a 30-day frequency of around 5 on its retargeting campaign, indicating that top-of-funnel prospecting is not feeding in enough, and they recommended increasing top-of-funnel spend. Dustin Baker suggested running this test on Tabber Falls rather than Stay on 30A to avoid disrupting Stay on 30A's strong performance, emphasizing that they must ensure the test is structured properly to yield conclusive insights rather than ambiguous results.

HG AI notes: none dropped in yet.

### Tàberg Falls — AM Alicia — account Táberg Falls (827872700004659) — live read

ToF (Discovery / Keyword) spend, not scored: $3,033 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lookalike Sales Campaign - 08/21/2026 | Sales (MoF lookalike) | 14d | $1,417 | 3 purchases | ROAS 3.3x | Review w/ HG AI | CPM $26.92 > $16.50; cost/booking $472.49 > $90 | 30d ROAS 5.2x, 9 purchases | First run |
| BoF - Website Retargeting Campaign - 08/21/2026 | Retargeting (BoF) | 14d | $1,404 | 4 purchases | ROAS 4.5x | Review w/ HG AI | CPC $0.71 > $0.62; CPM $23.11 > $16.50; cost/booking $350.91 > $90; freq 3.3 > 3.0 | 30d ROAS 8.2x, 15 purchases | First run |
| MoF - Leads Campaign - 06/19/26 | Lead Gen (MoF) | 30d | $1,798 | 3384 leads | CPL $0.53 | Monitor | within lines | 14d CPL $0.54 | First run |

Monthly ROI: August: spend $11,259, 31 Meta-attributed bookings, blended ROAS 4.5x, retargeting ROAS 8.0x, CPL $0.46 on 4015 leads · July: spend $11,739, 80 Meta-attributed bookings, blended ROAS 9.5x, retargeting ROAS 15.8x, CPL $0.67 on 2320 leads.

Meeting notes (Meta Ads Sync 2026-09-17): Dustin Baker suggested running this test on Tabber Falls rather than Stay on 30A to avoid disrupting Stay on 30A's strong performance, emphasizing that they must ensure the test is structured properly to yield conclusive insights rather than ambiguous results.

HG AI notes: none dropped in yet.

### FLOHOM — AM Makenna — account FLOHOM Ads (2100710320122219) — live read

ToF (Discovery / Keyword) spend, not scored: $1,948 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers – 08/17/26 | Lead Gen (MoF) | 30d | $1,337 | 2259 leads | CPL $0.59 | Monitor | within lines | 14d CPL $0.52 | First run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $1,385 | 20 purchases | ROAS 14.6x | Healthy | CPC $0.63 > $0.62; CPM $18.10 > $16.50 | 30d ROAS 10.4x, 33 purchases | First run |
| MoF - Lookalike Sales Campaign - 07/29/26 | Sales (MoF lookalike) | 14d | $1,318 | 17 purchases | ROAS 10.5x | Healthy | CPC $0.72 > $0.62; CPM $20.47 > $16.50 | 30d ROAS 9.1x, 32 purchases | First run |
| [Myrtle Beach] MoF - Lookalike Sales Campaign - 09/17/26 | Sales (MoF lookalike) | 14d | $106 | 1 purchases | ROAS 9.7x | Under gate | CPC $1.58 > $0.62; CPM $26.90 > $16.50; cost/booking $105.73 > $90 | spend $105.73 < $200 gate; 30d ROAS 9.7x, 1 purchases | First run |

Monthly ROI: August: spend $9,331, 57 Meta-attributed bookings, blended ROAS 5.8x, retargeting ROAS 8.2x, CPL $2.24 on 708 leads · July: spend $5,555, 103 Meta-attributed bookings, blended ROAS 17.2x, retargeting ROAS 19.1x, CPL $7.66 on 66 leads.

Meeting notes (Meta Ads Sync 2026-09-17): State Targeting Strategy and Geographic Radius: Shawal Nazir and Dustin Baker discussed optimizing state targeting to focus on a five-hour drive radius, noting that Flow Home spent about 5% of the client's budget on distant states with few conversions.

HG AI notes: none dropped in yet.

### Paradise Pointe — AM Makenna — account Paradise Pointe Ads (1585826092078255) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $500 over 21 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 21d | $1,026 | 37 purchases | ROAS 2.7x | Review w/ HG AI | CPC $0.91 > $0.62; CTR 1.47% < 2%; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 14-day window), not live; provisional, export has no status column | First run |
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 21d | $503 | 504 leads | CPL $1.00 | Monitor | within lines; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 30-day window), not live; provisional, export has no status column | First run |

Monthly ROI: August: spend $3,109, 94 Meta-attributed bookings, blended ROAS 16.8x, retargeting ROAS 18.0x, CPL $1.64 on 471 leads · July: spend $2,237, 74 Meta-attributed bookings, blended ROAS 21.6x, retargeting ROAS 16.7x, CPL $1.01 on 90 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Treetop Escapes — AM Makenna — account Treetop Escapes Ads (967636478877602) — live read

ToF (Discovery / Keyword) spend, not scored: $902 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $901 | 818 leads | CPL $1.10 | Review w/ HG AI | within lines | 14d CPL $0.86 | First run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $566 | 5 purchases | ROAS 10.2x | Healthy | CPM $17.78 > $16.50; cost/booking $113.22 > $90; freq 3.3 > 3.0 | 30d ROAS 9.9x, 11 purchases | First run |

Monthly ROI: August: spend $3,082, 28 Meta-attributed bookings, blended ROAS 8.8x, retargeting ROAS 16.3x, CPL $1.49 on 620 leads · July: spend $2,487, 44 Meta-attributed bookings, blended ROAS 14.5x, retargeting ROAS 22.2x, CPL $1.48 on 21 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Starlight Haven Weiss Lake — AM Charlotte — account Starlight Haven Weiss Lake (74756899) — live read

ToF (Discovery / Keyword) spend, not scored: $132 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $758 | 554 leads | CPL $1.37 | Review w/ HG AI | CPC $0.33 > $0.30 | 14d CPL $1.00 | First run |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $627 | 30 purchases | ROAS 19.8x | Scale w/ HG AI | CPC $0.69 > $0.62; CPM $17.15 > $16.50 | 30d ROAS 21.0x, 56 purchases | First run |

Monthly ROI: August: spend $2,351, 36 Meta-attributed bookings, blended ROAS 10.7x, retargeting ROAS 17.6x, CPL $1.23 on 617 leads · July: spend $2,163, 41 Meta-attributed bookings, blended ROAS 10.8x, retargeting ROAS 15.2x, CPL $0.74 on 826 leads.

Meeting notes (Meta Ads Strategy 2026-09-16): Core Offer Strategy and Variable Pricing: Dustin Baker brought up a point raised by Jillian Conley regarding core offers, noting that fixed-dollar discounts (such as a $100 off promotion used by Starlight Haven) can break pricing and hurt clients during slow seasons.

HG AI notes: none dropped in yet.

### Starlight Haven Hot Springs — AM Charlotte — account Starlight Haven Hot Springs (901138032027913) — live read

ToF (Discovery / Keyword) spend, not scored: $622 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| New Leads Campaign - 03/03/26 | Lead Gen (MoF) | 30d | $904 | 2489 leads | CPL $0.36 | Healthy | within lines | 14d CPL $0.34 | First run |
| Website Retargeting Campaign - 03/03/26 | Retargeting (BoF) | 14d | $280 | 8 purchases | ROAS 20.1x | Scale w/ HG AI | within lines | 30d ROAS 21.5x, 19 purchases | First run |

Monthly ROI: August: spend $2,193, 19 Meta-attributed bookings, blended ROAS 6.3x, retargeting ROAS 22.3x, CPL $0.36 on 2589 leads · July: spend $2,160, 17 Meta-attributed bookings, blended ROAS 5.1x, retargeting ROAS 17.1x, CPL $0.33 on 2813 leads.

Meeting notes (Meta Ads Strategy 2026-09-16): Core Offer Strategy and Variable Pricing: Dustin Baker brought up a point raised by Jillian Conley regarding core offers, noting that fixed-dollar discounts (such as a $100 off promotion used by Starlight Haven) can break pricing and hurt clients during slow seasons.

HG AI notes: none dropped in yet.

### Stay Saluda NC — AM Makenna — account Stay Saluda Ads (1863632561215857) — live read

ToF (Discovery / Keyword) spend, not scored: $900 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $593 | 500 leads | CPL $1.19 | Review w/ HG AI | within lines | 14d CPL $0.92 | First run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 14d | $414 | 3 purchases | ROAS 4.3x | Review w/ HG AI | CPC $0.86 > $0.62; cost/booking $138.09 > $90; freq 4.3 > 3.0 | 30d ROAS 5.6x, 8 purchases | First run |

Monthly ROI: August: spend $2,367, 9 Meta-attributed bookings, blended ROAS 3.7x, retargeting ROAS 5.2x, CPL $2.59 on 146 leads · July: spend $2,140, 10 Meta-attributed bookings, blended ROAS 2.6x, retargeting ROAS 0.8x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Ponderosa Pines Resort — AM Anna — account Ponderosa Pines Resort (1058846326445255) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $1,127 over 21 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| Leads Campaign - 07/16/26 | Lead Gen (MoF) | 21d | $402 | 452 leads | CPL $0.89 | Monitor | within lines; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 30-day window), not live; provisional, export has no status column | First run |
| Website Retarget Campaign - 07/13/26 | Retargeting (BoF) | 21d | $472 | 29 purchases | ROAS 24.9x | Scale w/ HG AI | CPM $17.71 > $16.50; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 14-day window), not live; provisional, export has no status column | First run |

Monthly ROI: August: spend $3,101, 103 Meta-attributed bookings, blended ROAS 15.0x, retargeting ROAS 21.3x, CPL $1.32 on 471 leads · July: spend $2,089, 17 Meta-attributed bookings, blended ROAS 3.6x, retargeting ROAS 22.3x, CPL $0.91 on 356 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Asheville River Cabins — AM Charlotte — account Asheville River Cabins Ads (615836588009747) — live read

ToF (Discovery / Keyword) spend, not scored: $1,205 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $301 | 887 leads | CPL $0.34 | Healthy | within lines | 14d CPL $0.27 | First run |
| BoF - Website Retargeting Campaign - 06/08/26 | Retargeting (BoF) | 14d | $420 | 30 purchases | ROAS 49.5x | Scale w/ HG AI | CPM $19.27 > $16.50 | 30d ROAS 47.9x, 62 purchases | First run |

Monthly ROI: August: spend $2,424, 82 Meta-attributed bookings, blended ROAS 27.2x, retargeting ROAS 65.0x, CPL $0.42 on 605 leads · July: spend $2,029, 39 Meta-attributed bookings, blended ROAS 18.6x, retargeting ROAS 51.6x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### American River Resort — AM Nicole — account American River Resort (953162737054331) — live read

ToF (Discovery / Keyword) spend, not scored: $906 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 30d | $302 | 217 leads | CPL $1.39 | Review w/ HG AI | CPM $17.13 > $14.84 | 14d CPL $1.39 | First run |

Paused in window, not scored: MoF - Lead Campaign - Retargeting Engagers (Lead Gen (MoF)), $262 / 30d, 1 leads, CPL $261.69. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: August: spend $1,529, 3 Meta-attributed bookings, blended ROAS 1.4x, CPL $18.30 on 30 leads · July: spend $1,544, 4 Meta-attributed bookings, blended ROAS 1.1x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Green Springs Inn — AM Alicia — account Green Springs Inn (1390516335151357) — live read

ToF (Discovery / Keyword) spend, not scored: $605 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign/08/28/2026 | Lead Gen (MoF) | 30d | $238 | 104 leads | CPL $2.29 | Review w/ HG AI | within lines | 14d CPL $1.76 | First run |
| BoF - Sales Campaign - Retargeting Website Visitors - 08/28/26 | Retargeting (BoF) | 14d | $137 | 5 purchases | ROAS 8.9x | Under gate | CPC $0.65 > $0.62 | spend $137.23 < $200 gate; 30d ROAS 10.9x, 9 purchases | First run |

Paused in window, not scored: MoF - Lead Campaign/07/28/2026 (Lead Gen (MoF)), $59 / 30d, 5 leads, CPL $11.81. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: August: spend $1,247, 23 Meta-attributed bookings, blended ROAS 8.2x, retargeting ROAS 17.1x, CPL $9.09 on 34 leads · July: spend $1,222, 17 Meta-attributed bookings, blended ROAS 7.8x, retargeting ROAS 14.6x, CPL $5.65 on 8 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Endless Stays — AM Nicole — account Endless Stays (896372356081479) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $602 over 21 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF Lead Campaign - Retargeting Engagers - 09/09/2026 | Lead Gen (MoF) | 21d | $119 | 92 leads | CPL $1.29 | Review w/ HG AI | CPC $0.31 > $0.30; CPM $21.21 > $14.84; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 30-day window), not live; provisional, export has no status column | First run |
| BoF - Sales Campaign - Retargeting Website Visitors | Retargeting (BoF) | 21d | $200 | 1 purchases | ROAS 8.1x | Healthy | CPC $0.69 > $0.62; CPM $25.20 > $16.50; cost/booking $200.13 > $90; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 14-day window), not live; provisional, export has no status column | First run |
| MoF Lead Campaign - Retargeting Engagers | Lead Gen (MoF) | 21d | $26 | 11 leads | CPL $2.34 | Under gate | CPM $25.31 > $14.84; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 30-day window), not live; provisional, export has no status column; spend $25.77 < $100 gate | First run |
| MoF Lead Campaign - Retargeting Engagers - 09/03/2026 | Lead Gen (MoF) | 21d | $12 | 5 leads | CPL $2.41 | Under gate | CPC $0.63 > $0.30; CPM $25.98 > $14.84; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 30-day window), not live; provisional, export has no status column; spend $12.03 < $100 gate | First run |

Monthly ROI: August: spend $1,553, 10 Meta-attributed bookings, blended ROAS 11.6x, retargeting ROAS 38.8x, CPL $9.73 on 26 leads · July: spend $1,534, 9 Meta-attributed bookings, blended ROAS 16.0x.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Canopy at Moody Moon — AM Alicia — account The Canopy At Moody Moon Ridge (1293707265980102) — live read

ToF (Discovery / Keyword) spend, not scored: $0 over 30 days.

No live Lead Gen or Sales campaigns with spend in the window.

Paused in window, not scored: 09/02 - Sales (Sales), $224 / 14d, 2 purchases, ROAS 0.5x. Live campaigns only are scored (decision 2026-09-23).

Paused in window, not scored: Sales ABO Ads Tests - 08/28/2026 (Sales), $87 / 14d, 2 purchases, ROAS 1.1x. Live campaigns only are scored (decision 2026-09-23).

Monthly ROI: no record in the Monthly ROI data files.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### AwayFrames — AM Alicia — account Awayframes Ad Account (2471256056603833) — live read

ToF (Discovery / Keyword) spend, not scored: $601 over 30 days.

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| MoF - Lead Campaign - Retargeting Engagers 07/31/2026 | Lead Gen (MoF) | 30d | $150 | 64 leads | CPL $2.35 | Review w/ HG AI | CPC $0.36 > $0.30 | 14d CPL $1.65 | First run |
| BoF - Sales Campaign - Retargeting Website Visitors 07/31/2026 | Retargeting (BoF) | 14d | $71 | 0 purchases | ROAS — | Under gate | CPC $0.65 > $0.62 | spend $71.13 < $200 gate | First run |

Monthly ROI: August: spend $869, 8 Meta-attributed bookings, blended ROAS 21.8x, retargeting ROAS 27.0x, CPL $2.68 on 58 leads · July: spend $923, 9 Meta-attributed bookings, blended ROAS 18.6x, CPL $2.44 on 2 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

### Bison Ridge Retreat — AM Chiara — account Bison Ridge Retreat Ad Account (950241787963535) — CSV export, provisional

ToF (Discovery / Keyword) spend, not scored: $399 over 21 days (export).

| Campaign | Type | Window | Spend | Results | Governing metric | State | Diagnostics vs investigate lines | Notes | Change vs last week |
|---|---|---|---|---|---|---|---|---|---|
| BoF - Sales Campaign - RT Website Visitors | Retargeting (BoF) | 21d | $102 | 0 purchases | ROAS 0.0x | Under gate | within lines; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 14-day window), not live; provisional, export has no status column; spend $102.45 < $200 gate | First run |
| MoF - Lead Campaign - RT Engagers | Lead Gen (MoF) | 21d | $100 | 38 leads | CPL $2.62 | Under gate | CPC $0.38 > $0.30; CPM $19.74 > $14.84; CTR here is link CTR from the export | source: CSV export 2026-09-01 to 2026-09-21 (21 days, not the 30-day window), not live; provisional, export has no status column; spend $99.53 < $100 gate | First run |

Monthly ROI: August: spend $952, 3 Meta-attributed bookings, blended ROAS 8.0x, retargeting ROAS —, CPL $2.47 on 63 leads · July: spend $924, 9 Meta-attributed bookings, blended ROAS 20.3x, retargeting ROAS —, CPL $1.75 on 23 leads.

Meeting notes: not mentioned in this week's meetings.

HG AI notes: none dropped in yet.

## Footer

- Windows: Lead Gen last 30 days, Sales/Retargeting last 14 days (live). CSV accounts use the export period 2026-09-01 to 2026-09-21 (21 days) and are provisional.
- Gates: $100 Lead Gen, $200 Sales/Retargeting. Campaigns under the gate are listed but not judged.
- Classification: by campaign objective (OUTCOME_LEADS → Lead Gen; OUTCOME_SALES → Sales, split into Retargeting (BoF) or MoF lookalike by name; OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT → ToF, not scored). CSV accounts have no objective column, so classification there is by name.
- Sales campaigns with an MoF or lookalike prefix are scored on the Retargeting ROAS bands because they optimise for purchases. The Benchmarks doc has no separate band for prospecting sales campaigns; confirm or add one.
- CTR on live rows is Meta's CTR (all clicks), not link CTR. The doc's click-rate lines are probably link CTR, so treat the CTR diagnostic as indicative.
- Frequency and cost per booking are diagnostics only and do not change the state (decision 2026-09-21).
- Only campaigns live (ACTIVE) at run time are scored. Paused campaigns that spent inside the window are listed per client as "Paused in window" and never enter Action needed or the counts (decision 2026-09-23; this report was regenerated under that rule on 2026-09-23).
- Unclassified campaigns: none.
- Previous report: none, first run.
- Meeting notes: every "Meta Ads Strategy" or "Meta Ads Sync" calendar event since the previous run that has a "Notes by Gemini" attachment, read via Drive. Client names are matched with an alias list (Flow Home = FLOHOM, Tabber = Tàberg Falls).
- Monthly ROI context from `Monthly ROI data/` (August 2026, July 2026). Revenue there comes from the Client Performance Tracking sheet, not the pixel, so its ROAS is not comparable to the pixel ROAS above.
