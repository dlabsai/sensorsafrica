import { getCurrentUser } from "../utils/user";

export const request = async (
  path: string,
  method: string,
  body?: any,
  auth = false,
) => {
  try {
    const headers = {
      "Content-Type": "application/json",
    } as { [key: string]: string };

    if (auth) {
      const user = getCurrentUser();

      if (!user) {
        throw "User not authenticated";
      }

      headers["Authorization"] = `Bearer ${user.idToken}`;
    }

    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}${path}`,
      {
        method,
        headers,
        body,
      },
    );

    return await response.json();
  } catch (e) {
    throw e;
  }
};
