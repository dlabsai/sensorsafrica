import React from "react";

import "./footer.css";

function DLabsFooter() {
  return (
    <div className="footer">
      Powered with &#x1F49B; by{" "}
      <a href="https://dlabs.ai" target="_blank" rel="noreferrer">
        <b style={{ fontSize: "12px" }}>DLabs.AI</b>
      </a>
    </div>
  );
}

export default DLabsFooter;
