import csv
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

#data lake feature lists and dicts#
PLANS = ["starter", "professional", "enterprise"]
SIZES = ["1-10", "11-50", "51-200", "201-1000", "1000+"]                                       
CHANNELS = ["organic", "google_ads", "linkedin_ads", "referral", "direct_sales"]
INDUSTRIES = ["SaaS", "Fintech", "Healthcare", "Retail", "Manufacturing", "Media"]
CAMPAIGNS_BY_CHANNEL = {             
      "google_ads": [                                                                            
          "GA_BrandSearch_AlwaysOn",                                                             
          "GA_CompetitorTerms_Q1",                                                               
          "GA_HighIntentSearch_Q2",                                                              
          "GA_Retargeting_Display",                                                              
          "GA_YouTubePreroll_Awareness",                                                         
      ],                                                                                         
      "linkedin_ads": [
          "LI_SponsoredContent_ThoughtLeadership",                                               
          "LI_LeadGen_BuyersGuide",
          "LI_SponsoredInMail_Demo",                                                             
          "LI_ABM_Enterprise",
          "LI_JobTitleTargeting_VP_Eng",                                                         
      ],          
      "referral_bonus": [                                                                        
          "Referral_CustomerAdvocacy_Program",
          "Referral_PartnerNetwork_Q1",                                                          
          "Referral_InfluencerProgram_SaaSPodcasts",
          "Referral_FriendsAndFamily",                                                           
      ],
      "content_marketing": [                                                                     
          "Content_SEO_BlogProduction",
          "Content_WebinarSeries_Q2",
          "Content_Whitepaper_StateOfSaaS",                                                      
          "Content_CaseStudies_EnterpriseWins",
          "Content_Newsletter_WeeklyDigest",                                                     
      ],                                                                                         
      "direct_sales": [
          "DS_OutboundSDR_MidMarket",                                                            
          "DS_Conference_SaaStr",
          "DS_FieldEvents_BostonRoadshow",                                                       
          "DS_ABM_Top100Accounts",
          "DS_DemoFollowUp",                                                                     
      ],          
  }
PRIORITIES = ["low", "medium", "high", "critical"]                                 
CATEGORIES = ["billing", "technical", "feature_request", "onboarding"]
PLAN_MRR = {"starter": 49, "professional": 199, "enterprise": 499}
CHURN_PROB_BY_TIER = {"starter": 0.45, "professional": 0.20, "enterprise": 0.08}

#raw customer#
customers = []
for i in range(500):
    customers.append({
        "customer_id": f"CUST_{i:05d}",
        "company_name": fake.unique.company(),
        "plan_tier": random.choice(PLANS),
        "signup_date": fake.date_between(start_date="-18M", end_date = "today"),
        "industry": random.choice(INDUSTRIES),
        "company_size": random.choice(SIZES),
        "acquisition_channel": random.choice(CHANNELS)
    })

with open("../data/raw/customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

#raw marketing spend#
start = date(2024, 10, 1)
end = date(2026, 3, 31)

weeks = []
current = start
while current <= end:
    weeks.append(current)
    current += timedelta(days=7)

marketing_spend = []
spend_id_counter = 0
for channel in CAMPAIGNS_BY_CHANNEL:
    for week in weeks:
        marketing_spend.append({
            "spend_id": f"SPEND_{spend_id_counter:05d}",
            "channel": channel,
            "spend_date": week,
            "amount_usd": round(random.uniform(500, 15000), 2),
            "campaign_name": random.choice(CAMPAIGNS_BY_CHANNEL[channel])
        })
        spend_id_counter += 1

with open("../data/raw/spend.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=marketing_spend[0].keys())
    writer.writeheader()
    writer.writerows(marketing_spend)

#raw support tickets#
tickets = []
ticket_id_counter = 0
for customer in customers:
    randomN = random.randint(0, 8)
    current_ticket_date = customer["signup_date"] + timedelta(days=7)

    for i in range(randomN):
        if random.random() < 0.8:
            resolved_date = current_ticket_date + timedelta(days=random.randint(1,30))
        else:
            resolved_date = None
        tickets.append({
            "ticket_id": f"TICKET_{ticket_id_counter:05d}",
            "customer_id": customer["customer_id"],
            "created_date": current_ticket_date,
            "resolved_date": resolved_date,
            "priority": random.choice(PRIORITIES),
            "category": random.choice(CATEGORIES)
        })
        
        ticket_id_counter += 1
        current_ticket_date += timedelta(days=random.randint(3, 30))
        if current_ticket_date > date(2026, 3, 31):
            break
    
with open("../data/raw/tickets.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
    writer.writeheader()
    writer.writerows(tickets)


#raw subscription events#
events = []
event_id_counter = 0
for customer in customers:
    events.append({
        "event_id": f"EVENT_{event_id_counter:05d}",
        "customer_id": customer["customer_id"],
        "event_type": "signup",
        "event_date": customer["signup_date"],
        "old_plan": None,
        "new_plan": customer["plan_tier"],
        "mrr_change": +PLAN_MRR[customer["plan_tier"]]
    })
    event_id_counter += 1
    churn_prob = CHURN_PROB_BY_TIER[customer["plan_tier"]]
    if random.random() < churn_prob:
        if customer["signup_date"] + timedelta(days=30) > date(2026, 3, 31):
            continue
        churn_date = fake.date_between(
            start_date = customer["signup_date"] + timedelta(days=30),
            end_date = date(2026, 3, 31),
        )
        events.append({
            "event_id": f"EVENT_{event_id_counter:05d}",
            "customer_id": customer["customer_id"],
            "event_type": "churn",
            "event_date": churn_date,
            "old_plan": customer["plan_tier"],
            "new_plan": None,
            "mrr_change": -PLAN_MRR[customer["plan_tier"]]
        })
        event_id_counter += 1

with open("../data/raw/events.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=events[0].keys())
    writer.writeheader()
    writer.writerows(events)
