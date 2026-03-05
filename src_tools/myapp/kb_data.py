TEXTS = {
  "products": [
    {
      "name": "p100_tech_specs",
      "page_content": """SKU P-100 Technical Specifications
The P-100 is a handheld device designed for field diagnostics and data collection. It features a 4.7-inch sunlight-readable display, a rugged IP67 enclosure, and a 4,500 mAh replaceable battery rated for up to 12 hours of mixed-use operation. Connectivity includes Bluetooth 5.3 with LE support, dual-band Wi‑Fi (802.11ac), and optional LTE-M for low-power wide-area connectivity. Onboard sensors include a tri-axis accelerometer, gyroscope, ambient light sensor, and temperature probe. Firmware v1.2 introduced an extended sampling mode that improves sensor accuracy by approximately 7–10% in variable temperature conditions while reducing power consumption in standby by 5%.

Supported Accessories and Compatibility
The P-100 maintains backward compatibility with the A1 and A2 accessory families, including snap-on barcode scanners and NFC readers. Legacy A0 accessories have entered end-of-support (EOS) as of 2024-06-30 and may not function reliably with firmware releases after v1.1 due to driver deprecations. Compatibility matrices are updated quarterly and include detailed pinout mappings, supported driver versions, and calibration guidelines.

Maintenance and Lifecycle
The device supports over-the-air (OTA) firmware updates via the device management console. Critical updates are signed with a rotating hardware-backed key and staged in two phases to reduce downtime. End-of-life (EOL) for the P-100 is projected for 2028-12-31 with a two-year extended support program covering security patches and critical bug fixes."""
    },
    {
      "name": "p_family_release_notes_v1_2",
      "page_content": """Release Notes v1.2 (P-100, P-200 Family)
Highlights
- Sensor Fusion Enhancements: Improved Kalman filter tuning yields a 2.7% average increase in F1 score for motion classification on the P-100 in controlled lab tests.
- Connectivity: Bluetooth stack updated to address rare pairing instability; Wi‑Fi roaming hysteresis lowered to improve handoffs in dense networks.
- Power Management: New adaptive sleep policy reduces background wakeups by 8–12% during low activity.

Known Issues
- Intermittent NFC timeouts under high EMI; fix scheduled for v1.2.1.
- A subset of units manufactured in March may report battery health inconsistently due to an ADC calibration offset; see Support Article SUP-1242.

Upgrade Guidance
- Devices on v1.0 or earlier should perform a two-step upgrade (v1.0 → v1.1 → v1.2) to ensure bootloader compatibility.
- For fleets using A2 barcode accessories, verify accessory firmware ≥ v3.4 to maintain full feature parity."""
    },
    {
      "name": "product_portfolio_overview",
      "page_content": """Product Portfolio Overview
Three tiers:
- P‑100 (Field Diagnostics): Rugged handheld optimized for sensor data capture and rapid deployment.
- P‑200 (Industrial Monitoring): Larger display, higher ingress protection, redundant radios for harsh environments.
- P‑300 (Analyst Edition): Enhanced compute with on-device ML acceleration and expanded storage.

All tiers integrate with the centralized device management console for provisioning, remote configuration, and security policy enforcement. Optional service bundles include extended warranty, advanced RMA, and quarterly performance optimization.

Datasheet Versioning
Datasheets use semver (e.g., datasheet-p100-1.4.0.pdf) and include compliance certifications and environmental specs."""
    },
    {
      "name": "compatibility_migration_guide_2025",
      "page_content": """Compatibility and Migration Guide (2025)
Roadmap deprecates A0 family and transitions to A1/A2 with unified driver APIs.

Migration Steps
1) Update base firmware to v1.2 or later
2) Install accessory service layer v3.x
3) Run calibration wizard to align sensor baselines

For custom middleware, new driver APIs add typed events and structured error codes. A compatibility shim is provided for six months to maintain legacy calls during migration."""
    },
    {
      "name": "p_series_datasheet_index",
      "page_content": """P-Series Datasheets Index
- P‑100: datasheet-p100-1.4.0.pdf
- P‑200: datasheet-p200-1.3.2.pdf
- P‑300: datasheet-p300-1.1.1.pdf

Datasheets include CE, FCC, RoHS certifications; operating range −20°C to 50°C (non-condensing); storage guidance and maintenance intervals."""
    }
  ],

  "support": [
    {
      "name": "runbook_network_timeouts_e42",
      "page_content": """Support Runbook: Network Timeouts (Error E42)
Symptoms
- Intermittent data transmission failures; UI shows E42.

Root Causes
- Unstable Wi‑Fi signal, aggressive roaming
- DHCP lease renewal collisions during peak hours
- Firmware v1.1 Wi‑Fi driver bug under interference

Resolution
1) Validate RSSI > −65 dBm; disable band steering temporarily
2) Increase DHCP lease duration
3) Apply firmware v1.2 patch for driver fixes
4) Verify LTE-M fallback APN profiles

Escalation
- Collect diag logs with “netdiag –all”; attach to ticket; escalate referencing KB case SUP-1108."""
    },
    {
      "name": "battery_health_troubleshooting",
      "page_content": """Troubleshooting Guide: Battery Health Reporting
Symptoms
- Rapid drops or fluctuating reporting during charging.

Diagnostics
- Check ADC calibration value (March builds affected)
- Review charge cycles and temperature profile in health logs

Remediation
- Install patch BH-2024-03 to recalibrate ADC
- Perform one full discharge/charge cycle to re-baseline
- If persistent, issue RMA (reason BH-CAL-OFFSET)

Prevention
- Updated factory calibration adds temperature-compensated step."""
    },
    {
      "name": "faq_quick_procedures",
      "page_content": """FAQ and Quick Procedures
- Soft reset: Hold power 10 seconds
- Collect logs: “diag collect –full”
- Recommended Wi‑Fi: WPA2-Enterprise with cert-based auth
- NFC instability near machinery: EMI; consider shielding and antenna repositioning."""
    },
    {
      "name": "incident_management_slas",
      "page_content": """Incident Management and SLAs
- Sev1: 15-minute acknowledgment; 4-hour workaround target
- Sev2: 30-minute acknowledgment; next-business-day remediation plan

Escalation Paths
Tier 1 → Tier 2 → Engineering on-call

PIRs
- Required for Sev1 within five business days; include root cause, impact, corrective actions."""
    },
    {
      "name": "support_article_sup_1242",
      "page_content": """Support Article SUP-1242: ADC Calibration Offset
Issue
- Battery health reporting inconsistencies on March builds.

Fix
- Apply BH-2024-03; verify calibration via health log diagnostics.

Verification
- Confirm stable reporting across a full discharge/charge cycle; update fleet policy accordingly."""
    }
  ],

  "sales": [
    {
      "name": "playbook_mid_market_positioning",
      "page_content": """Sales Playbook: Mid-Market Positioning
Value Narrative
- TCO reduction ~18% over 24 months through maintenance savings, battery lifespan, OTA efficiencies.
- Improved data accuracy reduces repeat site visits and accelerates time-to-value.

Competitive Landscape
- Versus Vendor X: Superior sensor fusion accuracy and telemetry.
- Versus Vendor Y: Lower maintenance overhead (modular accessories, extended warranties).

Proof Points
- ACME Logistics: 22% ticket reduction after migrating to P‑100 with proactive diagnostics.
- ROI Model: Break-even ~month 14 for fleets >200 units."""
    },
    {
      "name": "pricing_discount_guidance",
      "page_content": """Pricing and Discount Guidance
Tiers
- Basic: device + standard warranty
- Pro: adds advanced diagnostics
- Enterprise: fleet analytics + premium support

Regional Considerations
- EMEA: Q4 volume incentives
- APAC: accessory bundle discounts (import duties)

Deal Structuring
- Position Pro with deferred analytics activation for budget cycles
- Bundle A1/A2 to unlock margin and solve operational pain points."""
    },
    {
      "name": "objection_handling",
      "page_content": """Objection Handling and Messaging
Common Objections
- Upfront cost: Reframe around TCO savings; provide ROI calculators and financing
- Integration risk: Highlight robust driver APIs, migration shims; cite customer success stories

Messaging Pillars
- Reliability in harsh environments
- Predictable lifecycle (EOL/EOS clarity)
- Data accuracy improves operational decisions."""
    },
    {
      "name": "contracts_templates",
      "page_content": """Contracts and Templates
- MSA: SLAs aligned to premium support (99.9% cloud uptime, next-business-day hardware replacement for Enterprise)
- DPA: Standard contractual clauses and regional compliance
- SOW: Deliverables, acceptance criteria, change control to reduce ambiguity."""
    }
  ],

  "experiments": [
    {
      "name": "exp_e17_sensor_fusion_tuning",
      "page_content": """Experiment E17: Sensor Fusion Tuning
Hypothesis
- Kalman filter parameter adjustments raise F1 by ≥3%.

Method
- DS‑Alpha dataset; 10,000 labeled sequences; multiple temperatures (10–35°C)
- Ten repeated trials with randomized seeds

Results
- +2.7% mean F1 with 95% CI [2.2%, 3.1%]; strongest gains in high-vibration conditions
- Side effect: +3% CPU utilization under burst workloads; mitigated in firmware v1.2."""
    },
    {
      "name": "protocol_env_calibration",
      "page_content": """Protocol Template: Environmental Calibration
Preconditions
- Device temperature within 23–27°C; allow 10 minutes for thermal stabilization

Steps
- Initiate baseline capture
- Perform controlled movements for 60 seconds
- Verify variance thresholds
- Store calibration profile

Instrumentation
- Bench power supply to avoid battery-induced voltage fluctuations

Reproducibility
- Document firmware version, accessory model, ambient noise profile."""
    },
    {
      "name": "ota_efficiency_study",
      "page_content": """Results Summary: OTA Efficiency Study
Objective
- Measure impact of OTA delta updates vs full-image updates

Findings
- Delta updates reduced payload by 62% and cut maintenance windows by 35% in staged deployments

Constraints
- Delta generation less effective when base firmware deviates >2 versions; recommend aligned baselines."""
    },
    {
      "name": "data_handling_compliance",
      "page_content": """Data Handling and Compliance Notes
- Datasets anonymized and stored with lineage metadata (dataset ID, collection date, sensor configs)
- Access controlled via project-based roles
- Sensitive environment recordings require approval and encryption at rest with KMS-managed keys."""
    }
  ],

  "manufacturing": [
    {
      "name": "sop_line_start",
      "page_content": """Standard Operating Procedure (SOP): Line Start
- Verify torque driver calibration within last 30 days
- Inspect safety gates and interlocks; E‑stop test before first unit
- Preheat reflow oven to validated profile; confirm thermocouple readings within ±2°C

Quality Gates
- Post-board assembly AOI; rejects to rework station 2
- Record lot numbers for traceability; attach to batch record

Safety
- PPE enforced; ESD straps must pass continuity checks"""
    },
    {
      "name": "batch_br221_deviation",
      "page_content": """Batch Record BR‑221 and Deviation Summary
- Batch BR‑221 produced 480 units; AOI fail rate 1.7% due to solder bridging on U4
- Deviation DEV‑33 opened for station 3 nozzle misalignment; corrective action mid-batch
- Final yield 98.1%; reworked units passed functional test after nozzle realignment and reflow profile tweak"""
    },
    {
      "name": "capa_ca12_packaging_mislabel",
      "page_content": """CAPA CA‑12: Packaging Mislabel
Problem
- Incorrect accessory code printed on 2% of A2 bundle packaging

Root Cause
- Template mapping in print server reverted to v1.0 after maintenance restart

Corrective Action
- Lock configuration to v1.2 and add checksum verification before print jobs

Preventive Action
- Weekly audit of print templates; automated alerts on version drift"""
    },
    {
      "name": "maintenance_calibration_schedule",
      "page_content": """Maintenance and Calibration Schedule
- Torque drivers: monthly calibration; retain certificates for 24 months
- Reflow ovens: quarterly profile validation and thermocouple calibration
- Inline barcode scanners: weekly cleaning and functional test; replace after 500k scans or performance degradation"""
    }
  ],

  "services": [
    {
      "name": "onboarding_blueprint_6w",
      "page_content": """Engagement Blueprint: 6‑Week Onboarding
Milestones
- Week 1: Discovery + architecture workshop
- Weeks 2–3: Pilot to 10% of fleet; success criteria (uptime, latency, data integrity)
- Weeks 4–5: Rollout in staggered waves; monitoring + feedback loop
- Week 6: Handover and knowledge transfer; schedule health checks

Roles (RACI)
- PM (client-facing), solution architect, field engineer, customer success manager

Outcomes
- Runbooks, acceptance sign-off, 90-day optimization plan"""
    },
    {
      "name": "sow_template_v3",
      "page_content": """SOW Template v3: Deliverables and Acceptance
Deliverables
- Solution design doc, deployment checklist, configuration baseline, training session recordings

Acceptance Criteria
- Devices online for 7 consecutive days; error rates <0.5%; baselines stored in CMDB

Change Control
- Scope changes via CR form with impact assessment and approval chain"""
    },
    {
      "name": "customer_success_playbook",
      "page_content": """Customer Success Playbook
- Quarterly Business Reviews (QBRs): KPIs, risk register, roadmap alignment
- Proactive alerts on telemetry thresholds (battery health, connectivity failures)
- Escalation channel tied to premium support SLAs"""
    },
    {
      "name": "post_deployment_health_checks",
      "page_content": """Post-Deployment Health Checks
KPIs
- 99.5% device availability; median latency <150 ms; ticket volume downtrend

Actions
- Firmware drift remediation; accessory failure pattern analysis; user training refreshers if error classes spike"""
    }
  ]
}

