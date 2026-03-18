---
sourceFile: "Social media sentiment analysis dashboard with custom AI for Twitter, Reddit & LinkedIn | n8n workflow template"
exportedBy: "Kortex"
exportDate: "2026-03-12T11:19:51.112Z"
---

# Social media sentiment analysis dashboard with custom AI for Twitter, Reddit & LinkedIn | n8n workflow template

649c2e0d-73bc-41e8-8aca-69fda1487051

Social media sentiment analysis dashboard with custom AI for Twitter, Reddit & LinkedIn | n8n workflow template

a2f1ca12-898d-46f4-a656-62f7d84deb72

https://n8n.io/workflows/6430-social-media-sentiment-analysis-dashboard-with-custom-ai-for-twitter-reddit-and-linkedin/

Social media sentiment analysis dashboard with custom AI for Twitter, Reddit & LinkedIn | n8n workflow template

https://n8n.io/

https://github.com/n8n-io/n8n

https://app.n8n.cloud/login

Get Started

https://app.n8n.cloud/register

Back to Templates

https://n8n.io/workflows/

Google Sheets

https://n8n.io/integrations/google-sheets/

https://n8n.io/integrations/if/

https://n8n.io/integrations/slack/

Social media sentiment analysis dashboard with custom AI for Twitter, Reddit & LinkedIn

Use for free

vinci-king-01

https://n8n.io/creators/vinci-king-01/

Last update

Last update 13 days ago

Market Research

https://n8n.io/workflows/categories/market-research/

AI Summarization

https://n8n.io/workflows/categories/ai-summarization/

https://x.com/intent/post?url=https://n8n.io/workflows/6430-social-media-sentiment-analysis-dashboard-with-custom-ai-for-twitter-reddit-and-linkedin/

https://www.linkedin.com/sharing/share-offsite/?url=https://n8n.io/workflows/6430-social-media-sentiment-analysis-dashboard-with-custom-ai-for-twitter-reddit-and-linkedin/

Social Media Sentiment Analysis Dashboard with AI and Real-time Monitoring

🎯 Target Audience

Social media managers and community managers

Marketing teams monitoring brand reputation

PR professionals tracking public sentiment

Customer service teams identifying trending issues

Business analysts measuring social media ROI

Brand managers protecting brand reputation

Product managers gathering user feedback

🚀 Problem Statement

Manual social media monitoring is overwhelming and often misses critical sentiment shifts or trending topics. This template solves the challenge of automatically collecting, analyzing, and visualizing social media sentiment data across multiple platforms to provide actionable insights for brand management and customer engagement.

🔧 How it Works

This workflow automatically monitors social media platforms using AI-powered sentiment analysis, processes mentions and conversations, and provides real-time insights through a comprehensive dashboard.

Key Components

#### Scheduled Trigger

- Runs the workflow at specified intervals to maintain real-time monitoring

AI-Powered Sentiment Analysis

- Uses advanced NLP to analyze sentiment, emotions, and topics

Multi-Platform Integration

- Monitors Twitter, Reddit, and other social platforms

Real-time Alerting

- Sends notifications for critical sentiment changes or viral content

#### Dashboard Integration

- Stores all data in Google Sheets for comprehensive analysis and reporting

📊 Google Sheets Column Specifications

#### The template creates the following columns in your Google Sheets:

Description

When the mention was recorded

"2024-01-15T10:30:00Z"

Social media platform

User who posted the content

"@john\_doe"

Full text of the post/comment

"Love the new product features!"

sentiment\_score

Sentiment score (-1 to 1)

sentiment\_label

Sentiment classification

Primary emotion detected

Key topics identified

\["product", "features"\]

Likes, shares, comments

reach\_estimate

Estimated reach

influence\_score

User influence metric

alert\_priority

Alert priority level

🛠 Setup Instructions

Estimated setup time: 20-25 minutes

Prerequisites

n8n instance with community nodes enabled

ScrapeGraphAI API account and credentials

Google Sheets account with API access

Slack workspace for notifications (optional)

Social media API access (Twitter, Reddit, etc.)

Step-by-Step Configuration

1. Install Community Nodes

# Install required community nodes
npm install n8n-nodes-scrapegraphai
npm install n8n-nodes-slack

2. Configure ScrapeGraphAI Credentials

