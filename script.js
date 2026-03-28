const HOSTNAME = window.location.hostname;
const IS_LOCAL = HOSTNAME === "127.0.0.1" || HOSTNAME === "localhost";
const IS_GITHUB_PAGES = HOSTNAME === "seenapalliyashwanth.github.io";

const CONFIGURED_API_URL = IS_LOCAL
  ? "http://127.0.0.1:8000"
  : "";

const BASE_URL = CONFIGURED_API_URL.replace(/\/$/, "");

const PLASTIC_RULES = {
  PET: {
    decision: "Recyclable (Not Reusable)",
    explanation:
      "PET is recyclable but not recommended for repeated reuse as it degrades with heat and time."
  },
  HDPE: {
    decision: "Reusable",
    explanation:
      "HDPE is durable, heat-resistant, and commonly used for reusable containers."
  },
  PVC: {
    decision: "Single-use / Avoid Reuse",
    explanation:
      "PVC may release harmful chemicals and is not safe for reuse."
  }
};

function showResult(decision, explanation) {
  document.getElementById("decision").innerText = `Decision: ${decision}`;
  document.getElementById("explanation").innerText = explanation;
  document.getElementById("result").classList.remove("hidden");
}

// analyze based on dropdown selection
async function analyzePlastic() {
  console.log('analyzePlastic invoked');
  const plasticType = document.getElementById("plastic").value;

  if (!plasticType) {
    alert("Please select a plastic type.");
    return;
  }

  const localRule = PLASTIC_RULES[plasticType];
  if (IS_GITHUB_PAGES && localRule) {
    showResult(localRule.decision, `${localRule.explanation} (Local analysis)`);
    return;
  }

  try {
    const response = await fetch(
      `${BASE_URL}/analyze?plastic_type=${plasticType}`
    );
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    const data = await response.json();

    showResult(data.decision, data.explanation);
  } catch (error) {
    alert("Analysis service not reachable. Please try the dropdown option or start the backend.");
    console.error(error);
  }
}

// analyze by uploading an image file
async function analyzeImage() {
  console.log('analyzeImage invoked');
  const input = document.getElementById("imageInput");
  if (input.files.length === 0) {
    alert("Please upload an image.");
    return;
  }

  if (IS_GITHUB_PAGES && !BASE_URL) {
    alert(
      "Image analysis needs a deployed backend API. The GitHub Pages site can use the dropdown locally, but image upload will work only after you deploy the backend and set its URL in script.js."
    );
    return;
  }

  const formData = new FormData();
  formData.append("file", input.files[0]);

  try {
    const response = await fetch(
      `${BASE_URL}/analyze-image`,
      {
        method: "POST",
        body: formData
      }
    );

    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      throw new Error(`Invalid JSON response from server: ${jsonError.message}`);
    }

    if (!response.ok) {
      const details = data?.detail || data?.error || "Unknown server error";
      throw new Error(`Server returned ${response.status}: ${details}`);
    }

    showResult(
      data.decision || data.message || "Unknown",
      (data.explanation || data.detail || "No explanation") + " (Detected via ML)"
    );
  } catch (error) {
    const msg = error?.message ? `${error.message}` : "Unknown error";
    alert(`ML service error: ${msg}`);
    console.error("ML error details:", error);
  }
}