KB_REGISTRY = {
    "products": (
        "kb-xxxxxxxx-products",
        "Product catalogs and specifications, including SKUs, features, supported configurations, version history, release notes, pricing tiers, and public datasheets. \
Covers compatibility matrices, EOL/EOS announcements, and FAQs about capabilities."
    ),
    "support": (
        "kb-xxxxxxxx-support",
        "Customer support knowledge base: troubleshooting guides, known issues, incident runbooks, escalation procedures, SLAs, and configuration tips. \
Includes step-by-step resolutions, error code references, common diagnostics, and links to ticketing workflows."
    ),
    "sales": (
        "kb-xxxxxxxx-sales",
        "Sales playbooks and go-to-market materials: value propositions, competitive positioning, objection handling, ROI calculators, segment-specific messaging, \
case studies, contract templates, discount policies, and regional pricing guidance."
    ),
    "experiments": (
        "kb-xxxxxxxx-experiments",
        "R&D experiments repository: experiment protocols, hypotheses, datasets, results summaries, analysis notes, and reproducibility details. \
Includes experiment templates, instrumentation settings, and compliance notes for data handling."
    ),
    "manufacturing": (
        "kb-xxxxxxxx-manufacturing",
        "Manufacturing operations: SOPs, batch records, process parameters, quality control checklists, deviation reports, CAPA, maintenance schedules, \
supply chain logistics, and regulatory documentation relevant to production lines."
    ),
    "services": (
        "kb-xxxxxxxx-services",
        "Professional services and delivery: engagement scopes, implementation guides, onboarding frameworks, project plans, SOW templates, \
customer success playbooks, SLAs/OLAs, and post-deployment health checks."
    ),
}