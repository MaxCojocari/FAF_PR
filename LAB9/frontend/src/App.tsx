import { useState } from "react";
import "./App.css";
import { sendEmail } from "./services/email.service";

function App() {
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  const attachFile = () => {
    // getFtpLink()
  };

  const splitEmails = (to: string): string[] => {
    return to
      .split(",")
      .map((email) => email.trim())
      .filter((email) => email !== "");
  };

  const handleEmailSubmit = async () => {
    const emailObject = {
      subject,
      body,
      recipients: splitEmails(to),
    };
    await sendEmail(emailObject);
    console.log(emailObject);
  };

  const handleChange = (event) => {
    const fileUploaded = event.target.files[0];
    handleFile(fileUploaded);
  };

  return (
    <div className="main">
      <label>To</label>
      <input type="text" onChange={(e) => setTo(e.target.value)} />

      <label>Subject</label>
      <input type="text" onChange={(e) => setSubject(e.target.value)} />

      <textarea
        placeholder="Write something..."
        onChange={(e) => setBody(e.target.value)}
      ></textarea>

      <div className="buttons">
        <input
          type="file"
          onChange={handleChange}
          ref={hiddenFileInput}
          style={{ display: "none" }} // Make the file input element invisible
        />
        <button
          name="filename"
          className="submit-1"
          onClick={() => attachFile()}
        >
          Attach file
        </button>
        <button className="submit-2" onClick={() => handleEmailSubmit()}>
          Submit
        </button>
      </div>
    </div>
  );
}

export default App;
