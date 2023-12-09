import { useRef } from "react";
import "./App.css";

export const FileUploader = ({ handleFile }: any) => {
  // Create a reference to the hidden file input element
  const hiddenFileInput = useRef<HTMLInputElement>(null);

  // Programatically click the hidden file input element
  // when the Button component is clicked
  const handleClick = () => {
    hiddenFileInput.current?.click();
  };
  // Call a function (passed as a prop from the parent component)
  // to handle the user-selected file
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const fileUploaded = event.target.files[0];
      handleFile(fileUploaded);
    }
  };

  return (
    <>
      <button className="submit-1" onClick={handleClick}>
        Attach a file
      </button>
      <input
        type="file"
        onChange={handleChange}
        ref={hiddenFileInput}
        style={{ display: "none" }} // Make the file input element invisible
      />
    </>
  );
};
