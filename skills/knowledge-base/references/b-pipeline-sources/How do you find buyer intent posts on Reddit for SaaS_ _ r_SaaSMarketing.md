---
sourceFile: "How do you find buyer intent posts on Reddit for SaaS? : r/SaaSMarketing"
exportedBy: "Kortex"
exportDate: "2026-03-12T11:19:51.077Z"
---

# How do you find buyer intent posts on Reddit for SaaS? : r/SaaSMarketing

b957940d-b537-4a90-b509-05e0a35b8326

How do you find buyer intent posts on Reddit for SaaS? : r/SaaSMarketing

7a8cd6df-77d4-4ace-bb76-26943e52a5da

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/how\_do\_you\_find\_buyer\_intent\_posts\_on\_reddit\_for/

How do you find buyer intent posts on Reddit for SaaS? : r/SaaSMarketing

Skip to main content

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/how\_do\_you\_find\_buyer\_intent\_posts\_on\_reddit\_for/#main-content

How do you find buyer intent posts on Reddit for SaaS? : r/SaaSMarketing

Open navigation

https://www.reddit.com/

Go to Reddit Home

r/SaaSMarketing

TRENDING TODAY

Get the Reddit app

https://www.reddit.com/login/

Log in to Reddit

Expand user menu

Open settings menu

Skip to Navigation

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/how\_do\_you\_find\_buyer\_intent\_posts\_on\_reddit\_for/#left-sidebar-container

Skip to Right Sidebar

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/how\_do\_you\_find\_buyer\_intent\_posts\_on\_reddit\_for/#right-sidebar-container

Go to SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

addicted-coffee

https://www.reddit.com/user/addicted-coffee/

Locked post

Stickied post

Archived post

View post in other languages

How do you find buyer intent posts on Reddit for SaaS?

what's your system for finding high intent posts on Reddit?

I've been manually scanning subreddit and a few niche subs looking for posts where people ask for tool recommendations. It works but its not scalable.

#### Things I tried that didnt work:

Google Alerts (too slow)

Keyword searches (too much noise)

Social listening tools (built for agencies, too expensive)

I'm thinking about just building something myself. Would monitor specific subreddits and use intent classification to filter for posts where people are actually looking for solutions.

Would also label them by buyer stage and suggest reply angles so you dont sound spammy.

Before I build it I want to validate other people have this problem too.

But genuinely curious - do you have a better system? Or is manual scrolling just part of the game now?

edit 1: if anyone wants context, here's a short write-up + form for

https://leadhunt-eta.vercel.app/

Comments Section

https://www.reddit.com/user/kubrador/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzd5u2l/

manual scrolling is the game for most people, you're not missing some secret

the diy approach you're describing sounds reasonable but fair warning: the "intent classification" part is where everyone's side project goes to die. distinguishing "i need a tool" from "i'm venting about tools" is harder than it sounds

if you build it, keep the scope tiny. like, embarrassingly tiny. one subreddit, one keyword pattern, slack notifications. validate before you add the "buyer stage labeling" stuff

addicted-coffee

https://www.reddit.com/user/addicted-coffee/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzd7oc7/

Fair point. I agree this is where most side projects die.

I'm deliberately keeping the scope narrow though: not trying to “detect all intent,” just reduce how much founders have to manually scan.

That means posts only, aggressive pre-filtering, high confidence threshold (if it's ambiguous, it's dropped), and always explaining

something was flagged so people can ignore it.

Goal isn't to replace judgment, just surface a smaller, earlier shortlist so manual scanning starts closer to “worth replying to.”

Developer\_Akash

https://www.reddit.com/user/Developer\_Akash/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzdegk3/

yeah manual scrolling def doesn't scale, and most social listening tools are built for brand monitoring so they suck for this. honestly what you're describing is exactly what we built at

CatchIntent

https://catchintent.com/

, AI filters out the noise and surfaces actual intent posts so you're not going through hundreds of "what's everyone using" threads that go nowhere.

