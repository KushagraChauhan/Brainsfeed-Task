## How to use the deployed API?
Open postman and enter the url as- 
```sh
    https://task-brainsfeed.herokuapp.com/getdata
```
where ***getdata*** is the function that gets the following data about the website:
1. Title
2. Screenshot link
3. Short Description
4. Summary 
5. Paid service or not
6. Name of company

The online API does not fetch the emails as it takes time to match the emails with regex expressions on different pages of the website which therefore results in ***Request timeout*** with Heroku server.

Params to be passed-
```sh
    key: url
    value: website address
```

Example API Call-
[DataWallet](https://task-brainsfeed.herokuapp.com/getdata?url=http://www.datawallet.com)

Example API response-
```sh
{
    "Email": "",
    "Name": "Datawallet",
    "Paid Services": "Yes",
    "Screenshot Link": "https://file.io/b3GQiayxngZM",
    "Short Description": "\"Datawallet's Consumer First compliance puts your customers in charge of their data by providing transparency and control. This increases customer trust and maximizes opt-in rates. Who said compliance couldn't be a win-win?\"",
    "Summary": "Drive opt-in permission directly from your users, simplify download and data deletion requests, and build trust with transparency.\nDatawallet's Consumer First compliance puts your customers in charge of their data by providing transparency and control.\nDatawallet is powered by a secure and scalable blockchain giving you immutable proof of your customers data permissions.\nDatawallet gives your users a simple way to opt-in or out of selling their personal info.\nDatawallet gives you a secure mechanism to deliver data files to your users, and manage the download request end-to-end via our integrations or API.\nIntegrate Datawallet with the software your team already uses, or build out your own custom workflows with the Datawallet API.\nCCPA & GDPR mean compliance is no longer about minimizing opt-out.\nDatawallet gives you the tools to effectively request consent for new data collection and its use.\nDatawallet makes this information easy to understand for your users, helping to build trust with transparency.\n87% of customers say they’ll take their business elsewhere if they don’t trust how a company handles their data.",
    "Title": "Everything you need for CCPA and GDPR compliance | Datawallet"
}
```
