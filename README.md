# Meta Graph API Insights Pipeline

An automated data pipeline that queries social media metrics using the Meta Graph API, extracts engagement metrics, processes the payload using Python and Pandas, and generates CSV reports.

## Prerequisites
* Python 3.10+
* Meta for Developers Account (Page or Instagram Access Token)

## Environment Variables
Create a `.env` file in the root directory:
```env
META_ACCESS_TOKEN="EAAdwcelOZAVEBSSDhL3uTwvLTkjZCxVKeEQb9LIfbTzZCvJaPXFz2HL2vtYqUapdIhZBV3Eyfetr7ZBNmjcK8sSkPEwIIrXcI39ccT4QaiDJKlQxs89nRF02tbGTUT8PEqqBCQaZCevEDIcjZBMACSwvBGaLVMQb2lqi6z9twVfJZA9j2pTqVMO0aSvZA6mZBQmaTEUmhuLr3vMGrlagIQZCETle17y9xPpcdI5ezjYDg9DfZBomZAPXAaVTDpHdlAngOnpHxzj9e6ROgvsSsNxYQdZBqs"