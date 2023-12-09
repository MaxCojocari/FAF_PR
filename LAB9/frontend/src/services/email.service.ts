import axios from "axios";
import { API_URL } from "../config/config";

export const sendEmail = async (data: Object) => {
  return axios
    .post(`${API_URL}/api/email`, { ...data })
    .then((res) => {
      return res;
    })
    .catch((e) => console.log(e));
};

export const uploadFileToFtpServer = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios
    .post(`${API_URL}/api/email/attachment`, formData)
    .then((res) => {
      return res;
    })
    .catch((e) => console.log(e));
};
