const HOSTNAME = window.location.hostname;
const IS_LOCAL = HOSTNAME === "127.0.0.1" || HOSTNAME === "localhost";
const CONFIGURED_API_URL = IS_LOCAL ? "http://127.0.0.1:8000" : "";

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

function setLoading(button, isLoading, loadingText) {
  if (!button) {
    return;
  }
  button.disabled = isLoading;
  button.innerText = isLoading ? loadingText : button.dataset.defaultText;
}

async function buildOptimizedImage(file) {
  const bitmap = await createImageBitmap(file);
  const maxSize = 512;
  const scale = Math.min(1, maxSize / Math.max(bitmap.width, bitmap.height));
  const width = Math.max(1, Math.round(bitmap.width * scale));
  const height = Math.max(1, Math.round(bitmap.height * scale));

  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;

  const context = canvas.getContext("2d", { alpha: false });
  context.drawImage(bitmap, 0, 0, width, height);

  const blob = await new Promise((resolve) =>
    canvas.toBlob(resolve, "image/jpeg", 0.82)
  );

  if (!blob) {
    throw new Error("Image optimization failed.");
  }

  return new File([blob], "optimized-upload.jpg", { type: "image/jpeg" });
}

function getButtonByLabel(text) {
  return Array.from(document.querySelectorAll("button")).find(
    (button) => button.innerText.trim() === text
  );
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("button").forEach((button) => {
    button.dataset.defaultText = button.innerText;
  });
});

// analyze based on dropdown selection
async function analyzePlastic() {
  console.log('analyzePlastic invoked');
  const plasticType = document.getElementById("plastic").value;
  const button = getButtonByLabel("Analyze");

  if (!plasticType) {
    alert("Please select a plastic type.");
    return;
  }

  try {
    setLoading(button, true, "Analyzing...");
    const response = await fetch(
      `${BASE_URL}/analyze?plastic_type=${plasticType}`
    );
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    const data = await response.json();

    showResult(data.decision, data.explanation);
  } catch (error) {
    const localRule = PLASTIC_RULES[plasticType];
    if (localRule) {
      showResult(localRule.decision, `${localRule.explanation} (Fallback analysis)`);
      return;
    }

    alert("Analysis service not reachable. Please try again in a moment.");
    console.error(error);
  } finally {
    setLoading(button, false);
  }
}

// analyze by uploading an image file
async function analyzeImage() {
  console.log('analyzeImage invoked');
  const input = document.getElementById("imageInput");
  const button = getButtonByLabel("Analyze Image");
  if (input.files.length === 0) {
    alert("Please upload an image.");
    return;
  }

  try {
    setLoading(button, true, "Optimizing...");
    const optimizedFile = await buildOptimizedImage(input.files[0]);
    const formData = new FormData();
    formData.append("file", optimizedFile);

    setLoading(button, true, "Running ML...");
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
  } finally {
    setLoading(button, false);
  }
}
