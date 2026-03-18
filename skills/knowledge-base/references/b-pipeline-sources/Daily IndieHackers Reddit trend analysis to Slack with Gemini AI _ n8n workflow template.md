---
sourceFile: "Daily IndieHackers Reddit trend analysis to Slack with Gemini AI | n8n workflow template"
exportedBy: "Kortex"
exportDate: "2026-03-12T11:19:51.063Z"
---

# Daily IndieHackers Reddit trend analysis to Slack with Gemini AI | n8n workflow template

b5d8d6b0-c72a-4165-863c-eaa983366d10

Daily IndieHackers Reddit trend analysis to Slack with Gemini AI | n8n workflow template

8a3facd3-2433-4d03-b23b-b99a2f58bf6c

https://n8n.io/workflows/7214-daily-indiehackers-reddit-trend-analysis-to-slack-with-gemini-ai/

Daily IndieHackers Reddit trend analysis to Slack with Gemini AI | n8n workflow template

https://n8n.io/

https://github.com/n8n-io/n8n

https://app.n8n.cloud/login

Get Started

https://app.n8n.cloud/register

Back to Templates

https://n8n.io/workflows/

https://n8n.io/integrations/cron/

https://n8n.io/integrations/slack/

https://n8n.io/integrations/reddit/

Daily IndieHackers Reddit trend analysis to Slack with Gemini AI

Use for free

Click to explore

https://n8n.io/creators/charlesnguyen/

Last update

Last update 13 days ago

Market Research

https://n8n.io/workflows/categories/market-research/

Multimodal AI

https://n8n.io/workflows/categories/multimodal-ai/

https://x.com/intent/post?url=https://n8n.io/workflows/7214-daily-indiehackers-reddit-trend-analysis-to-slack-with-gemini-ai/

https://www.linkedin.com/sharing/share-offsite/?url=https://n8n.io/workflows/7214-daily-indiehackers-reddit-trend-analysis-to-slack-with-gemini-ai/

🚀 Daily IndieHackers Reddit Trend Analysis to Slack

Transform Reddit chaos into actionable startup intelligence

Get AI-powered insights from r/indiehackers delivered to your Slack every morning

🎯 Who's It For

This template is designed for

startup founders

growth teams

product managers

who need to:

Stay ahead of indie hacker trends without manual Reddit browsing

Understand what's working in the entrepreneurial community

Get actionable insights for product and marketing decisions

Keep their team informed about emerging opportunities

Perfect for teams building products for entrepreneurs or anyone wanting to leverage community intelligence for competitive advantage.

✨ What It Does

Transform your morning routine with

automated intelligence gathering

that delivers structured, AI-powered summaries of the hottest r/indiehackers discussions directly to your Slack channel.

🧠 Smart Analysis Features

Description

🔥 Hotness Scoring

Calculates engagement scores using time-decay algorithms

📊 Topic Extraction

Identifies key themes and trending subjects

💰 Traction Signals

Spots revenue, metrics, and growth indicators

🎯 Theme Clustering

Groups posts into actionable categories

⚡ Action Items

Generates specific recommendations for your team

📱 Slack Integration

#### Receive beautifully formatted messages with:

Executive summaries and key takeaways

Top 3 hottest posts with engagement metrics

Interactive buttons for deeper exploration

Team discussion prompts

⚙ How It Works

graph LR
    A\[🕐 Daily 8AM Trigger\] --&gt; B\[📱 Fetch Reddit Posts\]
    B --&gt; C\[🔄 Process Data\]
    C --&gt; D\[🤖 Gemini AI Analysis\]
    D --&gt; E\[✨ Groq Slack Formatting\]
    E --&gt; F\[💬 Deliver to Slack\]

🔄 The Complete Process

Step 1: Automated Trigger

Every morning at 8 AM, the workflow springs into action

Step 2: Reddit Data Collection

Fetches the latest 5 posts from r/indiehackers with full metadata