https://www.reddit.com/user/smarkman19/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzf6nlu/

High-intent posts are 90% about timing and 10% about clever filters, so the main point is you're right to focus on classification + angles, not just keyword alerts. What's worked for me is stacking a few layers:

Start with scoped sub lists (where your ICP actually hangs, not just big SaaS subs) and predefine “buying” patterns: “alternatives to”, “what do you use for”, “any tools for”, “moving from X to Y”, etc. Regex > plain keyword search.

Pipe subreddit RSS into something like Slack/Discord via Zapier/Make, then run a lightweight classifier (OpenAI or Claude) on title + body to tag intent and stage. Store examples and keep fine-tuning your prompt with false positives.

Have canned reply frameworks by stage: problem-aware (diagnose + questions), solution-aware (compare tradeoffs), product-aware (specific use case + 1 proof point). That keeps you from sounding like an ad.

I've tried F5Bot and Brand24 for broad alerts, but Pulse for Reddit plus a simple homebrew classifier is what made it feel scalable without agency-level tools. So the main point: manual scrolling should become QA, not the core system-your idea is basically the right architecture.

addicted-coffee

https://www.reddit.com/user/addicted-coffee/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzh2jcu/

This is super helpful, appreciate you writing it out.

You're basically describing the exact direction I'm testing: scoped subs only, aggressive pre-filtering, then lightweight classification just to shrink the haystack. Manual scanning still happens, but later and with fewer false positives.

I like the framing of “manual becomes QA, not the system.” That's a good way to think about it.

WallerBangGod

https://www.reddit.com/user/WallerBangGod/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzgjtub/

Forumscout does this on autopilot: monitors reddit (and other platforms like LinkedIn) for posts containing certain keywords, and uses AI to filter them so you only see the ones that are warm leads for your company/product/service

https://www.reddit.com/user/software38/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/o1u1wn1/

We plugged a keyword search tool (KWatch.io) into an LLM API (NLP Cloud). It was possible because KWatch returns results as API webhooks. On the NLP Cloud side we use GPT OSS 120B to automatically detect buying intent.

Hope it's useful!

https://www.reddit.com/user/yj292/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/o5c4cd9/

that's honestly where meltwater has worked well for me. it goes deeper than surface sentiment and helps uncover complaints, feature gaps, and category conversations that actually point to intent.

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzd65xm/

Comment removed by moderator

https://www.reddit.com/user/iBornToWin/

https://www.reddit.com/r/SaaSMarketing/comments/1qbtzm9/comment/nzdicag/

What is intent filter and how do you use it ? Something in API ? Can you talk a little about your e2 flow ? Will help a lot for people starting out like me.

Also even if you find the posts or users, we still need to manually take action like writing comments or DM. So isn't the problem of scaling will still exist ?

Related Answers Section

Related Answers

Top marketing tools for SaaS startups

https://www.reddit.com/answers/58334540-6e24-4a87-a145-32138aac9089/?q=Top+marketing+tools+for+SaaS+startups&source=PDP

How to price your SaaS product competitively

https://www.reddit.com/answers/49a87754-bbed-476e-89d2-7fd7d9b4a93a/?q=How+to+price+your+SaaS+product+competitively&source=PDP

Best practices for SaaS onboarding processes

https://www.reddit.com/answers/b3879ed5-2c62-4aad-b65c-d76621d6afc6/?q=Best+practices+for+SaaS+onboarding+processes&source=PDP

Innovative ways to generate leads for SaaS

https://www.reddit.com/answers/4483986c-5f0d-4f1b-af0d-0c1658154ff7/?q=Innovative+ways+to+generate+leads+for+SaaS&source=PDP

Common mistakes in SaaS marketing campaigns

https://www.reddit.com/answers/72e4b7e6-92e1-44a2-8ce6-94f5d1491561/?q=Common+mistakes+in+SaaS+marketing+campaigns&source=PDP

New to Reddit?

Create your account and connect with a world of communities.

Continue with Email

https://www.reddit.com/register/

Continue With Phone Number

