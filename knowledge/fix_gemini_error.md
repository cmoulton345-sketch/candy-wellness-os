# Fix: "Bad Request" Error in Gemini API Node

## What's Wrong (Simple Version)

Two things are causing the error:

1. **Old model name.** The workflow uses a Gemini model called `gemini-pro` that Google retired. It's like calling a phone number that's been disconnected — Google just says "bad request."

2. **Scraped content breaks the message.** When your workflow scrapes a webpage, that HTML content gets pasted directly into the message sent to Gemini. If the scraped HTML contains quote marks (`"`), it corrupts the message format and Google rejects it.

---

## How to Fix It (Step by Step in n8n)

### Step 1: Fix the Model Name

1. Open your workflow in n8n
2. Click on the **Gemini API** node (the HTTP Request node that calls Google)
3. Find the **URL** field — it will look something like this:
   ```
   https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=...
   ```
4. Change `gemini-pro` to `gemini-2.0-flash`:
   ```
   https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=...
   ```
5. Don't change anything else in the URL — just that one word

---

### Step 2: Fix the Content Problem

This is the bigger fix. You need to add a **Code node** between "HTML Extract" and "Gemini API" to clean the scraped content before sending it.

#### 2a. Add a new Code node

1. In your workflow, hover over the connection line between **HTML Extract** and **Gemini API**
2. Click the **+** button to add a node in between
3. Search for **Code** and select it
4. Name it `Build Gemini Body`

#### 2b. Paste this code into the Code node

```javascript
var scrapedContent = $input.first().json.content || '';
var title = $input.first().json.title || '';

var prompt = 'You are a social media manager. Based on the following scraped content, create a short, engaging Facebook post. Also provide a single keyword that best represents the topic for finding a relevant image.'
  + '\n\n' + 'You MUST respond with ONLY valid JSON in this exact format, no other text:'
  + '\n' + '{"post_text": "your post here", "image_keyword": "keyword"}'
  + '\n\n' + 'Title: ' + title
  + '\n\n' + 'Content:' + '\n' + scrapedContent;

var requestBody = {
  contents: [
    {
      parts: [
        {
          text: prompt
        }
      ]
    }
  ]
};

return [{
  json: {
    requestBody: requestBody
  }
}];
```

#### 2c. Update the Gemini API (HTTP Request) node

1. Click on the **Gemini API** node
2. In the **JSON Body** field, delete everything and replace it with:
   ```
   ={{ JSON.stringify($json.requestBody) }}
   ```
   That's it — one short line. This takes the safely-built message from the Code node and sends it.

---

### Step 3: Test It

1. Click **Test Workflow** (or test just the Gemini API node)
2. You should now get a valid response from Gemini instead of "Bad request"

---

## Your Flow Should Now Look Like This

```
Schedule Trigger → Set Config → Scrape URL → HTML Extract → Build Gemini Body → Gemini API → Parse Response → Get Image → Facebook Post
```

The new node is **Build Gemini Body** — it sits right before Gemini API and makes sure the scraped content is safe to send.
