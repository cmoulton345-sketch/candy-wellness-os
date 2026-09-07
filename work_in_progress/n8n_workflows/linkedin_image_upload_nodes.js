// ============================================================
// NEW NODE: "Fetch Image & Upload to LinkedIn"
// Type: Code Node  |  Mode: Run Once for All Items
// Place: After "Approved?" (Yes branch), BEFORE "Prepare LinkedIn (Approved)"
//        AND after "Force Publish or Retry?" → BEFORE "Prepare LinkedIn (Forced)"
// ============================================================

const PEXELS_API_KEY = 'YOUR_PEXELS_API_KEY'; // ← paste your Pexels key here

const topic = $('Pick Random Topic').first().json.topic || 'business technology';
const ACCESS_TOKEN = $('Setup Variables').first().json.linkedin_access_token;
const AUTHOR_URN = $('Setup Variables').first().json.linkedin_author_urn;

// ── STEP 1: Search Pexels for a relevant landscape photo ──
const searchResponse = await this.helpers.httpRequest({
  method: 'GET',
  url: `https://api.pexels.com/v1/search?query=${encodeURIComponent(topic)}&per_page=15&orientation=landscape`,
  headers: { 'Authorization': PEXELS_API_KEY }
});

const photos = searchResponse.photos;
if (!photos || photos.length === 0) {
  throw new Error(`No Pexels photos found for topic: "${topic}"`);
}

const photo = photos[Math.floor(Math.random() * photos.length)];

// ── STEP 2: Download the image binary ──
const imageResponse = await this.helpers.httpRequest({
  method: 'GET',
  url: photo.src.landscape,
  encoding: 'arraybuffer',
  returnFullResponse: true
});
const imageBinary = Buffer.from(imageResponse.body);

// ── STEP 3: Register the upload with LinkedIn ──
const registerResponse = await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://api.linkedin.com/v2/assets?action=registerUpload',
  headers: {
    'Authorization': `Bearer ${ACCESS_TOKEN}`,
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
  },
  body: JSON.stringify({
    registerUploadRequest: {
      owner: AUTHOR_URN,
      recipes: ['urn:li:digitalmediaRecipe:feedshare-image'],
      serviceRelationships: [{
        relationshipType: 'OWNER',
        identifier: 'urn:li:userGeneratedContent'
      }],
      supportedUploadMechanism: ['SYNCHRONOUS_UPLOAD']
    }
  })
});

const parsed = typeof registerResponse === 'string' ? JSON.parse(registerResponse) : registerResponse;
const uploadUrl = parsed.value.uploadMechanism['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest'].uploadUrl;
const assetUrn = parsed.value.asset; // e.g. urn:li:digitalmediaAsset:XXXXXXXXX

// ── STEP 4: Upload the image binary to LinkedIn ──
await this.helpers.httpRequest({
  method: 'PUT',
  url: uploadUrl,
  headers: {
    'Authorization': `Bearer ${ACCESS_TOKEN}`,
    'Content-Type': 'image/jpeg'
  },
  body: imageBinary,
  returnFullResponse: true
});

// ── Return asset URN for use in Prepare LinkedIn ──
return [{
  json: {
    assetUrn,       // ← used in Prepare LinkedIn to attach the image
    imageUrl: photo.src.landscape,
    photographer: photo.photographer,
    topic
  }
}];


// ============================================================
// MODIFIED: "Prepare LinkedIn (Approved)" node
// Replace existing code with this:
// ============================================================
/*
const rawPost = $json.full_post;
const escaped = rawPost.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t');

let assetUrn = null;
try { assetUrn = $('Fetch Image & Upload to LinkedIn').first().json.assetUrn; } catch(e) {}

return [{ json: {
  full_post_escaped: escaped,
  linkedin_access_token: $('Setup Variables').item.json.linkedin_access_token,
  linkedin_author_urn: $('Setup Variables').item.json.linkedin_author_urn,
  image_asset_urn: assetUrn   // ← NEW: passes asset to Publish Post node
} }];
*/


