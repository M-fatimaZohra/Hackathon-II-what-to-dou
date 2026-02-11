# ChatKit UI Blank Issue - Root Cause Analysis

## Status: Events Streaming ✅ | UI Rendering ❌

## Evidence

### What's Working
- ✅ Backend authentication successful
- ✅ SSE events streaming correctly (verified in Network tab)
- ✅ Database persistence working
- ✅ Event sequence correct: thread.created → thread.message.created → response.text.delta → response.done
- ✅ MCP tools executing properly

### What's Broken
- ❌ ChatKit UI completely blank (no input field, no messages, no UI elements)
- ❌ User messages not visible
- ❌ AI responses not visible
- ❌ Chat interface not rendering at all

## Network Tab Evidence

```
data: {"type": "thread.created", "thread": {"id": "204", "title": "Chat 204"}}
data: {"type": "thread.message.created", "message": {"id": "msg-user-204", "role": "user", "content": [{"type": "text", "text": "add task buying fish\n"}]}}
data: {"type": "response.text.delta", "delta": {"text": "I've"}}
data: {"type": "response.text.delta", "delta": {"text": " added"}}
...
data: {"type": "response.done"}
```

**Conclusion**: Events are being sent and received correctly. The problem is in the UI rendering layer.

---

## Root Cause: Web Component Initialization Failure

### Architecture Overview

ChatKit uses a **two-layer architecture**:

1. **React Wrapper** (`@openai/chatkit-react` v1.4.3)
   - Provides React hooks and components
   - Manages state and event handlers
   - Wraps the web component

2. **Web Component** (loaded from CDN)
   - Actual UI rendering happens here
   - Loaded via: `https://cdn.platform.openai.com/deployments/chatkit/chatkit.js`
   - Custom element: `<openai-chatkit>`

### The Problem

The React wrapper is working, but the **web component isn't rendering**. This is evidenced by:

1. **Blank UI** - No input field, no messages, no visual elements
2. **Events received** - Network tab shows events arriving
3. **No console errors reported** - Suggests silent failure

### Likely Causes

#### 1. Web Component Script Not Loading (Most Likely)

**Location**: frontend/src/app/layout.tsx:43-46

```tsx
<Script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  strategy="afterInteractive"
/>
```

**Issues**:
- CDN script might be failing to load (network error, CORS, 404)
- Script might be loading but failing to register the custom element
- Version mismatch between React wrapper (v1.4.3) and CDN script

**How to Verify**:
1. Open Browser DevTools → Console
2. Check for errors related to script loading
3. Run: `console.log(customElements.get('openai-chatkit'))`
   - Should return the constructor function
   - If `undefined`, web component isn't registered

#### 2. CustomApiConfig Incompatibility

**Location**: frontend/src/components/ChatProvider.tsx:77-168

The web component might not support CustomApiConfig properly, or our configuration is missing required fields.

**Current Configuration**:
```typescript
api: {
  domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || 'localhost-dev',
  url: `${CONFIG.API_BASE_URL}/${userId}/chat`,
  fetch: async (input, init) => { /* custom fetch with JWT */ }
}
```

**Potential Issues**:
- Missing required fields for CustomApiConfig
- Web component expects different URL format
- Custom fetch function not compatible with web component

#### 3. Timing Issue

The ChatKit component might be mounting before the web component is defined.

**From ChatKit React source** (node_modules/@openai/chatkit-react/dist/index.js):

```javascript
React.useLayoutEffect(() => {
  const el = ref.current;
  if (!el) return;

  if (customElements.get("openai-chatkit")) {
    el.setOptions(control.options);
    return;
  }

  let active = true;
  customElements.whenDefined("openai-chatkit").then(() => {
    if (active) {
      el.setOptions(control.options);
    }
  });

  return () => {
    active = false;
  };
}, [control.options]);
```

This code waits for the web component to be defined, but if the script never loads, it will wait forever silently.

#### 4. Missing CSS or Styling

The web component might be rendering but invisible due to CSS issues.

**Evidence Against This**:
- The screenshot shows the sidebar is open (backdrop visible)
- The sidebar container is rendering (white background visible)
- Only the ChatKit content area is blank

