// analyze based on dropdown selection
async function analyzePlastic() {
  console.log('analyzePlastic invoked');
  const plasticType = document.getElementById("plastic").value;
  const resultDiv = document.getElementById("result");

  if (!plasticType) {
    alert("Please select a plastic type.");
    return;
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/analyze?plastic_type=${plasticType}`
    );
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    const data = await response.json();

    document.getElementById("decision").innerText =
      "Decision: " + data.decision;

    document.getElementById("explanation").innerText =
      data.explanation;

    resultDiv.classList.remove("hidden");
  } catch (error) {
    alert("Backend not reachable. Is the server running?");
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

  const formData = new FormData();
  formData.append("file", input.files[0]);

  try {
    const response = await fetch(
      "http://127.0.0.1:8001/analyze-image",
      {
        method: "POST",
        body: formData
      }
    );
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();

    document.getElementById("decision").innerText =
      "Decision: " + data.decision;

    document.getElementById("explanation").innerText =
      data.explanation + " (Detected via ML)";

    document.getElementById("result").classList.remove("hidden");
  } catch (error) {
    alert("ML service unavailable.");
    console.error(error);
  }
}