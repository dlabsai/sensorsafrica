import { User } from "../types/user";
import { request } from "./base";

export const getItems = async () => {
  try {
    const result = await request("/process/list", "GET", undefined, true);

    if (!result.status) {
      throw result;
    }

    return result;
  } catch (e) {
    throw e;
  }
};
