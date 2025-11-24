# curly-waffle-spark
The "spark" in the name represents my exploration of Apache Spark (along with its libraries). This repository captures that. My successful MongoDB to SparkSQL setup is in `setup - success.ipynb` 

## Next Steps
1. Figure out what kind of data I'd like to scrape (maybe basketball/sports data?)
2. Start pipeline for data scraping (such as a script that executes on a remote server once a day on **AWS Lambda**)
3. Map out system design for the scraped data (data to **AWS S3**)
4. Set up transformation job in **PySpark** and use **AWS Glue** to trigger the transformation when data sent into **S3**
5. When transformation done, send the pre-processed data into **MongoDB** database - likely `Cluster0`. Pre-existing setup in `setup - success.ipynb` is **MongoDB $\rightarrow$ PySpark**, but will need to establish the other way around, or **PySpark $\rightarrow$ MongoDB**
6. Establish analytics, create dashboards/websites with all the findings. Ideas vary, can do more complicated ML if using word/image-based data.
7. Deploy solution using **AWS EC2** or **Vercel**, connecting to the backend using a lightweight API

## Gemini Response for The Pipeline
<h>I asked Google Gemini for how I could set up the pipeline, and it created a comprehensive, AWS-based solution that goes from scraping procedure all the way to deployment. The details are more in depth compared to above, and are in `gemini-response.md`