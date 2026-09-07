# n8n Social Automation Guide (Gemini + Facebook)

This configuration uses **Google Gemini** for content generation and **Facebook** for posting.

## Prerequisities

1.  **n8n Instance**
2.  **Google AI (Gemini) API Key**: Get it from [Google AI Studio](https://aistudio.google.com/).
3.  **Facebook App/Page**: You need a Page ID and an Access Token (Graph API) or use n8n's Facebook credential connection.

## Setup Instructions

### 1. Import Workflow
1.  Import `n8n_social_automation.json`.

### 2. Configure Credentials
*   **Gemini Chat**:
    *   Set up a "Google Gemini (PaLM)" credential.
    *   Enter your API Key.
    *   **Note**: Ensure the model is set to `gemini-pro` (or latest available).
*   **Facebook Post**:
    *   Set up "Facebook Graph API" credential.
    *   You will need to authenticate with a Facebook account that manages the Page.
    *   **Node Setup**: Enter your **Page ID** in the "Node ID" field (can be found in Page settings > About).

### 3. Workflow Logic used
1.  **Scrape**: Fetches URL content.
2.  **Gemini**: Analyzes text and returns:
    *   `post_text`: The Facebook caption.
    *   `image_keyword`: A keyword to find a relevant image.
3.  **Unsplash**: Uses the keyword to fetch a *real* high-quality image (free, no API key required for this method).
4.  **Facebook**: Publishes the image + caption to your page.

## Troubleshooting
*   **Gemini JSON Error**: If Gemini doesn't return perfect JSON, the "Parse Gemini JSON" node might fail. You can improve the prompt to enforce strict JSON output.
*   **Facebook Permissions**: Ensure your Facebook App/User has `pages_manage_posts` and `pages_read_engagement` permissions.