---

## Diagnostic Steps

### Step 1: Verify Web Component Loading

Open Browser DevTools Console and run:

```javascript
// Check if web component is registered
console.log('ChatKit defined:', customElements.get('openai-chatkit'));

// Check if script loaded
console.log('ChatKit script:', document.querySelector('script[src*="chatkit.js"]'));

// Check for any errors
console.log('Errors:', window.onerror);
```

**Expected Output**:
- `ChatKit defined: function OpenAIChatKit() { ... }`
- `ChatKit script: <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js">`

**If Undefined**:
- Web component script failed to load or register
- Check Network tab for script loading errors
- Check Console for JavaScript errors

### Step 2: Check Network Tab for Script

1. Open DevTools → Network tab
2. Filter by "JS"
3. Look for `chatkit.js` request
4. Check status code (should be 200)
5. Check response size (should be > 0)

**If 404 or Failed**:
- CDN URL is incorrect or unavailable
- Network connectivity issue
- CORS policy blocking the script

### Step 3: Inspect ChatKit Element

Open DevTools → Elements tab and search for `<openai-chatkit>`:

```html
<!-- Expected -->
<openai-chatkit class="...">
  #shadow-root (open)
    <div class="chatkit-container">
      <!-- UI elements here -->
    </div>
</openai-chatkit>

<!-- If Broken -->
<openai-chatkit></openai-chatkit>  <!-- Empty, no shadow root -->
```

**If Empty**:
- Web component registered but not initializing
- Configuration issue preventing render
- Missing required options

### Step 4: Check Console for Warnings

Look for ChatKit-specific warnings:

```
"ChatKit element is not mounted"
"ChatKit: Invalid configuration"
"ChatKit: Missing required option"
```

---

## Recommended Fixes

### Fix 1: Verify Script Loading (Immediate)

Add error handling and logging to layout.tsx:

```tsx
<Script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  strategy="afterInteractive"
  onLoad={() => console.log('ChatKit script loaded')}
  onError={(e) => console.error('ChatKit script failed to load:', e)}
/>
```

### Fix 2: Add Initialization Check (Immediate)

Update ChatAssistant.tsx to verify web component is ready:

```tsx
useEffect(() => {
  const checkChatKit = async () => {
    await customElements.whenDefined('openai-chatkit');
    console.log('ChatKit web component ready');
  };
  checkChatKit();
}, []);
```

### Fix 3: Fallback to HostedApiConfig (Alternative)

If CustomApiConfig isn't working, try HostedApiConfig:

```typescript
api: {
  type: 'hosted',
  apiKey: 'your-api-key',
  // ... other hosted config
}
```

### Fix 4: Add Explicit Height/Width (CSS Fix)

Ensure ChatKit has explicit dimensions:

```tsx
<ChatKit
  control={control}
  className="h-full w-full"
  style={{ minHeight: '400px' }}
/>
```

---

## Next Steps

1. **Run diagnostic commands** in browser console
2. **Check Network tab** for chatkit.js loading
3. **Inspect Elements tab** for `<openai-chatkit>` structure
4. **Report findings** - Share console output and network status
5. **Apply appropriate fix** based on diagnostic results

---

## Additional Context

### ChatKit Version Info
- `@openai/chatkit-react`: v1.4.3
- `@openai/chatkit`: v1.5.0 (types only)
- CDN script: Unknown version (loaded from OpenAI CDN)

### Browser Compatibility
ChatKit requires:
- Modern browser with Web Components support
- Custom Elements v1 API
- Shadow DOM support
- ES6+ JavaScript

### Known Issues
- ChatKit SDK is relatively new (v1.x)
- CustomApiConfig support may be limited
- Documentation may be incomplete
- CDN script version might not match npm package version

---

## Conclusion

The SSE streaming fix (PHR-0047) successfully resolved the event delivery issue. Events are now flowing correctly from backend to frontend. However, the ChatKit web component itself is not rendering, which is a separate issue from the event streaming.

**Most Likely Cause**: Web component script not loading or not initializing properly.

**Immediate Action**: Run diagnostic commands in browser console to determine exact failure point.