Step 3: Data Processing

Structures raw Reddit data for optimal AI analysis

Step 4: AI-Powered Analysis

Gemini AI performs deep analysis calculating hotness scores, extracting topics, and identifying patterns

Step 5: Slack Formatting

Groq AI Agent transforms insights into beautiful Slack Block Kit messages

Step 6: Team Delivery

Your designated Slack channel receives the formatted analysis

🛠 Requirements

#### You'll need API access for:

Google Gemini

(OAuth2). All have free tiers available.

🚀 Setup Guide

1⃣ Configure Your Credentials

#### Add these credentials in n8n:

Reddit OAuth2

Google Gemini

Slack OAuth2

. The workflow will guide you through each setup.

2⃣ Customize the Schedule

Daily at 8:00 AM

Edit the "Daily Schedule" cron trigger node

// Example: Run at 9:30 AM
{
  "triggerTimes": {
    "item": \[{ "hour": 9, "minute": 30 }\]
  }
}

3⃣ Set Your Slack Destination

"Send to Slack"

Select your target channel

Configure notification preferences

4⃣ Adjust Analysis Parameters

#### Post Limit:

Change from default 5 posts

// In "Get many posts" Reddit node
"limit": 10  // Recommended: 3-10 posts

#### Context Customization:

{
  "channel\_type": "team",
  "audience": "Growth, Product, and Founders", 
  "cta\_link": "https://your-dashboard.com",
  "timeframe\_label": "This Week"
}

🎨 Customization Options

🔍 Analysis Focus Areas

#### Transform the workflow for different insights:

SaaS-Focused Analysis

Add to Gemini prompt: "Focus on SaaS and B2B insights, 
prioritizing recurring revenue and product-market fit signals"

Geographic Targeting

Add: "Prioritize posts relevant to \[your region/market\]"

Stage-Specific Insights

Add: "Focus on \[early-stage/growth-stage\] startup challenges"

📈 Hotness Algorithm Tweaking

#### Default Formula:

(ups + 2\*num\_comments) \* freshness\_decay

#### Emphasize Comments:

(ups + 3\*num\_comments) \* freshness\_decay

#### Include Upvote Ratio:

(ups \* upvote\_ratio + 2\*num\_comments) \* freshness\_decay

🌐 Multi-Subreddit Analysis

#### Expand beyond r/indiehackers:

Additional Communities:
- r/startups
- r/entrepreneur  
- r/SideProject
- r/buildinpublic
- r/nocode

💾 Data Storage Extensions

#### Enhance with historical tracking:

Google Sheets

Trend storage

Historical analysis

Advanced data management

Rich analytics

External analytics

Custom dashboards

📊 Expected Output

📱 Daily Slack Message Structure

🚀 \*\*IndieHackers Trends — This Week\*\*

📋 \*\*TL;DR:\*\* \[One-sentence key insight\]

🔥 \*\*Hot Posts (Top 3)\*\*
1. \[Post Title\] (Hotness: 8.7)
   Topics: SaaS launch, pricing strategy
   💬 23 comments | 👍 156 ups | 📅 Posted 4 hours ago
   \[Open Reddit Button\]

🧭 \*\*Themes Summary\*\*
- Go-to-market tactics — 3 posts, hotness: 24.1
- Product launches — 2 posts, hotness: 18.3

✅ \*\*What to Do Now\*\*
- Test pricing page variations based on community feedback
- Consider cold email strategies mentioned in hot posts
- Validate product ideas using discussed frameworks

\[Open Dashboard Button\]

💡 Pro Tips for Success

🎯 Optimization Strategies

Week 1-2: Baseline

Monitor output quality and team engagement

Note which insights generate the most discussion

Week 3-4: Refinement

Adjust AI prompts based on feedback

Fine-tune hotness scoring for your needs

Month 2+: Advanced Usage

Add historical trend analysis

Create custom dashboards with stored data

