import React, { useState } from "react";

function App() {
  const [description, setDescription] = useState("");
  const [url, setUrl] = useState("");
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSkills([]);
    try {
      const response = await fetch("http://localhost:8000/extract-skills", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description, url })
      });
      const data = await response.json();
      setSkills(data.skills || []);
    } catch (err) {
      setError("Failed to fetch skills. Is the backend running?");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Job Skills Extractor</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Job Description:</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} rows={5} style={{ width: "100%" }} />
        </div>
        <div style={{ margin: "10px 0" }}>or</div>
        <div>
          <label>Job URL:</label>
          <input type="url" value={url} onChange={e => setUrl(e.target.value)} style={{ width: "100%" }} />
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: 16 }}>
          {loading ? "Extracting..." : "Extract Skills"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 16 }}>{error}</div>}
      {skills.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3>Top 10 Skills/Technologies:</h3>
          <ol>
            {skills.map((skill, idx) => <li key={idx}>{skill}</li>)}
          </ol>
        </div>
      )}
    </div>
  );
}

export default App;