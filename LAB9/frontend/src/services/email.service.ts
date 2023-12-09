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

export const uploadFileToFtpServer = async (data: Object) => {
  return axios
    .post(`${API_URL}/api/email/attachment`, { ...data })
    .then((res) => {
      return res;
    })
    .catch((e) => console.log(e));
};