Build feedback loops for continuous improvement

🚨 Common Pitfalls to Avoid

API Rate Limits

Reduce post count or increase time intervals

Poor Insight Quality

Refine prompts with specific examples

Team Engagement Drop

Rotate focus areas and encourage thread discussions

Information Overload

Limit to top 3 posts and key themes only

🔧 Troubleshooting

❌ Common Issues & Solutions

"Model not found" Error

Cause: Gemini regional availability
Fix: Check supported regions or switch to alternative AI model

Slack Formatting Broken

Cause: Invalid Block Kit JSON
Fix: Validate JSON structure in AI Agent output

Missing Reddit Data

Cause: API credentials or rate limits
Fix: Verify OAuth2 setup and check usage quotas

AI Timeouts

Cause: Too much data or complex prompts
Fix: Reduce post count or simplify analysis requests

⚡ Performance Optimization

Keep analysis under

for optimal speed

Monitor execution times in n8n logs

Add error handling nodes for production reliability

Use webhook timeouts for external API calls

🌟 Advanced Use Cases

📈 Competitive Intelligence

Modify prompts to track specific competitors or market segments mentioned in discussions

🎯 Product Validation

Focus analysis on posts related to your product category for market research

📝 Content Strategy

Use trending topics to inform your content calendar and thought leadership

🤝 Community Engagement

Identify opportunities to participate in discussions and build relationships

Ready to transform your startup intelligence gathering?

Deploy this workflow and start receiving actionable insights tomorrow morning!

More templates by Charles

Daily IndieHackers Reddit trend analysis to Slack with Gemini AI

