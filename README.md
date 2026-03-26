Project Overview & Personal Journey
I built this project as part of the technical challenge for the Software Engineer Intern position at Veridion. As an aspiring Data Engineer, I chose the Website Technologies Scraper task because I wanted to see if I could build a real "data pipeline" from scratch.

Before I wrote any code, I spent a lot of time researching how websites actually work "under the hood." I had to learn which libraries are best for this job and how to split my code so it doesn't become a mess. It was a journey of watching a lot of YouTube tutorials, reading documentation, and trial-and-error.

How I Built It: Step-by-Step
I decided to divide the project into two main files to keep things organized and easier to follow:

1. Researching "Digital Fingerprints"
I researched how industry-standard tools like Wappalyzer identify tech stacks. By studying their open-source schema (e.g., enthec/webappanalyzer), I learned that detection relies on three pillars: HTTP Headers, Meta Tags, and HTML patterns.

I verified this by manually using "Inspect Element" on several sites to see these "fingerprints" live. To scale this process and save time, I used Gemini to help populate tech_signatures.json. I designed the JSON structure and used the AI to generate a large set of common patterns for popular technologies. This allowed me to focus on building the core logic while ensuring the tool could identify a wide range of platforms immediately.

2. Creating the "Helper" (utils.py)
I put the "heavy lifting" logic here:

get_page_content: At first, I thought about using a simple requests call, but I learned that modern sites use a lot of JavaScript. So, I used Playwright. This function opens a "headless" browser (one you can't see), waits for the page to load, and grabs the HTML and the Headers.

check_for_techs: This function is the "brain." It uses BeautifulSoup4 to look through the HTML and see if any of our signatures match. I made sure it's not picky about capital letters (case-insensitive) so it finds more results.

3. The Main Script (main.py)
This is where I tied everything together. It reads the Parquet file (I learned this is a special way to store data efficiently), loads my signatures, and starts the loop to visit each website. At the end, it prints a nice summary in the terminal and saves everything in results.json.

The "Aha!" Moment: Learning from My Mistakes
One of the biggest lessons I learned happened when I started testing. At first, my code was only finding 3 technologies for all 200 sites. I was really confused!

The Problem: After a lot of debugging and re-reading my code, I found a classic "beginner mistake": I had a return statement indented incorrectly inside my loop. This caused the script to stop immediately after checking the very first signature, skipping the other 95% of my rules.

The Fix: I fixed the indentation so the loop could finish checking every signature for every site. I also added a small trick to lowercase all headers at the start so the search is faster.

The Result: My detection count went from 3 to 863 total identifications. It was a great feeling to see the terminal suddenly fill up with results!

Debate Topics: My Thoughts on the Future
a. Current Issues & What I'd Change
Speed: Right now, the script visits sites one by one. It's a bit slow.

The Solution: I've been reading about something called "Async," which would let the script visit multiple sites at the same time. This is something I want to learn next.

b. Scaling to Millions of Domains
If I had to do this for millions of sites in 1-2 months, I think I'd need:

Multiple Workers: Instead of one script, I'd have many "workers" (using tools like Redis or Celery) running on different computers.

Saving Bandwidth: I'd tell the browser not to load images or videos, because we only need the code to find the technologies.

c. Finding New Technologies
I'd keep an eye on open-source lists to see when new frameworks come out.

I'd look for "weird" or new patterns in the headers that I haven't seen before.

4. Research & Documentation 

For - handling headless browsers, managing contexts and rendering JavaScript websites I used : https://playwright.dev/python/docs/intro#running-the-example-test
    - learning how to navigate the  DOM tree and extract specific tags ( Meta, Scripts) efficiently i used : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - learning how to efficiently process the data.snappy.paraquet input file provided for the task , i found: https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html

This helped me to understand the design of the structure for tech_signature.json to ensure it follows industry standards : https://github.com/enthec/webappanalyzer
To learn how infrastructure technologies( Cloudflare, LiteSpeed) identify themselves in response headers I used: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers
I consulted MDN Web Docs to study the structure of the User-Agent header and understand how servers use it for device identification : https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent

To get everything working, I watched many YouTube tutorials that helped me structure my code and learn how to use libraries like pandas, playwright, and beautifulsoup4. These videos were essential for understanding how a User-Agent works and why it's so important in web scraping to avoid being blocked. This process also taught me how much details matter—I even learned the hard way that a single wrong indentation can break the entire logic!🙂

5. 
While running my tests, I noticed that the number of detected technologies can sometimes change slightly between scans. I realized this is a normal part of working with live data. It usualy happens because some websites load scripts at different speeds, or their security systems (anti-bot filters) might block certain headers during one scan but not the next. 

The last test of my code showed :

Domains Processed: 200

Total Technologies Identified: 863 (Average of 4.3 per site)

Success Rate: ~81.5% (The ones that failed were mostly because the sites were down or blocked my "bot").