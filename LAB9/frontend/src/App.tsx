import { useState } from "react";
import { sendEmail, uploadFileToFtpServer } from "./services/email.service";
import { FileUploader } from "./FileUploader";
import "./App.css";

function App() {
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [sent, setSent] = useState(false);

  const splitEmails = (to: string): string[] => {
    return to
      .split(",")
      .map((email) => email.trim())
      .filter((email) => email !== "");
  };

  const handleEmailAttachment = async (file: File) => {
    const ftpLink = await uploadFileToFtpServer(file);
    const newBody = body + `\n${ftpLink?.data["ftp-link"]}`;
    setBody(newBody);
  };

  const handleEmailSubmit = async () => {
    const emailObject = {
      subject,
      body,
      recipients: splitEmails(to),
    };
    await sendEmail(emailObject);
    setSent(true);
    setTimeout(() => {
      setSent(false);
    }, 2000);
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
        value={body}
      ></textarea>

      {sent && <div>Email sent successfully!</div>}
      <div className="buttons">
        <FileUploader handleFile={handleEmailAttachment} />
        <button className="submit-2" onClick={() => handleEmailSubmit()}>
          Submit
        </button>
      </div>
    </div>
  );
}

export default App;