Navigate to Credentials in your n8n instance

Add new ScrapeGraphAI API credentials

Enter your API key from ScrapeGraphAI dashboard

Test the connection to ensure it's working

3. Set up Google Sheets Connection

Add Google Sheets OAuth2 credentials

Grant necessary permissions for spreadsheet access

Create a new spreadsheet for sentiment analysis data

Configure the sheet name (default: "Sentiment Analysis")

4. Configure Social Media Monitoring

parameters in ScrapeGraphAI nodes

Add URLs for social media platforms you want to monitor

Customize the user prompt to extract specific sentiment data

Set up keywords, hashtags, and brand mentions to track

5. Set up Notification Channels

Configure Slack webhook or API credentials

Set up email service credentials for alerts

Define sentiment thresholds for different alert levels

#### Test notification delivery

6. Configure Schedule Trigger

Set monitoring frequency (every 15 minutes, hourly, etc.)

Choose appropriate time zones for your business hours

#### Consider social media platform rate limits

7. Test and Validate

Run the workflow manually to verify all connections

Check Google Sheets for proper data formatting

Test sentiment analysis with sample content

🔄 Workflow Customization Options

Modify Monitoring Targets

Add or remove social media platforms

Change keywords, hashtags, or brand mentions

Adjust monitoring frequency based on platform activity

Extend Sentiment Analysis

Add more sophisticated emotion detection

Implement topic clustering and trend analysis

Include influencer identification and scoring

Customize Alert System

Set different thresholds for different sentiment levels

Create tiered alert systems (info, warning, critical)

Add sentiment trend analysis and predictions

Output Customization

Add data visualization and reporting features

Implement sentiment trend charts and graphs

Create executive dashboards with key metrics

Add competitor sentiment comparison

📈 Use Cases

Brand Reputation Management

: Monitor and respond to brand mentions

Crisis Management

: Detect and respond to negative sentiment quickly

Customer Feedback Analysis

: Understand customer satisfaction and pain points

Product Launch Monitoring

: Track sentiment around new product releases

Competitor Analysis

: Monitor competitor sentiment and engagement

Influencer Identification

: Find and engage with influential users

🚨 Important Notes

Respect social media platforms' terms of service and rate limits

Implement appropriate delays between requests to avoid rate limiting

Regularly review and update your monitoring keywords and parameters

Monitor API usage to manage costs effectively

Keep your credentials secure and rotate them regularly

Consider privacy implications and data protection regulations

🔧 Troubleshooting

#### Common Issues:

ScrapeGraphAI connection errors: Verify API key and account status

Google Sheets permission errors: Check OAuth2 scope and permissions

Sentiment analysis errors: Review the Code node's JavaScript logic

Rate limiting: Adjust monitoring frequency and implement delays

Alert delivery failures: Check notification service credentials

#### Support Resources:

ScrapeGraphAI documentation and API reference

n8n community forums for workflow assistance

Google Sheets API documentation for advanced configurations

Social media platform API documentation

Sentiment analysis best practices and guidelines

More templates by vinci-king-01

Process incoming files and notify via email with GitHub storage

HTTP Request

\](https://n8n.io/workflows/13192-process-incoming-files-and-notify-via-email-with-github-storage/)

Automatically track certification changes with ScrapeGraphAI, GitLab and Rocket.Chat

Edit Fields (Set)

\](https://n8n.io/workflows/12154-automatically-track-certification-changes-with-scrapegraphai-gitlab-and-rocketchat/)

Score and route leads with Clearbit, Mattermost and Trello

HTTP Request

\](https://n8n.io/workflows/12751-score-and-route-leads-with-clearbit-mattermost-and-trello/)

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

AI Summarization

https://n8n.io/workflows/categories/ai-summarization/

Basic automatic Gmail email labelling with OpenAI and Gmail API

Sticky Note

Gmail Trigger

\](https://n8n.io/workflows/2740-basic-automatic-gmail-email-labelling-with-openai-and-gmail-api/)

⚡AI-powered YouTube video summarization & analysis

Edit Fields (Set)

\](https://n8n.io/workflows/2679-ai-powered-youtube-video-summarization-and-analysis/)

Gmail AI Email Manager

Gmail Trigger

\](https://n8n.io/workflows/4722-gmail-ai-email-manager/)

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