// ============================================================
// MODIFIED: "Prepare LinkedIn (Forced)" node  
// Same change — add image_asset_urn to return object
// ============================================================
/*
const rawPost = $json.full_post;
const escaped = rawPost.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t');

let assetUrn = null;
try { assetUrn = $('Fetch Image & Upload to LinkedIn').first().json.assetUrn; } catch(e) {}

return [{ json: {
  full_post_escaped: escaped,
  linkedin_access_token: $('Setup Variables').item.json.linkedin_access_token,
  linkedin_author_urn: $('Setup Variables').item.json.linkedin_author_urn,
  image_asset_urn: assetUrn   // ← NEW
} }];
*/

// ============================================================
// MODIFIED: "LinkedIn: Publish Post" node — JSON body
// Replace the existing JSON body with this.
// Key changes:
//   1. shareMediaCategory: "NONE" → "IMAGE"
//   2. Add "media" array referencing the asset URN
// ============================================================
/*
{
  "author": "{{ $json.linkedin_author_urn }}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "{{ $json.full_post_escaped }}"
      },
      "shareMediaCategory": "IMAGE",
      "media": [
        {
          "status": "READY",
          "description": { "text": "" },
          "media": "{{ $json.image_asset_urn }}",
          "title": { "text": "" }
        }
      ]
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
*/

// ============================================================
// SUMMARY — 4 changes to make in n8n:
//
// 1. ADD new Code node "Fetch Image & Upload to LinkedIn"
//    → paste Node 1 code above (lines 1–75)
//    → wire: Approved? (Yes) → [NEW] → Prepare LinkedIn (Approved)
//    → wire: Force Publish → [NEW] → Prepare LinkedIn (Forced)
//
// 2. REPLACE "Prepare LinkedIn (Approved)" code with modified version (lines 84–96)
//
// 3. REPLACE "Prepare LinkedIn (Forced)" code with modified version (lines 103–115)
//
// 4. REPLACE "LinkedIn: Publish Post" JSON body with updated version above
//
// Don't forget: paste your Pexels API key on line 8.
// ============================================================
  binary: {
    data: binaryData
  }
}];


// ============================================================
// NODE 2: Register LinkedIn Image Upload
// Type: HTTP Request node
// Method: POST
// URL: https://api.linkedin.com/v2/assets?action=registerUpload
// Auth: LinkedIn OAuth2 API (select your existing credential)
// Body: JSON (see below)
// ============================================================
/*
BODY (JSON):
{
  "registerUploadRequest": {
    "owner": "urn:li:person:YOUR_LINKEDIN_PERSON_ID",
    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
    "serviceRelationships": [{
      "relationshipType": "OWNER",
      "identifier": "urn:li:userGeneratedContent"
    }],
    "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
  }
}

OUTPUT will contain:
- value.uploadMechanism['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest'].uploadUrl
- value.asset  (this is the asset URN you'll reference in the post)
*/


// ============================================================
// NODE 3: Upload Image to LinkedIn
// Type: HTTP Request node
// Method: PUT
// URL (expression):
//   ={{ $json.value.uploadMechanism['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest'].uploadUrl }}
// Auth: LinkedIn OAuth2 API (same credential)
// Body: Binary data from "Fetch Pexels Image" node → data property
// Send as: Binary
// ============================================================
// LinkedIn returns 201 Created on success — no body returned.
// After this node, the asset is ready to reference in your post.


// ============================================================
// MODIFICATION TO "Prepare LinkedIn (Approved)" node
// Add this to your existing payload — share it and I'll write the exact code
// ============================================================
/*
The asset ID looks like: urn:li:digitalmediaAsset:XXXXXXXXXXXXX
Reference it in your post payload like this:

"content": {
  "contentEntities": [{
    "entity": "{{ $('Register LinkedIn Upload').first().json.value.asset }}"
  }],
  "shareMediaCategory": "IMAGE"
}
*/