\](https://n8n.io/workflows/7214-daily-indiehackers-reddit-trend-analysis-to-slack-with-gemini-ai/)

Generate market research reports from Google Maps reviews with Gemini AI

HTTP Request

Edit Fields (Set)

Loop Over Items (Split in Batches)

\](https://n8n.io/workflows/6928-generate-market-research-reports-from-google-maps-reviews-with-gemini-ai/)

Generate viral Facebook posts with Gemini 2.0 & AI image generation

Google Sheets

HTTP Request

\](https://n8n.io/workflows/8756-generate-viral-facebook-posts-with-gemini-20-and-ai-image-generation/)

Market Research

https://n8n.io/workflows/categories/market-research/

Scrape and summarize webpages with AI

HTTP Request

Edit Fields (Set)

\](https://n8n.io/workflows/1951-scrape-and-summarize-webpages-with-ai/)

Analyze Landing Page with OpenAI and Get Optimization Tips

HTTP Request

OpenAI Chat Model

\](https://n8n.io/workflows/3100-analyze-landing-page-with-openai-and-get-optimization-tips/)

Automated web scraping: email a CSV, save to Google Sheets & Microsoft Excel

Google Sheets

HTTP Request

Microsoft Excel 365

\](https://n8n.io/workflows/2275-automated-web-scraping-email-a-csv-save-to-google-sheets-and-microsoft-excel/)

Multimodal AI

https://n8n.io/workflows/categories/multimodal-ai/

✨🤖Automate Multi-Platform Social Media Content Creation with AI

HTTP Request

\](https://n8n.io/workflows/3066-automate-multi-platform-social-media-content-creation-with-ai/)

Generate AI viral videos with Seedance and upload to TikTok, YouTube & Instagram

Google Sheets

HTTP Request

\](https://n8n.io/workflows/5338-generate-ai-viral-videos-with-seedance-and-upload-to-tiktok-youtube-and-instagram/)

Generate AI videos with Google Veo3, save to Google Drive and upload to YouTube

Google Sheets

HTTP Request

\](https://n8n.io/workflows/4846-generate-ai-videos-with-google-veo3-save-to-google-drive-and-upload-to-youtube/)

Build complex workflows that other tools can't

. I used other tools before. I got to know the N8N and I say it properly: it is better to do everything on the n8n! Congratulations on your work, you are a star!

Igor Fediczko

https://x.com/@igordisco

Thank you to the n8n community

. I did the beginners course and promptly took an automation WAY beyond my skill level.

Robin Tindall

https://x.com/@robm

n8n is a beast for automation.

self-hosting and low-code make it a dev's dream. if you're not automating yet, you're working too hard.

https://x.com/anderoav

I've said it many times. But I'll say it again. n8n is the GOAT

. Anything is possible with n8n. You just need some technical knowledge + imagination. I'm actually looking to start a side project. Just to have an excuse to use n8n more 😅

Maxim Poulsen

@maximpoulsen

https://x.com/@maximpoulsen

It blows my mind.

I was hating on no-code tools my whole life, but n8n changed everything. Made a Slack agent that can basically do everything, in half an hour.

Felix Leber

@felixleber

https://www.linkedin.com/in/felixleber/

I just have to say,

n8n's integration with third-party services is absolutely mind-blowing

. It's like having a Swiss Army knife for automation. So many tasks become a breeze, and I can quickly validate and implement my ideas without any hassle.

https://x.com/1ronben

Found the holy grail of automation yesterday...

Yesterday I tried n8n and it blew my mind 🤯 What would've taken me 3 days to code from scratch? Done in 2 hours. The best part? If you still want to get your hands dirty with code (because let's be honest, we developers can't help ourselves 😅), you can just drop in custom code nodes. Zero restrictions.

Francois Laßl

@francois-laßl

https://www.linkedin.com/in/francois-la%C3%9Fl-817937243/

Anything is possible with n8n

. I think @n8n\_io Cloud version is great, they are doing amazing stuff and I love that everything is available to look at on Github.

https://x.com/@jodiem

There's nothing you can't automate with n8n

Our customer's words, not ours.

, and see for yourself.

Start building

https://app.n8n.cloud/register

https://n8n.io/

Automate without limits

Careers Hiring

https://n8n.io/careers/

https://n8n.io/contact/

https://merch.n8n.io/

https://n8n.io/press/

https://n8n.io/legal/

Brand Guideline

https://n8n.io/brandguidelines/

Case Studies

https://n8n.io/case-studies/

Zapier vs n8n

https://n8n.io/vs/zapier/

Make vs n8n

https://n8n.io/vs/make/

https://n8n.io/tools/

AI agent report

https://n8n.io/reports/ai-agent-development-tools/

Affiliate program

https://n8n.io/affiliates/

Expert partners

https://n8n.io/expert-partners/

Join user tests, get a gift

https://internal.users.n8n.cloud/form/n8n-usability-test-signup

https://lu.ma/n8n-events

AI benchmark

https://n8n.io/ai-benchmark/

Popular integrations

Google Sheets

https://n8n.io/integrations/google-sheets/

https://n8n.io/integrations/telegram/

https://n8n.io/integrations/mysql/

https://n8n.io/integrations/slack/

https://n8n.io/integrations/discord/

https://n8n.io/integrations/postgres/

https://n8n.io/integrations/notion/

https://n8n.io/integrations/gmail/

https://n8n.io/integrations/airtable/

Google Drive

https://n8n.io/integrations/google-drive/

Show more integrations

https://n8n.io/integrations/

Trending combinations

HubSpot and Salesforce

https://n8n.io/integrations/hubspot/and/salesforce/

Twilio and WhatsApp

https://n8n.io/integrations/twilio/and/whatsapp-business-cloud/

GitHub and Jira

https://n8n.io/integrations/github/and/jira-software/

Asana and Slack

https://n8n.io/integrations/asana/and/slack/

Asana and Salesforce

https://n8n.io/integrations/asana/and/salesforce/

Jira and Slack

https://n8n.io/integrations/jira-software/and/slack/

Jira and Salesforce

https://n8n.io/integrations/jira-software/and/salesforce/

GitHub and Slack

https://n8n.io/integrations/github/and/slack/

HubSpot and QuickBooks

https://n8n.io/integrations/hubspot/and/quickbooks-online/

HubSpot and Slack

https://n8n.io/integrations/hubspot/and/slack/

Show more integrations

https://n8n.io/integrations/

Top integration categories

Communication

https://n8n.io/integrations/categories/communication/

Development

https://n8n.io/integrations/categories/development/

Cybersecurity

https://n8n.io/integrations/categories/cybersecurity/

https://n8n.io/integrations/categories/ai/

Data & Storage

https://n8n.io/integrations/categories/data-and-storage/

https://n8n.io/integrations/categories/marketing/

Productivity

https://n8n.io/integrations/categories/productivity/

https://n8n.io/integrations/categories/sales/

https://n8n.io/integrations/categories/utility/

Miscellaneous

https://n8n.io/integrations/categories/miscellaneous/

Explore more categories

https://n8n.io/integrations/

Trending templates

Creating an API endpoint

https://n8n.io/workflows/1750-creating-an-api-endpoint/

AI agent chat

https://n8n.io/workflows/1954-ai-agent-chat/

Scrape and summarize webpages with AI

https://n8n.io/workflows/1951-scrape-and-summarize-webpages-with-ai/

Joining different datasets

https://n8n.io/workflows/1747-joining-different-datasets/

Back Up Your n8n Workflows To Github

https://n8n.io/workflows/1534-back-up-your-n8n-workflows-to-github/

Very quick quickstart

https://n8n.io/workflows/1700-very-quick-quickstart/

OpenAI GPT-3: Company Enrichment from website content

https://n8n.io/workflows/1862-openai-gpt-3-company-enrichment-from-website-content/

Pulling data from services that n8n doesn't have a pre-built integration for

https://n8n.io/workflows/1748-pulling-data-from-services-that-n8n-doesnt-have-a-pre-built-integration-for/

Convert JSON to an Excel file

https://n8n.io/workflows/1435-convert-json-to-an-excel-file/

Telegram AI Chatbot

https://n8n.io/workflows/1934-telegram-ai-chatbot/

Explore 800+ workflow templates

https://n8n.io/workflows/

Telegram bots

https://blog.n8n.io/telegram-bots/

Open-source chatbot

https://blog.n8n.io/open-source-chatbot/

Open-source LLM

https://blog.n8n.io/open-source-llm/

Open-source low-code platforms

https://blog.n8n.io/open-source-low-code-platforms/

Zapier alternatives

https://blog.n8n.io/free-zapier-alternatives/

Make vs Zapier

https://blog.n8n.io/make-vs-zapier/

https://blog.n8n.io/ai-agents/

AI coding assistants

https://blog.n8n.io/ai-coding-assistants/

ChatGPT Discord bot

https://blog.n8n.io/create-chatgpt-discord-bot/

Best AI chatbot

https://blog.n8n.io/best-ai-chatbot/

Show guides

https://blog.n8n.io/

https://n8n.io/imprint/

https://n8n.io/legal/security/

https://n8n.io/legal/privacy/

Report a vulnerability

https://n8n.io/legal/vulnerability-disclosure-policy/

© 2026 n8n | All rights reserved.

This website uses cookies

We use cookies to personalise content, ads and to analyse our traffic. We also share information about your use of our site with our advertising and analytics partners who may combine it with other information that you've provided to them or that they've collected from your use of their services.

https://n8n.io/legal/?eco\_features=CAMPAIGN\_PERSONALIZATION#privacy

Strictly necessary

\[-\] performance

Performance

\[-\] targeting

\[-\] functionality

Functionality

Save & Close

Decline all

Show details Hide details

Cookie declaration

About cookies

Strictly necessary

Performance

Functionality

Strictly necessary cookies allow core website functionality such as user login and account management. The website cannot be used properly without strictly necessary cookies.

Cookie report

Provider / Domain

Description

\_\_cf\_logged\_in

https://www.cloudflare.com/privacypolicy/

.cloudflare.com

4 weeks 2 days

Part of our security firewall Cloudflare (e.g. identifying trusted users)

AMCVS\_XXXXX

https://www.adobe.com/privacy/policy.html

.cloudflare.com

Adobe Experience Cloud cookie that serves as a flag indicating that the session has been initialized. Its value is always 1 and discontinues when the session has ended.

CF\_VERIFIED\_DEVICE\_XXXXX

https://www.cloudflare.com/privacypolicy/

.cloudflare.com

https://www.cloudflare.com/privacypolicy/

.cloudflare.com

5 months 4 weeks

This cookie is used by Cloudflare to help optimise the performance and security of the website and access to it. They do not contain user credentials, IP anonymisation is used.

This cookie is used for managing user session on the website. It typically maintains the user's state during the session, ensuring that users remain connected and their interactions with the site are coherent throughout their visit. This can include keeping users logged in, tracking their actions, or persisting settings during the session.

9 months 4 weeks

\_\_sec\_\_token

\_shopify\_essential

https://www.shopify.com/legal/privacy

merch.n8n.io

This cookie is essential for the secure checkout and payment function on the website and is provided by Shopify.

\_\_Host-airtable-session.sig

https://airtable.com/privacy

airtable.com

This cookie is used to ensure secure user sessions and for authentication purposes.

merch.n8n.io

This cookie is used to maintain an active user session on the website and ensure that the user's connection remains secure and uninterrupted during their browsing session.

9 months 4 weeks

https://airtable.com/privacy

.airtable.com

This cookie is used to record the user's consent to the use of cookies on the website, ensuring compliance with the website's privacy policy by remembering the user's preferences and consent state regarding cookies.

AWSALBTGCORS

https://airtable.com/privacy

airtable.com

This cookie is used to support load balancing, ensuring that visitor page requests are routed to the same server in any browsing session.

9 months 4 weeks

CookieScriptConsent

CookieScript

https://cookie-script.com/privacy-policy.html

This cookie is used by Cookie-Script.com service to remember visitor cookie consent preferences. It is necessary for Cookie-Script.com cookie banner to work properly.

\_\_sec\_\_ghost

9 months 4 weeks

localization

Flickr Inc.

https://www.flickr.com/help/privacy

merch.n8n.io

These cookies are set on pages with the Flickr widget.

\_\_Host-airtable-session

https://airtable.com/privacy

airtable.com

This cookie is used to manage the user session in a secure way, ensuring the user's interaction with the website is seamless and secure while accessing Airtable integrations or content.

Cloudflare Inc.

https://www.cloudflare.com/privacypolicy

.paddle.com

29 minutes 57 seconds

This cookie is used to distinguish between humans and bots. This is beneficial for the website, in order to make valid reports on the use of their website.

Performance cookies are used to see how visitors use the website, eg. analytics cookies. Those cookies cannot be used to directly identify a certain visitor.

Cookie report

Provider / Domain

Description

ph\_phc\_XXXXX\_posthog

https://posthog.com/privacy

.tapfiliate.com

https://www.adobe.com/privacy/policy.html

.cloudflare.com

4 weeks 2 days

Adobe Experience Cloud cookie that enables tracking visitors across multiple domains.

cfz\_google-analytics\_v4

https://policies.google.com/privacy

.cloudflare.com

Cloudflare Zaraz Google Analytics cookie

cfzs\_google-analytics\_v4

https://policies.google.com/privacy

.cloudflare.com

Cloudflare Zaraz Google Analytics session cookie

This cookie is used to recognize and distinguish individual users who visit the website, enabling personalized experiences and interactions.

\_ga\_Q7GL51X95F

https://policies.google.com/privacy

1 year 1 month

This cookie is used by Google Analytics to persist session state.

https://airtable.com/privacy

.airtable.com

This cookie is used to track user behavior and interaction to improve user experience and service functionality.

rl\_page\_init\_referrer

rl\_page\_init\_referring\_domain

originalClientId

4 weeks 2 days

rl\_anonymous\_id

This cookie is used to identify anonymously a visitor. It is generally used for tracking and analytics purposes, helping website owners understand how visitors interact with the site.

n8n\_tracking\_id

1 year 1 month

\_ga\_1EB8LCPG5B

https://policies.google.com/privacy

1 year 1 month

This cookie is used by Google Analytics to persist session state.

\_gat\_gtag\_UA\_146470481\_1

https://policies.google.com/privacy

This cookie is part of Google Analytics and is used to limit requests (throttle request rate).

rl\_group\_id

This cookie is used to group users for analytical purposes to enhance user experience on the website.

\_gat\_gtag\_UA\_146470481\_8

This cookie is part of Google Analytics and is used to limit requests (throttle request rate).

Shopify Inc.

https://www.shopify.com/legal/privacy

1 year 6 hours

This cookie is associated with Shopify's analytics suite.

Provider address: 151 O'Connor Street, Ground floor, Ottawa, ON, K2P 2L8, Canada

https://policies.google.com/privacy

1 year 1 month

This cookie name is associated with Google Universal Analytics - which is a significant update to Google's more commonly used analytics service. This cookie is used to distinguish unique users by assigning a randomly generated number as a client identifier. It is included in each page request in a site and used to calculate visitor, session and campaign data for the sites analytics reports.

https://policies.google.com/privacy

This cookie is set by Google Analytics. It stores and update a unique value for each page visited and is used to count and track pageviews.

\_ga\_0SC4FF2FH9

https://policies.google.com/privacy

1 year 1 month

This cookie is used by Google Analytics to persist session state.

\_shopify\_analytics

merch.n8n.io

Shopify Inc.

https://www.shopify.com/legal/privacy

This cookie is associated with Shopify's analytics suite.

Targeting cookies are used to identify visitors between different websites, eg. content partners, banner networks. Those cookies may be used by companies to build a profile of visitor interests or show relevant ads on other websites.

Cookie report

Provider / Domain

Description

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

linkedin.com targeting

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

linkedin.com targeting

UserMatchHistory

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

4 weeks 2 days

linkedin.com targeting

AnalyticsSyncHistory

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

4 weeks 2 days

linkedin.com targeting

Meta Platform Inc.

https://www.facebook.com/policy.php

.facebook.com

1 year 1 month

This cookie identifies the browser connecting to Facebook. It is not directly tied to individual Facebook the user. Facebook reports that it is used to help with security and suspicious login activity, especially around detection of bots trying to access the service. Facebook also say the behavioural profile associated with each datr cookie is deleted after 10 days. This cookie is also read via Like and other Facebook buttons and tags placed on many different websites.

Meta Platform Inc.

https://www.facebook.com/policy.php

.facebook.com

1 year 1 month

Facebook browser identification, authentication, marketing, and other Facebook-specific function cookies.

Meta Platform Inc.

https://www.facebook.com/policy.php

.facebook.com

This cookie carries out information about how the end user uses the website and any advertising that the end user may have seen before visiting the said website.

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

Identify users who've seen n8n ads on Reddit so that we can run our ads more efficiently.

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

1 year 1 month

This cookie is typically used for tracking user behavior and interaction with the website to improve user experience.

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

1 year 1 month

Used by Reddit to deliver advertising

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

1 year 1 month

This cookie is used to identify a unique visitor's session and preferences.

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

reddit\_session

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

session\_tracker

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

This cookie is used to track user sessions for improving user experience and ensuring secure browsing sessions. It helps in maintaining an active session for the user without needing to log in multiple times during their visit.

t2\_XXXXX\_recentclicks3

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

This cookie is used to store the user's theme preference on the website, allowing for a consistent and personalized visual experience across different pages.

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

Meta Platform Inc.

https://www.facebook.com/policy.php

.facebook.com

1 year 1 month

This cookie is associated with user preferences and saving settings to enhance the user experience on the website.

Meta Platform Inc.

https://www.facebook.com/policy.php

.facebook.com

1 year 1 month

This cookie is used to remember the user's preferences and previous interactions with the website.

Meta Platform Inc.

https://www.facebook.com/policy.php

.facebook.com

Contains browser and user unique ID combination, used for targeted advertising.

Reddit, Inc.

https://www.reddit.com/policies/privacy-policy

.reddit.com

This cookie is used by Cloudflare to identify trusted web traffic.

cfz\_facebook-pixel

Meta Platform Inc.

https://www.facebook.com/policy.php

.cloudflare.com

Cloudflare Zaraz facebook pixel cookie

This cookie is used to collect information about user behavior and preferences to optimize the user experience and for targeted advertising.

\_\_Secure-ROLLOUT\_TOKEN

https://policies.google.com/privacy

.youtube.com

5 months 4 weeks

https://policies.google.com/privacy

Used by Google AdSense for experimenting with advertisement efficiency across websites using their services

rl\_group\_trait

This cookie is used for segmenting audiences based on predefined criteria, aiming to provide more personalized and relevant content to the website users.

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

This is a Microsoft MSN 1st party cookie that ensures the proper functioning of this website.

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

This is a Microsoft MSN 1st party cookie for sharing the content of the website via social media.

https://policies.google.com/privacy

.doubleclick.net

Google Ads targeting

VISITOR\_PRIVACY\_METADATA

https://policies.google.com/privacy

.youtube.com

5 months 4 weeks

This cookie is used to store the user's consent and privacy choices for their interaction with the site. It records data on the visitor's consent regarding various privacy policies and settings, ensuring that their preferences are honored in future sessions.

LinkedIn Corporation

https://www.linkedin.com/legal/privacy-policy

.linkedin.com

5 months 4 weeks

Used to store guest consent to the use of cookies for non-essential purposes

\_\_Secure-YNID

.youtube.com

5 months 4 weeks

https://policies.google.com/privacy

.youtube.com

This cookie is set by YouTube to track views of embedded videos.

VISITOR\_INFO1\_LIVE

https://policies.google.com/privacy

.youtube.com

5 months 4 weeks

This cookie is set by Youtube to keep track of user preferences for Youtube videos embedded in sites;it can also determine whether the website visitor is using the new or old version of the Youtube interface.

test\_cookie

https://policies.google.com/privacy

.doubleclick.net

This cookie is set by DoubleClick (which is owned by Google) to determine if the website visitor's browser supports cookies.

Functionality cookies are used to remember visitor information on the website, eg. language, timezone, enhanced content.

Cookie report

Provider / Domain

Description

intercom-device-id-XXXXX

https://www.intercom.com/legal/privacy

.hockeystack.com

5 months 4 weeks

intercom-id-XXXXX

https://www.intercom.com/legal/privacy

.hockeystack.com

5 months 4 weeks

intercom-session-XXXXX

https://www.intercom.com/legal/privacy

.hockeystack.com

paddle\_session

https://www.paddle.com/legal/privacy

.paddle.com

Cookies are small text files that are placed on your computer by websites that you visit. Websites use cookies to help users navigate efficiently and perform certain functions. Cookies that are required for the website to operate properly are allowed to be set without your permission. All other cookies need to be approved before they can be set in the browser.

You can change your consent to cookie usage at any time on our Privacy Policy page.

We also use cookies to collect data for the purpose of personalizing and measuring the effectiveness of our advertising. For more details, visit the

Google Privacy Policy

https://business.safety.google/privacy/

#### Cookies consent ID :

https://cookie-script.com/cookie-report?identifier=ed53b7b2bda0a83153e40b6660e65372

CookieScript

https://cookie-script.com/

