const BACKEND = "http://127.0.0.1:8000";

const $ = (id) => document.getElementById(id);
let tabUrl = "";

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  tabUrl = tabs[0]?.url || "";
  $("url").textContent = tabUrl;
});

$("btn").addEventListener("click", async () => {
  $("btn").disabled = true;
  $("err").classList.remove("on");
  $("result").classList.remove("on");
  $("loader").classList.add("on");
  try {
    const dataUrl = await chrome.tabs.captureVisibleTab(null, { format: "jpeg", quality: 90 });
    const b64 = dataUrl.split(",")[1];
    const res = await fetch(`${BACKEND}/api/analyze-url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tabUrl, screenshot_b64: b64 })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Analysis failed");
    const v = data.verdict;
    const action = v.recommended_action || (v.is_phishing ? "block" : "allow");
    const banner = $("banner");
    banner.className = "banner " + action;
    banner.textContent =
      action === "block" ? "PHISHING" :
      action === "warn" ? "SUSPICIOUS" : "SAFE";
    $("conf").textContent = Math.round((v.confidence_score || 0) * 100) + "%";
    $("brand").textContent = v.brand_impersonated || "none";
    $("ms").textContent = data.elapsed_ms + " ms";
    $("reason").textContent = v.reasoning || "";
    $("result").classList.add("on");

    chrome.action.setBadgeText({ text: action === "block" ? "PH" : action === "warn" ? "??" : "OK" });
    chrome.action.setBadgeBackgroundColor({
      color: action === "block" ? "#ef4444" : action === "warn" ? "#f59e0b" : "#22c55e"
    });
  } catch (e) {
    $("err").textContent =
      e.message.includes("Failed to fetch")
        ? "Backend not reachable. Start it with run.ps1 first."
        : e.message;
    $("err").classList.add("on");
  } finally {
    $("btn").disabled = false;
    $("loader").classList.remove("on");
  }
});