https://www.reddit.com/login/

By continuing, you agree to our

User Agreement

https://www.redditinc.com/policies/user-agreement

and acknowledge that you understand the

Privacy Policy

https://www.redditinc.com/policies/privacy-policy

More posts you may like

I am looking for great saas that are for sale

https://www.reddit.com/r/SaaSSolopreneurs/comments/1qupiqr/i\_am\_looking\_for\_great\_saas\_that\_are\_for\_sale/

r/SaaSSolopreneurs

https://www.reddit.com/r/SaaSSolopreneurs/

- 1mo ago \[

I am looking for great saas that are for sale

\](https://www.reddit.com/r/SaaSSolopreneurs/comments/1qupiqr/i\_am\_looking\_for\_great\_saas\_that\_are\_for\_sale/) 17 upvotes · 27 comments

I ran Reddit marketing for 10+ SaaS companies, and here's what actually works

https://www.reddit.com/r/b2bmarketing/comments/1qbfbsh/i\_ran\_reddit\_marketing\_for\_10\_saas\_companies\_and/

r/b2bmarketing

https://www.reddit.com/r/b2bmarketing/

- 2mo ago \[

I ran Reddit marketing for 10+ SaaS companies, and here's what actually works

\](https://www.reddit.com/r/b2bmarketing/comments/1qbfbsh/i\_ran\_reddit\_marketing\_for\_10\_saas\_companies\_and/) 126 upvotes · 64 comments

How to get 5 clients per day with Reddit for your SAAS

https://www.reddit.com/r/micro\_saas/comments/1nvztvy/how\_to\_get\_5\_clients\_per\_day\_with\_reddit\_for\_your/

r/micro\_saas

https://www.reddit.com/r/micro\_saas/

- 5mo ago \[

How to get 5 clients per day with Reddit for your SAAS

\](https://www.reddit.com/r/micro\_saas/comments/1nvztvy/how\_to\_get\_5\_clients\_per\_day\_with\_reddit\_for\_your/) 42 upvotes · 13 comments

Looking to buy a small Saas

https://www.reddit.com/r/SaaSSolopreneurs/comments/1qm5qza/looking\_to\_buy\_a\_small\_saas/

r/SaaSSolopreneurs

https://www.reddit.com/r/SaaSSolopreneurs/

- 1mo ago \[

Looking to buy a small Saas

\](https://www.reddit.com/r/SaaSSolopreneurs/comments/1qm5qza/looking\_to\_buy\_a\_small\_saas/) 7 upvotes · 18 comments

How to get 5 clients per day with Reddit for your SAAS

https://www.reddit.com/r/SaaS/comments/1nvzrx0/how\_to\_get\_5\_clients\_per\_day\_with\_reddit\_for\_your/

https://www.reddit.com/r/SaaS/

- 5mo ago \[

How to get 5 clients per day with Reddit for your SAAS

\](https://www.reddit.com/r/SaaS/comments/1nvzrx0/how\_to\_get\_5\_clients\_per\_day\_with\_reddit\_for\_your/) 42 upvotes · 34 comments

Most SaaS posts die quietly on Reddit. Here's where they should go instead.

https://www.reddit.com/r/microsaas/comments/1mb96uy/most\_saas\_posts\_die\_quietly\_on\_reddit\_heres\_where/

r/microsaas

https://www.reddit.com/r/microsaas/

- 8mo ago \[

Most SaaS posts die quietly on Reddit. Here's where they should go instead.

\](https://www.reddit.com/r/microsaas/comments/1mb96uy/most\_saas\_posts\_die\_quietly\_on\_reddit\_heres\_where/) 35 upvotes · 8 comments

I'm looking for some honest advice from people who've actually scaled SaaS.

https://www.reddit.com/r/SaaSMarketing/comments/1pvxzom/im\_looking\_for\_some\_honest\_advice\_from\_people/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 2mo ago \[

I'm looking for some honest advice from people who've actually scaled SaaS.

\](https://www.reddit.com/r/SaaSMarketing/comments/1pvxzom/im\_looking\_for\_some\_honest\_advice\_from\_people/) 6 upvotes · 20 comments

Drop your SaaS. I will make you rank on ChatGPT

https://www.reddit.com/r/SaaSMarketing/comments/1nq0obp/drop\_your\_saas\_i\_will\_make\_you\_rank\_on\_chatgpt/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 6mo ago \[

Drop your SaaS. I will make you rank on ChatGPT

\](https://www.reddit.com/r/SaaSMarketing/comments/1nq0obp/drop\_your\_saas\_i\_will\_make\_you\_rank\_on\_chatgpt/) 74 upvotes · 107 comments

This Guy Built 5 'Boring' SaaS Apps and Makes $200K/Month. He Says New Ideas Are the Biggest Mistake

https://www.reddit.com/r/SaaSMarketing/comments/1r7625y/this\_guy\_built\_5\_boring\_saas\_apps\_and\_makes/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 21d ago \[

This Guy Built 5 'Boring' SaaS Apps and Makes $200K/Month. He Says New Ideas Are the Biggest Mistake

\](https://www.reddit.com/r/SaaSMarketing/comments/1r7625y/this\_guy\_built\_5\_boring\_saas\_apps\_and\_makes/) 90 upvotes · 29 comments

My SaaS made $100 in just one week! 🚀

https://www.reddit.com/r/microsaas/comments/1ni8auu/my\_saas\_made\_100\_in\_just\_one\_week/

r/microsaas

https://www.reddit.com/r/microsaas/

- 6mo ago \[

My SaaS made $100 in just one week! 🚀

\](https://www.reddit.com/r/microsaas/comments/1ni8auu/my\_saas\_made\_100\_in\_just\_one\_week/)

84 upvotes · 50 comments

Reddit SEO is bringing me 300+ visitors/day. No blog required. (Easy strategy)

https://www.reddit.com/r/micro\_saas/comments/1rlikhr/reddit\_seo\_is\_bringing\_me\_300\_visitorsday\_no\_blog/

r/micro\_saas

https://www.reddit.com/r/micro\_saas/

Reddit SEO is bringing me 300+ visitors/day. No blog required. (Easy strategy)

\](https://www.reddit.com/r/micro\_saas/comments/1rlikhr/reddit\_seo\_is\_bringing\_me\_300\_visitorsday\_no\_blog/) 171 upvotes · 40 comments

How to get your first SaaS customers as fast as possible

https://www.reddit.com/r/indie\_startups/comments/1rc1i7o/how\_to\_get\_your\_first\_saas\_customers\_as\_fast\_as/

r/indie\_startups

https://www.reddit.com/r/indie\_startups/

- 15d ago \[

How to get your first SaaS customers as fast as possible

\](https://www.reddit.com/r/indie\_startups/comments/1rc1i7o/how\_to\_get\_your\_first\_saas\_customers\_as\_fast\_as/) 55 upvotes · 19 comments

How one viral video generated $15k+ in new MRR for our SaaS

https://www.reddit.com/r/indie\_startups/comments/1qtr8n7/how\_one\_viral\_video\_generated\_15k\_in\_new\_mrr\_for/

r/indie\_startups

https://www.reddit.com/r/indie\_startups/

- 1mo ago \[

How one viral video generated $15k+ in new MRR for our SaaS

\](https://www.reddit.com/r/indie\_startups/comments/1qtr8n7/how\_one\_viral\_video\_generated\_15k\_in\_new\_mrr\_for/) 31 upvotes · 11 comments

How I got my first 20 SaaS customers (on Linkedin)

https://www.reddit.com/r/SaaSMarketing/comments/1nq2v1t/how\_i\_got\_my\_first\_20\_saas\_customers\_on\_linkedin/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 6mo ago \[

How I got my first 20 SaaS customers (on Linkedin)

\](https://www.reddit.com/r/SaaSMarketing/comments/1nq2v1t/how\_i\_got\_my\_first\_20\_saas\_customers\_on\_linkedin/) 29 upvotes · 16 comments

5 habits every SaaS founder needs to hit $10k MRR in 90 days

https://www.reddit.com/r/SaaSMarketing/comments/1m3278f/5\_habits\_every\_saas\_founder\_needs\_to\_hit\_10k\_mrr/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 8mo ago \[
5 habits every SaaS founder needs to hit $10k MRR in 90 days

\](https://www.reddit.com/r/SaaSMarketing/comments/1m3278f/5\_habits\_every\_saas\_founder\_needs\_to\_hit\_10k\_mrr/) 71 upvotes · 27 comments

Reddit marketing is underrated - 30 Day Case Study

https://www.reddit.com/r/juststart/comments/1p5ulbs/reddit\_marketing\_is\_underrated\_30\_day\_case\_study/

r/juststart

https://www.reddit.com/r/juststart/

- 4mo ago \[

Reddit marketing is underrated - 30 Day Case Study

\](https://www.reddit.com/r/juststart/comments/1p5ulbs/reddit\_marketing\_is\_underrated\_30\_day\_case\_study/) 25 upvotes · 20 comments

5 habits every SaaS founder needs to hit $10k MRR in 90 days

https://www.reddit.com/r/SaaSMarketing/comments/1mmgm6u/5\_habits\_every\_saas\_founder\_needs\_to\_hit\_10k\_mrr/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 7mo ago \[
5 habits every SaaS founder needs to hit $10k MRR in 90 days

\](https://www.reddit.com/r/SaaSMarketing/comments/1mmgm6u/5\_habits\_every\_saas\_founder\_needs\_to\_hit\_10k\_mrr/) 87 upvotes · 28 comments

I will help your SaaS grow online (and you pay $0 until it works)

https://www.reddit.com/r/SaaSMarketing/comments/1ogll15/i\_will\_help\_your\_saas\_grow\_online\_and\_you\_pay\_0/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 4mo ago \[

I will help your SaaS grow online (and you pay $0 until it works)

\](https://www.reddit.com/r/SaaSMarketing/comments/1ogll15/i\_will\_help\_your\_saas\_grow\_online\_and\_you\_pay\_0/) 23 upvotes · 50 comments

This Guy Built 50 “Useless” Free Tools and Turned It Into a $13K/Month SaaS (No Ads)

https://www.reddit.com/r/SaaSMarketing/comments/1r3tta3/this\_guy\_built\_50\_useless\_free\_tools\_and\_turned/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 25d ago \[

This Guy Built 50 “Useless” Free Tools and Turned It Into a $13K/Month SaaS (No Ads)

\](https://www.reddit.com/r/SaaSMarketing/comments/1r3tta3/this\_guy\_built\_50\_useless\_free\_tools\_and\_turned/) 24 upvotes · 20 comments

What kind of LinkedIn posts get the most attention?

https://www.reddit.com/r/SaaSMarketing/comments/1mzw0wp/what\_kind\_of\_linkedin\_posts\_get\_the\_most\_attention/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 7mo ago \[

What kind of LinkedIn posts get the most attention?

\](https://www.reddit.com/r/SaaSMarketing/comments/1mzw0wp/what\_kind\_of\_linkedin\_posts\_get\_the\_most\_attention/) 5 upvotes · 19 comments

My SaaS got 3200+ users without spending a single dollar on ads

https://www.reddit.com/r/microsaas/comments/1mhy473/my\_saas\_got\_3200\_users\_without\_spending\_a\_single/

r/microsaas

https://www.reddit.com/r/microsaas/

- 7mo ago \[

My SaaS got 3200+ users without spending a single dollar on ads

\](https://www.reddit.com/r/microsaas/comments/1mhy473/my\_saas\_got\_3200\_users\_without\_spending\_a\_single/)

107 upvotes · 48 comments

B2B SaaS Founders: Which Software Listing / Review Sites Actually Generate Leads or Sales?

https://www.reddit.com/r/SaaSMarketing/comments/1qatbni/b2b\_saas\_founders\_which\_software\_listing\_review/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 2mo ago \[

B2B SaaS Founders: Which Software Listing / Review Sites Actually Generate Leads or Sales?

\](https://www.reddit.com/r/SaaSMarketing/comments/1qatbni/b2b\_saas\_founders\_which\_software\_listing\_review/) 7 upvotes · 29 comments

Building a SaaS, cold outreach or paid ads first?

https://www.reddit.com/r/SaaS/comments/1nzcdfa/building\_a\_saas\_cold\_outreach\_or\_paid\_ads\_first/

https://www.reddit.com/r/SaaS/

- 5mo ago \[

Building a SaaS, cold outreach or paid ads first?

\](https://www.reddit.com/r/SaaS/comments/1nzcdfa/building\_a\_saas\_cold\_outreach\_or\_paid\_ads\_first/) 29 upvotes · 28 comments

Marketing a SaaS is 10x harder than building it (and no one talks about the boring parts)

https://www.reddit.com/r/SaaSMarketing/comments/1r8bt41/marketing\_a\_saas\_is\_10x\_harder\_than\_building\_it/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 20d ago \[

Marketing a SaaS is 10x harder than building it (and no one talks about the boring parts)

\](https://www.reddit.com/r/SaaSMarketing/comments/1r8bt41/marketing\_a\_saas\_is\_10x\_harder\_than\_building\_it/) 7 upvotes · 18 comments

I need help Marketing

https://www.reddit.com/r/SaaSMarketing/comments/1o4t66e/i\_need\_help\_marketing/

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

- 5mo ago \[

I need help Marketing

\](https://www.reddit.com/r/SaaSMarketing/comments/1o4t66e/i\_need\_help\_marketing/) 26 upvotes · 39 comments

Community Info Section

r/SaaSMarketing

https://www.reddit.com/r/SaaSMarketing/

SaaSMarketing

A community dedicated to sharing and discussing all aspects of SaaS marketing, from super tactical stuff all the way up to overarching strategy. If you're a SaaS founder and you're making $5K-$500K MRR, consider joining our premium mastermind community StartupSauce.com as well.

Anyone can view, post, and comment to this community

Reddit Rules

https://www.redditinc.com/policies/content-policy

Privacy Policy

https://www.reddit.com/policies/privacy-policy

User Agreement

https://www.redditinc.com/policies/user-agreement

Your Privacy Choices

https://support.reddithelp.com/hc/articles/43980704794004

Accessibility

https://support.reddithelp.com/hc/sections/38303584022676-Accessibility

Reddit, Inc. © 2026. All rights reserved.

https://redditinc.com/

Expand Navigation

Expand Navigation

Collapse Navigation

Collapse Navigation

0cAFcWeA7vLoKmiCmej\_Sk33TvYWa9JvSoY3xbEBA-6d6VnqyGq-W3R57tgcXttQn-3IUo0vUXFY4v3DI7wmDTBUUGdzYfwSoIo7iDAOZlw4OZqsc9Z99POd6FZz0k4CQX1RDabR0gKEqn-NLGNqkJEqh7O8DO\_5i93qqwte5sPSVTHyYcRDz2R3k1FL6AFI3v\_i6Aqyel3DIMU\_jERIFVfsSKh9Gvmf39Xs\_OyTPigdOZhqD\_knoO8AR2Hu6LRourXLJneE7MMIkehjoyyBCWXbZxqqCW\_bQBLPeGVgeCUHf1RGn6mgxnD4NcR1NcpEsVgTkxiUNQBGIfYa6eGcfUvxLImrZwGd\_Y-Zistl-THYEKd1qwbGhCxdz0IDpAGT\_HqivrOaEPe\_ielA5cLWO\_T8abNVFg0Fapk3R81kvRw9vmKfJ9AZXuwlmuX0DMkazNB6WpV4pP0v4s0uY20s0NbzVdnmHcUwTW\_jxpE0507SIY-gpA\_vGDPbtdaVrzG0x7RLIXMXsf4VJhEqTOR3egGWijZRmmLcejothAs9xw-0eOQwbSiqMnCQ-iBQqfdOgmkauSxQYyY4pTJE1FHhqhD3MxpjzhCYWCxyvoU7mSQ4PbxKTbpT5-JbLBrK7xJt5gUj9oDjF2-uC8UiIVQ2VOc88jauASLGditE79LkALqYNLM8MXUGYCvwnWy4ckUBGaj07J2uDXsUO6y3bVp-ueLmbz1lZ7EjNx59Jkt3YozDsHJyIqhPr4Aw-VbMxmc2-5O-0AKfJyo8RkW\_PaSArZ5MIBClYUN5e2qS24dL2QNsfFZYwu2iaUp5CEkVsf-vP8usEMA2EUvzdShbs8dv7RUi0oDigM8VmVa1\_Fey8Wic5n4oT8REwA4-mc2QCDbMu-ZEcdacvTUOAmzH4Q29X58oCUo2-7tTcz5kfwcR0JgdSobr1LlXUPPNbbVo0PhRSnTYAR2e4LI4OdOzW5iiMS0o30cbctarC0-zuZxBAKbZSIAO4lq5\_ZzFukaSK7S40nm9CN4VhnCD6imoyKb7oQ76wYvB6xHRQt-W2X9y81fEUX4AXxEIho640f\_TyhzbE4oC73IRoinm0fffpSeOQuSeKi1j5A1fGhCuR\_FpwMlIA9J9ouk2KAaaEiDKE4YspSGuOvkbUJs0z23oNRq\_93OBQlNBATIu91Wo7BR7mU0r8mqqJ3rruxIKN0HYCLSx0iPghEVu0IQAAG9zJew2VOPpJlwApR5hXQpHhfaROOsKCpfil4F9xo\_sFKu1Ixp3SCXgGCByRpHa-I2TdNJnGg7gR8SRqHVVmdMeWMrQU9\_CTnZwLSWDLmp3qZsPHjbz522QFxMwGbkKVPcXf3Rk7LyWmf6cfLjpJEcPZdIs4SeIkU2ud0ph1c8KXnHK7E26xi2NkoziSA8VyDelC1\_6wfk8mJZZNsXn0NHfXEss6YE0Pn8Fr7G821SSVzHXuF0y0GWMVUCdviBTiR10cpjEOWUqzrN2rlXK0sCYjCfcMPJDnWon9tcOjGmcmF0o1rqgJzWdR01tjwbV\_jJScGSRiC0Zzu\_pCbhIxTii4Yb63QdlhUTzLJgyPyAjfYVCk\_XsS1aUvVxj7X-jGj4NSmGvCS1yNdIO26a1GvyZfvPKtqCv3l1dgH4Dw5kPOOSaKx0Sr1Mm-bOC-QW3efogSbTRiGcujTwkv9dEwJu-PpJx2JkrxEQwNFxdoyrmFvFqwmWroK-SZONlsd5BY3u9g4yQKRcJAc470N-OPuUnbkdTunuFe8JAX9ihi-OsizDM8jDG7rnnqND\_Ya4gwQF\_b1EGS43vSnobej45PUMyo7wV0yOp4h1WWt6J09SnJv\_anhTd1nqjxrt73cZqUSaKyu6kU7QJvCbGlJccTh3GsPVy-1CpwYpfR\_Z-UXzN-0jbNOsPU1LX18da2wMjBI2oBrs6QllA-RGqbEphCm5WhrkLI6cBKfxxw2elDwdYRcILOw9jDtojyWYJE3d03X3Q2NmNraUcvdBRjefH3qUl\_IjBosOFnkaYNiJ3b\_J-DtS\_6JGqkSc5QrMPEn62kZ5MtAMc2UDO6R8OCfqY7msT-oJcS4SWqlO0GR9wiUPnn4WIuGys82hBvXWd6LXNRS-NCyKAD3gdOtlnr3gfEtiw

